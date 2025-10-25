import logging
import pytest
from twister_harness import Shell
import re


logger = logging.getLogger(__name__)

def test_read_spi_data(shell: Shell):
    logger.info("Testcase: check SPI register values in SPI bus.")
    lines = shell.exec_command("spi_read 0x15")
    logger.info("Check SPI register value on address 0x15.")
    resp = "".join([i.split(":")[1] for i in lines if "SPI emulator read" in i])
    assert "0x56" == resp.strip(), "SPI data in register 0x15 does not fit"
    lines = shell.exec_command("spi_read 0x17")
    logger.info("Check SPI register value on address 0x17.")
    resp = "".join([i.split(":")[1] for i in lines if "SPI emulator read" in i])
    assert "0x9A" == resp.strip(), "SPI data in register 0x17 does not fit"
    logger.info("SPI read test returned expected values.")

def test_write_spi_data(shell: Shell):
    logger.info("Testcase: change SPI register values in SPI bus.")
    shell.exec_command("spi_write 0x15 0xAA 0xBB 0xCC")
    lines = shell.exec_command("spi_read_range 0x15 3")
    logger.info("Check SPI register value on addresses 0x15-0x17.")
    resp = [i.strip() for i in lines if i.strip().startswith("0x")]
    val = [i.split(":")[1].strip() for i in resp]
    assert val == ['0xAA', '0xBB', '0xCC'], "SPI write data failed"
    logger.info("SPI write test returned expected values.")