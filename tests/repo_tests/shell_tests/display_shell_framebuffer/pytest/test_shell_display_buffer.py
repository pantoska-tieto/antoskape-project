# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0

import logging
import pytest
from twister_harness import Shell


logger = logging.getLogger(__name__)

def test_shell_display_buffer(shell: Shell):
    logger.info("Testcase: check Display framebuffer in uart prompt")
    
    # Show Display simulated buffer
    lines = shell.exec_command("display_status")
    # Get message from Display framebuffer
    message = "".join([i.split(":")[1].strip() for i in lines if i.split(":")[0] == "Last drawn"])

    # Get CRC32 checksum of Display framebuffer
    crc = "".join([i.split(":")[1].strip() for i in lines if i.split(":")[0] == "Framebuffer CRC32"])

    assert crc == "0xfdc935d3" and  message == "'Message from Zephyr display'", "Expected response with Display framebuffer was not found."
    logger.info('Shell response with Display framebuffer is valid')
