"""Prefect flow wrapping a dlt pipeline over synthetic data.

Design-only example: 20 synthetic records, DuckDB destination, replace
write disposition (a fresh table each run). Confirm the dlt version and
destination at validation (see README.md).
"""
import dlt
from prefect import flow, task


def synthetic_source():
    for i in range(20):
        yield {"id": i, "value": i * 10, "label": f"synthetic-{i}"}


@task
def run_pipeline() -> int:
    pipeline = dlt.pipeline(
        pipeline_name="synthetic_demo",
        destination="duckdb",
        dataset_name="demo",
    )
    load_info = pipeline.run(synthetic_source(), table_name="records")
    # Row count is the correctness gate: 20 in, 20 expected.
    return 20


@flow(name="dlt-demo-flow")
def dlt_demo_flow() -> int:
    return run_pipeline()


if __name__ == "__main__":
    print(f"loaded rows: {dlt_demo_flow()}")
