# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0

import logging
import pytest
from twister_harness import Shell
import re


logger = logging.getLogger(__name__)

def test_shell_battery_level(shell: Shell):
    logger.info("Testcase: check Heart Rate in uart prompt")
    hr_vals = []
    # Reference HRS values
    hr_ref = ['72', '95']

    # Get default Heart Rate [bpm]
    lines = shell.exec_command("get_hr")
    hr = "".join([i.split(":")[1].strip() for i in lines if i.split(":")[0] == "Heart rate"])
    hr_val = re.findall(r'\d+', hr)[0]
    hr_vals.append(hr_val)
    logger.info(f"Default Heart Rate detected: {hr_val} bpm")

    # Set reference Heart Rate for verification [bpm]
    shell.exec_command("set_hr 95")
    logger.info(f"Set reference Heart Rate: 95 bpm")

    # Get reference Heart Rate [bpm]
    lines = shell.exec_command("get_hr")
    hr = "".join([i.split(":")[1].strip() for i in lines if i.split(":")[0] == "Heart rate"])
    hr_val = re.findall(r'\d+', hr)[0]
    hr_vals.append(hr_val)
    logger.info(f"Reference Heart Rate detected: {hr_val} bpm")

    assert sorted(hr_ref) == sorted(hr_vals), "Expected HRS value were not found."
    logger.info('All HRS values are valid')
