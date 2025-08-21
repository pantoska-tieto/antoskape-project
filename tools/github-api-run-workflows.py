import requests
import json

# Global params
url = "https://api.github.com/repos/pantoska-tieto/antoskape-project/actions/workflows/build.yml/dispatches"

def run_workflows(runner_label=None, board_target=None, device_serial=None, tests_target=None):
    """Run remote Github workflows action
    """
    payload = json.dumps({
        "ref":"main",
        "inputs": {
            "runner_label": runner_label,
            "board_target": board_target,
            "device_serial": device_serial,
            "tests_target": tests_target
       }
    })
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer <token>"
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return response
    except requests.exceptions.RequestException as e:
        print(e)

if __name__ == "__main__":
    # Demanded workflow_dispatch inputs (defaults are used when not demanded)
    runner_label = None
    board_target = None
    device_serial = None
    tests_target = "unit"
    # Run workflow_dispatch
    resp = run_workflows(runner_label, board_target, device_serial, tests_target)
    print(resp.text)