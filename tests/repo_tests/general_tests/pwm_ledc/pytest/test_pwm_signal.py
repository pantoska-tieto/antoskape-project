'''
Hardware PWM measurement test with libgpiod ver.2.3.0
installed by pip:
https://pypi.org/project/gpiod/

'''

import gpiod
import time
from datetime import timedelta
import logging
import pytest
from gpiod.line import Edge, Direction, Bias

logger = logging.getLogger(__name__)

CHIP_NAME = "/dev/gpiochip4"  # Raspberry Pi 5
GPIO_PIN = 24
INTERVAL = 2  # [second]
DELTA_FREQ = 1  # [Hz]
DELTA_DUTY = 2  # [%]
# Expected PWM values - check src/main.c
EXP_FREQUENCY = 200
EXP_DUTY = 10   # 10% duty cycle

def measure_pwm():
    period_start = None
    high_time = 0
    signal_detected = False
    res = []

    chip = gpiod.Chip(CHIP_NAME)
    # Create LineSettings object and configure direction and edge detection
    settings = gpiod.LineSettings()
    settings.direction = Direction.INPUT
    #settings.bias = Bias.DISABLED
    settings.edge_detection = Edge.BOTH
    settings.bias =  Bias.PULL_UP

    request = chip.request_lines(
        consumer="pwm-measure",
        config={GPIO_PIN: settings}
    )

    logger.info(f"Monitoring PWM signal on GPIO{GPIO_PIN} for {INTERVAL} seconds...")
    start_time = time.time()

    while time.time() - start_time < INTERVAL:        
        if request.wait_edge_events(timedelta(seconds=1)):
            events = request.read_edge_events()

            for event in events:
                level = event.event_type
                if event.event_type.name == "RISING_EDGE":
                    tick = event.timestamp_ns
                    if period_start is not None:
                        period = tick - period_start

                        if period > 0:
                            frequency = 1_000_000_000 / period
                            duty_cycle = (high_time / period) * 100
                            logger.info(f"Frequency: {frequency:.2f} Hz, Duty Cycle: {duty_cycle:.2f}%")
                            signal_detected = True
                            res.append(["{:.2f}".format(frequency), "{:.2f}".format(duty_cycle)])
                    period_start = tick
                elif event.event_type.name == "FALLING_EDGE":
                    tick = event.timestamp_ns
                    if period_start is not None:
                        high_time = tick - period_start

    request.release()
    chip.close()
    return res

def test_pwm_signal():
    res = measure_pwm()
    logger.info(f"PWM results from GPIO measurement: {res}")
    # Get frequency values from PWM
    res_frequency = [(float(line[0]) > EXP_FREQUENCY - DELTA_FREQ and float(line[0]) < EXP_FREQUENCY + DELTA_FREQ) for line in res]
    # Get duty cycle values from PWM
    res_duty = [(float(line[1]) > EXP_DUTY - DELTA_DUTY and float(line[1]) < EXP_DUTY + DELTA_DUTY) for line in res]
    assert len(res_frequency) !=0 and all(res_frequency) and len(res_duty) != 0 and all(res_duty), "Detected PWM signal is not in expected range."
    logger.info("PWM test completed successfully.")