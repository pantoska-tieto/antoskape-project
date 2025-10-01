#include <zephyr/device.h>
#include <zephyr/drivers/adc.h>
#include <zephyr/init.h>

#define DT_DRV_COMPAT zephyr_mock_adc

static int mock_adc_channel_setup(const struct device *dev, const struct adc_channel_cfg *cfg) {
    return 0;
}

static int mock_adc_read(const struct device *dev, const struct adc_sequence *sequence) {
    if (sequence->buffer_size >= sizeof(uint16_t)) {
        ((uint16_t *)sequence->buffer)[0] = 1234;
        return 0;
    }
    return -ENOMEM;
}

static const struct adc_driver_api mock_adc_api __used = {
    .channel_setup = mock_adc_channel_setup,
    .read = mock_adc_read,
};

static int mock_adc_init(const struct device *dev) {
    return 0;
}

DEVICE_DT_DEFINE(DT_NODELABEL(mock_adc0), mock_adc_init, NULL, NULL, NULL,
                 POST_KERNEL, CONFIG_KERNEL_INIT_PRIORITY_DEFAULT,
                 &mock_adc_api);

