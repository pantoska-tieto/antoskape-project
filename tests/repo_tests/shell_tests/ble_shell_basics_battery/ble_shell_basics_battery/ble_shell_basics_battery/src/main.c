#include <zephyr/kernel.h>
#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/hci.h>
#include <zephyr/bluetooth/gatt.h>
#include <zephyr/bluetooth/services/bas.h>
#include <zephyr/settings/settings.h>
#include <zephyr/shell/shell.h>
#include <zephyr/device.h>
#include <zephyr/sys/util.h>

#define DEVICE_NAME CONFIG_BT_DEVICE_NAME

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

    // Initialize Battery Service - shown as Device Type: Battery in nRF Connect
    bt_bas_set_battery_level(85);

    // Start advertising with connectable and discoverable flags
    err = bt_le_adv_start(BT_LE_ADV_CONN_FAST_1, ad, ARRAY_SIZE(ad), sd, ARRAY_SIZE(sd));
    if (err) {
        printk("Advertising failed to start (err %d)\n", err);
        return 0;
    }

    printk("Advertising successfully started\n");
    return 0;
}