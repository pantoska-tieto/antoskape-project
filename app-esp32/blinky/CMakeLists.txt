# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

# Check if the board is native_sim (reject then because infinite loop is used in sample)
if((${BOARD} STREQUAL "native_sim/native/64"))
    message(FATAL_ERROR "This sample does not support native_sim boards. Build is skipped...")
endif()

# Path to custom overlay file 
set(DTC_OVERLAY_FILE "boards/esp32s3_devkitc.overlay")

find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(blinky)

target_sources(app PRIVATE src/main.c)
