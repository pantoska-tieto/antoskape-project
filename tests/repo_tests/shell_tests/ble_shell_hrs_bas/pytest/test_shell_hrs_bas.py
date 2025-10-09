# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0

import logging
import pytest
from twister_harness import Shell
import re


logger = logging.getLogger(__name__)

def test_shell_hrs_bas(shell: Shell):
    logger.info("Testcase: check Heart Rate and Battery Level in uart prompt")

    # Get Battery level in [%]
    lines = shell.exec_command("get_battery")
    bl = "".join([i.split(":")[1].strip() for i in lines if i.split(":")[0] == "Battery level"])
    bl_val = re.findall(r'\d+', bl)[0]

    # Get Heart Rate in [bpm]
    lines = shell.exec_command("get_hr")
    hr = "".join([i.split(":")[1].strip() for i in lines if i.split(":")[0] == "Heart rate"])
    hr_val = re.findall(r'\d+', hr)[0]

    assert bl_val == "60" and hr_val == "90", "Expected HRS and BAS values were not found."
    logger.info('Shell response to HRS and BAS is valid')
