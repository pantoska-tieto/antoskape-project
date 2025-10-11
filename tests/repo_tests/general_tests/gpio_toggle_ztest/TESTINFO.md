# Test suite information

### Test name
GPIO toggle test with Ztest framework.

### Test path
tests/repo_tests/general_tests/gpio_toggle_ztest

### Type
- Ztest test

### Description
This test is designed to verify the functionality of GPIO pin - toggling an LED on target board using Zephyr OS modul.

### Preconditions
- ESP32-S3 Devkitc target board.
- LED connected to tested GPIO13 pin.
- Signal from GPIO13 is connected to GPIO9 reference pin used for detection of LED state.

### Test steps
1. Run the test with `west twister`command.
2. Verify that logical state of tested GPIO13 and verification GPIUO9 are equal.
3. Repeat this test case  in 10 cycles.

### Expected results
LED is toggled in 10 cycles and logical state of both GPIO13 and GPIO9 are equal.

### Notes
HW prerequisite is required for this test! See [HW_resources_for_tests](../../../../documentation/HW_resources_for_tests.md) file for more details.