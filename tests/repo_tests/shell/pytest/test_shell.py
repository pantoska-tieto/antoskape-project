# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0

import logging
import timeit
import pytest

from twister_harness import Shell


logger = logging.getLogger(__name__)

def test_shell_print_help(shell: Shell):
    # Benchmarking start
    start_time = timeit.default_timer()
    logger.info(f"Def test_shell_print_help() - benchmark started")

    print("Testcase: check a commands are available in uart prompt:")
    logger.info('send "help" command')
    lines = shell.exec_command('help')
    assert 'Available commands:' in lines, 'expected response not found'
    logger.info('Shell response is valid')

    # Benchmarking end
    end_time = timeit.default_timer()
    execution_time = end_time - start_time
    logger.info(f"Def test_shell_print_help() executed in: {execution_time}sec")
    with open("pytest-benchmark.txt", "a") as f:
        f.write("### Benchmark: test_shell_print_help() ### \n")
        f.write(f"Execution time: {execution_time}sec \n")
        f.close()

def test_shell_print_version(shell: Shell):
    # Benchmarking start
    start_time = timeit.default_timer()
    logger.info(f"Def test_shell_print_version() - benchmark started")

    print("Testcase: check Zephyr kernel version is available:")
    logger.info('send "kernel version" command')
    lines = shell.exec_command('kernel version')
    assert any(['Zephyr version' in line for line in lines]), 'expected response not found'
    logger.info('Shell response is valid')

    # Benchmarking end
    end_time = timeit.default_timer()
    execution_time = end_time - start_time
    logger.info(f"Def test_shell_print_version() executed in: {execution_time}sec")
    with open("pytest-benchmark.txt", "a") as f:
        f.write("### Benchmark: test_shell_print_version() ### \n")
        f.write(f"Execution time: {execution_time}sec \n")
        f.close()
