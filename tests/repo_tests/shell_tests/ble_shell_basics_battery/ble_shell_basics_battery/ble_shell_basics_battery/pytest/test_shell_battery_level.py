# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0

import logging
import pytest
from twister_harness import Shell


logger = logging.getLogger(__name__)

def test_shell_battery_level(shell: Shell):
    logger.info("Testcase: check BT battery level in uart prompt")
    
    # Show GATT services
    lines = shell.exec_command("gatt show-db")
    # Get handle id for Battery level service
    handle = "".join([i.split(" ")[3] for i in lines if i.split(" ")[0] == "attr" and i.split(" ")[5] == "2a19"])

    # Get Battery level in [%]
    lines = shell.exec_command(f"gatt get {handle}")
    bat_level = "".join([i.split(" ")[1] for i in lines if i.split(" ")[0] == "00000000:"])
    assert int(bat_level, 16) == 85, "Expected Battery level value was not found."
    logger.info('Shell response to Battery level is valid')
