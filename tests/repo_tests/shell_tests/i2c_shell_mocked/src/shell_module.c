#include <zephyr/shell/shell.h>
#include <zephyr/drivers/emul.h>
#include <zephyr/drivers/i2c_emul.h>
#include <zephyr/sys/printk.h>
#include <stdlib.h>

// External functions from main.c
extern int custom_i2c_write(const struct emul *target, int reg_addr, int value);
extern int custom_i2c_read(const struct emul *target, int reg_addr);

// Emulator binding
static const struct emul *emul_i2c = NULL;

// Shell command: i2c_write <reg> <val>
static int cmd_i2c_write(const struct shell *shell, size_t argc, char **argv)
{
    if (argc != 3) {
        shell_error(shell, "Usage: i2c_write <reg> <val>");
        return -EINVAL;
    }

    int reg = strtol(argv[1], NULL, 0);
    int val = strtol(argv[2], NULL, 0);

    if (!emul_i2c) {
        emul_i2c = emul_get_binding("bmi@68");
        if (!emul_i2c) {
            shell_error(shell, "I2C emulator not found");
            return -ENODEV;
        }
    }

    int ret = custom_i2c_write(emul_i2c, reg, val);
    if (ret < 0) {
        shell_error(shell, "Write failed with error %d", ret);
    } else {
        shell_print(shell, "Write successful to reg 0x%02X with value 0x%02X", reg, val);
    }

    return ret;
}

// Shell command: i2c_read <reg>
static int cmd_i2c_read(const struct shell *shell, size_t argc, char **argv)
{
    if (argc != 2) {
        shell_error(shell, "Usage: i2c_read <reg>");
        return -EINVAL;
    }

    int reg = strtol(argv[1], NULL, 0);

    if (!emul_i2c) {
        emul_i2c = emul_get_binding("bmi@68");
        if (!emul_i2c) {
            shell_error(shell, "I2C emulator not found");
            return -ENODEV;
        }
    }

    int ret = custom_i2c_read(emul_i2c, reg);
    if (ret < 0) {
        shell_error(shell, "Read failed with error %d", ret);
    } else {
        shell_print(shell, "Read from reg 0x%02X returned value 0x%02X", reg, ret);
    }

    return 0;
}

// Register shell commands
SHELL_CMD_ARG_REGISTER(i2c_write, NULL, "Write I2C register: i2c_write <reg> <val>", cmd_i2c_write, 3, 0);
SHELL_CMD_ARG_REGISTER(i2c_read, NULL, "Read I2C register: i2c_read <reg>", cmd_i2c_read, 2, 0);