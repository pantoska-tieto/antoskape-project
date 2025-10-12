# Test suite information

### Test name
Successfull booting after power cycles.

### Test path
tests/repo_tests/general_tests/power_cycle_boot

### Type
- Pytest test
- Hardware test
- Shell test

### Description
This test is designed to verify a capabilities to boot without an errors after power cycle OFF/ON. The errorless booting state is verified by "Kernel uptime" feature available via UART Shell - the timestamp should be equal the time since last power ON event (with added 3 seconds around limit). Each time when power is ON, the different serial port is used for UART Shell communication. The new serial port is found automatically by python script.

### Preconditions
- ESP32-S3 Devkitc target board.

### Test steps
1. Run the test with `west twister`command.
2. Find the serial port used for UART Shell communication.
3. Verify that "Kernel uptime" timestamp is equal to time since power = ON event (with added 3 seconds around limit).
4. Repeat this test case in 2 power OFF/ON cycles.

### Expected results
"Kernel uptime" timestamp == time since power=ON event.

### Notes
N.A.