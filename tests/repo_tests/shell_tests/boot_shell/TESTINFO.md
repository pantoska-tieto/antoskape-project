# Test suite information

### Test name
	Test for successful connection to Wifi router.

### Test path
tests/repo_tests/shell_tests/wifi_shell

### Type
- Pytest test
- Shell test
- "shell harness" test

### Description
This test is designed to verify errorless boot capability of the board. After booting to operating system, the basic shell commands are executed to verify the boot process is successfully completed. Various kernel configurations are used in multiple test cases for different initial booting conditions. Excpet the  regular pytest files the native Zephyr "shell harness" test with help of regex-patterns inside testcase.yaml is executed as well.

<strong>Shell harness test:</strong><br/>
For more info about Shell harness see the official Zephyr documentation [Custom Shell module](https://docs.zephyrproject.org/latest/develop/test/twister.html) or [Test user guide](../../../../Tests_user_guide.md) in this repository.

### Preconditions
N.A.

### Test steps
1. Run the test with `west twister`command.
2. Verify the successfull booting process with shell command `help`.
3. Verify the successfull booting process with shell command `kernel version`.
4. Verify the successfull booting process with Shell harness tests.

### Expected results
Return string from shell command `help` consists of 'Available commands:'.<br/>
Return string from shell command `kernel version` consists of 'Zephyr version'.<br/>

### Notes
N.A.