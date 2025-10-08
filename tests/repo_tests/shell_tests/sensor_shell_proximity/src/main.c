
#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/sensor.h>
#include <zephyr/shell/shell.h>
#include <zephyr/init.h>
#include <zephyr/sys/printk.h>

static int simulated_value = 0;

static int simulated_sensor_sample_fetch(const struct device *dev, enum sensor_channel chan) {
    ARG_UNUSED(dev);
    ARG_UNUSED(chan);
    return 0;
}

static int simulated_sensor_channel_get(const struct device *dev, enum sensor_channel chan, struct sensor_value *val) {
    ARG_UNUSED(dev);
    ARG_UNUSED(chan);
    val->val1 = simulated_value;
    val->val2 = 0;
    return 0;
}

static const struct sensor_driver_api simulated_sensor_api = {
    .sample_fetch = simulated_sensor_sample_fetch,
    .channel_get = simulated_sensor_channel_get,
};

static int simulated_sensor_init(const struct device *dev) {
    ARG_UNUSED(dev);
    return 0;
}

DEVICE_DEFINE(simulated_sensor, "SIMULATED_PROXIMITY", simulated_sensor_init,
              NULL, NULL, NULL, POST_KERNEL, CONFIG_KERNEL_INIT_PRIORITY_DEFAULT,
              &simulated_sensor_api);

// Shell command to set proximity value
static int cmd_set_proximity(const struct shell *shell, size_t argc, char **argv) {
    if (argc != 2) {
        shell_print(shell, "Usage: set_proximity <value>");
        return -EINVAL;
    }

    simulated_value = atoi(argv[1]);
    shell_print(shell, "Proximity value set to %d", simulated_value);
    return 0;
}

// Shell command to get proximity value
static int cmd_get_proximity(const struct shell *shell, size_t argc, char **argv) {
    const struct device *dev = device_get_binding("SIMULATED_PROXIMITY");
    if (!dev) {
        shell_error(shell, "Simulated sensor device not found");
        return -ENODEV;
    }

    struct sensor_value val;
    if (sensor_sample_fetch(dev) < 0 || sensor_channel_get(dev, SENSOR_CHAN_PROX, &val) < 0) {
        shell_error(shell, "Failed to read sensor value");
        return -EIO;
    }

    shell_print(shell, "Proximity: %d", val.val1);
    return 0;
}

SHELL_CMD_ARG_REGISTER(set_proximity, NULL, "Set simulated proximity value", cmd_set_proximity, 2, 0);
SHELL_CMD_ARG_REGISTER(get_proximity, NULL, "Get simulated proximity value", cmd_get_proximity, 1, 0);

int main(void)
{
    printk("Proximity sensorr test started\n");
    return 0;
}