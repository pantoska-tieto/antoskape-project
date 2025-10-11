# How to setup test config for native_sim while needed a shell prompt?

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

### Two working workarounds

<strong><u>A) Recommended: Shell on process stdin/stdout (POSIX backend)</u></strong>
- What this does: Puts the Zephyr shell on the simulator process’ stdin/stdout so the pytest “native” device adapter can interact with it directly. No /dev/pts involved.
- Kconfig to enable:
  - CONFIG_SHELL=y
  - CONFIG_SHELL_BACKEND_POSIX=y
  - CONFIG_SHELL_BACKEND_SERIAL=n
  - CONFIG_CONSOLE=y
  - CONFIG_STDOUT_CONSOLE=y
  - Enable stdin for native_sim (symbol name depends on your Zephyr version, one of):
    - CONFIG_NATIVE_POSIX_STDIN_CONSOLE=y (older native_posix)
    - or CONFIG_NATIVE_SIM_STDIN_CONSOLE=y (newer native_sim)
- Keep the prompt string consistent with what the fixture looks for:
  - Either keep defaults (usually “uart:~$ ”), or explicitly set:
    - CONFIG_SHELL_PROMPT="uart:~$ "
    - If available, also set CONFIG_SHELL_PROMPT_POSIX="uart:~$ "
    - Optionally set CONFIG_SHELL_PROMPT_UART="uart:~$ " to match what the plugin reads from .config
- Where to place this:
  - Add an overlay for native_sim only (e.g. overlay-native_sim.conf) and reference it in your test’s testcase.yaml via extra_args: CONF_FILE=path/to/overlay-native_sim.conf, or place a board-specific overlay at boards/native_sim.conf in your test app.
- Run:
  - west twister -T tests/repo_tests/shell_tests/i2c_shell_mocked -p native_sim
- Result: The plugin will use NativeSimulatorAdapter, the shell prompt will appear on stdout, and Shell.wait_for_prompt() will pass.<br/>

<br/>

<u><strong>B) Alternative: Keep UART shell backend and use serial</u></strong>
- What this does: Uses the native UART driver that exposes a /dev/pts/N. Then the harness must connect as a serial device, not “native”.
- Kconfig:
  - CONFIG_SHELL=y
  - CONFIG_SHELL_BACKEND_SERIAL=y
  - CONFIG_UART_CONSOLE=y
  - CONFIG_UART_NATIVE_POSIX=y (or CONFIG_UART_NATIVE_SIM=y depending on version)
- Caveat: The pytest plugin will by default pick “native” for native_sim platforms, so it won’t connect to the PTY. You’d need to force the device type to “serial” and supply the PTY path. This is brittle because the PTY is allocated dynamically. Unless you have a custom runner that surfaces the PTY path to the harness, this is harder to automate reliably. Prefer option A.

If you need to customize the fixture behavior

- There is no different import for native_sim; you still use from twister_harness import Shell.
- If you want to control prompt handling yourself, override the plugin fixture “shell” in your test module to avoid failing during setup. Example pattern:

  - Define your own shell fixture (same name) and set the expected prompt explicitly.
  - Optionally defer waiting for the prompt to inside your test.

  <br/>

<em>Example:</em>

```
  from twister_harness import DeviceAdapter, Shell
  import pytest

  @pytest.fixture
  def shell(dut: DeviceAdapter) -> Shell:
      sh = Shell(dut, timeout=20.0)
      sh.prompt = "uart:~$ "  # must match what your backend actually prints
      # Optionally: don’t wait here; wait in the test after any required settling
      assert sh.wait_for_prompt()
      return sh

  def test_shell_i2c(shell: Shell):
      shell.send_command("help")
      shell.expect("i2c", timeout=5)
```

<br/>

This only works if the shell is on stdout (option A). If your shell is on a UART PTY, this will still fail because the adapter isn’t connected to that PTY.

Checklist to get it working on Linux

- Ensure the test app actually enables the shell and the correct backend for native_sim (POSIX backend recommended).
- Ensure the prompt string configured matches what the fixture expects (default “uart:~$ ” is fine; if you change it, set it consistently so the fixture can find it).
- Run twister as usual; builds and logs will be under twister-out, and the plugin will manage the simulator and PTY.

<br/>

## Outcome

- With POSIX shell backend on native_sim, your existing from twister_harness import Shell test will work. No other import is needed. The key is to put the shell on stdin/stdout so the “native” device adapter sees the prompt.
