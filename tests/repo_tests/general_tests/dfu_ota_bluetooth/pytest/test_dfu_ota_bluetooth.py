# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0

import logging
import pytest
import os
import sys
import shutil
import time
import subprocess
from twister_harness import DeviceAdapter
from pathlib import Path


logger = logging.getLogger(__name__)
# setting path for tools module
_p = Path(os.path.abspath(__file__)).parents[4]
sys.path.append(f"{str(_p)}/tests")
from tools import tools

# BLE peer name to connect to
peer_name = "TietoBLE-OTA"

def test_image_list(dut: DeviceAdapter):
    # Wait for device to boot and advertise
    time.sleep(5)
    # Retry to get SMP server data in loop if any delay issue
    attempts = 2
    delay = 5
    last_stdout = ""
    last_stderr = ""
    
    for i in range(attempts):
        _out, _err, _ret = tools.run_cmd(["/home/peter/go/bin/mcumgr", "--conntype", "ble", "--connstring", f"peer_name={peer_name}", "image", "list"])
        last_stdout = _out
        last_stderr = _err
        logger.info(f"Attempt {i+1}/{attempts} mcumgr image list stdout:\n{_out}")
        if _ret == 0:
            assert "Images:" in _out, "MCUmgr 'image list' failed to return expected data."
            logger.info("MCUmgr 'image list' returned expected data.")
            return
        time.sleep(delay)

    # On failure, include stderr for diagnostics
    logger.error(f"mcumgr final stderr:\n{last_stderr}")
    assert False, "MCUmgr 'image list' did not succeed or did not return 'Images:'"