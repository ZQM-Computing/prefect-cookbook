# 04 — dlt Flow: A Prefect-Scheduled dlt Pipeline

**Design-only — gate 1 target. Not runtime-validated.** This pattern wraps a
dlt pipeline in a Prefect flow: extract synthetic records, load them to a
destination, and report the row count as the flow's result. It mirrors the
fleet's Prefect-scheduled dlt flow shape without copying its data.

## Prerequisites

- Prefect 3.9.0
- Python 3.11+, dlt installed in the flow's environment
- A destination: DuckDB (local file) or Postgres (see dlt-cookbook)
- Bash

## Files

- `dlt_flow.py` — Prefect flow wrapping a dlt pipeline over synthetic data

## Steps

```bash
python3 dlt_flow.py
```

## Expected output

- The pipeline loads the synthetic records (20 rows in the example source)
  into the destination table.
- The flow result reports the loaded row count (20), matching the source
  count — the count check is the pattern's correctness gate.
- A second run replaces or appends per the pipeline's write disposition
  (stated in the file), and the count check accounts for it — a count that
  silently doubles across runs is a disposition bug, not a success.

## Failure behavior

- Destination unreachable: the pipeline fails at load with a connection
  error; the flow run fails. Fix the destination, not the flow.
- Schema mismatch (destination table exists with different columns): dlt
  fails or evolves the schema per its settings — the expected behavior must
  be stated before the run (the example uses a fresh table each run to avoid
  this).
- dlt not installed in the worker's environment: import error at flow run
  time, even if the submitting shell has dlt. The worker environment is the
  flow environment (pattern 03).

## Versions note / fleet grounding / to confirm at validation

- Fleet evidence (shape only, not expected output): the fleet runs a
  Prefect-scheduled dlt flow (Node-3, 59 rows in its demo) and a standalone
  `dlt_demo` (Node-1, 191 rows kept). This pattern's 20-row synthetic source
  is its own example; its count gate is 20, not 59 or 191.
- Prefect 3.9.0 per the fleet seed; dlt version to confirm at validation
  (the fleet's dlt version is not pinned in the seed — record it at
  validation, do not guess it here).
- The destination used at validation (DuckDB file vs Postgres) and the
  write disposition spelling.
