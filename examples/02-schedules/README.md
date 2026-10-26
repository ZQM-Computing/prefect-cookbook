# 02 — Schedules: Scheduled Flows and Cron-Style Triggers

**Design-only — gate 1 target. Not runtime-validated.** This pattern deploys
a flow on a cron schedule: a small daily ingestion flow that runs on its own,
with the schedule visible in the UI and the next run time predictable.

## Prerequisites

- Prefect 3.9.0
- Python 3.11+
- A running Prefect server and a work pool (pattern 03 covers pools; a
  process pool is enough for this pattern)
- Bash

## Files

- `deploy.py` — deploys the flow with a cron schedule

## Steps

```bash
python3 deploy.py
```

## Expected output

- A deployment named `daily-ingest` exists for the flow, visible in the UI.
- The deployment's schedule shows the cron expression from `deploy.py`
  (daily, 06:00 UTC in the example) and a next-run time consistent with it.
- Triggering a manual run from the deployment succeeds (proving the schedule
  is not the only thing wired up — the deployment itself works).

## Failure behavior

- Cron expression invalid: deployment creation fails with a schedule-parse
  error. Fix the expression; do not deploy unscheduled and "remember" to run
  it.
- No worker for the pool: scheduled runs queue in Late/Scheduled state and
  never execute. A schedule without a worker is a wish, not a run — check the
  worker first (pattern 03).
- Timezone confusion: cron runs in the schedule's timezone, not the author's.
  The example pins UTC explicitly; a run at the wrong hour is a timezone bug,
  not a Prefect bug.

## Versions note / to confirm at validation

- The Prefect 3.9.0 deployment API spelling used in `deploy.py`
  (`flow.deploy` vs `flow.serve` vs YAML) — Prefect 3 moved deployment
  authoring between releases, and the exact 3.9.0 spelling is the open item.
- The cron schedule object name and timezone argument spelling on 3.9.0.
- The work-pool name on the validation host (the example uses `default-pool`
  as a placeholder).
