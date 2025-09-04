# GitHub workflow\_dispatch panel

A **workflow** is a configurable automated process that will run one or more jobs. Workflows are defined by a YAML file checked in to your repository and will run when triggered by an event in your repository, or they can be triggered manually, or at a defined schedule.

**Workflow Dispatch** is a trigger in GitHub Actions that allows you to manually start a workflow. To run a workflow manually, the workflow must be configured in .yml file to run on the `workflow_dispatch` event. When a workflow is configured to run on the `workflow_dispatch` event, you can run the workflow using the Actions tab on GitHub, GitHub CLI, or the REST API. To trigger the `workflow_dispatch` event, your workflow must be in the default branch (main)!

## How to get into workflow UI panel

For basic guideline how to find and trigger workflow manually see the official GitHub page:  
[https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)

To utilize the `workflow_dispatch` event, you need to add it to your repository workflow file in the `.github/workflows`/build.yml. Here is a basic example (extract) from build.yml file at the time of writing this guide:

![Workflow dispatch code in build.yml file](images/workflow_dispatch_code.png)

The UI output of this implementation is generated  in GitHub repository after the work branch is merged to default branch. Find the UI by clicking on main menu "Actions" -> left menu "Build" -> click on \<Run workflow> button:

![Workflow dispatch button in GitHub repository](images/workflow_dispatch_button.png)

The UI for an user updates shows after clicking on the \<Run workflow> button:

![Workflow dispatch panel in GitHub repository](images/workflow_dispatch.png)

## How to trigger workflow dispatch event manually

To manually trigger a workflow:

1.  Navigate to GitHub Actions section where the workflow button is available.
2.  Select the workflow you want to run.
3.  Click on \<Run workflow> button.
4.  Fill in any input parameters if required.
5.  Confirm your setup and trigger event by clicking on \<Run workflow> button at the bottom on UI panel.

## Description of input parameters in workflow UI panel

Workflow dispatch panel allows to use 4 types of inputs: `string`, `choice`, `boolean`, and `environment.` Based on input type, the user can enter the parameter value directly as a string (string, boolean, environment) or choose from pre-defined dropdown menu (choice). The meanings and rules to fill in correct input parameters to UI panel are mentioned in next table:

|Field title|Meaning/description|Parameter to enter|
|--- |--- |--- |
|Use workflow from|Git branch/Tag, on which the workflow event is triggered and workflow jobs are started. Despite this field is "string" type, the existing GitHub branches are provided in secondary dropdown menu. By entering a string the demanded branch is filtered from all available branch names.|Branch name/tag by entering a string & selecting branch/tag in dropdown menu.[STRING]|
|Label of the runner to execute the job|GitHub runner on which the workflow jobs running. It can be GitHub-hosted runner (not recommended due to the restricted quota) or self-hosted runner (must be registered and pre-installed in advance).|String with runner-label matching the registered runner in GitHub. Only 1 single string is allowed![STRING]Default = raspberrypi5-productionExample = vmware-test|
|Target board for the build|Target board Zephyr qualifier (Device Under Test = DUT): The set of additional tokens, separated by a forward slash (/) that follow the board name (and optionally board revision) to form the board target. The currently accepted qualifiers are SoC, CPU cluster and variant. See Board terminology in Zephyr RTOS for additional details.|Target platform/board qualifier to be build & tested. Only 1 single string is allowed![STRING]Default = esp32s3_devkitc/esp32s3/procpuExample = nrf5340dk/nrf5340/cpuapp|
|Serial device for connecting target board|Serial port in OS where the DUT is connected to. Depends on the host operating system.|Serial port for connection the DUT. Only 1 single string is allowed![STRING]Default = /dev/ttyUSB0Example = /dev/ttyACM0|
|Test TAGs to filter tests|Test tag(s) - tags to restrict which tests to run by tag value. Default is to not do any tag filtering.  Multiple invocations are treated as a logical 'or' relationship. Test tags are located in sample.yaml or testcase.yaml files within the tests-section. Example:tests:
  testing.ztest.base.verbose_0_userspace:
    filter: CONFIG_ARCH_HAS_USERSPACE
    extra_args: CONF_FILE=prj_verbose_0.conf
    tags:
      - userspace
    extra_configs:
      - CONFIG_TEST_USERSPACE=y|Test tags to filter demanded tests to run. Multiple strings separated by space are allowed![STRING]Default = N/AExample = unit sanitary|
