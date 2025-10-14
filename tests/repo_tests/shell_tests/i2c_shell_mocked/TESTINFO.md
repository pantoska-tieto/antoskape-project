# Test suite information

### Test name
Test for I2C write & read commands with UART shell prompt on emulated I2C bus.

### Test path
tests/repo_tests/shell_tests/i2c_shell_mocked

### Type
- Shell test
- Pytest test
- Simulation test

### Description
This test is designed to verify Write & Read process through emulated regular I2C commands and custom-shell commands to I2C bus register space with native_sim simulation board. The real I2C bus is emulated with help of Bosch BMI160 sensor's emulation driver available in Zephyr samples. This driver is adapted to I2C functionalities only and extended with custom-shell commands to write/read values into/from arbitrary register address within 8-bit register space.

### Preconditions
- #include <zephyr/drivers/i2c_emul.h> - Zephyr BMS160 emulation driver.
- `harness: console` in testcase.yaml.

### Test steps
1. Run the test with `west twister`command.
2. Verify with custom-shell command `i2c_read`, that I2C bus value on register address 0x68 is 0x55.
3. Update the I2C value in register address 0x69 to 0x56 with custom-shell command `custom_i2c_write`.
4. Verify with custom-shell command `i2c_read`, that I2C bus value on register address 0x69 is 0x56.

### Expected results
I2C value 0x55 on register address 0x68.
I2C value 0x56 on register address 0x69.

### Notes
Because of "native_sim" board used in test, the output from stdin/stdout is routed to /dev/pts/x. The output from this device is automatically captured by `harness: console` keyword in testcase.yaml file and evaluated by assert() function.

Manual interraction with pseudoterminal /dev/pts/x can be managed by external serial port commmunication tools like minicom, screen, etc. Port number (x) can be found in the output of west twister command - see example:

```
uart connected to pseudotty: /dev/pts/4  --> !!
*** Booting Zephyr OS build v4.2.0-3707-g49157ea8fc71 ***
I2C emulator found and binded.
I2C emulator write to address: 0x68 with value: 0x55
mock_i2c_transfer: wrote 0x55 to reg 0x68
mock_i2c_transfer: read 0x55 from reg 0x68
I2C emulator read from address: 0x68 with value: 0x55
I2C emulator write to address: 0x69 with value: 0x56
mock_i2c_transfer: wrote 0x56 to reg 0x69
mock_i2c_transfer: read 0x56 from reg 0x69
I2C emulator read from address: 0x69 with value: 0x56
```

To start a communication tool and write/read I2C values manually, open new terminal and run (example for minicom tool):

```
minicom -D /dev/pts/4 115200

uart:~$ i2c_write 0x70 0x59
Write successful to reg 0x70 with value 0x59
uart:~$ i2c_read 0x70
Read from reg 0x70 returned value 0x59
```

Manual interraction with I2C emulated bus is possible only with custom-shell commands: <strong>i2c_read, i2c_write</strong>. The source code for shell-custom commands can be found in file `src/shell_module.c`.