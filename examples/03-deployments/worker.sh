#!/usr/bin/env bash
# Start a process-pool worker against the Prefect server.
# Design-only example: set PREFECT_API_URL for your server, and use the
# pool name from prefect.yaml. Worker logs go to stderr by design —
# check the worker's stderr, not just its stdout, for execution logs.
set -euo pipefail

export PREFECT_API_URL="${PREFECT_API_URL:-http://localhost:4300/api}"
prefect worker start --pool default-pool
