import yaml
import json
import os
from pathlib import Path


def parse_yaml(tests):
    """Parse YAML files and store them to json

    :param: list tests: list of paths to tests yaml configs
    :return: dict summary: tests config data in dict-format
    """
    summary = {}
    for t in tests:
        with open(t, 'r') as f:
            result =  yaml.safe_load(f)
            new_result = {
                t : result
            }
            summary = summary | new_result
    return summary

def get_tests_list(target):
    """Read filesystem to get all tests from target folder

    :param: string target: path to target folder
    :return: list summary: all tests paths in list-format
    """
    test_list = [f"{root}\\{file}" for root, dirs, files in os.walk(target, topdown=True) for file in files if file == "testcase.yaml"]
    print(test_list)
    return test_list


if __name__ == "__main__":
    # Setup workspace folder
    _p = Path(os.path.abspath(__file__)).parents[2]
    os.chdir(os.path.join(_p))
    # Get list of all tests
    tests = get_tests_list("tests")
    # Parse testcase.yaml files
    tests_list = parse_yaml(tests)
    try:
        with open("tests_list.json", "w") as f:
            json.dump(tests_list, f, indent=4)
            print("tests_list.json with all available tests was created")
    except Exception as e:
        print(f"Error when saving list of all available tests:\n {e}")
