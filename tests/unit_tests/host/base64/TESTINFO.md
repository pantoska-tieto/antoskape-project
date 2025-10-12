# Test suite information

### Test name
Test for successful toggling the GPIO pin with Pytest.

### Test path
tests/unit_tests/host/base64

### Type
- Ztest
- Unit test

### Description
This Unit test is designed to verify the capability of Host lib/utils/base64.c module.

### Preconditions
N.A.

### Test steps
1. Run the test with `west twister`command.
2. Verify base64_encode functionality.
3. Verify base64_decode functionality.
3. Verify error paths - encode functionality.
3. Verify error paths - decode functionality.

### Expected results
Return values from lib/utils/base64.c module must fit the expected values.

### Notes
N.A.