# Test suite information

### Test name
Test for BLE GATT services - transmitting the Battery Level and Heart Rate values with demanded advertising.

### Test path
tests/repo_tests/shell_tests/ble_shell_hrs_bas

### Type
- Pytest test
- Shell test

### Description
This test is designed to verify a basic functionalitiey of the Bluetooth LE - advertising feature in the Zephyr OS and providing Battery service (BAS) and Heart Rate Service (HRS) with hardcoded simulated values.
<p>For verification a values in UART Shell the <strong>custom-shell commands</strong> are used to verify the Battery Level and Heart Rate values.</p>
<p>
More info about Custom Shell module and custom-shell commnds can be found in official Zephyr documentation:<br/>

[Custom Shell module](https://docs.zephyrproject.org/latest/samples/subsys/shell/shell_module/README.html#shell-module)<p>

### Preconditions
- #include <zephyr/bluetooth/services/bas.h> in main.c - GATT service fo BAS.
- #include <zephyr/bluetooth/services/hrs.h> in main.c - GATT service fo HRS.

### Test steps
1. Run the test with `west twister`command.
2. Verify that GATT service with Battery Level Characteristic is available in UART Shell: UUID=0x2a19 (BAS level).
3. For UUID=0x2a19 find respective handle ID (0x0012 for BAS level).
4. Find Battery Level value with shell command: gatt get 0x0012
5. Verify that GATT service with Heart Rate is available in UART Shell: UUID=0x2a37 (HRS bpm).
6. For UUID=0x2a19 find respective handle ID (0x0017 for HRS bpm).
7. Find Battery Level value with shell command: gatt get 0x0017

### Expected results
Battery Level Characteristic value == 60 (60%).
Heart Rate bpm value == 90 (90bpm).

### Notes
Because the custom-shell commands are invoked in test assert statement, the HEX->DEC casting is not neede because for write/read the HEX values are used already.