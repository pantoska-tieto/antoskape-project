import argparse
import logging
import subprocess
import os
from pathlib import Path

# Setup workspace environment
logger = logging.getLogger(__name__)
_p = Path(os.path.abspath(__file__)).parents[2]
os.chdir(os.path.join(_p))

def define_args():
    """Define CLI arguments set

    :return: obj parser: parser object with arguments
    """
    parser = argparse.ArgumentParser(
        description=(
            "Script to get Zephyr tests scope"
        )
    )

    # Path to txt-file with tests list
    parser.add_argument(
        "--test_list",
        required=False,
        default=None,
        help="List with tests to be run",
    )
    parser.add_argument(
        "--platform",
        required=True,
        default=None,
        help="Platform to identify DUT",
    )
    parser.add_argument(
        "--device_serial",
        required=False,
        default=None,
        help="Serial port for connecting DUT",
    )
    return parser

def run_cmd(cmd):
        """Execute CLI command

        :param: str cmd: CLI commands to execute
        :return: str out: stdout output from Popen method
        :return: str err: stderr output from Popen method
        :return: str returncode: return code from Popen method
        """
        logger.info(f"CLI command to execute: {cmd}.")
        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
            # Return output from command (byte string to string format)
            return res.stdout, res.stderr, res.returncode
        except Exception as e:
            logger.error(f"Failure during CLI command execution: {str(e)}.")

if __name__ == "__main__":
    parser = define_args()
    args = parser.parse_args()
    print(os.getcwd())
    if args.test_list and args.test_list != "":
        with open(args.test_list, "r") as file:
            tests = file.readlines()
            logger.info(f"Selected tests to run:\n")
            [logger.info(t.replace("\n", "")) for t in tests]
            for line in tests:
                run_cmd(f'west twister -vv --platform {args.platform} -j 1 --device-testing --device-serial {args.device_serial} --west-flash --flash-before -T {line.replace("\n", "")}')
