# Test suite information

### Test name
Test for basic Bluetooth LE Central role functionality.

### Test path
tests/repo_tests/general_tests/bluetooth_central

### Type
- Pytest test
- Hardware test
- Shell test

### Description
This test is designed to verify basic Bluetooth LE Central role functionality by scanning for other Bluetooth LE devices and establishing a connection to the ones with a strong enough signal (threshold for filtering BT devices is -60dBm).
This threshold helps the app filter out weaker signals, ensuring it only interacts with devices that are within a reasonable RSSI range for communication. Among all BT devices fulfilling the threshold, the test will search for device with specific advertising name "PA-iPhone" and connect to it. So the needed prerequisite for this test is a second compatible board or use an Bluetooth LE enabled device that can act as a Peripheral - iPhone mobile phone in this case with "nRF Connect" mobile application installed.

### Preconditions
- ESP32-S3 Devkitc target board with BLE enabled.
- A second compatible board or use an off-the-shelf Bluetooth LE enabled device that can act as a Peripheral (eg. smartphone, smartwatch, etc.).

### Test steps
1. Run the test with `west twister`command.
2. The BT Central scans for Peripheral devices and filters a Peripherals which have a signal strength higher than -60dBm.
3. Search for device with specific advertising name "PA-iPhone" (Target BT device) among all filtered devices.
3. Connect and Disconnect to/from the Target BT Peripheral device.
4. If there are no connections, the Central keeps scanning continuously.

### Expected results
Target BT Peripheral device with specific advertising name "PA-iPhone" is found and verified it was successfully connected and disconnected.

### Notes
#### nRF Connect mobile application setup
1. Open the nRF Connect mobile application.
2. Select "Peripheral" mode from the app menu on the bottom.
3. Select "Add Advertiser" to create a new Bluetooth devices.
4. Enter the advertising name "PA-iPhone". No specific ADVERTISED SERVICES are needed to add, leave it empty.
5. Go back to Peripheral-panel and start the BT Device by pressing the run-button.

#### BT Central role
In Bluetooth Low Energy (BLE), the Central device is one of the two primary roles in a connection. Here's a breakdown of the roles and how the Central is distinguished:

<br/>

<table>
    <thead>
      <th><strong>ROLE</strong></th>
      <th><strong>DESCRIPTION</strong></th>
    </thead>
      <tbody>
        <tr>
        <td>Central</td>
        <td>Initiates and manages connections to Peripheral devices.</strong></td>
        </tr>
        <tr><td>Peripheral</td>
        <td>Advertises its presence and waits for a Central to connect to it.</td>
        </tr>
</table>

<br/>

<strong>Key Characteristics of a Central Device</strong>

- Initiator: It scans for advertising packets from peripherals and initiates the connection.
- Controller: Once connected, it typically controls the communication and can request data.
- Examples: Smartphones, laptops, or embedded devices acting as BLE masters.