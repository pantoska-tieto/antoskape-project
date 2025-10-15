import logging
import pytest
import time
from twister_harness import Shell


logger = logging.getLogger(__name__)
GPIO_OUT_PIN = 13   # ouptput pin to toggle LED
GPIO_IN_PIN = 9     # auxiliary pin to check GPIO_OUT_PIN state
LOOPS = 10
SLEEP = 2

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

def pin_config(shell: Shell, dev, pin, mode, resistor, init_state, init_logic=False):
    """ Gpio nofiguration helper

    conf <device> <pin> <configuration <i|o>[u|d][h|l][0|1]> [vendor specific]

    <i|o> - input|output
    [u|d] - pull up|pull down, otherwise open
    [h|l] - active high|active low, otherwise defaults to active
    high
    [0|1] - initialise to logic 0|logic 1, otherwise defaults to
    logic 0
    """
    logic = "1" if (init_logic and mode == "o") else "0" if (not init_logic and mode == "o") else ""
    # Conf syntax - example: gpio conf gpio0 9 ouh1"
    conf_cmd = f"gpio conf {dev} {pin} {mode}{resistor}{init_state}{logic}"
    res = shell.exec_command(conf_cmd)
    logger.info(f"Configured pin {pin}: {conf_cmd}")

def test_gpio_toggle(shell: Shell):
    logger.info("Testcase: verify gpio toggle command in shell prompt")
    dev = pick_gpio_device(shell)
    # Set auxiliary input pin, initial high
    pin_config(shell, dev, GPIO_IN_PIN, "i", "u", "h")
    # Initial state setup
    res = []
    loop_state = shell.exec_command(f"gpio get {dev} {GPIO_IN_PIN}")

    for i in range(LOOPS + 1):
        # Toggle pin
        toggle = shell.exec_command(f"gpio toggle {dev} {GPIO_OUT_PIN}")
        # Check toggle state
        _s = shell.exec_command(f"gpio get {dev} {GPIO_IN_PIN}")
        res.append(True) if _s != loop_state else res.append(False)
        loop_state  = _s
        time.sleep(SLEEP)

    assert False not in res, f"GPIO toggle failed, states: {res}"
    logger.info(f"GPIO toggle passed {LOOPS} loops, states: {res}")