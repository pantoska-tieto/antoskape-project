#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/i2c.h>
#include <zephyr/drivers/emul.h>
#include <zephyr/logging/log.h>
#include <string.h>

LOG_MODULE_REGISTER(i2c_mock_sample, LOG_LEVEL_DBG);

// Mock I2C emulator data
struct i2c_mock_data {
    uint8_t value;
};

// Emulator transfer function
static int i2c_mock_transfer(const struct emul *emul,
                             struct i2c_msg *msgs,
                             int num_msgs,
                             int addr)
{
    struct i2c_mock_data *data = (struct i2c_mock_data *)emul->data;

    for (int i = 0; i < num_msgs; i++) {
        if (msgs[i].flags & I2C_MSG_READ) {
            memset(msgs[i].buf, data->value, msgs[i].len);
            LOG_INF("Mock I2C read: returning 0x%02x", data->value);
        } else if (msgs[i].flags & I2C_MSG_WRITE) {
            LOG_INF("Mock I2C write: received 0x%02x", msgs[i].buf[0]);
            data->value = msgs[i].buf[0];
        }
    }

    return 0;
}

// Emulator API
static const struct i2c_emul_api i2c_mock_api = {
    .transfer = i2c_mock_transfer,
};

// Emulator instance
static struct i2c_mock_data i2c_mock_data = {
    .value = 0x42,
};

// Register emulator with DT node label `mock_sensor`

EMUL_DEFINE(i2c_mock_emul, DT_NODELABEL(mock_sensor),
            &i2c_mock_api,
            &i2c_mock_data);


int main(void)
{
    const struct device *i2c_dev = DEVICE_DT_GET(DT_NODELABEL(i2c0));
    uint8_t tx_buf[1] = { 0x55 };
    uint8_t rx_buf[1] = { 0 };
    struct i2c_msg msgs[2];

    if (!device_is_ready(i2c_dev)) {
        LOG_ERR("I2C device not ready");
        return 0;
    }

    // Write
    msgs[0].buf = tx_buf;
    msgs[0].len = 1;
    msgs[0].flags = I2C_MSG_WRITE | I2C_MSG_STOP;

    // Read
    msgs[1].buf = rx_buf;
    msgs[1].len = 1;
    msgs[1].flags = I2C_MSG_READ | I2C_MSG_STOP;

    int ret = i2c_transfer(i2c_dev, msgs, 2, 0x50);
    if (ret == 0) {
        LOG_INF("I2C transfer successful, read: 0x%02x", rx_buf[0]);
    } else {
        LOG_ERR("I2C transfer failed: %d", ret);
    }
}
