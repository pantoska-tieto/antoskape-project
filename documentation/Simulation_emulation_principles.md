# Simulation/emulation principles in testing

### Table of Contents
1. [Zephyr application - home page](../README.md)
2. [Add new board to project](Add_new_board_to_project.md)
3. [Artifactory storage server](Artifactory_storage_server.md)
4. [GitHub workflow_dispatch panel](Github_workflow_dispatch_panel.md)
5. [HW resources for tests](HW_resources_for_tests.md)
6. [Kconfig tester guide](Kconfig_tester_guide.md)
7. [Raspi runner installation](Raspi_runner_installation.md)
8. [Shell tests with native_sim](Shell_tests_with_native_sim.md)
9. [Tests list](Tests_list.md)
10. [Tests user guide](Tests_user_guide.md)
11. [MCUmgr subsystem for testing purposes](MCUmgr_subsystem_for_testing_purpose.md)
12. Simulation/emulation principles in testing [this page]
13. [BLE terms, roles and definitions](BLE_terms_definitions.md)
---

Sensor emulator APIs are a general feature in Zephyr RTOS, especially for unit testing and driver validation. Zephyr provides a structured way to emulate hardware devices like SPI, I2C, GPIO, and others using its device emulation framework.<br/>

<br/>

## Key Points About Zephyr's Emulator Framework:

- Purpose: Allows developers to test drivers and applications without physical hardware.
- Supported Buses: SPI, I2C, GPIO, and more.
- Integration: Emulators are integrated via devicetree nodes and can be accessed using emul_get_binding().
- Customization: You can define custom behavior using APIs like spi_emul_api or i2c_emul_api.

Where the emulation is used:

- Driver development: validate logic before hardware is available.
- CI pipelines: Run automated tests using emulated devices.
- Twister framework: Zephyr’s test runner supports emulators for hardware-independent testing.

### Documentation for study

