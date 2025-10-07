cmake_minimum_required(VERSION 3.20.0)
set(DTC_OVERLAY_FILE "boards/native_sim.overlay")
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(mock_adc_sample)

target_sources(app PRIVATE src/main.c)
target_sources(app PRIVATE drivers/adc/mock_adc.c)
