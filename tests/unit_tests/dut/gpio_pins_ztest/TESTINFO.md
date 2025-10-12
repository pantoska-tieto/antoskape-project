# Test suite information

### Test name
Test for successful toggling functionality of GPIO pin with Ztest.

### Test path
tests/unit_tests/dut/gpio_pins_ztest

### Type
- Ztest test
- Unit test

### Description
This Unit test is designed to verify the capability toggle GPIO13 pin via the Zephyr libraries in DUT.

### Preconditions
N.A.

### Test steps
1. Run the test with `west twister`command.
2. Verify the availability of GPIO13.
3. Set and verify the GPIO13 features to Output role with pull down, active high, logic 1.
4. Set and verify the GPIO13 state "0".
5. Set and verify the GPIO13 state "1".
6. Set and verify the GPIO13 toggle functionality.
7. Set and verify the GPIO13 features to Input role with pull up, active high.
8. Verify the GPIO13 state.

### Expected results
String return values from Zephyr modules must fit to expected strings.

### Notes
N.A.