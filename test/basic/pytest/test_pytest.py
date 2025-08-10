import pytest

# Utility def
def func(x):
    print("Function for calculating is invoked...")
    return x + 1

# Sample test
def test_answer():
    print("Hello world test is started...")
    assert func(4) == 5, "Test failed because 3 + 1 is not 5"
