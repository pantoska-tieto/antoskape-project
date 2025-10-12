# Test suite information

### Test name
Test to transmit simulated display-framebuffer data through UART serial port.

### Test path
tests/repo_tests/shell_tests/display_shell_framebuffer

### Type
- Pytest test
- Shell test

### Description
This test is designed to verify dsiplay status and display framebuffer content with custom-shell commands. For verification a values in UART Shell the <strong>custom-shell commands</strong> are used to verify the framebuffer content through the CRC32 checksum.
<p>
More info about Custom Shell module and custom-shell commnds can be found in official Zephyr documentation:<br/>

[Custom Shell module](https://docs.zephyrproject.org/latest/samples/subsys/shell/shell_module/README.html#shell-module)<p>

### Preconditions
- #include <zephyr/bluetooth/services/hrs.h> in main.c - GATT service fo HRS.

### Test steps
1. Run the test with `west twister`command.
2. Read dsiplay status with custom-shell command `display_status`.
3. Read CRC32 checksum value of framebuffer with custom-shell command `display_status`.
4. Verify the checksum and status values are as expected.

### Expected results
crc == "0xfdc935d3" and  message == "'Message from Zephyr display'"

### Notes
N.A.