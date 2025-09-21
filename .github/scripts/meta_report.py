from jinja2 import Environment, FileSystemLoader
import json
from datetime import datetime
from pathlib import Path
import os
import argparse


# Setup workspace folder
_p = Path(os.path.abspath(__file__)).parents[2]
os.chdir(os.path.join(_p))

def define_args():
    """Define CLI arguments set
    Returns: parser object with arguments
    """
    parser = argparse.ArgumentParser(
        description=(
            "Script to get Zephyr test run details"
        )
    )

    parser.add_argument(
        "--run_id",
        required=False,
        default=None,
        help="GitHub workflow run ID",
    )
    return parser

if __name__ == "__main__":
    parser = define_args()
    args = parser.parse_args()
    # Metadata file with tests results
    with open("metadata.json", 'r') as f:
        metadata = json.load(f)
        f.close()

    # Prepare data for the Jinja template
    report_rows = []
    run = metadata["runs"][0]
    for test_file, cases in run["tests"]["details"].items():
        for case in cases:
            report_rows.append({
                "tag": run["tag"],
                "test_file": test_file,
                "case": case["case"],
                "status": case["status"]
            })

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('.github/scripts/report_template.html')

    # Extract summary stats from the test run
    summary = metadata["runs"][0]["tests"]
    timestamp = metadata["runs"][0]["timestamp"]
    run_time = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

    # Render the report HTML file
    output = template.render(report_rows=report_rows, 
                             summary=summary,
                             run_time=run_time,
                             run_id=args.run_id)

    # Save report file
    with open("twister_test_report.html", "w", encoding="utf-8") as f:
        f.write(output)
        print("HTML test report saved to twister_test_report.html")