# 01 — First Flow: Writing and Running a Flow with Retries

**Design-only — gate 1 target. Not runtime-validated.** This pattern writes a
first Prefect flow: one task that sometimes fails, a flow that retries it,
and a local run that shows the retry in the UI. Retries are the reason to use
an orchestrator instead of a bare script.

## Prerequisites

- Prefect 3.9.0
- Python 3.11+
- A running Prefect server (fleet: Node-1 on :4300, Node-3 on :4200 per the
  seed — UI port to confirm at validation for the run host) or a local
  `prefect server start`
- Bash

## Files

- `flow.py` — a flow with a flaky task and retries
- `run.sh` — sets `PREFECT_API_URL` and runs the flow

## Steps

```bash
bash run.sh
```

## Expected output

- The flow run completes successfully after the task's transient failure.
- The run shows at least one task retry (the task fails on its first attempt
  by design — a run with zero retries means the flakiness did not trigger).
- The flow run appears in the Prefect UI under the flow's name.

## Failure behavior

- Task failing on every attempt: the flow run fails after retries are
  exhausted. Retries convert transient failures into successes; they do not
  fix deterministic failures. Check the task logs, not the retry count.
- `PREFECT_API_URL` pointing at a stopped server: the run fails at
  submission with a connection error. Start the server first
  (`prefect server start`); the flow does not run offline.
- Wrong Python environment (Prefect not installed in the active env): import
  error before any flow code runs. The script does not install Prefect — the
  environment is a prerequisite.

## Versions note / to confirm at validation

- Prefect 3.9.0 per the fleet seed. The `@flow` / `@task` decorator surface
  and `retries` / `retry_delay_seconds` arguments are the Prefect 3 stable
  API; any 3.9.0 deviation is a validation finding.
- The server UI port on the validation host (fleet seed says Node-1 :4300,
  Node-3 :4200).
