# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

# Overlay pin numbering in esp32s3_devkitc
set(DTC_OVERLAY_FILE "boards/esp32s3_devkitc.overlay")
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(gpio_manipulation)

target_sources(app PRIVATE
    src/main.c
    )
