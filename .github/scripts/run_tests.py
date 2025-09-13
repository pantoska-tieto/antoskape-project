import argparse
import subprocess
import os
from pathlib import Path

# Setup workspace environment
_p = Path(os.path.abspath(__file__)).parents[2]
os.chdir(os.path.join(_p))

def str2bool(val):
    """Parse Boolean value from Github Actions input

    :return: bool: True if no integration tests are run
    """
    return str(val).lower() not in ("yes", "true", "t", "1")

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
        help="List in text file with tests to be run",
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
    parser.add_argument(
        "--tag",
        required=False,
        default=None,
        help="Test tags to filter tests",
    )
    parser.add_argument(
        "--pytest_args",
        required=False,
        default=None,
        help="Arguments to the pytest subprocess",
    )
    parser.add_argument(
        "--scenario",
        required=False,
        default=None,
        help="Test suite scenario to run",
    )
    parser.add_argument(
        "--target",
        required=False,
        default=None,
        help="Path to text file with tests list",
    )
    parser.add_argument(
        "--no_integration_tests",
        required=False,
        type=str2bool,
        default=True,
        help="Condition to run integration tests only",
    )
    return parser

def run_cmd(cmd):
    """Execute CLI command

    :param: str cmd: CLI commands to execute
    :return: str out: stdout output from Popen method
    :return: str err: stderr output from Popen method
    :return: str returncode: return code from Popen method
    """
    print(f"CLI command to execute: {cmd}.")
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        # Return output from command (byte string to string format)
        return res.stdout, res.stderr, res.returncode
    except Exception as e:
        print(f"[ERROR] Failure during CLI command execution: {str(e)}.")

if __name__ == "__main__":
    parser = define_args()
    args = parser.parse_args()
    # Extra arguments to be passed to west twister command
    arguments = ""
    if args.tag and (args.tag != "N/A" and args.tag != ""):
        arguments += f" --tag {args.tag} --force-tags"
    if args.pytest_args and (args.pytest_args != "N/A" and args.pytest_args != ""):
        arguments += f" --pytest-args {args.pytest_args}"
    if args.scenario and (args.scenario != "N/A" and args.scenario != ""):
        arguments += f" --scenario {args.scenario}"

    if args.test_list and args.test_list != "":
        with open(args.test_list, "r") as file:
            tests = file.readlines()
            print(f"Selected tests to run:\n")
            [print(t.replace("\n", "")) for t in tests]

        # Unit tests for local libs (no device needed)
        if args.target and "app/unit/host" in args.target:
            cmd_test = "west twister -vv"
        # Robot tests
        elif args.target and "app/robot" in args.target:
            cmd_test = "pabot"
        # Only integration tests for specific platfom(s)
        elif args.no_integration_tests and args.no_integration_tests is False and args.platform and args.platform != "":
            cmd_test = f"west twister -vv --platform {args.platform} --device-testing --device-serial --tag integration --west-flash --flash-before"
        # Only integration tests for all platforms
        elif args.no_integration_tests and args.no_integration_tests is False and args.platform and args.platform == "":
            cmd_test = "west twister -vv --device-testing --device-serial --tag integration --west-flash --flash-before"
        # All other tests (device HW needed)
        else:
            cmd_test = f"west twister -vv --platform {args.platform} --device-testing --device-serial {args.device_serial} --west-flash --flash-before"

        for line in tests:
            out, err, code = run_cmd(f'{cmd_test} {line.replace("\n", "")}{arguments}')
            print(out)
            # Show test summary reports review
            print(err)
            print(f"Return code for test command from subprocess.run: {code}")
    else:
         raise Exception("No test list provided!")
