"""
GitHub workflow script:
Create GITHUB_OUTPUT variable with file-names of all tests to run
with west twister

"""
import os
import re


regex = re.compile('.*_tests.txt')
for dir in os.listdir('.'):
    if regex.match(dir):
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f'test_list={os.path.join(dir)}\n')
