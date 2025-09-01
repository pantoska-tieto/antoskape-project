# Copyright (c) 2025 Tietoevry
#
# SPDX-License-Identifier: Apache-2.0

import pytest
from twister_harness import Shell
from twister_harness import DeviceAdapter
import logging
import re
import sys

logger = logging.getLogger(__name__)
# setting path
sys.path.append("../../../test")
from test.tools import tools as tools


@pytest.mark.dependency(name="connect_wifi")
def test_wifi_connect(wifi_connect, shell: Shell):
    logger.info("Testcase: check data transport with zperf tool:")
    if wifi_connect:
        logger.info("Wifi connection established, starting zperf test...")
    else:
        pytest.skip("WiFi connection could not be established, skipping zperf test.")


@pytest.mark.dependency(depends=["connect_wifi"])
def test_zperf_communication(shell: Shell):
    logger.info("Testcase: check network communication ESP32 -> host runner.")
    # Start iperf server on Raspi
    logger.info("Start iperf server listening...")
    out, err = tools.run_cmd("iperf -s -l 1K -B 192.168.1.199")
    _r = re.search("Server listening on TCP port", out)
    if _r:
        logger.info(
            f"Iperf server is listening for data..."
        )
    else:
        raise Exception("Iperf server could not be started!")

    # Send data from ESP32 to Raspi
    lines = shell.exec_command("zperf tcp upload 192.168.1.199 5001 10 1K 5M")
    lines = dut.readlines_until("Rate", timeout=30)
    assert any("Upload completed!" in l for l in lines), "Data transfer from UUT to host runner failed!"
    logger.info("Network communication ESP32 -> host runner succeeded.")  
