"""First Prefect flow: a flaky task with retries.

The task fails on its first attempt by design (a counter file), then
succeeds. This demonstrates retries converting a transient failure into a
successful flow run. No real data is involved; the "work" is synthetic.
"""
from pathlib import Path
from prefect import flow, task

ATTEMPT_FILE = Path("attempt.txt")


@task(retries=2, retry_delay_seconds=5)
def flaky_step() -> str:
    attempt = int(ATTEMPT_FILE.read_text().strip()) if ATTEMPT_FILE.exists() else 0
    attempt += 1
    ATTEMPT_FILE.write_text(str(attempt))
    if attempt < 2:
        raise RuntimeError(f"transient failure on attempt {attempt}")
    return f"flaky step succeeded on attempt {attempt}"


@flow(name="first-flow")
def first_flow() -> str:
    return flaky_step()


if __name__ == "__main__":
    print(first_flow())
