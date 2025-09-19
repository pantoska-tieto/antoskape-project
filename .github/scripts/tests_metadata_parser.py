import json
import time
from datetime import datetime
import os
from pathlib import Path
from copy import deepcopy
import pprint
import shutil


# Initialization
empty = {}
empty["count"] = 0
empty["passed"] = 0
empty["failed"] = 0
empty["blocked"] = 0
empty["details"] = {}
# Prepare metadata record skeleton
record = {}
record["timestamp"] = int(datetime.now().timestamp())
record["tag"] = datetime.now().strftime("%Y%m%d%H%M%S")
record["tests"] = deepcopy(empty)

metadata_file = "metadata.json"

def download(filename):
    """Download file from external repository

    :param: string filename: file name to download
    :return: None
    """
    # TODO!
    #  Implement when a repository is applied
    pass

def upload(filename):
    """Upload file to external repository

    :param: string filename: file name to upload
    :return: None
    """
    # TODO!
    #  Implement when a repository is applied
    pass

def parse_tests_results(test_list):
    """Parse twister-out/ folders to get test results

    :param: string test_list: list of all twister.json files from test run
    :return: dict suite_summ: test results in dict-format
    """
    suite_summ = {}
    for f in test_list:
        with open(f) as f:
            f_content =  json.load(f)
            for key, val in f_content.items():
                if key == "testsuites":
                    tc = val
                    for items in tc:
                        # Parse 'testsuites' dict part
                        tcases = []
                        tsuite = ""
                        for k, v in items.items():
                            if k == "path":
                                tsuite = v
                            if k == "testcases":
                                for x in v:
                                    tcase = x["identifier"]
                                    status = x["status"]
                                    tcases.append({"case": tcase, "status": status})
                                    suite_summ[tsuite] = tcases
                                    #print(suite_summ[tsuite])
    return suite_summ

def download_metadata():
    """Download existing metadata file from repository

    :return: None
    """
    metadata = {}
    # TODO: download metadata.json from repository
    # def download()
    # debugger - remove!
    global metadata_file

    if Path(metadata_file).is_file():
        # Make backup for debugging if needed
        shutil.copyfile(metadata_file, metadata_file + ".bckp")
        with open(metadata_file) as fp:
            metadata = json.load(fp)
            fp.close()
        return metadata
    else:
        return metadata

def upload_metadata(data):
    """Upload new metadata file torepository

    :return: None
    """
    # TODO: upload metadata.json to repository
    # def uplload()
    # debugger - remove!
    global metadata_file
    if "invalid" in data.keys():
        print("[ERROR] Metadata file is invalid. Skip uploading to prevent loss of data!")
    else:
        with open(metadata_file, 'w') as fp:
            fp.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
        # TODO!
        #  upload(metadata_file)

if __name__ == "__main__":
    # Setup workspace folder
    _p = Path(os.path.abspath(__file__)).parents[2]
    os.chdir(os.path.join(_p))

    # Read metadata.json from artifactory
    meta_file = download_metadata()
    if "runs" in meta_file.keys() and len(meta_file["runs"]) > 0:
        last_md = meta_file["runs"][0]
    else:
        # Empty new tests record
        last_md = record

    # Get twister-out log-data
    test_list = [f"{root}/{file}" for root, dirs, files in os.walk(os.getcwd(), topdown=True) 
                for file in files if file == "twister.json"]
    # Parse latest test results from GitHub workflow
    new_stats = parse_tests_results(test_list)
    # Complete latest test results dict
    record["tests"]["details"] = new_stats
    # Test cases states
    record["tests"]["count"] = sum([len(i) for i in record["tests"]["details"].values()])
    details = [i for i in record["tests"]["details"].values()]
    passed_cases = len([dic["status"] for item in details for dic in item if dic["status"] == "passed"])
    failed_cases = len([dic["status"] for item in details for dic in item if dic["status"] == "failed"])
    blocked_cases = len([dic["status"] for item in details for dic in item if dic["status"] == "blocked"])
    record["tests"]["passed"] = passed_cases
    record["tests"]["failed"] = failed_cases
    record["tests"]["blocked"] = blocked_cases

    # Join existing and new metadata into one dict
    if not 'runs' in meta_file.keys():
        meta_file['runs'] = []
    meta_file['runs'] = [record] + meta_file['runs']

    # Store final metadata to artifactory
    upload_metadata(meta_file)
