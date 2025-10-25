#include <zephyr/kernel.h>
#include <zephyr/init.h>
#include <zephyr/drivers/emul.h>
#include <zephyr/drivers/spi_emul.h>
#include <zephyr/shell/shell.h>
#include <zephyr/sys/printk.h>
#include <string.h>
#include <stdlib.h>
#include <zephyr/shell/shell_uart.h>

// SPI emulator 8-bit register space
static uint8_t spi_regs[256];

// Mocking SPI transceive operations with 8-bit register space
static int mock_spi_transceive(const struct emul *emul,
                               const struct spi_config *config,
                               const struct spi_buf_set *tx_bufs,
                               const struct spi_buf_set *rx_bufs)
{
    ARG_UNUSED(emul);
    ARG_UNUSED(config);

    if (tx_bufs->count < 1 || rx_bufs->count < 1) {
        return -EINVAL;
    }

    const uint8_t *tx_data = tx_bufs->buffers[0].buf;
    uint8_t *rx_data = rx_bufs->buffers[0].buf;

    uint8_t cmd = tx_data[0];
    bool is_read = cmd & 0x80;
    uint8_t reg_addr = cmd & 0x7F;

    if (is_read) {
        for (size_t i = 0; i < rx_bufs->buffers[0].len; i++) {
            rx_data[i] = spi_regs[reg_addr + i];
        }
        printk("SPI emulator multi-read from reg 0x%02X: ", reg_addr);
        for (size_t i = 0; i < rx_bufs->buffers[0].len; i++) {
            printk("0x%02X ", rx_data[i]);
        }
        printk("\n");
    } else {
        for (size_t i = 1; i < tx_bufs->buffers[0].len; i++) {
            spi_regs[reg_addr + i - 1] = tx_data[i];
        }
        printk("SPI emulator multi-write starting at reg 0x%02X\n", reg_addr);
    }
    return 0;
}

// Custom shell Write command
static int cmd_spi_write(const struct shell *shell, size_t argc, char **argv)
{
    if (argc < 3) {
        shell_print(shell, "Usage: spi_write <reg> <val1> [val2] ...");
        return -EINVAL;
    }

    uint8_t reg = strtol(argv[1], NULL, 0);
    shell_print(shell, "Writing to SPI registers starting at 0x%02X:", reg);

    for (size_t i = 2; i < argc; i++) {
        uint8_t val = strtol(argv[i], NULL, 0);
        spi_regs[reg] = val;
        shell_print(shell, "  0x%02X: 0x%02X", reg, val);
        reg++;
    }

    return 0;
}

// Custom shell Read command
static int cmd_spi_read(const struct shell *shell, size_t argc, char **argv)
{
    if (argc != 2) {
        shell_print(shell, "Usage: spi_read <reg>");
        return -EINVAL;
    }

    uint8_t reg = strtol(argv[1], NULL, 0);
    shell_print(shell, "SPI emulator read from reg 0x%02X: 0x%02X", reg, spi_regs[reg]);
    return 0;
}

// Custom shell Read command for multiple registers from a range
static int cmd_spi_read_range(const struct shell *shell, size_t argc, char **argv)
{
    if (argc != 3) {
        shell_print(shell, "Usage: spi_read_range <start> <count>");
        return -EINVAL;
    }

    uint8_t start = strtol(argv[1], NULL, 0);
    uint8_t count = strtol(argv[2], NULL, 0);

    shell_print(shell, "Reading %d registers starting from 0x%02X:", count, start);
    for (uint8_t i = 0; i < count; i++) {
        shell_print(shell, "  0x%02X: 0x%02X", start + i, spi_regs[start + i]);
    }
    return 0;
}

// Register custom shell commands
SHELL_CMD_REGISTER(spi_write, NULL, "Write SPI registers", cmd_spi_write);
SHELL_CMD_REGISTER(spi_read, NULL, "Read SPI register", cmd_spi_read);
SHELL_CMD_REGISTER(spi_read_range, NULL, "Read range of SPI registers", cmd_spi_read_range);

// Early initialization of SPI emulator
static int setup_spi_emul(void)
{
    const struct emul *emul = emul_get_binding("bmi@3");
    if (!emul) {
        printk("SPI emulator not found!\n");
        return -ENODEV;
    }

    struct spi_emul *spi_emul_inst = (struct spi_emul *)emul;
    static struct spi_emul_api mock_api = {
        .io = mock_spi_transceive,
    };
    spi_emul_inst->api = &mock_api;

    // Simulated sensor SPI data
    spi_regs[0x12] = 0x34; // Accel X LSB
    spi_regs[0x13] = 0x12; // Accel X MSB
    spi_regs[0x14] = 0x78; // Accel Y LSB
    spi_regs[0x15] = 0x56; // Accel Y MSB
    spi_regs[0x16] = 0xBC; // Accel Z LSB
    spi_regs[0x17] = 0x9A; // Accel Z MSB

    printk("SPI emulator initialized early.\n");
    return 0;
}

// Helper function for printing to shell
static void spi_read_range_print(uint8_t start, uint8_t count)
{
    printk("Reading %d registers starting from 0x%02X:\n", count, start);
    for (uint8_t i = 0; i < count; i++) {
        printk("  0x%02X: 0x%02X\n", start + i, spi_regs[start + i]);
    }
}


// Ensure emulator is initialized before application starts
SYS_INIT(setup_spi_emul, APPLICATION, CONFIG_APPLICATION_INIT_PRIORITY);

// Main function
int main(void)
{
    printk("System ready. Use 'spi_write', 'spi_read', and 'spi_read_range' commands.\n");
    // Print to shell for console test
    spi_read_range_print(0x12, 6);
    return 0;
}
