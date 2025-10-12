# Test suite information

### Test name
Test for successful toggling the GPIO pin with Pytest.

### Test path
tests/unit_tests/dut/gpio_pins_pytest

### Type
- Pytest test
- Shell test
- Unit test

### Description
This Unit test is designed to verify the capability toggle GPIO13 pin via the shell commands in DUT.

### Preconditions
N.A.

### Test steps
1. Run the test with `west twister`command.
2. Verify the availability of GPIO13 pin with shell command `gpio info`.
3. Set and verify the GPIO13 features to Output role with pull down, active high, logic 1 with shell command `gpio conf`.
4. Set and verify the GPIO13 state "0" with shell command `gpio set`.
5. Set and verify the GPIO13 state "1" with shell command `gpio set`.
6. Set and verify the GPIO13 toggle functionality with shell command `gpio toggle`.
7. Set and verify the GPIO13 features to Input role with pull up, active high with shell command `gpio conf`.
8. Verify the GPIO13 state with shell command `gpio get`.

### Expected results
String return values from UART shell prompt according to the command used.

### Notes
N.A.