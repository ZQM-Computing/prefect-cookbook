# 04 — dlt Flow: A Prefect-Scheduled dlt Pipeline

**Design-only — gate 1 target. Not runtime-validated.** This pattern wraps a
dlt pipeline in a Prefect flow: extract synthetic records, load them to a
destination, and report the row count as the flow's result. It mirrors the
fleet's Prefect-scheduled dlt flow shape without copying its data.

## Prerequisites

- Prefect 3.9.0
- Python 3.11
- Dependencies from the repository's bounded `requirements-test.txt`
- Local filesystem access for the DuckDB database file
- This example implements DuckDB only; Postgres is a separate destination pattern, not a configured option here

## Files

- `dlt_flow.py` — Prefect flow wrapping a dlt pipeline over synthetic data

## Steps

```bash
python -m pip install -r requirements-test.txt
python examples/04-dlt-flow/dlt_flow.py
```

Run the repeatability and destination assertions with:

```bash
python -m pytest -q
```

## Expected output

- The pipeline loads the synthetic records (20 rows in the example source)
  into the destination table.
- The flow queries the actual destination table and returns the observed row count (20); a mismatch raises an error.
- The pipeline explicitly uses `write_disposition="replace"`.
- The automated contract test runs the flow twice and independently queries the local DuckDB file to assert 20 rows, 20 distinct IDs, and the expected ID range. This guards against a silent doubling on repeat runs.

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
- Prefect is bounded to the fleet-seed version `3.9.0`; dlt is constrained to the current major line (`>=1.0,<2`) in `requirements-test.txt`.
- CI prints the exact resolved Prefect, dlt, and DuckDB versions for each run; review that log before treating a specific combination as validated.
- The test uses a local DuckDB file and explicit replace disposition. It does not validate a Postgres destination or production worker deployment.
- Status remains design-only until the exact-head runtime test workflow passes.
