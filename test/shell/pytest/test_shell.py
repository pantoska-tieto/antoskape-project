# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0

import pytest

from twister_harness import Shell


def test_shell_print_help(shell: Shell):
    print("pantoska - shell test 1!")
    lines = shell.exec_command('help')
    assert 'Available commands:' in lines, 'expected response not found'


def test_shell_print_version(shell: Shell):
    print("pantoska - shell test 2!")
    lines = shell.exec_command('kernel version')
    assert any(['Zephyr version' in line for line in lines]), 'expected response not found'

