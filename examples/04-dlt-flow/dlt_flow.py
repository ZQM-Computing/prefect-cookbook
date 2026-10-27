"""Prefect flow wrapping a dlt pipeline over deterministic synthetic data.

The local DuckDB destination is replaced on each run. The flow returns a row
count queried from the destination, not an expected count hard-coded in code.
"""
from __future__ import annotations

from collections.abc import Iterator

import dlt
from prefect import flow, task

EXPECTED_ROWS = 20
TABLE_NAME = "records"


def synthetic_source() -> Iterator[dict[str, int | str]]:
    """Yield a deterministic, credential-free source dataset."""
    for i in range(EXPECTED_ROWS):
        yield {"id": i, "value": i * 10, "label": f"synthetic-{i}"}


@task
def run_pipeline() -> int:
    """Load the fixture with replace semantics and verify the destination count."""
    pipeline = dlt.pipeline(
        pipeline_name="synthetic_demo",
        destination="duckdb",
        dataset_name="demo",
    )
    # A failed load must raise rather than produce a successful-looking count.
    pipeline.run(
        synthetic_source(),
        table_name=TABLE_NAME,
        write_disposition="replace",
    )

    # Query through dlt's destination client so the table/schema qualification
    # follows the configured destination rather than assuming a raw DB path.
    with pipeline.sql_client() as client:
        qualified_table = client.make_qualified_table_name(TABLE_NAME)
        rows = client.execute_sql(f"SELECT COUNT(*) FROM {qualified_table}")

    if not rows or not rows[0]:
        raise RuntimeError("Destination row-count query returned no result")

    actual_count = int(rows[0][0])
    expected_count = sum(1 for _ in synthetic_source())
    if actual_count != expected_count:
        raise RuntimeError(
            f"Destination row-count mismatch: expected {expected_count}, "
            f"found {actual_count}"
        )
    return actual_count


@flow(name="dlt-demo-flow")
def dlt_demo_flow() -> int:
    """Run the local synthetic dlt pipeline and return its verified row count."""
    return run_pipeline()


if __name__ == "__main__":
    print(f"loaded rows: {dlt_demo_flow()}")
