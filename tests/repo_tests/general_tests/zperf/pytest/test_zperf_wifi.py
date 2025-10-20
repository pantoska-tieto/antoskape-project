# Copyright (c) 2025 Tietoevry
#
# SPDX-License-Identifier: Apache-2.0

import pytest
from twister_harness import Shell
from twister_harness import DeviceAdapter
import logging
import re
import sys
import os
from pathlib import Path


logger = logging.getLogger(__name__)
# setting path for tools module
_p = Path(os.path.abspath(__file__)).parents[5]
sys.path.append(f"{str(_p)}/tests")
from tools import tools


@pytest.mark.dependency(name="connect_wifi", scope="module")
def test_wifi_connect(wifi_connect, shell: Shell):
    logger.info("Testcase: test wifi connection")
    logger.info("Connect to wifi network.")
    assert wifi_connect, "WiFi connection could not be established, skipping zperf test."
    logger.info("Wifi connection established, starting zperf test...")

@pytest.mark.dependency(depends=["connect_wifi"], scope="module")
def test_udp_from_runner_to_dut(request, dut: DeviceAdapter, shell: Shell):
    logger.info("Testcase: test UDP communication host runner -> DUT")
    config = request.config
    dut_ip = config.getini("dut_ip_address")

    logger.info("Testcase: check UDP communication host runner -> DUT.")
    # Initiate UDP port on DUT
    lines = shell.exec_command("zperf udp download 5001")

    # Send UDP packets from host runner
    logger.info("Start UDP packets upload with iperf tool...")
    _out, _err, _ret = tools.run_cmd(["iperf", "-l", "1K", "-u", "-c", f"{dut_ip}", "-b", "1M"])

    # Read response message from DUT
    lines = dut.readlines_until("rate", timeout=30)
    assert any("received packets" in l for l in lines), "UDP packets were not received on DUT!"
    logger.info("UDP packets were received successfully on DUT.")     
