# Tests list

### Table of Contents
1. [Zephyr application - home page](../README.md)
2. [Add new board to project](Add_new_board_to_project.md)
3. [Artifactory storage server](Artifactory_storage_server.md)
4. [GitHub workflow_dispatch panel](Github_workflow_dispatch_panel.md)
5. [HW resources for tests](HW_resources_for_tests.md)
6. [Kconfig tester guide](Kconfig_tester_guide.md)
7. [Raspi runner installation](Raspi_runner_installation.md)
8. [Shell tests with native_sim.md](Shell_tests_with_native_sim.md)
9. Tests list [this page]
10. [Tests user guide](Tests_user_guide.md)
11. [MCUmgr subsystem for testing purposes](MCUmgr_subsystem_for_testing_purpose.md)
12. [Simulation/emulation principles in testing](Simulation_emulation_principles.md)
---


Tests are stored in multiple directories based on <br/>
- test framework used (robot FW, pytest, unittest, ...),
- test target (simulation/emulation/hardware test),
- test type (manual test, automated test, ...), etc.

<br/>

<table>
    <thead>
      <th><strong>TEST FOLDER</strong></th>
      <th><strong>DESCRIPTION</strong></th>
    </thead>
      <tbody>
        <tr>
        <td>tests/manual_tests/</td>
        <td>Test to run manually (requiring test-depend. setup or tools to be initated, specific test commands etc.)</strong></td>
        </tr>
        <tr><td>tests/repo_tests/general_tests/</td>
        <td>Automated tests. Harware and simulation tests for generic device functionalities.</td>
        </tr>
        <tr><td>tests/repo_tests/shell_tests/</td>
        <td>Automated tests. Tests using UART Shell interface to test generic device functionalities.</td>
        </tr>
        <tr><td>tests/robot_tests/</td>
        <td>Test to run with Robot Framework. Not used in this project.</td>
        </tr>
        <tr><td>tests/unit_tests/dut/</td>
        <td>Automated tests. Unit tests with Ztest/Pytest framwork for Device Under Test (DUT) features/modules.</td>
        </tr>
        </tr>
        <tr><td>tests/unit_tests/host/</td>
        <td>Automated tests. Unit tests with Ztest framwork for HOST system features/modules.</td>
        </tr>
      </tbody>
</table>

<br/>

## Overview

