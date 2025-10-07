#include <zephyr/kernel.h>
#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/hci.h>
#include <zephyr/bluetooth/gatt.h>
#include <zephyr/shell/shell.h>
#include <zephyr/sys/util.h>
#include <zephyr/sys/printk.h>
#include <zephyr/settings/settings.h>
#include <zephyr/bluetooth/services/bas.h> // Include Battery Service
#include <zephyr/bluetooth/services/hrs.h> // Include Heart Rate Service for reference

#define DEVICE_NAME CONFIG_BT_DEVICE_NAME
uint8_t battery_level = 60;
uint8_t heart_rate = 90;

static int cmd_get_battery(const struct shell *shell, size_t argc, char **argv)
{
    shell_print(shell, "Battery level: %d%%", battery_level);
    return 0;
}

static int cmd_get_hr(const struct shell *shell, size_t argc, char **argv)
{
    shell_print(shell, "Heart rate: %d bpm", heart_rate);
    return 0;
}

SHELL_CMD_REGISTER(get_battery, NULL, "Get current battery level", cmd_get_battery);
SHELL_CMD_REGISTER(get_hr, NULL, "Get current heart rate", cmd_get_hr);

// Advertise your device as connectable
// Include the complete device name ("Tieto BLE" or whatever is set via bt_set_name)
static const struct bt_data ad[] = {
    BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
    BT_DATA(BT_DATA_NAME_COMPLETE, CONFIG_BT_DEVICE_NAME,  sizeof(CONFIG_BT_DEVICE_NAME) - 1)
};

static const struct bt_data sd[] = {
    // Full name in scan response
    BT_DATA(BT_DATA_NAME_COMPLETE, CONFIG_BT_DEVICE_NAME, sizeof(CONFIG_BT_DEVICE_NAME) - 1),
};


int main(void)
{
    int err;
    printk("Starting Bluetooth Shell test\n");

    err = bt_enable(NULL);
    if (err) {
        printk("Bluetooth init failed (err %d)\n", err);
        return 0;
    }

    printk("Bluetooth initialized\n");

    if (IS_ENABLED(CONFIG_SETTINGS)) {
		settings_load();
	}

	printk("Bluetooth Settings loaded\n");

    // Set Service hardcoded values
    bt_bas_set_battery_level(battery_level);  // Set initial battery level to 85%
    bt_hrs_notify(heart_rate);                // Simulate 90 bpm

    // Start advertising with connectable and discoverable flags
    err = bt_le_adv_start(BT_LE_ADV_CONN_FAST_1, ad, ARRAY_SIZE(ad), sd, ARRAY_SIZE(sd));
    if (err) {
        printk("Advertising failed to start (err %d)\n", err);
        return 0;
    }

    printk("Advertising successfully started\n");
    return 0;
}