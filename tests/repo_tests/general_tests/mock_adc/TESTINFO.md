# Test suite information

### Test name
Test for reading mocked sensor parameter value from ADC converter.

### Test path
tests/repo_tests/general_tests/mock_adc

### Type
- Shell harness test

### Description
This test is designed to verify a capabilities to read sensor value from mocked ADC sensor. ADC sensor is mocked with help of standard ADC Zephyr module by assigning the hardcoded test value "1234" to the ADC output buffer.

### Preconditions
- #include <zephyr/drivers/adc.h> - ADC driver.

### Test steps
1. Run the test with `west twister`command.
2. Verify that mocked sensor value from ADC converter is "1234" (managed in main() function).

### Expected results
Sensor value == "1234".

### Notes
Simulation tests without a DUT board needed.