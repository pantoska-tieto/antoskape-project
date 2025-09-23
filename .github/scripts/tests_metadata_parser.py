import json
import time
from datetime import datetime
import os
from pathlib import Path
from copy import deepcopy
import subprocess
import shutil
import argparse
import requests
from requests.auth import HTTPBasicAuth
import pytz


# Initialization
empty = {}
empty["count"] = 0
empty["passed"] = 0
empty["failed"] = 0
empty["blocked"] = 0
empty["details"] = {}
# Prepare metadata record skeleton
bratislava_tz = pytz.timezone("Europe/Bratislava")
record = {}
record["timestamp"] = int(datetime.now(bratislava_tz).timestamp())
record["tag"] = datetime.now(bratislava_tz).strftime("%Y%m%d%H%M%S")
record["tests"] = deepcopy(empty)

metadata_file = "metadata.json"
artifactory_url = "http://tieto-artifactory.com:8082/artifactory/generic-local/"

def define_args():
    """Define CLI arguments set

    :return: obj parser: parser object with arguments
    """
    parser = argparse.ArgumentParser(
        description=(
            "Script to get cli arguments"
        )
    )

    parser.add_argument(
        "--artifactory_user",
        required=True,
        default=None,
        help="Artifactory username",
    )
    parser.add_argument(
        "--artifactory_pwd",
        required=True,
        default=None,
        help="Artifactory passwd",
    )
    return parser

def check_host():
    """Check that hostname is reachable

    :return: str status_code: return code from get command
    """
    global artifactory_url
    parser = define_args()
    args = parser.parse_args()   
    username = args.artifactory_user
    password = args.artifactory_pwd
    
    try:
        r = requests.get(artifactory_url, auth=HTTPBasicAuth(username, password), timeout=15)
        print(f"Return code from HOST: {r.status_code}")
        return r.status_code        
    except Exception as e:
        print(f"Error in checking Artifactory host occurred: {e}")

def run_cmd(cmd):
    """Execute CLI command

    :param: str cmd: CLI commands to execute
    :return: str out: stdout output from Popen method
    :return: str err: stderr output from Popen method
    :return: str returncode: return code from Popen method
    """
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        # Return output from command (byte string to string format)
        return res.stdout, res.stderr, res.returncode
    except Exception as e:
        print(f"[ERROR] Failure during CLI command execution: {str(e)}.")

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
                                tsuite = v.replace("../customer-application/", "")
                            if k == "testcases":
                                for x in v:
                                    tcase = x["identifier"]
                                    status = x["status"]
                                    tcases.append({"case": tcase, "status": status})
                                    suite_summ[tsuite] = tcases
                                    #print(suite_summ[tsuite])
    return suite_summ

def download_metadata():
    """Download existing metadata file from artifactory repository

    :return: dict metadata: metadata file in JSON format
    """
    metadata = {}
    global artifactory_url
    global metadata_file
    parser = define_args()
    args = parser.parse_args()

    try:
        if (check_host() != 200):
            print(f"Artifactory {artifactory_url} is not reachable. Skip downloading metadata.json file!")
            return metadata
        out, err, code = run_cmd(f"curl -u {args.artifactory_user}:{args.artifactory_pwd} -O '{artifactory_url}{metadata_file}' -o {metadata_file}")
        print(f"Download CURL out: {out}")
        print(f"Download CURL err: {err}")
        print(f"Download CURL code: {code}")
    except Exception as e:
        print(f"[ERROR] Download metadata file from artifactory failed: {e}")

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
    """Upload new metadata file to artifactory repository

    :return: None
    """
    global artifactory_url
    global metadata_file
    parser = define_args()
    args = parser.parse_args()

    if "invalid" in data.keys():
        print("[ERROR] Metadata file is invalid. Skip uploading to prevent loss of data!")
    else:
        with open(metadata_file, 'w') as fp:
            fp.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
        try:
            if (check_host() != 200):
                print(f"Artifactory {artifactory_url} is not reachable. Skip uploading metadata.json file!")
                return
            out, err, code = run_cmd(f"curl -u {args.artifactory_user}:{args.artifactory_pwd} -X PUT '{artifactory_url}{metadata_file}' -T {metadata_file}")
            print(f"Upload CURL out: {out}")
            print(f"Upload CURL err: {err}")
            print(f"Upload CURL code: {code}")
        except Exception as e:
            print(f"[ERROR] Upload metadata file to artifactory failed: {e}")

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
