import argparse
import subprocess
import os
from pathlib import Path


# Setup workspace environment
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
        help="Text filename with tests to be run",
    )
    parser.add_argument(
        "--platform",
        required=True,
        default=None,
        help="Platform to identify DUT",
    )
    parser.add_argument(
        "--test_hardware",
        required=False,
        default=None,
        help="Test target is hardware or simulation",
    )
    parser.add_argument(
        "--device_serial",
        required=False,
        default=None,
        help="Text file path with udev port rules",
    )
    parser.add_argument(
        "--tag",
        required=False,
        default=None,
        help="Test tags to filter tests",
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
        "--integration_tests",
        required=False,
        default=None,
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

def parse_serial_ports(file):
    """Parse udev symlinks file to get serial port(s)

    :param: str file: path to the file
    :return: list ports: list with symlinks for serial ports 
    """
    with open(file, "r") as f:
        lines = f.readlines()
        # Return empty list for simulated/emulated targes
        ports = ["/dev/" + p.split(",")[4].split("\"")[1] for p in lines] if \
            len(lines) > 0 else []
        return ports

if __name__ == "__main__":
    parser = define_args()
    args = parser.parse_args()
    # Extra arguments to be passed to west twister command
    arguments = ""

    if args.tag and (args.tag != "N/A" and args.tag != ""):
        arguments += f" --tag {args.tag} --force-tags"
    if args.scenario and (args.scenario != "N/A" and args.scenario != ""):
        arguments += f" --scenario {args.scenario}"

    if args.test_list and args.test_list != "":
        with open(args.test_list, "r") as file:
            tests = file.readlines()
            print(f"Selected tests to run:\n")
            [print(t.replace("\n", "")) for t in tests]

        if args.test_hardware and args.test_hardware == "Simulation_Emulation":
            # Only integration tests for all platforms - without a port
            if args.integration_tests and args.integration_tests == "yes":
                cmd_test = f"west twister -vv --platform {args.platform} --detailed-test-id \
                    --tag integration"
            # Tests on simulated/emulated targes - no port!
            elif "native_" in args.platform or "qemu" in args.platform:
                cmd_test = f"west twister -vv --platform {args.platform} --detailed-test-id"
                
            # Run all tests from the tests list file
            for line in tests:
                out, err, code = run_cmd(f'{cmd_test} {line.replace("\n", "")}{arguments}')
                print(out)
                # Show test summary reports review
                print(err)
                print(f"Return code for test command from subprocess.run: {code}")
        else:
            # Run tests for all devices connected to test bench
            for port in parse_serial_ports(args.device_serial):
                # Unit tests for local libs (no device needed)
                if args.target and "app/unit/host" in args.target:
                    cmd_test = "west twister -vv --detailed-test-id"
                # Robot tests
                # TODO! Add looping over ports for all devices
                elif args.target and "app/robot" in args.target:
                    cmd_test = "pabot"
                # Only integration tests on platfom(s) hardware
                elif args.integration_tests and args.integration_tests == "yes" and port and port != "":
                    cmd_test = f"west twister -vv --platform {args.platform} --detailed-test-id \
                        --device-testing --device-serial {port} --tag integration \
                        --flash-before"            
                # All other tests (device HW needed)
                else:
                    cmd_test = f"west twister -vv --platform {args.platform} --detailed-test-id \
                        --device-testing --device-serial {port} --flash-before"

                # Run all tests from the tests list file
                for line in tests:
                    out, err, code = run_cmd(f'{cmd_test} {line.replace("\n", "")}{arguments}')
                    print(out)
                    # Show test summary reports review
                    print(err)
                    print(f"Return code for test command from subprocess.run: {code}")
    else:
         raise Exception("No test list provided!")
