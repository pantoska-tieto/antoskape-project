# Test suite information

### Test name
Test for successful booting of the board.

### Test path
tests/repo_tests/shell_tests/boot_shell

### Type
- Pytest test
- Shell test
- Hardware test

### Description
This test is designed to verify the capability to detect available Wifi network surrounding and connect to demanded SSID network.

### Preconditions
- ESP32-S3 Devkitc board,
- Running Wifi router with pre-defined SSID name within the range of the board.

### Test steps
1. Run the test with `west twister`command.
2. Scan surrounding Wifi network for target SSID name with shell command `wifi scan`.
3. Connect to Wifi network with target SSID name with shell command `wifi connect`.
4. Get the status of Wifi connection with shell command `wifi status`.

### Expected results
Return string from shell command `wifi scan` consists of target SSID name.<br/>
Return string from shell command `wifi status` consists of target SSID name.<br/>

### Notes
Wifi connection credentials (secrets) to connect to target SSID are storen in `vars.json` file located in the root directory of the project. This file content is parsed during the GitHub workflow run to retrieve the necessary credentials for the test and hidden for direct access to expose the secrets in the GitHub repository.