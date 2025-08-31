"""
Pytest fixture file for
- getting GitHub secrets variables to be applied in test cases.

"""
import pytest
import json


@pytest.fixture
def get_secrets():
    with open('../vars.json', 'r') as f:
        return json.load(f)