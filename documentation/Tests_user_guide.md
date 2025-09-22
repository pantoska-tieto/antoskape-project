# Zephyr tests user guide

This document will guide you through the process of adding and setting up Zephyr tests in the application. All application tests are stored under the `tests/` directory. Each test suite is a folder containing test cases. Each test case is a file with a `.py` or `.c` extension (based on test framework used for the test suite - Pytest, Ztest).

All tests cases in automated process are run in the default branch (main) of the repository with the command skeleton:<br/>

"west twister -vv --platform {platform} --detailed-test-id --device-testing --device-serial {device_serial} --flash-before"

To run test case manually on custom branch code use the GitHub Actions tab  `workflow_dispatch` event, where the additional parameters can be added to the command:<br/>

[https://github.com/pantoska-tieto/antoskape-project/actions/workflows/build.yml](https://github.com/pantoska-tieto/antoskape-project/actions/workflows/build.yml)

## How to add a new test

For basic guideline how to setup Zephyr tests in the application, see the official Zephyr documentation:  
[https://docs.zephyrproject.org/latest/develop/test/ztest.htmls](https://docs.zephyrproject.org/latest/develop/test/ztest.html)<br/>
<br/>

1\. Create new test suite folder under tests/ root sub-folder depending on test-type, for example `tests/repo_tests` for generic application test. Use a meaningfull folder  name. For example, `tests/repo_tests/ble_device_recognition` for BLE device recognition test case.

2\. Create the following structure of files in the test suite folder:<br/>
- `testcase.yaml` - test case configuration file, which contains test case details such as test name, tags, and other parameters.
- `sample.yaml` - test case configuration file, which contains build setup parameters + test case details [OPTIONAL - for samples where the separate Build and Testing process is demanded].
- `src/test.py` or `src/test.c` - test case file, which contains the test code.
- `proj.conf` - configuration file for the test suite, which contains the test suite parameters.
- `CMakeLists.txt` - setup file for compilation process.
- `README.*` - README.rst/README.md file with guidelines/setup recommendations or other important details related to test suite/test_cases.
- other folders/files as needed (e.g., `boards/`, `Kconfig` etc.).<br/>
<br/>

Example:

![Test Suite structure](images/test_suite_structure.png)

<br/>

Test suites stored in `tests/repo_tests/` folder are run in automated mode as generic application tests. To assign any test suite from `tests/` folder to specific test run (regardless of test suite storage folder) you can use a specific tag in `testcase.yaml`  or `sample.yaml` and key `tags:`. Afterwards the test suite can be called in `workflow_dispatch` event with applying this tag in `workflow_dispatch` event field "Test TAGs to filter tests". The same rule is applicable for "Test suite scenario to run" field.<br/>

<br/>
  
## How to setup the test

For basic guideline how to setup Zephyr tests in the application, see the official Zephyr documentation:  
[https://docs.zephyrproject.org/latest/develop/test/twister.html#tests](https://docs.zephyrproject.org/latest/develop/test/twister.html#tests)<br/>
<br/>

1\. Update Test Suite files as requested for demanded test. Pay attention to the crutial setup options like:<br/>
- Update `testcase.yaml` or `sample.yaml` file with reference for target device/board architecture to be tested on. For example to add ESP32 S3 devkitc board into test configuration, add `esp32s3_devkitc/esp32s3/procpu` to `platform_allow` section (see below example).
- Update `testcase.yaml` or `sample.yaml` file with demanded test framework to be applied in test run:  `harness: ztest` for Ztest, `harness: pytest` for Pytest (see below example).


```
tests:
  repo_tests.dut.gpio_toggle_ztest:
    platform_allow:
      - esp32s3_devkitc/esp32s3/procpu
      - esp32c3_devkitm
    tags:
      - gpio
      - integration
      - ztest
    harness: ztest
    integration_platforms:
      - esp32s3_devkitc/esp32s3/procpu
      - esp32c3_devkitm

```

2\. Add board overlay with external DTC file into the `boards/` folder if applicable - needed for the DUT board consists of a differences in HW/configuration which are not implemented in Zephyr yet. Overlay files are typically stored in<br/>

`tests/<test_suite>/board/<board name>.overlay (.conf)`​<br/>

files, where there are automatically recognized by Zephyr applications.<br/>

3\. Add a tag(s) to `tags:` section to be applied in GitHub workflow dispatch panel when running the tests with demanded tag-specification.

4\. Update the `prj.conf` file with generic configuration parameters. This file:<br/>
- defines build-time configuration options for your Zephyr application, sample, or test.
- uses the same syntax as Kconfig files (simple KEY=VALUE pairs).
- customizes which Zephyr features, drivers, and kernel options are enabled or disabled for that specific build/test run.

<br/>
Example - build-time configuration to get Bluetooth support:<br/>
<br/>

```
CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE=2048

CONFIG_BT=y
CONFIG_LOG=y
CONFIG_BT_SMP=y
CONFIG_BT_SIGNING=y
CONFIG_BT_PERIPHERAL=y
CONFIG_BT_DIS=y
CONFIG_BT_ATT_PREPARE_COUNT=5
CONFIG_BT_BAS=y
CONFIG_BT_HRS=y
CONFIG_BT_IAS=y
CONFIG_BT_CTS=y
CONFIG_BT_CTS_HELPER_API=y
CONFIG_BT_PRIVACY=y
CONFIG_BT_DEVICE_NAME="TIETO Bluetooth"
CONFIG_BT_DEVICE_APPEARANCE=833
CONFIG_BT_DEVICE_NAME_DYNAMIC=y
CONFIG_BT_DEVICE_NAME_MAX=65
CONFIG_BT_KEYS_OVERWRITE_OLDEST=y
CONFIG_BT_SETTINGS=y
CONFIG_FLASH=y
CONFIG_FLASH_MAP=y
CONFIG_NVS=y
CONFIG_SETTINGS=y

```
<br/>
5\. Update the `CMakeLists.txt` file with build-time configuration options. This file:<br/>

<br/>

## Notes  
1\. Never use a passwords hardcoded in test code! Use the GitHub secrets variables instead. 

For basic guideline how to use secrets in GitHub Actions, see the official documentation:  
[https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)<br/>

<br/>

Example for Pytest workaround:<br/>

_conftest.py with generic fixtures - vars.json file consists of GitHub secrets variables exported to it within GitHub jobs:_

```
@pytest.fixture(scope="module")
def get_secrets(request):
    # Root path - pytest.ini location
    with open(os.path.join(request.config.rootpath, "vars.json"), "r") as f:
        return json.load(f)
```

<br/>

_Appying imported secrets in pytest test cases:_

```
@pytest.mark.dependency(name="scan")
def test_wifi_scan(get_secrets, dut: DeviceAdapter, shell: Shell):
    logger.info("Testcase: check available wifi SSIDs")
    shell.exec_command('wifi scan')
    lines = dut.readlines_until("Scan request done", timeout=20)
    assert any(get_secrets['PANT_SSID'].lower() in l.lower() for l in lines), "Scanning for demanded Wifi SSID failed!"
    logger.info("Wifi SSID was found.")  
```

<br/>

2\. Output files (in .zip format) from test run available for download in GitHub workflows (see Actions tab):

- _application_html_test_report_artifacts_ - HTML summary report of the test results in the actual workflow run.
- _summary_test_results_artifacts_ - detailed test results artifacts for tests (twister-out/ files from twister tool).
- _twister_out_json_files_artifacts_ - JSON files from test results for non-Robot tests (twister.json files from twister tool).
- _metadata_file_artifacts_ - metadata DB file for non-Robot tests (metadata.json with incremental content of all test runs).
- _application_tests_lists_artifacts_ - list of all tests in the repository (single line record in .txt format, content of testcase.yaml, sample.yaml for all available application tests in .json format).
- _twister_out_xml_files_artifacts_ - XML files from test results for non-Robot tests (twister.xml files from twister tool).