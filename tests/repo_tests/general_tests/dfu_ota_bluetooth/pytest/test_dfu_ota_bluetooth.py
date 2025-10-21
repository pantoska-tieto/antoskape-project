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
logger.info("DFU with OTA through Bluetooth started...")

# setting path for tools module
_p = Path(os.path.abspath(__file__)).parents[5]
sys.path.append(f"{str(_p)}/tests")
from tools import tools

# General setup
home_dir = os.path.expanduser("~")
logger.info("Home dir for Zephyr app:", home_dir)
mcumgr_path = Path(f"{os.path.expanduser("~")}/go/bin/mcumgr")

if mcumgr_path.exists():
    #MCUMGR_PATH = str(mcumgr_path)
    pass
else:
    raise FileNotFoundError(f"mcumgr tool not found on path: {mcumgr_path}")

MCUMGR_PATH = "/github/home/go/bin/mcumgr"

PEER_NAME = "TietoBLE-OTA"  # BLE peer name to connect to
BUILD_DIR = "build/smp_svr/zephyr/zephyr.signed.bin"
TEST_PATH = "tests/repo_tests/general_tests/dfu_ota_bluetooth"
old_hash = ""               # image hash-tag 
new_hash = ""               # image hash-tag 

def cmd_mcumgr(cmd):
    # Execute MCUmgr command on remote device
    time.sleep(5)
    logger.info(f"MCUmgr command to execute: {cmd}")
    _out, _err, _ret = tools.run_cmd(cmd)
    if _ret == 0:
        logger.info(f"MCUmgr command was executed successfully: {cmd}")
        return _out, _err, _ret
    else:
        # On failure, include stderr for diagnostics
        logger.error(f"MCUmgr command failed - final stderr:\n{last_stderr}\n")
        raise Exception("[ERROR] MCUmgr command failed.")

@pytest.mark.order(1)
def test_old_image_list(dut: DeviceAdapter):
    # Check image list on board
    global old_hash
    _out, _err, _ret = tools.run_cmd([MCUMGR_PATH, "--conntype", "ble", "--connstring", f"peer_name={PEER_NAME}", "image", "list"])
    time.sleep(5)
    logger.info(f"OUT from test_old_image_list(): {_out}")
    old_hash = "".join([i.split(":")[1].strip() for i in _out.split("\n") if "hash" in i])
    assert "Images:" in _out, "MCUmgr 'image list' failed to return expected data."
    logger.info("MCUmgr 'image list' returned expected data.")

@pytest.mark.order(2)
def test_build_new_image():
    # Build new test image to be used for DFU
    _out, _err, _ret = tools.run_cmd(["west", "build", "-p", "always", "-b", "esp32s3_devkitc/esp32s3/procpu", "--sysbuild", TEST_PATH, "--", "-DEXTRA_CONF_FILE='overlay-bt.conf'"]) 
    assert _ret == 0, f"Buld for new image failed:\n{_err}\n"
    logger.info(f"New image was successfully built.")

@pytest.mark.order(3)
def test_upload_new_image():
    # Upload new test image to device
    _out, _err, _ret = tools.run_cmd([MCUMGR_PATH, "--conntype", "ble", "--connstring", f"peer_name={PEER_NAME}", "image", "upload", BUILD_DIR])
    time.sleep(5)
    logger.info(f"OUT from test_upload_new_image(): {_out}")
    resp = "".join([i for i in _out.split("\n") if "Done" in i])
    assert "Done" in resp, "New FW upload failed."
    logger.info("New FW was uploaded successfully.")

@pytest.mark.order(4)
def test_new_image_list():
    # Check image list on board - existing + new images
    global new_hash
    _out, _err, _ret = tools.run_cmd([MCUMGR_PATH, "--conntype", "ble", "--connstring", f"peer_name={PEER_NAME}", "image", "list"])
    time.sleep(5)
    logger.info(f"OUT from test_new_image_list(): {_out}")
    resp = "".join([i for i in _out.split("\n") if "slot=1" in i])
    _h = _out.split("\n")[_out.split("\n").index(resp) + 4]
    new_hash = _h.split(":")[1].strip()
    assert "slot=1" in resp, "MCUmgr 'image list' failed for new image on board."
    logger.info("MCUmgr 'image list' returned expected data.")

@pytest.mark.order(5)
def test_set_pending():
    # Update status to 'pending' for new test image to be installed in next 'reset'
    tools.run_cmd([MCUMGR_PATH, "--conntype", "ble", "--connstring", f"peer_name={PEER_NAME}", "image", "test", new_hash])
    _out, _err, _ret = tools.run_cmd([MCUMGR_PATH, "--conntype", "ble", "--connstring", f"peer_name={PEER_NAME}", "image", "list"])
    logger.info(f"OUT from test_set_pending(): {_out}")
    time.sleep(5)
    assert "flags: pending" in _out, "New FW image has wrong flag."
    logger.info("New FW image changed its status to 'pending' successfully.")

@pytest.mark.order(6)
def test_reset_fw():
    # Reset board to upgrade FW to new test image
    _out, _err, _ret = tools.run_cmd([MCUMGR_PATH, "--conntype", "ble", "--connstring", f"peer_name={PEER_NAME}", "reset"])
    # Wait for the boot to complete
    time.sleep(15)
    assert "Done" in _out, "Soft reset of a device failed."
    logger.info("Soft reset of a device was successfull.")

@pytest.mark.order(7)
def test_dfu():
    # Check the new image (new FW) after boot in active and confirmed
    _out, _err, _ret = tools.run_cmd([MCUMGR_PATH, "--conntype", "ble", "--connstring", f"peer_name={PEER_NAME}", "image", "list"])
    time.sleep(5)
    logger.info(f"OUT from test_dfu(): {_out}")
    new_hash_fin = "".join([i.split(":")[1].strip() for i in _out.split("\n") if "hash" in i])
    assert new_hash == new_hash_fin and old_hash != new_hash_fin, "OTA DFU via Bluetooth failed."
    logger.info("OTA DFU via Bluetooth was successfully finished.")
