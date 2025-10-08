# Copyright (c) 2025 Tietoevry
#

import logging
import pytest
import asyncio
import pytest_asyncio
import re
from twister_harness import Shell


logger = logging.getLogger(__name__)

# Simulated sensor async generator
async def sensor_simulation(shell:Shell, start=10, stop=0, delay=0.5):
    for value in range(start, stop - 1, -1):
        # Set simulated sensor value via Shell
        lines = shell.exec_command(f"set_proximity {value}")
        logger.info(f"Simulated proximity sensor value set to: {value} [cm]")
        await asyncio.sleep(delay)
        #yield value

# Main async function that consumes sensor values
async def sensor_detection(shell:Shell, threshold=5, delay=0.5):
    # Simulate sensor delay to eliminate initial zero-distance reading
    await asyncio.sleep(0.5) 
    while True:
        await asyncio.sleep(delay) 
        # Get simulated sensor value from Shell
        detected_value = shell.exec_command("get_proximity")
        ret = "".join([i for i in detected_value if "Proximity" in i])
        dist = "".join(re.findall("[0-9]/*", ret))
        logger.info(f"Proximity Sensor value measured: {dist} [cm]")
        if int(dist) <= threshold:
            return dist

@pytest.mark.asyncio
async def test_sensor_proximity_threshold(shell:Shell):    
    # Start simulation in background
    simulation_task = asyncio.create_task(sensor_simulation(shell))

    # Start detection and wait for result with timeout [s]
    await asyncio.sleep(0.5) # Initial delay to avoid zero reading
    try:
        distance = await asyncio.wait_for(
            sensor_detection(shell, threshold=5, delay=0.5),
            timeout=12.0
        )
    except asyncio.TimeoutError:
        simulation_task.cancel()
        pytest.fail("[ERROR] Sensor detection timed out before reaching threshold")

    logger.info(f"Threshold distance found at: {distance} [cm]")
    assert int(distance) <= 5, "Expected threshold distance from proximity Sensor was not found."
    logger.info('Expected threshold distance from proximity Sensor is valid')
