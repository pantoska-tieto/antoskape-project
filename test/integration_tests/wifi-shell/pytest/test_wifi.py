# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0

import pytest

from twister_harness import Shell


def test_wifi_connect(shell: Shell):
    print("Custom Tieto wifi test!")
    lines = shell.exec_command('wifi connect -s "Razus13932" -p "spravca1961966" -k 1')
    assert any(['Connected' in line for line in lines]), 'Wifi connection failed!'
