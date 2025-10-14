import logging
import pytest
from twister_harness import Shell
import re


logger = logging.getLogger(__name__)

def test_read_i2c_data(shell: Shell):
    logger.info("Testcase: check register values in I2C bus.")
    lines = shell.exec_command('i2c_read 0x68')
    logger.info("Check register value on address 0x68.")
    message = [i for i in lines if "I2C emulator read" in i]
    addr = re.findall(r"0x[0-9]+", "".join(message).split(":")[1].strip())
    val1 = re.findall(r"0x[0-9]*", "".join(message).split(":")[2].strip())
    lines = shell.exec_command('i2c_read 0x69')
    logger.info("Check register value on address 0x69.")
    message = [i for i in lines if "I2C emulator read" in i]
    addr = re.findall(r"0x[0-9]+", "".join(message).split(":")[1].strip())
    val2 = re.findall(r"0x[0-9]*", "".join(message).split(":")[2].strip())
    assert "".join(val1) == "0x55" and "".join(val2) == "0x56", "I2C data is not correct."
    logger.info("I2C read test returned expected values.")