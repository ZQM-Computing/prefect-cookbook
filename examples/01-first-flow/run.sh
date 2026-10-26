#!/usr/bin/env bash
# Run the first flow against a Prefect server.
# Design-only example: set PREFECT_API_URL for your server, then compare
# with README.md expected output.
set -euo pipefail

export PREFECT_API_URL="${PREFECT_API_URL:-http://localhost:4300/api}"
rm -f attempt.txt
python3 flow.py
echo "attempts recorded: $(cat attempt.txt)"
