# GitHub workflow\_dispatch panel

### Table of Contents
1. [Zephyr application - home page](../README.md)
2. [Add new board to project](Add_new_board_to_project.md)
3. [Artifactory storage server](documentation/Artifactory_storage_server.md)
4. GitHub workflow_dispatch panel [this page]
5. [HW resources for tests](HW_resources_for_tests.md)
6. [Kconfig tester guide](Kconfig_tester_guide.md)
7. [Raspi runner installation](Raspi_runner_installation.md)
8. [Shell tests with native_sim](Shell_tests_with_native_sim.md)
9. [Tests list](Tests_list.md)
10. [Tests user guide](Tests_user_guide.md)
11. [MCUmgr subsystem for testing purposes](MCUmgr_subsystem_for_testing_purpose.md)
12. [Simulation/emulation principles in testing](Simulation_emulation_principles.md)
13. [BLE terms, roles and definitions](BLE_terms_definitions.md)
---

A **workflow** is a configurable automated process that will run one or more jobs. Workflows are defined by a YAML file checked in to your repository and will run when triggered by an event in your repository, or they can be triggered manually, or at a defined schedule.

**Workflow Dispatch** is a trigger in GitHub Actions that allows you to manually start a workflow. To run a workflow manually, the workflow must be configured in .yml file to run on the `workflow_dispatch` event. When a workflow is configured to run on the `workflow_dispatch` event, you can run the workflow using the Actions tab on GitHub, GitHub CLI, or the REST API. To trigger the `workflow_dispatch` event, your workflow must be in the default branch (main)!<br/>
<br/>

## How to get into workflow UI panel

For basic guideline how to find and trigger workflow manually see the official GitHub page:  
[https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)

To utilize the `workflow_dispatch` event, you need to add it to your repository workflow file in the `.github/workflows/build.yml`. Here is a basic example (extract) from build.yml file at the time of writing this guide:<br/>
<br/>

![Workflow dispatch code in build.yml file](images/workflow_dispatch_code.png)

<br/>
The UI output of this implementation is generated  in GitHub repository after the work branch is merged to default branch. Find the UI by clicking on main menu "Actions" -> left menu "Build" -> click on \<Run workflow> button:<br/>
<br/>
<br/>

![Workflow dispatch button in GitHub repository](images/workflow_dispatch_button.png)

<br/>
The UI for an user updates shows after clicking on the \<Run workflow> button:<br/>
<br/>
<br/>

![Workflow dispatch panel in GitHub repository](images/workflow_dispatch.png)
<br/>
<br/>


## How to trigger workflow dispatch event manually

To manually trigger a workflow:

1.  Navigate to GitHub Actions section where the workflow button is available.
2.  Select the workflow you want to run.
3.  Click on \<Run workflow> button.
4.  Fill in any input parameters if required.
5.  Confirm your setup and trigger event by clicking on \<Run workflow> button at the bottom on UI panel.<br/>
<br/>

## Description of input parameters in workflow UI panel

Workflow dispatch panel allows to use 4 types of inputs: `string`, `choice`, `boolean`, and `environment.` Based on input type, the user can enter the parameter value directly as a string (string, boolean, environment) or choose from pre-defined dropdown menu (choice). The meanings and rules to fill in correct input parameters to UI panel are mentioned in next table:<br/>
<br/>
<br/>

