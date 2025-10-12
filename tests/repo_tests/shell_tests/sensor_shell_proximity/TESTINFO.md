# Test suite information

### Test name
Test for data evaluation from proximity sensor.

### Test path
tests/repo_tests/shell_tests/sensor_shell_proximity

### Type
- Pytest test
- Shell test

### Description
This test is designed to verify Read capability from external sensor through the custom-shell commands. The ouput from sensor driver is mocked by custom-shell commands in regular interval 0.5 sec and evaluated back by custom-shell command in asynchronous mode. When the pre-defined threshold is achieved the test is considered passed.

### Preconditions
- #include <zephyr/drivers/sensor.h> - Zephyr sensor driver.

### Test steps
1. Run the test with `west twister`command.
2. Start mocking the proximity sensor value from x=10 to x=0 within a cysle in descending order with 0.5 sec interval with custom-shell command `set_proximity x`.
3. Start getter for proximity sensor running in infinite cycle and reading the sensor value in 0.5 sec interval with custom-shell command `get_proximity`.
4. When the proximity sensor value reach the hardcoded threshold value 5, the test stops and is considered passed.

### Expected results
Threshold value from proximity sensor == 5. 

### Notes
N.A.