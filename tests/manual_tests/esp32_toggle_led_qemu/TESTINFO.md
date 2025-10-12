# Test suite information

### Test name
Toggle LED test for ESP32 boards with QEMU simulation.

### Test path
tests/manual_tests/esp32_toggle_led_qemu

### Type
- Manual test

### Description
This test script is designed to verify the functionality of toggling an LED on an ESP32 board using QEMU simulation. No target board is required for this test. The test script will run on Host machine with Espressif QEMU installed.

### Preconditions
- No board connected (simulation test).
- Espressif QEMU package installed on Host.
- See [README.md](README.md) file for more details.

### Test steps
1. Install Espressif QEMU package on Host.
2. Build the sample binaries into the output folder `build/`.
3. Run the simulation:
```
   qemu-system-xtensa -nographic -machine esp32s3 -drive file=build/zephyr/zephyr_4mb.bin,if=mtd,format=raw
   ```

### Expected results
10 cycles with `LED state: OFF` and `LED state: ON` output in UART terminal.

### Notes
Not suitable for automated test due to the need for manual installation of Espressif QEMU package on Host computer.