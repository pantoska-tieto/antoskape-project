# How to add a new board into Zephyr project

### Table of Contents
1. [Zephyr application - home page](../README.md)
2. Add new board to project [this page]
3. [Artifactory storage server](Artifactory_storage_server.md)
4. [GitHub workflow_dispatch panel](Github_workflow_dispatch_panel.md)
5. [HW resources for tests](HW_resources_for_tests.md)
6. [Kconfig tester guide](Kconfig_tester_guide.md)
7. [Raspi runner installation.md](Raspi_runner_installation.md)
8. [Shell commands with native_sim.md](Shell_commands_with_native_sim.md)
9. [Tests list](Tests_list.md)
10. [Tests user guide](Tests_user_guide.md)
---



## 1. Create Board Directory
- Navigate to: `boards/<architecture>/<board_name>/`
- Example: `boards/arm/my_custom_board/`
- Create this directory if it doesn’t exist.

## 2. Add Board Files
Inside the board directory, create the following files:
- `Kconfig.board` – board-specific configuration options.
- `board.cmake` – CMake logic for board selection.
- `<board_name>.dts` – main device tree source file.
- `<board_name>_defconfig` – default configuration for the board.
- `board.yaml` – metadata for the board (used by Twister and CI).

## 3. Create Device Tree Files
- Use existing SoC and peripheral bindings.
- Include SoC `.dtsi` files using `#include`.
- Define memory regions, peripherals, and aliases.

## 4. Define Pinmux and Peripherals
- If needed, create a `pinmux.c` or similar file in your board directory or reference existing ones.
- Ensure GPIO, UART, SPI, I2C, etc., are correctly defined in the DTS.

## 5. Create or Reuse SoC Support
- If your board uses a new SoC, you may need to add SoC support under `soc/<architecture>/<vendor>/`.
- Otherwise, reuse existing SoC support.

## 6. Add Board to CMake and Kconfig
- Ensure your board is discoverable by Zephyr’s build system.
- Update `boards/Kconfig` and `boards/CMakeLists.txt` if necessary.

## 7. Update project sample/test files


Typical Zephyr project sample/test folder structure:<br/>
<br/>

```
my_sample/
├── CMakeLists.txt                      # CMake build configuration for the Zephyr project
├── prj.conf                            # Project-specific configuration options for Zephyr
├── pytest/
│   └──test_feature.py                  # Pytest test file (optional)
├── src/
│   └── main.c                          # Main application/test source file (mandatory)
├── boards/
│   └──esp32s3_devkitc.overlay          # Custom board definitions/overlays (.dts, .overlay, .yaml files)
├── overlay-myboard.dts                 # Optional device tree overlay to modify hardware configuration
├── README.rst                          # Optional documentation in reStructuredText format
├── testcase.yaml                       # Twister sample/test configuration file (with test suite/case names etc.)
```

<br/>

Example for testcase.yaml content:<br/>

<br/>

```
tests:
  repo_tests.wifi_shell:
    harness: pytest
    harness_config:
      pytest_dut_scope: session
    platform_allow:
      - native_sim/native/64
      - esp32s3_devkitc/esp32s3/procpu
      - esp8684_devkitm
      - nrf52833dk/nrf52833
    integration_platforms:
      - esp32s3_devkitc/esp32s3/procpu
      - nrf52833dk/nrf52833
    tags:
      - wifi
      - integration
```
<br/>
Example for "ESP32 S3 Devkitc" compound board identifier:<br/>

<br/>

```
<board_name>/<soc_name>/<core_name>

Example:  esp32s3_devkitc/esp32s3/procpu

- esp32s3_devkitc   → The board name (defined in Zephyr's boards/ directory)​
- esp32s3           → The SoC (System on Chip) name​
- procpu            → The core name (ESP32-S3 has dual cores: procpu and appcpu)​

How to get compound identifier?
1. Get list of available boards:        "west boards"​ command in terminal
2. Get list of available SoCs:          zephyr/boards/<vendor>/board.yml​
3. Get list of available Cores:​         zephyr/soc/<vendor>/soc.yml​​
```
<br/>

- Ensure your board is discoverable by Zephyr’s build system: <br/>
add board's <strong>compound identifier</strong> to `plattform_allow:` section<br/>
(`- esp32s3_devkitc/esp32s3/procpu`)
- Create new Device tree source (DTS) overlay-file (.dts, .overlay, .yaml) if board hardware configuration differs from default Devicetree (DT) structure in Zephyr RTOS. Save this overlay file to board/ subfolder.
- If overlay-file is needed, define the path to overlay file in `CMakeLists.txt` file with<br/>
<br/>
`set(DTC_OVERLAY_FILE "boards/<board_name>.overlay")`<br/>
<br/>
before the find_package() declaration. See example:

```
cmake_minimum_required(VERSION 3.20.0)
set(DTC_OVERLAY_FILE "boards/esp32s3_devkitc.overlay")

find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(mock_adc_sample)
target_sources(app PRIVATE src/main.c)
```
<br/>

- All additional declarations, definitions, and configurations should be placed in main application source file `src/main.c`.

<br/>

## 8. Build and run sample/test files with using new board

- west build -p always -b <board_name>/<soc_name>/<core_name> tests/my_sample

    <i>Example:</i><br/>

     `west build -p always -b esp32s3_devkitc/esp32s3/procpu tests/my_sample`

- west twister -vv --platform <board_name>/<soc_name>/<core_name> -T tests/my_sample

    <i>Example for test triggered on real board hardware:</i><br/>

     `west twister -vv --platform esp32s3_devkitc/esp32s3/procpu --device-testing --device-serial /dev/ttyUSB0 --flash-before -T tests/my_sample`