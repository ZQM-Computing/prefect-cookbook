"""Deploy a flow on a daily cron schedule.

Design-only example: the deployment API spelling is the Prefect 3.9.0
surface as documented for this pattern; confirm the exact call against
3.9.0 at validation (see README.md). The flow itself is synthetic.
"""
from prefect import flow, task


@task
def ingest_day() -> str:
    # Synthetic stand-in for a daily ingest step.
    return "ingested one synthetic day"


@flow(name="daily-ingest-flow")
def daily_ingest_flow() -> str:
    return ingest_day()


if __name__ == "__main__":
    daily_ingest_flow.deploy(
        name="daily-ingest",
        work_pool_name="default-pool",
        cron="0 6 * * *",
        timezone="UTC",
    )
