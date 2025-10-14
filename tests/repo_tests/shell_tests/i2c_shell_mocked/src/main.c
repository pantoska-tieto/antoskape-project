/*
 * Copyright 2023 Google LLC
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/drivers/emul_sensor.h>
#include <zephyr/drivers/sensor.h>
#include <zephyr/drivers/i2c_emul.h>
#include <zephyr/drivers/emul.h>
#include <zephyr/sys/printk.h>
#include "checks.h"
#include "fixture.h"


// Simulate a proper I2C device by using an array to represent the register space
static uint8_t bmi160_regs[256];

// Universal I2C transfer mock with 8-bit register space
static int mock_i2c_transfer(const struct emul *target, struct i2c_msg *msgs, int num_msgs, int addr)
{
    ARG_UNUSED(target);
    ARG_UNUSED(addr);
    
    // Handle address probe (zero-length write for 'i2c scan' command)
    if (num_msgs == 1 && msgs[0].len == 0 && !(msgs[0].flags & I2C_MSG_READ)) {
        // Acknowledge the probe
        printk("I2C probe at address 0x%02X\n", addr);
        return 0;
    }

    if (num_msgs != 2) {
        return -ENOSYS;
    }

    uint8_t reg_addr = msgs[0].buf[0];

    // Write operation
    if (!(msgs[1].flags & I2C_MSG_READ)) {
        bmi160_regs[reg_addr] = msgs[1].buf[0];
        //printk("mock_i2c_transfer: wrote 0x%02X to reg 0x%02X\n", msgs[1].buf[0], reg_addr);
        return 0;
    }

    // Read operation
    if (msgs[1].flags & I2C_MSG_READ) {
        msgs[1].buf[0] = bmi160_regs[reg_addr];
        //printk("mock_i2c_transfer: read 0x%02X from reg 0x%02X\n", msgs[1].buf[0], reg_addr);
        return 0;
    }

    return -ENOSYS;
}

// User-configurable variables for universal I2C testing
static int user_mem_address = 0x68;         // I2C register address to write/read
static int user_mem_value = 0x55;           // Value to write
static int user_mem_cell_to_read = 0x68;    // I2C register address to read

// Universal I2C write operation
int custom_i2c_write(const struct emul *target, int reg_addr, int value) {
    struct i2c_msg msgs[2];
    uint8_t reg = reg_addr;
    uint8_t val = value;
    msgs[0].buf = &reg;
    msgs[0].len = 1;
    msgs[0].flags = 0; // Read register address
    msgs[1].buf = &val;
    msgs[1].len = 1;
    msgs[1].flags = 0; // Write operation

    printk("I2C emulator write to address: 0x%02X with value: 0x%02X\n", reg_addr, value); 

    // You can change the last argument to be the I2C device address if needed
    return mock_i2c_transfer(target, msgs, 2, reg_addr);
}

// Universal I2C read operation
int custom_i2c_read(const struct emul *target, int reg_addr) {
    struct i2c_msg msgs[2];
    uint8_t reg = reg_addr;
    uint8_t read_buf = 0;
    msgs[0].buf = &reg;
    msgs[0].len = 1;
    msgs[0].flags = 0; // Read register address
    msgs[1].buf = &read_buf;  // READ value from I2C
    msgs[1].len = 1;
    msgs[1].flags = I2C_MSG_READ;

    int ret = mock_i2c_transfer(target, msgs, 2, reg_addr);
    if (ret == 0) {
        printk("I2C emulator read from address: 0x%02X with value: 0x%02X\n", reg_addr, read_buf); 
        return read_buf;
    }
    return ret;
}

int main(void)
{
	// Get the emulator instance by label
    const struct emul *emul_i2c = emul_get_binding("bmi@68");
    if (!emul_i2c) {
        printk("I2C emulator not found!\n");
        return 0;
    }
    else {
        printk("I2C emulator found and binded.\n");
    }

    struct i2c_emul *i2c_emul_inst = (struct i2c_emul *)emul_i2c;

    // Assign your mock API to the emulator
    struct i2c_emul_api mock_bus_api = {
        .transfer = mock_i2c_transfer,
        // TODO! You can add .configure, .init, etc. if needed
    };

    i2c_emul_inst->api = &mock_bus_api;

    // Test code to demonstrate read/write operations
    // Perform custom write if address is set
    if (user_mem_address >= 0) {
        int ret = custom_i2c_write(emul_i2c, user_mem_address, user_mem_value);      
        if (ret < 0) {
            printk("I2C write operation failed with error %d\n", ret);
        }

    }

    // Perform custom read if cell is set
    if (user_mem_cell_to_read >= 0) {
        int ret = custom_i2c_read(emul_i2c, user_mem_cell_to_read);     
        if (ret < 0) {
            printk("I2C read operation failed with error %d\n", ret);
        }
    }

    // Perform custom write if address is set
    if (user_mem_address >= 0) {
        int ret = custom_i2c_write(emul_i2c, 0x69, 0x56);      
        if (ret < 0) {
            printk("I2C write operation failed with error %d\n", ret);
        }

    }

    // Perform custom read if cell is set
    if (user_mem_cell_to_read >= 0) {
        int ret = custom_i2c_read(emul_i2c, 0x69);     
        if (ret < 0) {
            printk("I2C read operation failed with error %d\n", ret);
        }
    }
    return 0;
}