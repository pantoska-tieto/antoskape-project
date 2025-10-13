# Test suite information

### Test name
Test for I2C write & read commands with UART shell prompt on emulated I2C bus.

### Test path
tests/repo_tests/shell_tests/i2c_shell_mocked

### Type
- Shell test
- Console harness test
- Simulation test

### Description
This test is designed to verify Write & Read process through custom-shell commands to I2C bus register space with native_sim simulation. The real I2C bus is emulated wtih help of Bosch BMS160 sensor's emulation driver - adapted to I2C functionalities only with using custom write/read register address/values.
To store mocked I2C values on fictive I2C register address the 8-bit register space is used through the uint8_t list.

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

Output from /dev/pts/x

```
uart connected to pseudotty: /dev/pts/4
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