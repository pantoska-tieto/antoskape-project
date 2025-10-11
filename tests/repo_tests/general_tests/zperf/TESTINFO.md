# Test suite information

### Test name
Test for a capabilities to transfer data package through Wifi connection with using perf-tool.

### Test path
tests/repo_tests/general_tests/zperf

### Type
- Pytest test
- Shell test

### Description
This test is designed to verify UDP packet transport from Host runner to Zephyr DUT (ESP32.S3 Devkitc in this case). The <strong>ZPERF</strong> and <strong>IPERF</strong> shell utilities are used as traffic generators and performance verification tools. The test UDP 1kB packet pattern is transmitted over Wifi connection between Host runner and DUT. The test is performed in two phases: sending and receiving UDP packets while Zephyr is acting as a server (zperf) and Host side must manage UDP transport by iPerf tool.

<strong>zperf details:</strong><br/>
[zperf: Network Traffic Generator](https://docs.zephyrproject.org/latest/connectivity/networking/api/zperf.html)

### Preconditions
- ESP32-S3 Devkitc target board.
- Wifi connection credentials must be setup to connect DUT to Wifi network.
- iPerf tool installed on Host runner (Linux OS).

### Test steps
1. Run the test with `west twister`command.
2. Verify that 1kB UDP packet was receiver in DUT.

### Expected results
"received packets" should be catched via DeviceAdapter API to confirm successfull receiving of UDP packet in DUT.

### Notes
N.A.