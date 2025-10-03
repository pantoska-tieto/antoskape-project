import gpiod
import time
import logging
import pytest

logger = logging.getLogger(__name__)

CHIP_NAME = "/dev/gpiochip4"  # Raspberry Pi 5
GPIO_PIN = 24
INTERVAL = 2  # [second]
DELTA_FREQ = 1  # [Hz]
DELTA_DUTY = 1  # [%]
# Expected PWM values - check src/main.c
EXP_FREQUENCY = 200
EXP_DUTY = 10   # 10% duty cycle

def test_pwm_signal():
    period_start = None
    high_time = 0
    signal_detected = False
    res = []

    chip = gpiod.Chip(CHIP_NAME)
    line = chip.get_line(GPIO_PIN)

    # Request line for both edge events
    line.request(consumer="pwm-measure",
                 type=gpiod.LINE_REQ_EV_BOTH_EDGES)

    logger.info(f"Monitoring PWM signal on GPIO{GPIO_PIN} for {INTERVAL} seconds...")
    start_time = time.time()

    while time.time() - start_time < INTERVAL:
        if line.event_wait(1):
            event = line.event_read()
            tick = event.sec * 1_000_000_000 + event.nsec
            level = event.type

            if level == gpiod.LineEvent.RISING_EDGE:
                if period_start is not None:
                    period = tick - period_start
                    if period > 0:
                        frequency = 1_000_000_000 / period
                        duty_cycle = (high_time / period) * 100
                        #logger.info(f"Frequency: {frequency:.2f} Hz, Duty Cycle: {duty_cycle:.2f}%")
                        signal_detected = True
                        res.append(["{:.2f}".format(frequency), "{:.2f}".format(duty_cycle)])
                period_start = tick

            elif level == gpiod.LineEvent.FALLING_EDGE:
                if period_start is not None:
                    high_time = tick - period_start

    line.release()
    chip.close()
    return res

if __name__ == "__main__":
    res = test_pwm_signal()
    # Get frequency values from PWM
    res_frequency = [(float(line[0]) > EXP_FREQUENCY - DELTA_FREQ and float(line[0]) < EXP_FREQUENCY + DELTA_FREQ) for line in res]
    # Get duty cycle values from PWM
    res_duty = [(float(line[1]) > EXP_DUTY - DELTA_DUTY and float(line[1]) < EXP_DUTY + DELTA_DUTY) for line in res]
    assert all(res_frequency) and all(res_duty), "Detected PWM signal is not in expected range."
    logger.info("PWM test completed successfully.")