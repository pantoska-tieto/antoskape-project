# Tests list

Tests are stored in multiple directories based on <br/>
- test framework used (robot FW, pytest, unittest, ...),
- test target (simulation/emulation/hardware test),
- test type (manual test, automated test, ...), etc.

<br/>

<table>
    <thead>
      <th><strong>TEST PATH</strong></th>
      <th><strong>REQUIRED RESOURCES</strong></th>
      <th><strong>PURPOSE</strong></th></tr>
    </thead>
      <tbody>
        <tr>
        <td>tests/repo_tests/power_cycle_boot</td>
        <td>Raspberry Pi 5, GPIO 25</strong></td>
        <td>Control power off/on relay.</strong></td>
        </tr>
        <tr><td>tests/repo_tests/pwm_ledc</td>
        <td>Raspberry Pi 5, GPIO 24</td>
        <td>Measure PWM signal - frequency and duty cycle.</strong></td>
        </tr>
        <tr><td>tests/repo_tests/gpio_toggle_pytest</td>
        <td>ESP32 S3 devkitc, GPIO 9 (Device Under Test)</td>
        <td>Verify tested GPIO pin status after toggling.</strong></td>
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
        <td  colspan="3"><strong>REPOSITORY - SHELL TESTS</strong></td>
        </tr>
        <td>1</td>
        <td><a href="../tests/repo_tests/shell_tests/ble_shell_basics_battery/TESTINFO.md">Test for BLE GATT service - transmitting the Battery Level value with demanded advertising.</a></td>
        <td>[PYTEST] Test to transmit simulated Battery Level value from Bluetooth LE device. The verification through UART serial port.</td>
        </tr>
        <td>2</td>
        <td><a href="../tests/repo_tests/shell_tests/ble_shell_hrs_bas/TESTINFO.md">Test for BLE GATT services - transmitting the Battery Level and Heart Rate values with demanded advertising.</a></td>
        <td>[PYTEST] Test to transmit simulated BAS and HRS values from Bluetooth LE device. The verification through UART serial port.</td>
        </tr>
        </tr>
        <td>3</td>
        <td><a href="../tests/repo_tests/shell_tests/ble_shell_hrs_mocked/TESTINFO.md">Test for BLE GATT service - capability to transmit and update the Heart Rate value through UART serial port.</a></td>
        <td>[PYTEST] Test to transmit simulated HRS value and update it in BLE device through UART serial port. The verification through UART serial port.</td>
        </tr>
        </tr>
        <td>4</td>
        <td><a href="../tests/repo_tests/shell_tests/display_shell_framebuffer/TESTINFO.md">Test to transmit simulated display-framebuffer data through UART serial port.</a></td>
        <td>[PYTEST] Test to transmit simulated display framebuffer and its CRC32 checksum data. The verification through UART serial port.</td>
        </tr>
        <tr>
        <td>5</td>
        <td><a href="../tests/repo_tests/general_tests/gpio_toggle_pytest/TESTINFO.md">GPIO toggle test with GPUO initiation and toggling through UART shell commands.</a></td>
        <td>[PYTEST] Test for GPIO initiation & toggle capabilities through UART shell commands. The verification through UART serial port.</td>
        </tr>
        </tr>
        <td>6</td>
        <td><a href="../tests/repo_tests/shell_tests/i2c_shell_mocked/TESTINFO.md">Test for I2C write & read commands with UART shell prompt on emulated I2C bus.</a></td>
        <td>[PYTEST] Test to transmit and accept I2C bus shell commands with using emulated I2C bus (derived from Zephyr emulation module for Bosch BMS160 sensor). The verification through UART serial port.</td>
        </tr>
        </tr>
        <td>7</td>
        <td><a href="../tests/repo_tests/shell_tests/sensor_shell_proximity/TESTINFO.md">Test for data evaluation from proximity sensor.</a></td>
        <td>[PYTEST] Test to receive & update for simulated data from proximity sensor. The verification through UART serial port.</td>
        </tr>
        </tr>
        </tr>
        <td>8</td>
        <td><a href="../tests/repo_tests/shell_tests/shell/TESTINFO.md">Test for successful booting of the board.</a></td>
        <td>[PYTEST] Test to transmit a data after successfull booting through the UART serial port. The verification through UART serial port.</td>
        </tr>
        </tr>
        <td>9</td>
        <td><a href="../tests/repo_tests/shell_tests/wifi_shell/TESTINFO.md">Test for successful connection to Wifi router.</a></td>
        <td>[PYTEST] Test to create the connection to Wifi router with demanded SSID after booting the board. The verification through UART serial port.</td>
        </tr>
        </tr>
        <tr>
        <td  colspan="3"><strong>ROBOT FW TESTS</strong></td>
        </tr>
        </tr>
        <td>9</td>
        <td><a href="../tests/robot_tests/hello/hello.robot">Hello world test for Robot framework.</a></td>
        <td>[ROBOT] Hello world sample for Robot FW test.</td>
        </tr>
        </tr>
      </tbody>
</table>

<br/>
