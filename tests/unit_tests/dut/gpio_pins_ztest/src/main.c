/*
 * Copyright (c) 2024 Nordic Semiconductor ASA
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/ztest.h>

#if DT_NODE_HAS_PROP(DT_ALIAS(led9), gpios)
#define TEST_NODE DT_GPIO_CTLR(DT_ALIAS(led9), gpios)
#define TEST_PIN DT_GPIO_PIN(DT_ALIAS(led9), gpios)
#else
#error Unsupported board
#endif


ZTEST(gpio_pins_ztest, test_gpio_manipulation)
{
	int response;
	const struct device *port;

	port = DEVICE_DT_GET(TEST_NODE);
	zassert_true(device_is_ready(port), "GPIO dev is not ready");

	response = gpio_pin_configure(port, TEST_PIN, GPIO_OUTPUT | GPIO_ACTIVE_HIGH);
	zassert_ok(response, "Pin configuration failed: %d", response);

	response = gpio_pin_set(port, TEST_PIN, 0);
	zassert_ok(response, "Pin low state set failed: %d", response);

	response = gpio_pin_set(port, TEST_PIN, 1);
	zassert_ok(response, "Pin high state set failed: %d", response);

	response = gpio_pin_toggle(port, TEST_PIN);
	zassert_ok(response, "Pin toggle failed: %d", response);

	response = gpio_pin_configure(port, TEST_PIN, GPIO_INPUT | GPIO_PULL_DOWN);
	zassert_ok(response, "Failed to configure pin as input with pull down: %d", response);

	response = gpio_pin_get(port, TEST_PIN);
	zassert_equal(response, 0, "Invalid pin state: %d", response);
}

ZTEST_SUITE(gpio_pins_ztest, NULL, NULL, NULL, NULL, NULL);
