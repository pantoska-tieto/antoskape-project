# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0

import logging
import pytest
import time
from twister_harness import Shell


logger = logging.getLogger(__name__)
GPIO_PIN = 13   # gpio pin to test

def pick_gpio_device(shell: Shell): 
    lines = shell.exec_command("gpio devices")
    # Skip header line "Device ..."; find the first subsequent device name 
    for line in lines: 
        parts = line.strip().split() 
        if not parts: 
            continue 
        if parts[1].startswith("gpio0"):
            return parts[0] 
    raise AssertionError("No GPIO devices found; ensure CONFIG_GPIO_SHELL=y and device has GPIO")

def test_gpio_toggle(shell: Shell):
    logger.info("Testcase: verify GPIO functions in shell prompt")
    # Get gpio controller
    dev = pick_gpio_device(shell)

    # Ready test
    res = shell.exec_command(f"gpio info {dev}")
    assert any([f"{GPIO_PIN}" in line for line in res]), "GPIO dev is not ready"

    # Configuration output test
    res = shell.exec_command(f"gpio conf {dev} {GPIO_PIN} odh1")
    assert res, f"GPIO configuration output test (pull down, active high, logic 1) failed for pin {GPIO_PIN}" 

    # Set state 0 test
    res = shell.exec_command(f"gpio set {dev} {GPIO_PIN} 0")
    assert res, f"GPIO 'set 0' test failed for pin {GPIO_PIN}"

    # Set state 1 test
    res = shell.exec_command(f"gpio set {dev} {GPIO_PIN} 1")
    assert res, f"GPIO 'set 1' test failed for pin {GPIO_PIN}"

    # Toggle test
    res = shell.exec_command(f"gpio toggle {dev} {GPIO_PIN}")
    assert res, f"GPIO 'toggle' test failed for pin {GPIO_PIN}"

    # Configuration input test
    res = shell.exec_command(f"gpio conf {dev} {GPIO_PIN} iuh")
    assert res, f"GPIO configuration input test (pull up, active high) failed for pin {GPIO_PIN}" 

    # Get state test
    res = shell.exec_command(f"gpio get {dev} {GPIO_PIN}")
    assert any(['1' or '0' in res for line in res]), f"GPIO 'get' test failed for pin {GPIO_PIN}"

    logger.info(f"GPIO functions test is successfull")