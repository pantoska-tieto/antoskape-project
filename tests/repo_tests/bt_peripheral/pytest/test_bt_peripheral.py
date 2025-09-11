# Copyright (c) 2025 Tietoevry
#
import logging
import pytest
import asyncio
import pytest_asyncio
from bleak import BleakScanner
from twister_harness import DeviceAdapter


logger = logging.getLogger(__name__)

async def bluetooth_discovery(dut: DeviceAdapter):
    await asyncio.sleep(5)
    devices = await BleakScanner.discover(10.0, return_adv=True)
    bt_name = []
    # Find BT device by name
    for device in devices:
        advertisement_data = devices[device][1]
        bt_name.append(advertisement_data.local_name)

    assert "TIETO Bluetooth" in bt_name
    logger.info('Bluetooth device found')

def test_bt_discovery(dut: DeviceAdapter):
        logger.info(f'Running Bluetooth discovery')
        asyncio.run(bluetooth_discovery(dut))