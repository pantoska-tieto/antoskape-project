#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/hci.h>
#include <zephyr/bluetooth/gatt.h>
#include <zephyr/shell/shell.h>
#include <zephyr/sys/printk.h>
#include <stdlib.h>
#include <zephyr/settings/settings.h>
#include <zephyr/bluetooth/services/hrs.h>


static uint8_t heart_rate = 72;
static void notify_heart_rate(void);

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

BT_GATT_SERVICE_DEFINE(sim_hrs_svc,
    BT_GATT_PRIMARY_SERVICE(BT_UUID_DECLARE_16(0x180D)),
    BT_GATT_CHARACTERISTIC(BT_UUID_DECLARE_16(0x2A37),
                           BT_GATT_CHRC_NOTIFY,
                           BT_GATT_PERM_NONE,
                           NULL, NULL, NULL),
    BT_GATT_CCC(NULL, BT_GATT_PERM_READ | BT_GATT_PERM_WRITE),
);

static const struct bt_gatt_attr *hrm_attr = &sim_hrs_svc.attrs[1];

static void notify_heart_rate(void)
{
    bt_gatt_notify(NULL, hrm_attr, &heart_rate, sizeof(heart_rate));
}

static int cmd_set_hr(const struct shell *shell, size_t argc, char **argv)
{
    if (argc != 2) {
        shell_print(shell, "Usage: set_hr <value>");
        return -EINVAL;
    }

    heart_rate = (uint8_t)atoi(argv[1]);
    shell_print(shell, "Heart rate set to %d bpm", heart_rate);
    notify_heart_rate();
    return 0;
}

static int cmd_get_hr(const struct shell *shell, size_t argc, char **argv)
{
    shell_print(shell, "Heart rate: %d bpm", heart_rate);
    return 0;
}

SHELL_CMD_ARG_REGISTER(set_hr, NULL, "Set simulated heart rate", cmd_set_hr, 2, 0);
SHELL_CMD_ARG_REGISTER(get_hr, NULL, "Get simulated heart rate", cmd_get_hr, 1, 0);


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

    // Start advertising with connectable and discoverable flags
    err = bt_le_adv_start(BT_LE_ADV_CONN_FAST_1, ad, ARRAY_SIZE(ad), sd, ARRAY_SIZE(sd));
    if (err) {
        printk("Advertising failed to start (err %d)\n", err);
        return 0;
    }

    printk("Advertising successfully started\n");

    while (1) {
        notify_heart_rate();
        k_sleep(K_SECONDS(5));
    }
    return 0;
}