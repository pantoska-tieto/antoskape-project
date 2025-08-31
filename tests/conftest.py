"""
Pytest fixture file for
- getting GitHub secrets variables to be applied in test cases.

"""
import pytest
import json
import os


@pytest.fixture(scope="module")
def get_secrets(request):
    # Root path - pytest.ini location
    with open(os.path.join(request.config.rootpath, "vars.json"), "r") as f:
        return json.load(f)