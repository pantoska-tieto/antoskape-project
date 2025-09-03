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
    return parser

if __name__ == "__main__":
    parser = define_args()
    args = parser.parse_args()
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
    with open(os.path.join(f"{scope}_tests.txt"), "w") as f:
      for line in test_list:
        f.write(f"{line}\n")
