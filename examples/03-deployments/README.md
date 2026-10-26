# 03 — Deployments: Flows as Services with Work Pools

**Design-only — gate 1 target. Not runtime-validated.** This pattern runs a
flow as a service: a process work pool, a worker, and a deployment whose
entrypoint is a module path. The fleet lesson baked in here: Prefect 3.9
local process-pool deploys need the real `EntrypointType.MODULE_PATH` enum —
the string form and `push=False` shortcuts fail.

## Prerequisites

- Prefect 3.9.0
- Python 3.11+
- A running Prefect server
- Bash

## Files

- `prefect.yaml` — deployment sketch (pool, entrypoint, work-queue notes)
- `worker.sh` — starts a process-pool worker

## Steps

```bash
bash worker.sh
# In a second shell, create/run the deployment per prefect.yaml.
```

## Expected output

- The worker registers against the process pool and shows as Online in the UI.
- A flow run submitted to the deployment executes on the worker (logs appear
  under the worker, not under the submitting shell).
- Stopping the worker leaves queued runs in Scheduled state — proof the
  deployment is worker-backed, not shell-backed.

## Failure behavior

- Entrypoint spelled as a string instead of the `MODULE_PATH` enum: the
  deployment fails at creation/run with an entrypoint-type error. This is the
  known Prefect 3.9 trap — use the enum (see `prefect.yaml` notes).
- Worker pointed at the wrong pool: runs queue forever in Scheduled. Match
  the pool name in `prefect.yaml` and `worker.sh` exactly.
- Worker started in the wrong Python environment (Prefect or the flow's
  imports missing): the worker registers but runs fail at import. The worker
  environment must be the flow's environment.

## Versions note / to confirm at validation

- The exact `prefect.yaml` schema and `prefect deploy` CLI spelling on
  Prefect 3.9.0 (the file below is a sketch with the fleet-verified
  MODULE_PATH note, not a verbatim 3.9.0 file — the verbatim file is a
  validation output).
- The `PREFECT_API_URL` the worker needs on the validation host
  (fleet: Node-1 :4300, Node-3 :4200 per the seed).
