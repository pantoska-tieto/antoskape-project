# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0

import logging
import pytest

from twister_harness import Shell


logger = logging.getLogger(__name__)

def test_shell_print_help(shell: Shell):
    print("Testcase: check a commands are available in uart prompt:")
    logger.info('send "help" command')
    lines = shell.exec_command('help')
    assert 'Available commands:' in lines, 'expected response not found'
    logger.info('Shell response is valid')

def test_shell_print_version(shell: Shell):
    print("Testcase: check Zephyr kernel version is available:")
    logger.info('send "kernel version" command')
    lines = shell.exec_command('kernel version')
    assert any(['Zephyr version' in line for line in lines]), 'expected response not found'
    logger.info('Shell response is valid')