1. For more comprehensive guidelines about Emulators/simulators see Zephyr documentation [Zephyr’s device emulators/simulators](https://docs.zephyrproject.org/latest/hardware/emulator/index.html).
2. BUS Emulators details can be found in [External Bus and Bus Connected Peripherals Emulators](https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/hardware/emulator/bus_emulators.rst).
3. PERIPHERAL Emulators overview can be found in [Zephyr’s device emulators/simulators](https://docs.nordicsemi.com/bundle/ncs-latest/page/zephyr/hardware/emulator/index.html).


<br/>

## Which device types/protocols/interfaces can be emulated in Zephyr?

<strong>BUS PROTOCOL EMULATORS</strong>

<table>
    <thead>
      <th><strong>PROTOCOL</strong></th>
      <th><strong>EMULATOR API</strong></th>
      <th><strong>KCONFIG OPTION</strong></th></tr>
    </thead>
      <tbody>
        <tr>
        <td>SPI</td>
        <td>spi_emul_api</strong></td>
        <td>CONFIG_SPI_EMUL</strong></td>
        </tr>
        <tr>
        <td>I2C</td>
        <td>i2c_emul_api</td>
        <td>CONFIG_I2C_EMUL</strong></td>
        </tr>
        <tr>
        <td>MSPI</td>
        <td>mspi_emul_api</td>
        <td>CONFIG_MSPI_EMUL</strong></td>
        </tr>
        <tr>
        <td>UART</td>
        <td>uart_emul_api</td>
        <td>CONFIG_UART_EMUL</strong></td>
        </tr>
        <tr>
        <td>eSPI</td>
        <td>espi_emul_api</td>
        <td>CONFIG_ESPI_EMUL</strong></td>
        </tr>
      </tbody>
</table>

<br/>

<strong>PERIPHERAL DEVICE EMULATORS</strong><br/>

<table>
    <thead>
      <th><strong>PROTOCOL</strong></th>
      <th><strong>EMULATOR API</strong></th>
      <th><strong>KCONFIG OPTION</strong></th></tr>
    </thead>
      <tbody>
        <tr>
        <td>ADC</td>
        <td>adc_emul_api</strong></td>
        <td>CONFIG_ADC_EMUL</strong></td>
        </tr>
        <tr>
        <td>DMA</td>
        <td>dma_emul_api</td>
        <td>CONFIG_DMA_EMUL</strong></td>
        </tr>
        <tr>
        <td>EEPROM</td>
        <td>eeprom_emul_api</td>
        <td>CONFIG_EEPROM_EMULATOR</strong></td>
        </tr>
        <tr>
        <td>EEPROM (RAM)</td>
        <td>eeprom_sim_api</td>
        <td>CONFIG_EEPROM_SIMULATOR</strong></td>
        </tr>
        <tr>
        <td>Flash</td>
        <td>flash_sim_api</td>
        <td>CONFIG_FLASH_SIMULATOR</strong></td>
        </tr>
        <tr>
        <td>GPIO</td>
        <td>gpio_emul_api</td>
        <td>CONFIG_GPIO_EMUL</strong></td>
        </tr>
        <tr>
        <td>RTC</td>
        <td>rtc_emul_api</td>
        <td>CONFIG_RTC_EMUL</strong></td>
        </tr>
      </tbody>
</table>

<br/>

### Emulator Features

Emulators are defined via devicetree and initialized using macros like EMUL_DT_DEFINE() or EMUL_DT_INST_DEFINE().
- They implement standard APIs that mimic real device behavior.
- They can be used in unit tests, shell commands, and CI pipelines.
- Some emulators support backend APIs for injecting test data or controlling behavior dynamically.

<br/>

## Example for SPI emulation with `spi_emul_api`

Below mentioned overview explains how to simulate a SPI sensor in Zephyr using the `spi_emul_api` interface. This is useful for testing sensor drivers without requiring actual hardware.


### Key Components

#### 1. `spi_emul_api`
A struct defining the behavior of the SPI emulator. You implement the `.io` function to handle SPI transactions.

```c
static struct spi_emul_api mock_api = {
    .io = mock_spi_transceive,
};
```
<br/>

#### 2. `mock_spi_transceive()`
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

<br/>

#### 3. `spi_regs[]`
A static array representing the sensor's internal register space.

```c
static uint8_t spi_regs[256];  // 8-bit addressable register space
```

---

<br/>

### Setup Steps

#### 1. Define Register Map

Populate `spi_regs[]` with mock sensor data:

```c
spi_regs[0x12] = 0x34; // Accel X LSB
spi_regs[0x13] = 0x12; // Accel X MSB
spi_regs[0x14] = 0x78; // Accel Y LSB
spi_regs[0x15] = 0x56; // Accel Y MSB
spi_regs[0x16] = 0xBC; // Accel Z LSB
spi_regs[0x17] = 0x9A; // Accel Z MSB
```

#### 2. Implement `mock_spi_transceive()`

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

#### 3. Bind Emulator to Device

Use `emul_get_binding()` to get the emulator instance and assign your API:

```c
const struct emul *emul = emul_get_binding("bmi@3");
struct spi_emul *spi_emul_inst = (struct spi_emul *)emul;
spi_emul_inst->api = &mock_api;
```

This links your emulator to the device node in the devicetree (e.g., `bmi@3`).


#### 4. Add Custom Shell Command

Register a shell command to read a range of registers:

```c
SHELL_CMD_REGISTER(spi_read_range, NULL, "Read range of SPI registers", cmd_spi_read_range);
```

And implement it using `shell_print()` to display values from `spi_regs[]`.


---

<br/>

### Injecting Mock Data into Real Driver

If you're testing a real sensor driver (e.g., BMI160), and it uses SPI, you can:
1. Point its devicetree node to the emulator.
2. Ensure the emulator is initialized before the driver starts (`SYS_INIT()`).
3. Use shell commands or test cases to interact with the driver.
