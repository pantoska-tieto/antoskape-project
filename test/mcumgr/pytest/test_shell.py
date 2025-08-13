# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import logging
from pathlib import Path

import pytest
from twister_harness import DeviceAdapter, MCUmgr, Shell
from twister_harness.helpers.utils import find_in_config, match_lines, match_no_lines
from utils import check_with_mcumgr_command, check_with_shell_command

logger = logging.getLogger(__name__)

# This string is used to verify that the device is running the application
WELCOME_STRING = "smp_sample: build time:"

def test_shell_command(dut: DeviceAdapter, shell: Shell, mcumgr: MCUmgr):
    """
    Verify shell commands in shel console on the device
    """
    logger.info('MCUmgr test started...')
    new_version = '0.0.2+0'

    # dut.connect()
    logger.info('Verify new APP is booted')
    output = dut.readlines_until(WELCOME_STRING)
    check_with_shell_command(shell, new_version, swap_type='test')
    check_with_mcumgr_command(mcumgr, new_version)
    logger.info('MCUmgr test finished.')
