# Copyright (c) 2025 Tietoevry
#
import logging
import pytest
import asyncio
import pytest_asyncio
from bleak import BleakScanner


logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_bluetooth_discovery():
    devices = await BleakScanner.discover(10.0, return_adv=True)
    bt_name = []
    # Find BT device by name
    for device in devices:
        advertisement_data = devices[device][1]
        bt_name.append(advertisement_data.local_name)

    assert "TIETO Zephyr Peripheral" in bt_name, "Bluetooth device not found"
    logger.info('Bluetooth device found')