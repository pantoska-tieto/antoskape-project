# Test suite information

### Test name
DFU OTA over Bluetooth.

### Test path
tests/repo_tests/general_tests/dfu_ota_bluetooth

### Type
- Pytest test
- Hardware test

### Description
This test is designed to verify DFU OTA (Device Firmware Update Over-the-Air) to upgrade the image of a Zephyr-based 
application at run time over the Bluetooth. This process allows Bluetooth Low Energy devices to receive a firmware image (FW)
over the air from another Bluetooth Low Energy device. In case of this test the new FW is build in the runner machine
and sent to the target device with help of Zephyr MCUmgr subsystem and mcumgr-CLI tool.

For more details about MCUmgr subsystem see [MCUmgr subsystem for testing purposes](../../../../documentation/MCUmgr_subsystem.md).

### Preconditions
- ESP32-S3 Devkitc target board.
- `mcumgr` CLI tool installed.

### Test steps
1. Run the test with `west twister`command.
2. Get image list from target BT device:<br/>
`$USER/go/bin/mcumgr --conntype ble --connstring peer_name='TietoBLE-OTA' image list`
3. Build new test-image to be used for DFU OTA:<br/>
`west build -p always -b <board> --sysbuild tests/repo_tests/smp_svr -- -DEXTRA_CONF_FILE="overlay-bt.conf"`
4. Flash new-test image to target BT device:<br/>
`$USER/go/bin/mcumgr --conntype ble --connstring peer_name="TietoBLE-OTA" image upload build/smp_svr/zephyr/zephyr.signed.bin`
5. Update the state of new-test image to "pending":<br/>
`$USER/go/bin/mcumgr --conntype ble --connstring peer_name="TietoBLE-OTA" image test <has string of new-test image>`
6. Perform a soft reset of a device:<br/>
`$USER/go/bin/mcumgr --conntype ble --connstring peer_name="TietoBLE-OTA" reset`
7. Get image list from target BT device and verify the new-test image is running:<br/>
`$USER/go/bin/mcumgr --conntype ble --connstring peer_name='TietoBLE-OTA' image list`

### Expected results
New FW is running on target BT device.

### Notes
<strong>Current status (23.10.2025)</strong><br/>
Test is running in automated process without an error only in local environment. In case of GitHub CI workflow the following error appears
for `mcumgr` commands:<br/>

"can't init hci: can't create socket: address family not supported by protocol"<br/>

This is caused by insufficient permission granted in GitHub container to use Host's BT HCI stack. The more advanced research should be done 
to grant this access for container's processes. 