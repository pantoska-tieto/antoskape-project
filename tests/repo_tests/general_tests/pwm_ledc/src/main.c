#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/pwm.h>
#include <zephyr/logging/log.h>
#include <zephyr/sys/printk.h>

LOG_MODULE_REGISTER(pwm_ledc_sample, LOG_LEVEL_INF);

#define PWM_CTLR_NODE DT_ALIAS(pwm_led0)

#if !DT_NODE_HAS_STATUS(PWM_CTLR_NODE, okay)
#error "Unsupported board: pwmled0 devicetree alias is not defined"
#endif

static const struct pwm_dt_spec pwm_led = PWM_DT_SPEC_GET(PWM_CTLR_NODE);

int main(void)
{
    // Set duty cycle PWM signal
    uint32_t period = 5000U;     // 5000 microseconds = 200Hz
    uint32_t pulse_width = 500U; // 500 microseconds => duty cycle = 10%

    if (!device_is_ready(pwm_led.dev)) {
        LOG_ERR("PWM device is not ready");
        return 0;
    }

    // Start transmitting PWM signal 
    int ret = pwm_set_dt(&pwm_led, PWM_USEC(period), PWM_USEC(pulse_width));
    if (ret) {
        LOG_ERR("Failed to set PWM: %d", ret);
    } else {
        LOG_INF("PWM set: period = %u us, pulse = %u us", period, pulse_width);
    }
}