/*
 * Copyright (c) 2021 Nordic Semiconductor ASA
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <app_version.h>
#include <custom_lib/custom_lib.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(main, CONFIG_APP_LOG_LEVEL);

int main(void)
{
	printk("Zephyr Example Application %s\n", APP_VERSION_STRING);
	printk("Custom lib get value returned: %d\n", custom_lib_get_value(1));

	return 0;
}

