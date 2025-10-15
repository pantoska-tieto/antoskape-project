# How to setup test config for native_sim tests while needed a shell prompt?

### Table of Contents
1. [Zephyr application - home page](../README.md)
2. [Add new board to project](Add_new_board_to_project.md)
3. [Artifactory storage server](Artifactory_storage_server.md)
4. [GitHub workflow_dispatch panel](Github_workflow_dispatch_panel.md)
5. [HW resources for tests](HW_resources_for_tests.md)
6. [Kconfig tester guide](Kconfig_tester_guide.md)
7. [Raspi runner installation](Raspi_runner_installation.md)
8. Shell tests with native_sim [this page]
9. [Tests list](Tests_list.md)
10. [Tests user guide](Tests_user_guide.md)
---

Error in `west twister...` command run if pytest expects a shell prompt:<br/>

```
dut = NativeSimulatorAdapter()
@pytest.fixture(scope=determine_scope)
def shell(dut: DeviceAdapter) -> Shell:
"""Return ready to use shell interface"""
shell = Shell(dut, timeout=20.0)
if prompt := find_in_config(Path(dut.device_config.app_build_dir) / 'zephyr' / '.config',
'CONFIG_SHELL_PROMPT_UART'):
shell.prompt = prompt
logger.info('Wait for prompt')
if not shell.wait_for_prompt():
>           pytest.fail('Prompt not found')
E           Failed: Prompt not found
```

<br/>

## Root cause of “prompt not found” with native_sim

- For native_sim, the pytest plugin attaches to the simulator process’ stdin/stdout (device type “native”). If your shell backend is UART-based, the prompt is printed on a pseudo-terminal (/dev/pts/N), not on the process stdout. The plugin won’t see it and times out waiting for the prompt.
- The log shows the plugin found CONFIG_SHELL_PROMPT_UART and then waited for it on stdout, which never arrives because the shell isn’t on stdout.

Two working workarounds can be applied.

<br/>

### A) Recommended: Shell on process stdin/stdout (POSIX backend)
You can use the Kconfig symbol `CONFIG_UART_NATIVE_PTY_0_ON_STDINOUT=y` in a prj.conf or any .conf file to enable Zephyr's native POSIX UART backend 
to connect UART_0 to the host's stdin/stdout via a pseudoterminal (PTY). Update the testcase.yaml/sample.yaml:<br/>

```
CONFIG_KERNEL_SHELL=y
CONFIG_CRC=y

# native POSIX UART backend to connect UART_0 to the host's stdin/stdout via a pseudoterminal (PTY)
CONFIG_UART_NATIVE_PTY_0_ON_STDINOUT=y
```

Then you can use the the regular `harness: pytest` in  testcase.yaml/sample.yaml to invoke Pytest to run the test. Pytest plugin will then attach to the simulator process’ stdin/stdout and is able to read from pseudoterminal /dev/pts/N without any additional setup:

```
from twister_harness import Shell

def test_shell_print_help(shell: Shell):
    logger.info('send "help" command')
    lines = shell.exec_command('command in pseudoterminal')
    . . .
```

For direct access to pseudoterminal without using Pytest test there is a simple way to verify shell-command output (create a test case) inside testcase.yaml/sample.yaml (regex can be used):

```
harness: shell
    harness_config:
      pytest_dut_scope: session
      shell_commands:
        - command: "command in pseudoterminal"
          expected: ".*Framebuffer CRC32: 0xfdc935d3.*"
```

<strong>Note:</strong><br/>
For console/session configuration, the regex field does not support standard escape sequences like \s (for whitespace) or other backslash-based patterns as you'd expect in full-featured regex engines like Python or Perl!

<br/>

### B) Alternative: Use harness: console in testcase.yaml
If you don’t want to use the native POSIX UART backend (CONFIG_UART_NATIVE_PTY_0_ON_STDINOUT=y is not added to prj.conf), you can use the `harness: console` keyword to run the test. This will attach to the simulator process’ stdin/stdout and is able to read from pseudoterminal /dev/pts/N without any additional setup.

<br/>

1. Extend src/main.c with test-logic writing a test value to UART shell e.g.:

```
// Perform custom write if address is set
if (user_mem_address >= 0) {
    int ret = custom_i2c_write(emul_i2c, 0x69, 0x56);      
    if (ret < 0) {
        printk("I2C write operation failed with error %d\n", ret);
    }
}
```

2. Extend testcase.yaml/sample.yaml with `harness: console` section and verify main.c test-logic (prints on pseudoterminal /dev/pts/N) with regex-pattern:

```
tests:
  sensor.shell.i2c.read.console:
    tags:
      - sensor
      - i2c
    platform_allow:
      - native_sim
      - native_sim/native/64
    harness: console
    harness_config:
      type: one_line
      regex:
        - ".*write to address: 0x68 with value: 0x55.*"
```

<strong>Note:</strong><br/>
For console/session configuration, the regex field does not support standard escape sequences like \s (for whitespace) or other backslash-based patterns as you'd expect in full-featured regex engines like Python or Perl!

 <br/>


### Split configuration file on tes-case level
If each test case needs a differnet configuration file, the following logic can be applied in testcase.yaml/sample.yaml:

```
tests:
  display.shell.framebuffer:
    platform_allow:
      - esp32s3_devkitc/esp32s3/procpu
    tags:
      - display
      - shell
    harness: pytest
    extra_args:
      - EXTRA_CONF_FILE=conf/board_prj.conf   
```

The prj.conf is empty and conf/board_prj.conf consists of all CONFIG_ symbols needed to configure the test environment.

For "display.shell.framebuffer" test case the default prj.conf will be ignored and replaced by "conf/board_prj.conf" configuration. This approach is useful when you have multiple test cases that need different configurations.

## Outcome
For best performance and reliability, it is recommended to use the native POSIX UART backend (CONFIG_UART_NATIVE_PTY_0_ON_STDINOUT=y) in a prj.conf. In this case you have a shell prompt available in regular Pytest. If Pytest tests are not intended to use, you can use the `harness: console` keyword to run the test directly on the simulator process’ stdin/stdout.
