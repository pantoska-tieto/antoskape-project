import pytest
import re
import logging
from twister_harness import Shell
from twister_harness import DeviceAdapter


logger = logging.getLogger(__name__)

def test_bt_central_role(dut: DeviceAdapter, shell: Shell):
    logger.info("Testcase: check Bluetooth LE Central functionality")
    lines = dut.readlines_until("Disconnected", timeout=20)
    logger.info(f"BT scanning results: {lines}")
    # Find MAC address for disconnected device
    resp = [i.strip() for i in lines if "Disconnected" in i][0]
    mac_addr = re.findall(r"([0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5})", resp)[0]
    # Find MAC address for device with expected advertising
    device = [i.split(" ")[3] for i in lines if "Name: PA-iPhone" in i][0]    
    logger.info(f"MAC address of auxiliary BT device: {device}")
    assert mac_addr ==  device, "Auxilliary BT device was not found!"
    logger.info("Bluetooth LE Central role functionality tests passed.")  