|Pattern to filter specific tests (regex)|The test pattern to select demanded tests. The twister command runs only the tests matching the specified pattern. The pattern can include regular expressions!|Test pattern (incl. REGEX) to filter demanded tests to run. Only 1 single string is allowed![STRING]Default = N/AExample = shell.*vt100|
|Arguments to the pytest subprocess (extend YAML config)|Additional arguments for Pytest subprocess. This parameter will extend the pytest_args from the harness_config in YAML file. Example:--pytest-args "--maxfail=2 --disable-warnings"This will run Twister and pass the arguments --maxfail=2 --disable-warnings to the pytest subprocess, limiting failures to 2 and disabling warnings output.|Option(s) to be forwarded to pytest subprocess when running Twister tests. Multiple strings separated by space are allowed! Prepend "--" before each option.[STRING]Default = N/AExample = --maxfail=2  --disable-warnings|
|Test suite scenario to run|Each testsuite can consist of multiple test scenarios. This parameter allows to filter specific scenario to run while other scenarios in the same test suite are ignored.Scenarios are named by 'path/relative/to/Zephyr/base/section.subsection_in_testcase_yaml', or just 'section.subsection' identifier. See an example for scenario "esp.wifi.sec.wpa2":tests:
  esp.wifi.sec.none:
    tags: wifi
    filter: CONFIG_WIFI_ESP32
    extra_configs:
      - CONFIG_ESP32_WIFI_STA_AUTO_DHCPV4=y
    platform_allow:
      - esp32_devkitc/esp32/procpu
      - esp32s2_saola
  esp.wifi.sec.wpa2:
    tags: wifi
    filter: CONFIG_WIFI_ESP32
    extra_configs:
      - CONFIG_WIFI_TEST_AUTH_MODE_WPA2=y
      - CONFIG_ESP32_WIFI_STA_AUTO_DHCPV4=y
    platform_allow:
      - esp32_devkitc/esp32/procpu|Test scenario name to filter when running the testcase. Only 1 single string is allowed!Note: to find the demanded test scenario faster in search process, select the respective "Test scope to run" folder, where the scenario exists, in next option![STRING]Default = N/AExample = esp.wifi.sec.wpa2|
|Tests scope to run|Select the target folder, where the search proces looks for all test suites located there to run. Test suite is identified by existing project file prj.conf. In case the Test suite scenario parameter is used, the selected folder path is assigned to argument "--testsuite-root" in twister command and thus the looking for demanded scenarion is faster. In this case only demanded test scenario is selected to run with twister command and other test suites/test cases are ignored!Mapping UI field -> GitHub application folder (note that the native Zephyr RTOS tests in zephyr/tests/ workspace can be selected too):  app/repo -> __w/antoskape-project/antoskape-project/customer-application/tests/repo
app/integration -> __w/antoskape-project/antoskape-project/customer-application/tests/integration
app/unit -> __w/antoskape-project/antoskape-project/customer-application/tests/unit
app(all tests) -> __w/antoskape-project/antoskape-project/customer-application/tests
zephyr(all tests) -> __w/antoskape-project/antoskape-project/zephyr/tests|Target folder where all test cases are selected to run with twister command. This path is assigned to "--testsuite-root" argument if Test suite scenario is filled in previous parameter. Only 1 single string is allowed![CHOICE]Default = app/repoExample = app/unit|


## Twister command examples

This GitHub repository workflow has implemented the following Twister command skeleton with respect to workflow dispatch trigger parameters available:

"Test suite scenario to run" parameter is not filled (empty field) . All test suites from desired folder are selected to run.

```
west twister -vv --platform esp32s3_devkitc/esp32s3/procpu \
    --device-testing --device-serial /dev/ttyUSB0 \
    --west-flash \
    --flash-before \
    --tag net --force-tags 
    --test-pattern  shell.*vt100 \
    --pytest-args "--maxfail=2 --disable-warnings" \
    -T tests/repo
```

"Test suite scenario to run" parameter is filled with scenario-string. All test suites/test cases from desired folder are ignored except the demanded test scenario, which will run with "west twister" command.

```
west twister -vv --platform esp32s3_devkitc/esp32s3/procpu \
    --device-testing --device-serial /dev/ttyUSB0 
    --west-flash \
    --flash-before \
    --tag net --force-tags \
    --test-pattern  shell.*vt100 \
    --pytest-args "--maxfail=2 --disable-warnings" \
    --scenario sample.pytest.shell \
    --testsuite-root tests/repo
```