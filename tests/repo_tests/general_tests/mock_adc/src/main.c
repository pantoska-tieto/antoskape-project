#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/adc.h>
#include <zephyr/sys/printk.h>
#include <stdlib.h>


#define ADC_RESOLUTION 12
#define ADC_CHANNEL_ID 0

int main(void) {
    // const struct device *adc_dev = DEVICE_DT_INST_GET(0);
    const struct device *adc_dev = DEVICE_DT_GET(DT_NODELABEL(mock_adc0));

    if (!device_is_ready(adc_dev)) {
        printk("ADC device not ready\n");
        return 1;
    }

    struct adc_channel_cfg channel_cfg = {
        .gain = ADC_GAIN_1,
        .reference = ADC_REF_INTERNAL,
        .acquisition_time = ADC_ACQ_TIME_DEFAULT,
        .channel_id = ADC_CHANNEL_ID,
    };

    adc_channel_setup(adc_dev, &channel_cfg);

    uint16_t sample_buffer;
    struct adc_sequence sequence = {
        .channels = BIT(ADC_CHANNEL_ID),
        .buffer = &sample_buffer,
        .buffer_size = sizeof(sample_buffer),
        .resolution = ADC_RESOLUTION,
    };

    if (adc_read(adc_dev, &sequence) == 0) {
        printk("ADC read value: %d\n", sample_buffer);
        k_sleep(K_SECONDS(5));
        exit(0);

    } else {
        printk("ADC read failed\n");
    }
    return 0;
}
