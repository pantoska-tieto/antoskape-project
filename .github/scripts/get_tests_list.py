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
    return parser

if __name__ == "__main__":
    parser = define_args()
    args = parser.parse_args()
    # Tests from specific folder are filtered (no scenario is specified)
    if args.tests_scope:
        match args.tests_scope:
            case "app/repo":
                scope = "repo"
                target = "tests/repo_tests"
            case "app/integration":
                scope = "integration"
                target = "tests/integration_tests"
            case "app/unit":
                scope = "unit"
                target = "tests/unit_tests"
            case "app(all tests)":
                scope = "application"
                target = "tests"
            case "zephyr(all tests)":
                scope = "zephyr"
                target = "../zephyr/tests"

        # Get list of demanded tests
        test_list = [root for root, dirs, files in os.walk(target, topdown=True) for file in files if file == "prj.conf"]
        # Create demanded tests list in .txt file form
        with open(f"{scope}_tests.txt", "w") as f:
            for line in test_list:
                f.write(f"-T {line}\n")

    # Specific test scenario is specified
    if args.tests_scenario:
        # Store option --testsuite-root to support test scenario filtering
        with open("scenario_tests.txt", "w") as f:
            f.write(f"--testsuite-root {args.tests_scenario}\n")


    