<table>
    <thead>
      <th><strong>FIELD TITLE</strong></th>
      <th><strong>DESCRIPTION</strong></th>
      <th><strong>PARAMETER TO ENTER</strong></th></tr>
    </thead>
      <tbody>
        <tr><td>Use workflow from</td><td>Git branch/Tag, on which the workflow event is triggered and workflow jobs are started. Despite this field is "string" type, the existing GitHub branches are provided in secondary dropdown menu. By entering a string the demanded branch is filtered from all available branch names.</td><td>Branch name/tag by entering a string &amp; selecting branch/tag in dropdown menu.<br /><br /><strong>[STRING]</strong></td>
        </tr>
        <tr><td>Label of the runner to execute the job</td><td><a href="https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/apply-labels">GitHub runner</a> on which the workflow jobs running. It can be GitHub-hosted runner (not recommended due to the restricted quota) or self-hosted runner (must be registered and pre-installed in advance).</td><td>String with runner-label matching the registered runner in GitHub. Only 1 single string is allowed!<br /><br /><strong>[STRING]</strong><br /><strong>Default = raspberrypi5-production</strong><br /><strong>Example = vmware-test</strong></td></tr>
        <tr><td>Target board for the build</td><td>Target board Zephyr qualifier (Device Under Test = DUT): The set of additional tokens, separated by a forward slash (<code>/</code>) that follow the <a href="https://docs.zephyrproject.org/latest/glossary.html#term-board-name">board name</a> (and optionally <a href="https://docs.zephyrproject.org/latest/glossary.html#term-board-revision">board revision</a>) to form the <a href="https://docs.zephyrproject.org/latest/glossary.html#term-board-target">board target</a>. The currently accepted qualifiers are <a href="https://docs.zephyrproject.org/latest/glossary.html#term-SoC">SoC</a>, <a href="https://docs.zephyrproject.org/latest/glossary.html#term-CPU-cluster">CPU cluster</a> and <a href="https://docs.zephyrproject.org/latest/glossary.html#term-variant">variant</a>. See <a href="https://docs.zephyrproject.org/latest/hardware/porting/board_porting.html#board-terminology">Board terminology</a> in Zephyr RTOS for additional details.</td><td>Target platform/board qualifier to be build &amp; tested. Only 1 single string is allowed!<br /><br /><strong>[STRING]</strong><br /><strong>Default = esp32s3_devkitc/esp32s3/procpu</strong><br /><strong>Example = nrf5340dk/nrf5340/cpuapp</strong></td></tr>
        <tr><td>Tests target</td><td>Target of executed test - real hardware or simulation/emuation without flashing to real board. It has the impact on using west twister command arguments <code>--device-testing, --device-serial, --flash-before</code> (omitted in case of Simulation/Emulation).<br/>
        When "Real_hardware" option is selected, the Auto mapping of physical USB ports to udev rules is automatically applied and a persistent symbolic links are mapped to physical serial ports. All hardware tests are then executed with serial ports symlinks.</td><td><strong>[CHOICE]</strong><br /><strong>Default = Real_hardware</strong><br /><strong>Example = Simulation_Emulation</strong></td></tr>
        <tr><td>Test TAGs to filter tests</td><td><p><a href="https://docs.zephyrproject.org/latest/develop/test/twister.html">Test tag(s)</a> - tags to restrict which tests to run by tag value. Default is to not do any tag filtering. &nbsp;Multiple invocations are treated as a logical 'or' relationship. Test tags are located in sample.yaml or testcase.yaml files within the tests-section.&nbsp;<br /><strong>Example:</strong></p>tests:
        testing.ztest.base.verbose_0_userspace:
          filter: CONFIG_ARCH_HAS_USERSPACE
          extra_args: CONF_FILE=prj_verbose_0.conf
          tags:
            - userspace
          extra_configs:
          - CONFIG_TEST_USERSPACE=y</td><td>Test tags to filter demanded tests to run. Multiple strings separated by space are allowed!<br /><br /><strong>[STRING]</strong><br /><strong>Default = N/A</strong><br /><strong>Example = unit sanitary&nbsp;</strong></td></tr>
          <td>Arguments to the pytest subprocess (extend YAML config)</td><td><a href="https://docs.zephyrproject.org/latest/develop/test/twister.html">Additional arguments</a> for Pytest subprocess. This parameter will extend the pytest_args from the harness_config in YAML file.&nbsp;<br /><strong>Example:</strong><br /><code>--pytest-args "--maxfail=2 --disable-warnings"</code><br /><br />This will run Twister and pass the arguments --maxfail=2 --disable-warnings to the pytest subprocess, limiting failures to 2 and disabling warnings output.</td><td>Option(s) to be forwarded to pytest subprocess when running Twister tests. Multiple strings separated by space are allowed! Prepend "--" before each option.<br /><br /><strong>[STRING]</strong><br /><strong>Default = N/A</strong><br /><strong>Example = --maxfail=2 &nbsp;--disable-warnings</strong></td></tr>
          <tr><td>Test suite scenario to run</td><td><p>Each testsuite can consist of multiple <a href="https://docs.zephyrproject.org/latest/develop/test/twister.html">test scenarios.</a> This parameter allows to filter specific scenario to run while other scenarios in the same test suite are ignored.</p><p>Scenarios are named by 'path/relative/to/Zephyr/base/section.subsection_in_testcase_yaml', or just 'section.subsection' identifier. See an example for scenario "esp.wifi.sec.wpa2":</p>
            <code>esp.wifi.sec.none:
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
  - esp32_devkitc/esp32/procpu</code>
          </td><td><p>Test scenario name to filter when running the testcase. Only 1 single string is allowed!<br /><strong>Note:&nbsp;</strong><br />to find the demanded test scenario faster in search process, select the root-folder where the scenario exists in "Test scope to run" option.</p><p><strong>[STRING]</strong><br /><strong>Default = N/A</strong><br /><strong>Example = esp.wifi.sec.wpa2</strong></p></td></tr>
          <tr><td>Target operation with image</td><td>BAsed on selected option only the BUILD workflow ["Build only"], or both BUILD with TESTING workflows are triggered ["Build with testing"].</td><td><strong>[CHOICE]</strong><br /><strong>Default = Build with testing</strong><br /><strong>Example = Build only</strong></td></tr>
          <tr><td>Tests scope to run</td><td><p>Select the target folder, where the search proces looks for all test suites located there to run. Test suite is identified by existing project file prj.conf.</p><p>In case the Test suite scenario parameter is used, the selected folder path is assigned to argument <strong>"--testsuite-root"</strong> in twister command and thus the searching for demanded scenarion is faster. In this case only demanded test scenario is selected to run with twister command and other test suites/test cases are ignored!</p><p>Mapping UI field -&gt; GitHub application folder (note that the native Zephyr RTOS tests in zephyr/tests/ workspace can be selected too): &nbsp;</p>
          <code>app/repo -&gt; __w/antoskape-project/antoskape-project/customer-application/tests/repo_tests</code><br/>
          <br/>
          <code>app/unit/dut -&gt; __w/antoskape-project/antoskape-project/customer-application/tests/unit_tests/dut</code><br/>
          <br/>
          <code>app/unit/host -&gt; __w/antoskape-project/antoskape-project/customer-application/tests/unit_tests/host</code><br/>
          <br/>
          <code>app/robot -&gt; __w/antoskape-project/antoskape-project/customer-application/tests/robot_tests</code><br/>
          <br/>
          <code>integration_tests -&gt; __w/antoskape-project/antoskape-project/customer-application/tests</code><br/>
          <br/>
          <code>zephyr_framework_tests -&gt; __w/antoskape-project/antoskape-project/zephyr/tests</code></td><td>Target folder where all test cases are selected to run with twister command. This path is assigned to "--testsuite-root" argument if Test suite scenario is filled in previous parameter. Only 1 single string is allowed!<br /><br /><strong>[CHOICE]</strong><br /><strong>Default = app/repo</strong><br /><strong>Example = app/unit/host</strong></td></tr>
      </tbody>
