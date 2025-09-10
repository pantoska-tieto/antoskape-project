import argparse
import os

def define_args():
    """Define CLI arguments set
    Returns: parser object with arguments
    """
    parser = argparse.ArgumentParser(
        description=(
            "Script to get Zephyr tests scope"
        )
    )

    parser.add_argument(
        "--tests_scope",
        required=False,
        default=None,
        help="Tests range to be run",
    )
    parser.add_argument(
        "--tests_scenario",
        required=False,
        default=None,
        help="Specific test scenario to be run",
    )
    parser.add_argument(
        "--tests_robot",
        required=False,
        default=None,
        help="Robot tests to be run",
    )
    return parser

def get_test_paths(scope):
    """Define CLI arguments set

    :param: str scope: tag to point to test folder
    :return: str scope: string to use in filename
    :return: str target: real path to test folder
    """
    match scope:
        case "app/repo":
            scope = "repo"
            target = "tests/repo_tests"
        case "app/integration":
            scope = "integration"
            target = "tests/integration_tests"
        case "app/unit/dut":
            scope = "unit_dut"
            target = "tests/unit_tests/dut"
        case "app/unit/host":
            scope = "unit_host"
            target = "tests/unit_tests/host"
        case "app/robot":
            scope = "robot"
            target = "tests/robot_tests"
        case "zephyr_all_tests":
            scope = "zephyr"
            target = "../zephyr/tests"
    return scope, target


if __name__ == "__main__":
    parser = define_args()
    args = parser.parse_args()
    # Tests from specific folder are filtered (no scenario is specified)
    if args.tests_scope:
        scope, target = get_test_paths(args.tests_scope)
        # Get list of demanded tests
        test_list = [root for root, dirs, files in os.walk(target, topdown=True) for file in files if file == "prj.conf"]
        # Create demanded tests list in .txt file form
        with open(f"{scope}_tests.txt", "w") as f:
            for line in test_list:
                f.write(f"-T {line}\n")

    # Specific test scenario criteria exists
    if args.tests_scenario:
        scope, target = get_test_paths(args.tests_scenario)
        # Store option --testsuite-root to support test scenario filtering
        with open("scenario_tests.txt", "w") as f:
            f.write(f"--testsuite-root {target}\n")

    # Robot tests are triggered
    if args.tests_robot:
        scope, target = get_test_paths(args.tests_robot)
        # Robot tests
        with open("robot_tests.txt", "w") as f:
            f.write(f"--testlevelsplit {target}\n")
