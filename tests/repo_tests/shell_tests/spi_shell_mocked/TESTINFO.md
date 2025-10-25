# Test suite information

### Test name
Test for SPI write & read commands with UART shell prompt on emulated SPI bus.

### Test path
tests/repo_tests/shell_tests/spi_shell_mocked

### Type
- Shell test
- Pytest test
- Simulation test (native_Sim)

### Description
This test is designed to verify Write & Read process on SPI bus through custom-shell commands and emulated SPI bus register space with native_sim simulation board. The real SPI bus is emulated with help of Bosch BMI160 sensor's emulation driver available in Zephyr samples. This driver is adapted to SPI functionalities only and extended with custom-shell commands to write/read values into/from arbitrary register address within 8-bit register space.

### Preconditions
- #include <zephyr/drivers/spi_emul.h> - Zephyr BMS160 emulation driver.
- `harness: console` in testcase.yaml for shell console test.

### Test steps
1. Run the test with `west twister`command (SPI bus registers are written with sample values within test initiation).
2. Console test: verify through the pseudoterminal (console test), that all SPI bus values fit the sample values.
3. Pytest: verify with custom-shell command `spi_read xxx`, that SPI bus values on specific register addresses fit the sample values.
4. Update the specific SPI bus registers values with custom-shell command `spi_write xxx`.
5. Verify with custom-shell command `spi_read_range xxx xxx`, that SPI bus registers values fit the values from step 4.

### Expected results
SPI registers values for test steps 2 and 3:
    Reading 6 registers starting from 0x12:
    0x12: 0x34
    0x13: 0x12
    0x14: 0x78
    0x15: 0x56
    0x16: 0xBC
    0x17: 0x9A

SPI registers values for test steps 4 and 5:
    Reading 6 registers starting from 0x12:
    0x15: 0x56
    0x16: 0xAA
    0x17: 0xBB

### Notes
<strong>Example fo I2C bus - the same is valid for SPI as well:</strong><br/>

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

Manual interraction with I2C emulated bus is possible only with custom-shell commands implemented to test source code.