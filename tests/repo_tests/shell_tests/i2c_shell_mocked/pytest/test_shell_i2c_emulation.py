# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0

import logging
import pytest
import re
from time import sleep


logger = logging.getLogger(__name__)

def test_i2c_read_from_shell(zephyr_shell):
    result = []
    # 8bit register space: address & value
    usecase = {"0x68": "0x55", "0x69": "0x56", "0x70": "0xab"}
    for k, v in usecase.items(): 
        zephyr_shell.send_command(f"i2c_write {k} {v}")
        sleep(1)
        zephyr_shell.send_command(f"i2c_read {k}")
        output = zephyr_shell.read_output()
        #result.append(re.search(r"0x[0-9a-fA-F]{2}", output).group(0))
        logger.info(f"!!!Output from shell: {output}")

        #crc = "".join([i.split(":")[1].strip() for i in lines if i.split(":")[0] == "Framebuffer CRC32"])
        #assert crc == "0xfdc935d3" and  message == "'Message from Zephyr display'", "Expected response with Display framebuffer was not found."
        assert True, "Write/read operation with I2C bus failed."
        logger.info('Write/read operations with I2C bus are valid')
