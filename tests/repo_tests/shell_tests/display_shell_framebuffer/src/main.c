#include <zephyr/kernel.h>
#include <zephyr/shell/shell.h>
#include <zephyr/sys/crc.h>
#include <zephyr/sys/printk.h>
#include <string.h>

// #include <zephyr/display/display.h>
// ESP32 board (like ESP32-S3 DevKitC) doesn't have a native display driver in Zephyr by default
// So we simulate a display driver with a dummy framebuffer and show its status via shell command

#define FRAMEBUFFER_SIZE 128
static uint8_t framebuffer[FRAMEBUFFER_SIZE];

static int cmd_display_status(const struct shell *shell, size_t argc, char **argv)
{
    // Simulate drawing a message into framebuffer
    memset(framebuffer, 0, sizeof(framebuffer));
    memcpy(framebuffer, "Message from Zephyr display", strlen("Message from Zephyr display"));

    // Compute CRC32 checksum of framebuffer
    uint32_t checksum = crc32_ieee(framebuffer, sizeof(framebuffer));

    shell_print(shell, "Last drawn: 'Message from Zephyr display'");
    shell_print(shell, "Framebuffer CRC32: 0x%08x", checksum);
    return 0;
}

SHELL_CMD_REGISTER(display_status, NULL, "Show simulated display status", cmd_display_status);

int main(void)
{
    printk("Dummy display driver test started\n");
    return 0;
}