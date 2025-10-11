# Test suite information

### Test name
Bluetooth LE advertising test.

### Test path
tests/repo_tests/general_tests/bt_peripheral

### Type
- Pytest test
- Hardware test

### Description
This test is designed to verify a basic functionalitiey of the Bluetooth LE - advertising feature in the Zephyr OS.

### Preconditions
- ESP32-S3 Devkitc target board.
- Python library - BleakScanner.

### Test steps
1. Run the test with `west twister`command.
2. Verify that BT device is advertising with required name.

### Expected results
Required BT device advertising name is available to connect.

### Notes
N.A.