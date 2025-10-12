# Test suite information

### Test name
GPIO toggle test with GPUO initiation and toggling through UART shell commands.

### Test path
tests/repo_tests/shell_tests/gpio_toggle_pytest

### Type
- Pytest test
- Shell test
- Hardware test

### Description
This test is designed to verify GPIO toggle capability with UART Shall commands. For verification a GPIO pin state during toggle cycles the other reference GPIO pin (configured as Input) is utilized. Thest is executed on target ESP32 S3 devkitc board as Hardware test, so that the corresponding wiring must be prepared before test starts. Toggle capability is verified in 10 test cycles.

### Preconditions
- ESP32 S3 devkitc board.
- Output from GPIO13 (tested pin) is wired to GPIO9 (reference pin).

### Test steps
1. Run the test with `west twister`command.
2. Toggle tested pin state with shell command.
3. Read GPIO pin status with reference GPIO through shell command.
4. Repeat this proceeding in 10 cycles.

### Expected results
True/False values after toggle step should fit the expected values.

### Notes
GPIO pin setup for Input/Output functionality is performed automatically in Pytest script.