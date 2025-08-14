# Zephyr application

This repo is representing **custom Zephyr RTOS application** for building and testing custom testcases with Pytest framework. It is using structure based on basic Zephyr example applicationn
https://github.com/zephyrproject-rtos/example-application

It is representing a typical T3 topology model in conjunction with GitHub workflows/actions and CI/CD automation process.
<br/>

## General description

* .github/workflows/build.yml   - basic CI/CD workflow file,
* .github/workflows/reports-summary-publish.yml   - workflow file for tests summary report,
* app/    -   dir for boards applications,
* app-esp32/  -   dir for ESP32 boards applications,
* test/ - dir for test suites/cases.
  
  <br/>

## Testing

Before trigerring a test, make sure you have a proper Zephyr development
environment. Follow the official
[Zephyr Getting Started Guide](https://docs.zephyrproject.org/latest/getting_started/index.html).

1. Clone this repo to your customer-application/ directory by initiation workspace in
"customer-application" folder by the commands:

```copy
cd <your Zephyr development env directory>
west init -m git clone https://github.com/pantoska-tieto/antoskape-project.git customer-application

Result:

drwxrwxr-x 13 peter peter 4096 Aug 14 17:35 .
drwxr-x--- 23 peter peter 4096 Jul 30 19:44 ..
drwxrwxr-x  3 peter peter 4096 Jul 23 14:33 bootloader
drwxrwxr-x 15 peter peter 4096 Aug 14 16:45 customer-application
drwxrwxr-x  9 peter peter 4096 Jul 23 14:35 modules
drwxrwxr-x  3 peter peter 4096 Aug 14 16:37 .pytest_cache
drwxrwxr-x  2 peter peter 4096 Jul 28 15:49 sources
drwxrwxr-x  4 peter peter 4096 Jul 23 14:33 tools
drwxrwxr-x  2 peter peter 4096 Aug 11 20:03 twister-out
drwxrwxr-x  2 peter peter 4096 Aug 11 20:01 twister-out.1
drwxrwxr-x  6 peter peter 4096 Jul 23 14:38 .venv
drwxrwxr-x  2 peter peter 4096 Jul 23 14:17 .west
drwxrwxr-x 42 peter peter 4096 Aug 11 21:56 zephyr
```

<br />

2. Update Zephyr environment data within your application directory.

```copy
cd customer-application
west update

```

<br />

3. Run a desired test case from test/ directory with "west twister" from workspace root directory with following command (example for ESP32 S3 Devkitc board).

```copy
west twister -vv --platform esp32s3_devkitc/esp32s3/procpu --device-testing --device-serial /dev/ttyUSB0  --west-flash -T customer-application/test/shell
```

<br />

## Building and running

Make sure you already initiated the environment like mentioned in the previous chapter "Testing".

Build and flash the application from workspace root directory with following command (blinky example for ESP32 S3 Devkitc board):

```copy
west build -p always -b esp32s3_devkitc/esp32s3/procpu customer-application/app-esp32/blinky
west flash
```

<br />

**NOTES:**

1. To enable the building/testing for other target boards than ESP32 S3 Devkitc, update the respective testcase.yml/sample.yaml files in sections
   platform_allow
   integration_platforms (if required in integration tests)
   with demanded target board string - see example:

```copy
common:
  sysbuild: true
    platform_allow:
      - esp32s3_devkitc/esp32s3/procpu
      - esp32_devkitc/esp32/procpu
      - esp32s2_saola
    timeout: 600
    slow: true
    tags:
      - pytest
      - mcuboot
      - mcumgr
    tests:
    boot.with_mcumgr.test_upgrade:
    platform_allow:
      - esp32s3_devkitc/esp32s3/procpu
      - esp32_devkitc/esp32/procpu
      - esp32s2_saola
    integration_platforms:
      - esp32s3_devkitc/esp32s3/procpu
      - esp32_devkitc/esp32/procpu
      - esp32s2_saola
    harness: pytest
    harness_config:
    pytest_root:
      - "pytest/test_shell.py"
```

<br/>

2. All above test/build commands can be triggered from within customer-application directory as well. Update then the target test/application paths accordingly!