</table>
<br/>

## Integration tests

Integration tests can be split over any of tests/ subfolders. The only criterias to <a href="Tests_user_guide.md">include arbitraty test</a> into the Integration tests set are:<br/>

* the testcase.yaml/sample.yaml file consists of "- integration" tag under "tags" section.
* target board platform is added under "integration_platforms" section in testcase.yaml/sample.yaml file.<br/>
<br/>
See example:<br/>
<br/>

![Test case assigned to Integration tests](images/integration_test.png)

<br/>
<br/>

## Multiple filtering parameters in the same workflow command

Workflow dispatch panel allows users to apply multiple filtering input parameters at the same time - all are passsed as an filtering arguments to the same workflow command. The order of filtering arguments passed to "west twister" command is the same as they are listed in the workflow UI panel (from top to bottom). From concurrency aspect the sooner arguments in command have higher priority than later ones.  See the priority order for workflow dispatch parameters/arguments in following table (0 = highest priority):<br/>
<br/>

<table>
    <thead>
      <th><strong>PARAMETER/ARGUMENT NAME</strong></th>
      <th><strong>PRIORITY</strong></th>
    </thead>
      <tbody>
        <tr><td>Test TAGs to filter tests</td><td>0</td></tr>
        <tr><td>Arguments to the pytest subprocess (extend YAML config)</td><td>1</td></tr>
        <tr><td>Test suite scenario to run</td><td>2</td></tr>
      </tbody>
