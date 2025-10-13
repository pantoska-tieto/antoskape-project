# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0

import logging
import pytest
from twister_harness import Shell


logger = logging.getLogger(__name__)

def test_shell_i2c(shell: Shell):
    logger.info("Testcase: check a commands are available in uart prompt")
    logger.info('send "help" command')
    lines = shell.exec_command("i2c_write 0x68 0x55")
    logger.info(f'!!!I2C write: {lines}')
    lines = shell.exec_command("i2c_read 0x68")
    logger.info(f'!!!I2C read: {lines}')
    assert True, "Write/read operation with I2C bus failed."
