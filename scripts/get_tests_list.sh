#!/usr/bin/env bash
set -euo pipefail

# Usage examples:
#  1) scripts/get_tests_list.sh test/basic samples/basic/blinky
#  2) scripts/get_tests_list.sh "test/basic samples/basic/blinky"
#  3) scripts/get_tests_list.sh tests.txt   # file with one test per line

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <test1> [<test2> ...] | $0 \"test1 test2 ...\" | $0 <file_with_tests>"
  exit 2
fi

# Build array of tests from args, a single string, or from a file
declare -a tests
if [[ $# -eq 1 && -f "$1" ]]; then
  # Read tests from file (one per line)
  mapfile -t tests < "$1"
elif [[ $# -eq 1 ]]; then
  # Split a single string by whitespace or commas into an array
  # Remove empty entries
  readarray -t tests < <(printf '%s\n' "$1" | tr ' \t,' '\n' | sed '/^$/d')
else
  # Treat each argument as one test path
  tests=("$@")
fi

# Show what we will run
echo "Script received list of tests to run:"
for t in "${tests[@]}"; do
  [[ -n "$t" ]] && echo "  - $t"
done

# Configuration via env (override when calling the script)
platform="${PLATFORM:-esp32s3_devkitc/esp32s3/procpu}"
twister_args="${TWISTER_ARGS:--vv}"          # e.g. "--timeout 180 --enable-slow"
jobs="${JOBS:-auto}"                         # e.g. "8"

status=0
for t in "${tests[@]}"; do
  # Skip empty lines if any
  [[ -z "$t" ]] && continue

  echo "Running: west twister ${twister_args} --platform ${platform} -j ${jobs} -T ${t}"
  if ! west twister ${twister_args} --platform "${platform}" -j "${jobs}" -T "${t}"; then
    echo "FAILED: ${t}"
    status=1
  fi
  echo
done

exit "${status}"