</table>
<br/>

When running workflow dispatch command with multiple arguments, the filtering criterias are applied with following rules:<br/>
* if sooner argument result is FALSE (no test found), then the later argument in command is applied,
* if sooner arguments result is TRUE (test(s) found), then the filtering process is finished and all later arguments are ignored.<br/>
<br/>

## Twister command examples

This GitHub repository workflow has implemented the following Twister command skeleton with respect to workflow dispatch trigger parameters available:

"Test suite scenario to run" parameter is not filled (empty field) . All test suites from desired folder are selected to run.

```c
west twister -vv --platform esp32s3_devkitc/esp32s3/procpu \
    --device-testing --device-serial /dev/ttyUSB0 \
    --west-flash \
    --flash-before \
    --tag net --force-tags \
    --pytest-args "--maxfail=2 --disable-warnings" \
    -T tests/repo
```

"Test suite scenario to run" parameter is filled with scenario-string. All test suites/test cases from desired folder are ignored except the demanded test scenario, which will run with "west twister" command.

```c
west twister -vv --platform esp32s3_devkitc/esp32s3/procpu \
    --device-testing --device-serial /dev/ttyUSB0 
    --west-flash \
    --flash-before \
    --tag net --force-tags \
    --pytest-args "--maxfail=2 --disable-warnings" \
    --scenario sample.pytest.shell \
    --testsuite-root tests/repo
```
<br/>

## Zephyr tests terminology

<br/>
<table>
    <thead>
      <th><strong>TERM</strong></th>
      <th><strong>DESCRIPTION</strong></th>
    </thead>
      <tbody>
        <tr><td>Test suite</td><td><p>Top folder consisting of set of tests (sub-folders).</p>
                        <p><strong>Example:</strong><br /><code>tests/kernel</code></p></td></tr>
        <tr><td>Test</td><td><p>Sub-folders under Test suite. These are
                        named by 'path/relative/to/Zephyr/base/section.subsection_in_testcase_yaml',<br/>or just 'section.subsection'
                        identifier.</p>
                        <p><strong>Example:</strong><br /><code>tests/kernel/ipi_cascade</code></p></td></tr>
        <tr><td>Test scenario</td><td><p>Test scenario is named by 'path/relative/to/Zephyr/base/section.subsect
                        ion_in_testcase_yaml', or just 'section.subsection' identifier.</p>
                        <p><strong>Example:</strong><br/>tests/basic/shell consists of scenario <strong>sample.pytest.shell</strong><br /><code>tests:
    sample.pytest.shell:
      harness: pytest
      harness_config:
        pytest_dut_scope: session
      tags: antoska</code></p></td></tr>
        <tr><td>Test case</td><td><p>Test functions = test cases. Test case is on the lowest level in test terminology and is represented by test-function inside test-file.py (in Pytest context).</p>
        <p><strong>Example:</strong><br />tests/repo_tests/shell/pytest/test_shell.py consists of tes case:<br/>
        <code>def test_shell_print_version(shell: Shell):</code></p></td></tr>
      </tbody>
</table>