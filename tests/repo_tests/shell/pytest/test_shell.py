# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0

import logging
import timeit

from twister_harness import Shell

logger = logging.getLogger(__name__)


def test_shell_print_help(shell: Shell):
    logger.info("Testcase: check a commands are available in uart prompt.")
    lines = shell.exec_command('help')
    assert 'Available commands:' in lines, 'expected response not found'
    logger.info('response is valid')


def test_shell_print_version(shell: Shell):
    logger.info("Testcase: check Zephyr kernel version is available.")
    lines = shell.exec_command('kernel version')
    assert any(['Zephyr version' in line for line in lines]), 'expected response not found'
    logger.info('response is valid')

# Benchmarking
logger.info("Benchmarking: test_shell_print_help()")
logger.info(timeit.timeit(lambda: test_shell_print_help(), number=10))
logger.info("Benchmarking: test_shell_print_version()")
logger.info(timeit.timeit(lambda: test_shell_print_version(), number=10))
