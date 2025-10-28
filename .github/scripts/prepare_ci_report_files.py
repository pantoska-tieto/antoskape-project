"""
GitHub workflow script:
Copy .xml files from all twister-out/ folders to central folder
test-summary/ for test-reporting GitHub action

"""
import os
import re
import shutil
regex = re.compile('twister-out.*')
for dir in os.listdir('.'):
    if regex.match(dir):
    print(f"Found: {dir}")
    if os.path.exists(os.path.join(dir, "twister_suite_report.xml")):
        shutil.copyfile(os.path.join(dir, "twister_suite_report.xml"), \
        os.path.join("test-summary", \
        f"twister_suite_report{dir.split('-out')[1]}.xml"))
    else:
        print(f"File twister_suite_report.xml not found in {dir}")