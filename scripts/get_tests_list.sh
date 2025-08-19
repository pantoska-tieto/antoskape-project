#!/usr/bin/env bash
set -euo pipefail

# List your Twister test directories here (relative to repo root)
if [[ $# -lt 1 ]]; then
  echo "Usage: $0 tests"
  exit 2
fi
tests="$1"
echo "Script received list of tests to run: ${tests}"

# Configuration via env (override when calling the script)
platform="${PLATFORM:-esp32s3_devkitc/esp32s3/procpu}"
twister_args="${TWISTER_ARGS:--vv}"    # e.g. "--timeout 180 --enable-slow"                   # e.g. "8"

status=0
for t in "${tests[@]}"; do
  echo "Running: west twister ${twister_args} --platform ${platform} -T ${t}"
  if ! west twister ${twister_args} --platform "${platform}" -T "${t}"; then
    echo "FAILED: ${t}"
    status=1
  fi
done

exit "${status}"