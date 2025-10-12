# Test suite information

### Test name
Test for BLE GATT service - capability to transmit and update the Heart Rate value with mocked value.

### Test path
tests/repo_tests/shell_tests/ble_shell_hrs_mocked

### Type
- Pytest test
- Shell test

### Description
This test is designed to verify a basic functionalitiey of the Bluetooth LE - advertising feature in the Zephyr OS and providing Heart Rate Service (HRS) with mocked value. 
<p>For verification a values in UART Shell the <strong>custom-shell commands</strong> are used to verify the Battery Level and Heart Rate values.</p>
<p>
More info about Custom Shell module and custom-shell commnds can be found in official Zephyr documentation:<br/>

[Custom Shell module](https://docs.zephyrproject.org/latest/samples/subsys/shell/shell_module/README.html#shell-module)<p>

### Preconditions
- #include <zephyr/bluetooth/services/hrs.h> in main.c - GATT service fo HRS.

### Test steps
1. Run the test with `west twister`command.
2. Read Heart Rate value with custom-shell command `get_hr`.
3. Verify with custom-shell command `get_hr` that value is as expected.
4. Update the Heart Rate value with custom-shell command: `set_hr`.
5. Verify with custom-shell command `get_hr` that value is as expected.

### Expected results
Heart Rate value == 72 (72 bpm) and 90 (90 bpm).

### Notes
N.A.