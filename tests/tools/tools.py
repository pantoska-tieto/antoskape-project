"""
Tools for testing

"""
import pytest
import logging
import subprocess
import re

logger = logging.getLogger(__name__)


def run_cmd(cmd):
        """Execute CLI command

        :param: str cmd: CLI commands to execute
        :return: str out: stdout output from Popen method
        :return: str err: stderr output from Popen method
        """
        logger.info(f"CLI command to execute: {cmd}.")
        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
            # Return output from command (byte string to string format)
            return res.stdout, res.stderr, res.returncode
        except Exception as e:
            logger.error(f"[Error] Failure during CLI command execution: {str(e)}.")

def search_pattern(data, regex):
    for line in data.split("\n"):
        _r = re.match(regex, line)
        if _r:
            return True
            break
    return False 