"""Runtime contract tests for the Prefect/dlt DuckDB example."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "examples" / "04-dlt-flow" / "dlt_flow.py"


def load_example():
    spec = importlib.util.spec_from_file_location("prefect_dlt_example", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_replace_flow_queries_real_destination_count_and_is_repeatable(tmp_path, monkeypatch):
    """Two runs replace the fixture and leave exactly 20 real destination rows."""
    monkeypatch.chdir(tmp_path)
    module = load_example()

    assert module.dlt_demo_flow() == 20
    assert module.dlt_demo_flow() == 20

    database = tmp_path / "synthetic_demo.duckdb"
    assert database.is_file(), "Expected dlt to create its local DuckDB destination"

    connection = duckdb.connect(str(database), read_only=True)
    try:
        count, distinct_ids, min_id, max_id = connection.execute(
            'SELECT COUNT(*), COUNT(DISTINCT id), MIN(id), MAX(id) FROM "demo"."records"'
        ).fetchone()
    finally:
        connection.close()

    assert count == 20
    assert distinct_ids == 20
    assert min_id == 0
    assert max_id == 19
