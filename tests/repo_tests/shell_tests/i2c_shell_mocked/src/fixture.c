/*
 * Copyright 2023 Google LLC
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include "fixture.h"

#include <zephyr/drivers/emul_sensor.h>
#include <zephyr/drivers/sensor.h>

static void sensor_bmi160_setup_emulator(const struct device *dev, const struct emul *emulator)
{
	static struct {
		enum sensor_channel channel;
		q31_t value;
	} values[] = {
		{SENSOR_CHAN_ACCEL_X, 0},       {SENSOR_CHAN_ACCEL_Y, 1 << 28},
		{SENSOR_CHAN_ACCEL_Z, 2 << 28}, {SENSOR_CHAN_GYRO_X, 3 << 28},
		{SENSOR_CHAN_GYRO_Y, 4 << 28},  {SENSOR_CHAN_GYRO_Z, 5 << 28},
	};
	static struct sensor_value scale;

	/* 4g */
	scale.val1 = 39;
	scale.val2 = 226600;

	/* 125 deg/s */
	scale.val1 = 2;
	scale.val2 = 181661;
}

static void *bmi160_setup(void)
{
	static struct bmi160_fixture fixture = {
		.dev_i2c = DEVICE_DT_GET(DT_ALIAS(accel_1)),
		.emul_i2c = EMUL_DT_GET(DT_ALIAS(accel_1)),
	};

	sensor_bmi160_setup_emulator(fixture.dev_i2c, fixture.emul_i2c);

	return &fixture;
}
