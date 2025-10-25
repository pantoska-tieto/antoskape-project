
# 🧪 Mocking SPI Sensor in Zephyr with `spi_emul_api`

This guide explains how to simulate a SPI sensor in Zephyr using the `spi_emul_api` interface. This is useful for testing sensor drivers without requiring actual hardware.

---

## 📦 Overview

Zephyr provides a flexible **SPI emulator framework** that allows you to:
- Emulate SPI devices with custom behavior.
- Inject test data into drivers.
- Validate driver logic in unit tests or simulations.

---

## 🧰 Key Components

### 1. `spi_emul_api`
A struct defining the behavior of the SPI emulator. You implement the `.io` function to handle SPI transactions.

```c
static struct spi_emul_api mock_api = {
    .io = mock_spi_transceive,
};
```

### 2. `mock_spi_transceive()`
Your custom function that mimics how the sensor responds to SPI reads/writes.

```c
static int mock_spi_transceive(const struct emul *emul,
                               const struct spi_config *config,
                               const struct spi_buf_set *tx_bufs,
                               const struct spi_buf_set *rx_bufs)
{
    // Interpret tx_bufs and populate rx_bufs based on your emulated register map
}
```

### 3. `spi_regs[]`
A static array representing the sensor's internal register space.

```c
static uint8_t spi_regs[256];  // 8-bit addressable register space
```

---

## 🛠️ Setup Steps

### ✅ Step 1: Define Register Map

Populate `spi_regs[]` with mock sensor data:

```c
spi_regs[0x12] = 0x34; // Accel X LSB
spi_regs[0x13] = 0x12; // Accel X MSB
spi_regs[0x14] = 0x78; // Accel Y LSB
spi_regs[0x15] = 0x56; // Accel Y MSB
spi_regs[0x16] = 0xBC; // Accel Z LSB
spi_regs[0x17] = 0x9A; // Accel Z MSB
```

### ✅ Step 2: Implement `mock_spi_transceive()`

Handle SPI read/write commands based on your protocol (e.g., MSB set for read):

```c
bool is_read = cmd & 0x80;
uint8_t reg_addr = cmd & 0x7F;

if (is_read) {
    // Fill rx_data from spi_regs[]
} else {
    // Write tx_data to spi_regs[]
}
```

### ✅ Step 3: Bind Emulator to Device

Use `emul_get_binding()` to get the emulator instance and assign your API:

```c
const struct emul *emul = emul_get_binding("bmi@3");
struct spi_emul *spi_emul_inst = (struct spi_emul *)emul;
spi_emul_inst->api = &mock_api;
```

This links your emulator to the device node in the devicetree (e.g., `bmi@3`).

---

## 🧪 Injecting Mock Data into Real Driver

If you're testing a real sensor driver (e.g., BMI160), and it uses SPI, you can:
1. Point its devicetree node to the emulator.
2. Ensure the emulator is initialized before the driver starts (`SYS_INIT()`).
3. Use shell commands or test cases to interact with the driver.

---

## 🧵 Example Shell Command

Register a shell command to read a range of registers:

```c
SHELL_CMD_REGISTER(spi_read_range, NULL, "Read range of SPI registers", cmd_spi_read_range);
```

And implement it using `shell_print()` to display values from `spi_regs[]`.

---

## 🧪 Testing Strategy

- Use `printk()` or `shell_print()` to verify emulator behavior.
- Write unit tests using Zephyr’s `ztest` framework.
- Combine with `twister` for automated regression testing.

---

## 📌 Notes

- Emulator must be initialized **before** the driver accesses it.
- Use `SYS_INIT()` with appropriate priority (`APPLICATION` or earlier).
- Emulator logic should match the real sensor’s SPI protocol.
