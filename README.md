# Prefect Cookbook

<!-- ZQM-START -->
<!-- markdownlint-disable MD033 -->
<p align="center">
  <strong>ZQM Computing — Geospatial Engineering & Scientific Computing</strong><br>
  <a href="https://github.com/ZQM-Computing">ZQM Computing</a>
</p>
<!-- markdownlint-enable MD033 -->
<!-- ZQM-END -->

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A **Prefect cookbook** for workflow orchestration, schedules, and deployments. Patterns are drawn from the ZQM fleet's Prefect 3.9.0 installs (Node-1 on port 4300, Node-3 on port 4200) and its scheduled dlt flow. It is intended for Data engineers who orchestrate geospatial pipelines with retries and schedules. Validate each pattern against your own data, software versions, and operating environment before adopting it.

## Repository role and status

**Status:** Active, public. Patterns 01–03 remain design-only. Pattern 04 has a passing exact-head CI runtime contract for its synthetic Prefect + dlt + local DuckDB path; this does not validate worker deployment, Postgres, or production fleet behavior.

**What this repository is:** Prefect patterns — see the table below.

**What it contributes:** Part of the ZQM Computing geospatial portfolio. The umbrella index for the series is [geospatial-cookbooks](https://github.com/ZQM-Computing/geospatial-cookbooks).

**Standing:** This repository is maintained independently. Automated checks cover only the paths and environments configured in its workflows; they do not establish production readiness or operational certification.

## Who this is for

Data engineers who orchestrate geospatial pipelines with retries and schedules.

## Prerequisites

- Prefect 3.9.0
- Python 3.11+
- Postgres or DuckDB as a flow destination (see dlt-cookbook)

## Patterns

| # | Example | Status | What it demonstrates |
|---|---------|--------|----------------------|
| 01 | [01-first-flow](examples/01-first-flow/README.md) | Written (design-only) | Writing and running a first flow with retries |
| 02 | [02-schedules](examples/02-schedules/README.md) | Written (design-only) | Scheduled flows and cron-style triggers |
| 03 | [03-deployments](examples/03-deployments/README.md) | Written (design-only) | Deploying flows as services with work pools |
| 04 | [04-dlt-flow](examples/04-dlt-flow/README.md) | Runtime-tested in CI (local DuckDB only) | A Prefect-scheduled dlt pipeline over synthetic data with destination-count and repeat-run assertions |

## Repository layout

```text
prefect-cookbook/
├── .github/workflows/dlt-example.yml  # isolated synthetic runtime contract
├── examples/
│   └── 04-dlt-flow/                   # Prefect + dlt + local DuckDB example
├── tests/test_dlt_flow.py             # destination count and repeat-run assertions
├── requirements-test.txt              # bounded test/runtime dependencies
├── README.md
└── LICENSE
```

## Validation

Run the bounded local runtime contract from the repository root:

```bash
python -m pip install -r requirements-test.txt
python -m pytest -q
```

The test uses synthetic rows and a temporary local DuckDB file. The verified CI combination is Python `3.11.17`, Prefect `3.9.0`, dlt `1.31.0`, and DuckDB `2.0.0`, pinned in `requirements-test.txt`. A passing run validates this local example on that runner only; it does not validate a Prefect server, worker deployment, Postgres destination, production fleet, or scheduled production flow.

## Roadmap

- First pattern pass: the first two table rows
- Second pass: the remaining rows, from fleet-verified setups
- Extend runtime tests to the other patterns only when their prerequisites and expected behavior are explicit

## Contributing

A contributing guide lands with the first pattern pass. Report security issues to <zqmcomputing@gmail.com> — please do not open a public issue for those.

## More from this series

- [dlt-cookbook](https://github.com/ZQM-Computing/dlt-cookbook) — ELT pipelines from Python into Postgres and DuckDB
- [nifi-cookbook](https://github.com/ZQM-Computing/nifi-cookbook) — Visual dataflow and ingestion pipelines
- [dbt-cookbook](https://github.com/ZQM-Computing/dbt-cookbook) — SQL transformations and tests on warehouse tables
