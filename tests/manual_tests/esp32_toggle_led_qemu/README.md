## Toggle LED test for ESP32 boards with QEMU simulation
### Description
This test script is designed to verify the functionality of toggling an LED on an ESP32 board using QEMU simulation. 
No target board is required for this test. The test script will run on Host machine with Espressif QEMU installed.
The test script will toggle the LED on the virtual board what is represented by teminal messages "LED state: OFF: and "LED state: OFF". The LED is toggled every 1 second. The test script will run in 10 cycles and then must be interrupted by manual intervention - see <strong>Usage</strong> section for more details.

<br/>

### Prerequisites
- Espressif QEMU package installed on Host.

<br/>

#### Usage

- Build the sample binaries into the output folder `build/`:<br/>

   ```
   west build -p always -b esp32s3_devkitc/esp32s3/procpu tests/manual_tests/esp32_toggle_led_qemu
   ```

- Run the simulation:

   ```
   qemu-system-xtensa -nographic -machine esp32s3 -drive file=build/zephyr/zephyr_4mb.bin,if=mtd,format=raw
   ```

- Check the output on terminal, it should be:

   ```
   *** Booting Zephyr OS build v4.2.0-3707-g49157ea8fc71 ***
   Test cycle: 1
   LED state: OFF
   Test cycle: 2
   LED state: ON
   Test cycle: 3
   LED state: OFF
   ...
   ```

- Stop the QEMU simulation running on background:

   ```
   ps aux | grep qemu-system-xtensa
   kill <PID>
   ```

<br/>   

#### Installation of Espressif QEMU

For list of supported features in Espressif QEMU see the documentation on <a href="documentation/Tests_user_guide.md">https://github.com/espressif/esp-toolchain-docs/blob/main/qemu/README.md</a>.

1. Download Espressif QEMU installation package by wget tool from <a href="https://github.com/espressif/qemu/releases/">https://github.com/espressif/qemu/releases/</a>.

   ```
   cd ~/Downloads
   wget -O qemu-xtensa-softmmu-esp_develop_9.2.2_20250817-aarch64-linux-gnu.tar.xz https://github.com/espressif/qemu/releases/download/esp-develop-9.2.2-20250817/qemu-xtensa-softmmu-esp_develop_9.2.2_20250817-aarch64-linux-gnu.tar.xz
   ```

2. Extract the package to a directory of your choice.

   ```
   tar -xf qemu-xtensa-softmmu-esp_develop_9.2.2_20250817-aarch64-linux-gnu.tar.xz
   ```

3. Choose a directory of your choice to install Espressif QEMU.

   ```
   mkdir -p /home/<USER>/espressif-qemu/
   mv ~/Downloads/qemu/* /home/<USER>/espressif-qemu/
   ```

4. Export new environment variable for QEMU binaries.

   ```
   export PATH="/home/<USER>/espressif-qemu/bin:$PATH"
   ```

5. Then, build the application:

   ```
   cd customer-application
   west build -p always -b esp32s3_devkitc/esp32s3/procpu tests/manual_tests/esp32_toggle_led_qemu
   ```

6. Next, create a 4 MB binary from your compiled binary file and pad the end with zeros.

   ```
   dd if=/dev/zero of=build/zephyr/zephyr_4mb.bin bs=1M count=4
   dd if=build/zephyr/zephyr.bin of=build/zephyr/zephyr_4mb.bin conv=notrunc
   ```

7. Finally you can run the application in QEMU (see <strong>Usage</strong> section for more details).
