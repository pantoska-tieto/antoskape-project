/*
 * Copyright (c) 2025 Tietoevry
 *
 * SPDX-License-Identifier: Apache-2.0
 */
#include <stdio.h>
#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>

/* The devicetree node identifier for the "led0" alias. */
#define LED0_NODE DT_ALIAS(led0)
#define LED9_NODE DT_ALIAS(led9)

static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED0_NODE, gpios);
static const struct gpio_dt_spec led9 = GPIO_DT_SPEC_GET(LED9_NODE, gpios);

int main(void)
{
	int ret;

	if (!gpio_is_ready_dt(&led)) {
		printf("GPIO device not ready\n");
		return 0;
	}

	if (!gpio_is_ready_dt(&led9)) {
		printf("GPIO device to verify LED state not ready\n");
		return 0;
	}

	ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);
	if (ret < 0) {
		printf("Error %d: failed to configure pin %d\n",
		       ret, led.pin);
		return 0;
	}
	ret = gpio_pin_configure_dt(&led9, GPIO_INPUT);
	if (ret < 0) {
		printf("Error %d: failed to configure state check pin %d\n",
		       ret, led9.pin);
	}

	return 0;
}
