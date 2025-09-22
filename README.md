# Zephyr application

This repo is representing **custom Zephyr RTOS application** for building and testing custom testcases with Pytest framework. It is using structure based on basic Zephyr example applicationn
https://github.com/zephyrproject-rtos/example-application

It is representing a typical T2 topology model in conjunction with GitHub workflows/actions and CI/CD automation process.
<br/>

## General description

* .github/workflows/build.yml   - basic CI/CD workflow file,
* .github/workflows/reports-summary-publish.yml   - workflow file for tests summary report,
* app/    -   dir for boards applications,
* app-esp32/  -   dir for ESP32 boards applications,
* test/ - dir for test suites/cases.

<br/>
Before starting, make sure you have a proper Zephyr development
environment. Follow the official
[Zephyr Getting Started Guide](https://docs.zephyrproject.org/latest/getting_started/index.html).

<br/>

## Initialization - create new workspace from scratch
Initialize the workspace folder (customer-application) where the customer-application and all Zephyr modules will be cloned. 

```copy
cd \<any target directory\>
west init -m https://github.com/pantoska-tieto/antoskape-project --mr main customer-application
cd customer-application
west update

Result in customer-application/ directory:

drwxrwxr-x  8 peter peter 4096 Aug 14 21:58 .
drwxrwxr-x 11 peter peter 4096 Aug 14 21:31 ..
drwxrwxr-x  2 peter peter 4096 Aug 14 21:31 .west
drwxrwxr-x 10 peter peter 4096 Aug 14 21:31 antoskape-project    --> github repo content!
drwxrwxr-x  3 peter peter 4096 Aug 14 21:58 bootloader
drwxrwxr-x  9 peter peter 4096 Aug 14 22:01 modules
drwxrwxr-x  4 peter peter 4096 Aug 14 21:58 tools
drwxrwxr-x 23 peter peter 4096 Aug 14 21:42 zephyr
```

<br/>

## Initialization - add application to existing workspace
Clone this repo to your customer-application/ directory within the ready Zephyr development environment workspace.<br/>
Workspace root directory = \<your Zephyr development environment directory\>

```copy
cd <your Zephyr development env directory>
git clone https://github.com/pantoska-tieto/antoskape-project.git customer-application

Result in your Zephyr development env directory:

drwxrwxr-x 13 peter peter 4096 Aug 14 17:35 .
drwxr-x--- 23 peter peter 4096 Jul 30 19:44 ..
drwxrwxr-x  3 peter peter 4096 Jul 23 14:33 bootloader
drwxrwxr-x 15 peter peter 4096 Aug 14 16:45 customer-application    --> github repo content!
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

Since you are using an existing Zephyr workspace, you can use 'west build' or any other west commands to build, flash, and debug.

<br/>

## Building and running
Build and flash the application from workspace root directory with following command (blinky example for ESP32 S3 Devkitc board) 
- example for application added to existing workspace:

```copy
west build -p always -b esp32s3_devkitc/esp32s3/procpu customer-application/app-esp32/blinky
west flash
```

<br/>
Building, flashing and testing jobs can be automated by GitHub workflow process and executed on GitHub runners - machines that execute jobs. Besides the GitHub-hosted runners the users can host own runners/machines and customize the environment used to run jobs - self-hosted runners. This project used self-hosted runners by default. For more details see <a href="documentation/Raspi_runner_installation.md">Raspi_runner_installation</a> guide.
<br/>

## Testing
Run a desired test case from tests/ with "west twister" from workspace root directory with following command (example for ESP32 S3 Devkitc board)
- example for application added to existing workspace.

```copy
west twister -vv --platform esp32s3_devkitc/esp32s3/procpu --device-testing --device-serial /dev/ttyUSB0  --west-flash --flash-before -T customer-application/tests/shell
```
<br/>
Tests can be triggered from GitHub Actions workflows automatically by workflow .yaml file. This file contains also workflow_dispatch configuration which is used to trigger the workflow manually.  For more details see <a href="documentation/Github_workflow_dispatch_panel.md">Github_workflow_dispatch_panel</a> guide.

For more detailed information how to add and update application tests see <a href="documentation/Tests_user_guide.md">Tests User Guide</a>.

<br/>

## NOTES

1. To enable the building/testing for other target boards than ESP32 S3 Devkitc, update the respective testcase.yml/sample.yaml files in sections
   platform_allow
   integration_platforms (if required in integration tests)
   with demanded target board string - see example, or read <a href="documentation/Tests_user_guide.md">Tests User Guide</a>:

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

