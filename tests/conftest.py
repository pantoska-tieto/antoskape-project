"""
Pytest fixture file for
- getting GitHub secrets variables to be applied in test cases.

"""
import pytest
import json
import os
from twister_harness import Shell
import time

# Enable custom parameters in pytest.ini
def pytest_addoption(parser):
    parser.addini("dut_ip_address", help="IP address of DUT board", default="192.168.1.104")
    parser.addini("self_host_runner_ip_address", help="IP address of self-hosted runner", default="192.168.1.199")

@pytest.fixture(scope="module")
def get_secrets(request):
    # Root path - pytest.ini location
    with open(os.path.join(request.config.rootpath, "vars.json"), "r") as f:
        return json.load(f)

@pytest.fixture
def wifi_connect(get_secrets, shell: Shell):
    ssid = get_secrets['PANT_SSID']
    lines = shell.exec_command(f'wifi connect -s {ssid} -p {get_secrets['PANT_SSID_PW']} -k 1')

    # Check for wifi connection status in asynchronous returns from uart
    def wait_for_wifi_status(timeout=20, step=1) -> bool:
        timeout_time = time.time() + timeout
        while time.time() < timeout_time:
            try:
                lines = shell.exec_command("wifi status")
                response = shell.get_filtered_output(lines)
                if any([f"SSID: {ssid}" in line for line in response]):
                    return True
            except TwisterHarnessTimeoutException:
                print("Timeout waiting for wifi status expired...")
                return False
            time.sleep(step)
        return False   

    return wait_for_wifi_status()
