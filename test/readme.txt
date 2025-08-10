Run pytest
- for native_sim_64 for Raspberry Pi (arm64 architecture)
- without Twister build process

west twister --platform native_sim_64 -T test/shell
west twister -vv --platform esp32s3_devkitc/esp32s3/procpu -T test/shell

        --test-only -> not to build with Twister