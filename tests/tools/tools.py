"""
Tools for testing

"""
import logging
import subprocess

logger = logging.getLogger(__name__)


def run_cmd(cmd):
        """Execute CLI command

        :param: str cmd: CLI commands to execute
        :return: str out: stdout output from Popen method
        :return: str err: stderr output from Popen method
        """
        logger.info(f"CLI command to execute: {cmd}.")
        try:
            p = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            )
            out, err = p.communicate()
            # Return output from command (byte string to string format)
            return out.decode("utf-8"), err.decode("utf-8")
        except Exception as e:
            logger.error(f"[Error] Failure during CLI command execution: {str(e)}.")