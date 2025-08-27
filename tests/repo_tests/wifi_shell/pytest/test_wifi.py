# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0

import pytest
import time
from twister_harness import Shell
from twister_harness import DeviceAdapter
import os

# Initiate variables
# Get the path of the runner file
env_file = os.getenv("GITHUB_ENV") 
with open(env_file, "r") as env_file:
    env_content = env_file.readlines()
    if any("SSID" in line for line in env_content):
        env_ssid = os.environ["SSID"]
    if any("SSID_PWD" in line for line in env_content):
        env_ssid_passwd = os.environ["SSID_PWD"]
print(f"pantoska SSID: {env_ssid}")


@pytest.mark.dependency(name="scan")
def test_wifi_scan(dut: DeviceAdapter, shell: Shell):
    print("Testcase: check available wifi SSIDs:")
    shell.exec_command("wifi scan")
    lines = dut.readlines_until("Scan request done", timeout=20)
    assert any(env_ssid.lower() in l.lower() for l in lines), "Scanning for demanded Wifi SSID failed!"    


@pytest.mark.dependency(depends=["scan"])
def test_wifi_connect(shell: Shell):
    print("Testcase: check successfull wifi connection:")
    lines = shell.exec_command(f"wifi connect -s {env_ssid} -p {env_ssid_passwd} -k 1")

    # Check for wifi connection status in asynchronous returns from uart
    def wait_for_wifi_status(timeout=20, step=1) -> bool:
        timeout_time = time.time() + timeout
        while time.time() < timeout_time:
            try:
                lines = shell.exec_command("wifi status")
                response = shell.get_filtered_output(lines)
                if any([f"SSID: {env_ssid}" in line for line in response]):
                    return True
            except TwisterHarnessTimeoutException:
                print("Timeout waiting for wifi status expired...")
                return False
            time.sleep(step)
        return False   

    assert wait_for_wifi_status(), "Wifi connection failed!"
