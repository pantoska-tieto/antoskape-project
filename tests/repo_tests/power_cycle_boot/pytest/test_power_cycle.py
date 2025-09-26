import logging
import serial
import pytest
import os
from lgpio import gpiochip_open, gpio_claim_output, gpio_write, gpiochip_close
from time import sleep
from twister_harness import Shell
from serial.tools import list_ports


logger = logging.getLogger(__name__)

# GPIO pin to control relay
RELAY_PIN = 23
# Number ot test cycles
CYCLES = 2
# Power on/off interval [s]]
INTERVAL = 20
# Delta time for assertion [s]
DELTA = 3
# Open GPIO controller chip (4 for Raspberry Pi5)
chip = gpiochip_open(4)
# Set the pin as output
gpio_claim_output(chip, RELAY_PIN)
# Initial setup to power=on
gpio_write(chip, RELAY_PIN, 1)
# Initial serial port (until power=off step)
SERIAL_PORT = "/dev/ttyUSB0"
BAUDRATE = 115200

def find_new_port():
    """Find new serial port after power=on
    default: /dev/ttyUSB0 --> /dev/ttyUSB1
    """
    ports = list_ports.comports()
    # Find new UART to Serial port
    for port in ports:
        description = port.description or ""
        manufacturer = port.manufacturer or ""
        if "CP2102" in description or "Silicon Labs" in manufacturer:
            logger.info(f"Found ESP32 serial port: {port.device}")
            return port.device
    logger.error("New device serial port not found")
    return None

def reopen_shell(shell: Shell):
    """New Shell object with a fresh serial connection
    """
    port = find_new_port()
    if port:
        try:
            # Close old serial connection
            shell._device._serial_connection.close()
            # Reopen new serial connection
            ser = serial.Serial(port, BAUDRATE, timeout=1)
            shell._device._serial_connection = ser
            logger.info(f"Serial port {port} reopened successfully")
            return shell
        except Exception as e:
            logger.exception(f"Failed to reopen new serial port {port}")
    else:
        logger.error("Serial port not available after power ON")
    return None

def test_power_cycle(shell: Shell):
    result = []
    # Even number of cycles - to get serial name back to /dev/ttyUSB0
    for cycle in range(CYCLES):
        # Power OFF
        logger.info(f"Cycle nr: {cycle + 1} - Power OFF")
        gpio_write(chip, RELAY_PIN, 0)
        sleep(INTERVAL)

        # Power ON
        logger.info(f"Cycle nr: {cycle + 1} - Power ON")
        gpio_write(chip, RELAY_PIN, 1)    
        sleep(INTERVAL)
        
        # Reinitialize shell after power ON
        shell = reopen_shell(shell)
        assert shell is not None, f"Failed to reopen shell after power ON in cycle {cycle + 1}"

        # Kernel up time in [ms]
        line = shell.exec_command("kernel uptime")
        upt = [v for v in line if v.split(":")[0] == "Uptime"]
        result.append("".join(upt))

    # Release GPIO chip
    gpiochip_close(chip)
    logger.info(f"Total: {result}")
    assert all([
        int(line.split(" ")[1]) in range(INTERVAL*1000, INTERVAL*1000 + DELTA*3000) 
        for line in result
    ]), "Booting failed in power cycle test!"
    logger.info('Power cycle test completed successfully')
