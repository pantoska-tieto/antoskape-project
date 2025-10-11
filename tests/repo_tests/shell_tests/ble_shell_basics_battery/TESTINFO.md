# Test suite information

### Test name
Test for BLE GATT service - transmitting the Battery Level value with demanded advertising.

### Test path
tests/repo_tests/shell_tests/ble_shell_basics_battery

### Type
- Pytest test
- Shell test

### Description
This test is designed to verify a basic functionalitiey of the Bluetooth LE - advertising feature in the Zephyr OS and providing Battery Service (BAS) with hardcoded Battery Level Characteristic simulated value.

### Preconditions
- #include <zephyr/bluetooth/services/bas.h> in main.c - GATT service fo BAS.

### Test steps
1. Run the test with `west twister`command.
2. Verify that GATT service with Battery Level Characteristic is available in UART Shell: UUID=0x2a19 (BAS).
3. For UUID=0x2a19 find respective handle ID (0x0012 for BAS).
4. Find Battery Level value with shell command: gatt get 0x0012

### Expected results
Battery Level Characteristic value == 0x55 (85%).

### Notes
N.A.