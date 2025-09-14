/*
 * Copyright (c) 2016 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/ztest.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>


/* 1000 msec = 1 sec */
#define SLEEP_TIME_MS   2000

/* The devicetree node identifier for the "led0" alias. */
// #define LED0_NODE DT_ALIAS(led0)
#define SIZE 10

/* The devicetree node identifier for the 
// "led0" - control gpio pin and 
// "led9 - pin to verify LED state
// aliases. */
#define LED0_NODE DT_ALIAS(led0)
#define LED9_NODE DT_ALIAS(led9)

static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED0_NODE, gpios);
static const struct gpio_dt_spec led9 = GPIO_DT_SPEC_GET(LED9_NODE, gpios);

/*
 * A build error on this line means your board is unsupported.
 * See the sample documentation for information on how to fix this.
 */
// static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED0_NODE, gpios);
int ret;
int ret9;


bool contains_false(bool *list, int size) {
    for (int i = 0; i < size; i++) {
        if (!list[i]) {
            return true;  // Found a false value
        }
    }
    return false;  // All values are true
}


ZTEST(gpio, test_gpio_toggle_and_verify)
{
    zassert_true(gpio_is_ready_dt(&led), "GPIO device not ready");
    printk("GPIO system is ready\n");

    zassert_true(gpio_is_ready_dt(&led9), "GPIO device to verify LED state not ready");
    printk("GPIO system to verify LED state is ready\n");

    ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);
    printk("Initial Pin configure: %d\n", ret);
    zassert_true(ret == 0, "Failed to configure GPIO");

    ret9 = gpio_pin_configure_dt(&led9, GPIO_INPUT);
    printk("Initial Pin configure: %d\n", ret9);
    zassert_true(ret9 == 0, "Failed to configure GPIO to verify LED state");

    // Initial setup
    bool *list = NULL;      // Start with an empty list of booleans
    int size = 0;           // Current size of the list
    int init_state = 0;     // Initial state of the LED pin

    for (int i = 0; i < SIZE + 1; i++) {
        
        bool *temp = realloc(list, (size + 1) * sizeof(bool));
        if (temp == NULL) {
            free(list);
            printk("Memory allocation failed.\n");
        }
        list = temp;

        // Toggle pin with LED connected
        ret = gpio_pin_toggle_dt(&led);
        zassert_true(ret == 0, "Failed to toggle GPIO");

        // Read pin state to verify LED state
        int actual_state = gpio_pin_get(led9.port, led9.pin);
        if (actual_state != init_state) {            
            list[size] = true;
            size++;
            init_state = actual_state; // Update init_state to the new state
        }
        else {
            list[size] = false;
            size++;
            init_state = actual_state;
        }
    
        k_msleep(SLEEP_TIME_MS);
    }

    zassert_true(contains_false(list, size), "GPIO (LED) state mismatch, test failed");
}

ZTEST_SUITE(gpio, NULL, NULL, NULL, NULL, NULL);