<table>
    <thead>
      <th><strong>TEST NR.</strong></th>
      <th><strong>TEST</strong></th>
      <th><strong>DESCRIPTION</strong></th></tr>
    </thead>
      <tbody>
        <tr>
        <td  colspan="3"><strong>MANUAL TESTS</strong></td>
        </tr>
        <tr>
        <td>1</td>
        <td><a href="../tests/manual_tests/esp32_toggle_led_qemu/TESTINFO.md">GPIO toggle test with QEMU emulation</a></td>
        <td>Test GPIO toggle capability with LED connected with using QEMU emulation.</td>
        </tr>
        <tr>
        <td  colspan="3"><strong>REPOSITORY - GENERAL TESTS</strong></td>
        </tr>
        <tr>
        <td>1</td>
        <td><a href="../tests/repo_tests/general_tests/bt_peripheral/TESTINFO.md">Bluetooth LE advertising test.</a></td>
        <td>[PYTEST] Test for Bluetooth LE advertising capabilities.</td>
        </tr>
        <tr>
        <td>2</td>
        <td><a href="../tests/repo_tests/general_tests/gpio_toggle_ztest/TESTINFO.md">GPIO toggle test with Ztest framework.</a></td>
        <td>[ZTEST] Test for GPIO toggle capability with Ztest framework.</td>
        </tr>
        <tr>
        <td>3</td>
        <td><a href="../tests/repo_tests/general_tests/mock_adc/TESTINFO.md">Test for reading mocked sensor parameter value from ADC converter.</a></td>
        <td>Mocked temperature value from mocked ADC sensor.</td>
        </tr>
        <tr>
        <td>4</td>
        <td><a href="../tests/repo_tests/general_tests/power_cycle_boot/TESTINFO.md">Successfull booting after power cycles.</a></td>
        <td>[PYTEST] Test booting capabilities in power cycle test on board HW.</td>
        </tr>
        <tr>
        <td>5</td>
        <td><a href="../tests/repo_tests/general_tests/pwm_ledc/TESTINFO.md">Test for PWM capabilities with LED connected with using LEDC Controller.</a></td>
        <td>[PYTEST] Test to emit specific PWM signal to LED connected and verify it with other GPIO pin.</td>
        </tr>
        <tr>
        <td>6</td>
        <td><a href="../tests/repo_tests/general_tests/zperf/TESTINFO.md">Test for a capabilities to transfer data package through Wifi connection with using perf-tool.</a></td>
        <td>[PYTEST] Test to transmit and receive UDP data package via Wifi connection with using Linux performance analysis tool.</td>
        </tr>
        <tr>
        <td>7</td>
        <td><a href="../tests/repo_tests/general_tests/dfu_ota_bluetooth/TESTINFO.md">Test for a capabilities to perform DFU OTA over Bluetooth.</a></td>
        <td>[PYTEST] Test to execute DFU OTA (Device Firmware Update Over-the-Air) upgrade of Zephyr image on target device over the Bluetooth.</td>
        </tr>
        <tr>
        <td  colspan="3"><strong>REPOSITORY - SHELL TESTS</strong></td>
        </tr>
        <tr>
        <td>1</td>
        <td><a href="../tests/repo_tests/shell_tests/ble_shell_basics_battery/TESTINFO.md">Test for BLE GATT service - transmitting the Battery Level value with demanded advertising.</a></td>
        <td>[PYTEST] Test to transmit simulated Battery Level value from Bluetooth LE device. The verification through UART serial port.</td>
        </tr>
        <tr>
        <td>2</td>
        <td><a href="../tests/repo_tests/shell_tests/ble_shell_hrs_bas/TESTINFO.md">Test for BLE GATT services - transmitting the Battery Level and Heart Rate values with custom-shell commands.</a></td>
        <td>[PYTEST] Test to transmit simulated BAS and HRS values from Bluetooth LE device via custom-shell commands (Zephyr Shell module). The verification through UART serial port.</td>
        </tr>
        <tr>
        <td>3</td>
        <td><a href="../tests/repo_tests/shell_tests/ble_shell_hrs_mocked/TESTINFO.md">Test for BLE GATT service - capability to transmit and update the Heart Rate value with mocked value.</a></td>
        <td>[PYTEST] Test to transmit simulated HRS value mocked with script and update it in BLE device via custom-shell commands (Zephyr Shell module). The verification through UART serial port.</td>
        </tr>
        <tr>
        <td>4</td>
        <td><a href="../tests/repo_tests/shell_tests/display_shell_framebuffer/TESTINFO.md">Test to transmit simulated display-framebuffer data through UART serial port.</a></td>
        <td>[PYTEST] Test to transmit simulated display framebuffer and its CRC32 checksum data. The verification through UART serial port.</td>
        </tr>
        <tr>
        <td>5</td>
        <td><a href="../tests/repo_tests/shell_tests/gpio_toggle_pytest/TESTINFO.md">GPIO toggle test with GPIO initiation and toggling through UART shell commands.</a></td>
        <td>[PYTEST] Test for GPIO initiation & toggle capabilities through UART shell commands. The verification through UART serial port.</td>
        </tr>
        <tr>
        <td>6</td>
        <td><a href="../tests/repo_tests/shell_tests/i2c_shell_mocked/TESTINFO.md">Test for I2C write & read commands with UART shell prompt on emulated I2C bus.</a></td>
        <td>[PYTEST] Test to write and read register values in I2C bus through  the custom shell commands with using emulated I2C bus (derived from Zephyr emulation module for Bosch BMS160 sensor). The verification through UART serial port.</td>
        </tr>
        <tr>
        <td>7</td>
        <td><a href="../tests/repo_tests/shell_tests/sensor_shell_proximity/TESTINFO.md">Test for data evaluation from proximity sensor.</a></td>
        <td>[PYTEST] Test to receive & update for simulated data from proximity sensor. The verification through UART serial port.</td>
        </tr>
        <tr>
        <td>8</td>
        <td><a href="../tests/repo_tests/shell_tests/boot_shell/TESTINFO.md">Test for successful booting of the board.</a></td>
        <td>[PYTEST] Test to transmit a data after successfull booting through the UART serial port. The verification through UART serial port.</td>
        </tr>
        <tr>
        <td>9</td>
        <td><a href="../tests/repo_tests/shell_tests/wifi_shell/TESTINFO.md">Test for successful connection to Wifi router.</a></td>
        <td>[PYTEST] Test to create the connection to Wifi router with demanded SSID after booting the board. The verification through UART serial port.</td>
        </tr>
        <tr>
        <td>10</td>
        <td><a href="../tests/repo_tests/shell_tests/spi_shell_mocked/TESTINFO.md">Test for SPI write & read commands with UART shell prompt on emulated SPI bus.</a></td>
        <td>[PYTEST] Test to write and read register values in SPI bus through  the custom shell commands with using emulated SPI bus (derived from Zephyr emulation module for Bosch BMS160 sensor). The verification through UART serial port.</td>
        </tr>
        <tr>
        <td  colspan="3"><strong>UNIT TESTS</strong></td>
        </tr>
        <tr>
        <td>1</td>
        <td><a href="../tests/unit_tests/dut/gpio_pins_pytest/TESTINFO.md">Test for successful toggling functionality of GPIO pin with Pytest.</a></td>
        <td>[PYTEST, DUT] Test for DUT module to verify the capability of toggle operation on target GPIO pin via the shell commands. The verification through UART serial port.</td>
        </tr>
        <tr>
        <td>2</td>
        <td><a href="../tests/unit_tests/dut/gpio_pins_ztest/TESTINFO.md">Test for successful toggling functionality of GPIO pin with Ztest.</a></td>
        <td>[ZTEST, DUT] Test for DUT module to verify the capability of toggle operation on target GPIO pin via the shell commands.</td>
        </tr>
        <tr>
        <td>3</td>
        <td><a href="../tests/unit_tests/host/base64/TESTINFO.md">Test for Host base64 module.</a></td>
        <td>[ZTEST, HOST] Test for HOST module to verify base64 module capability.</td>
        </tr>
        <tr>
        <td  colspan="3"><strong>ROBOT FW TESTS</strong></td>
        </tr>
        <tr>
        <td>9</td>
        <td><a href="../tests/robot_tests/hello/TESTINFO.md">Hello world test for Robot framework.</a></td>
        <td>[ROBOT] Hello world sample for Robot FW test.</td>
        </tr>
      </tbody>
</table>

<br/>
