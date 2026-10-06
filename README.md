# dbt + Snowflake + Airflow Data Pipeline

An end-to-end analytics engineering pipeline that transforms Snowflake's sample **TPC-H** order data into clean, query-ready fact tables using **dbt**, orchestrated and scheduled with **Apache Airflow** via **Astronomer Cosmos**.

This was my first data engineering project — built to learn how raw warehouse data gets modeled, tested, and automated in a real pipeline rather than run as one-off SQL scripts.

## What it does

1. **Source**: Raw `orders` and `lineitem` tables from Snowflake's `SNOWFLAKE_SAMPLE_DATA.TPCH_SF1` dataset
2. **Staging models**: Clean, renamed 1:1 views of the raw source tables (`stg_tpch_orders`, `stg_tpch_line_items`)
3. **Intermediate models**: Join orders to their line items and calculate discounted line amounts (`int_order_items`, `int_order_items_summary`)
4. **Mart model**: A final, analysis-ready fact table (`fct_orders`) joining order-level details with aggregated item sales — ready to query or plug into a BI tool
5. **Tests**: dbt data tests (including relationship/referential checks) validate the pipeline's output on every run
6. **Orchestration**: Airflow, running dbt through Cosmos, schedules the whole pipeline to run daily — turning a set of SQL files into a self-running, testable production pipeline

## Architecture

```
Snowflake (raw TPC-H data)
        │
        ▼
  dbt staging models  (views)
        │
        ▼
  dbt intermediate models  (joins + calculations)
        │
        ▼
  dbt mart model  (fct_orders)
        │
        ▼
  Snowflake (DBT_DB.DBT_SCHEMA)

Orchestrated daily by Airflow (Astronomer Cosmos) ⟲
```

## Tech stack

| Layer | Tool |
|---|---|
| Data warehouse | Snowflake |
| Transformation | dbt Core |
| Orchestration | Apache Airflow (via Astronomer CLI) |
| dbt ↔ Airflow integration | Astronomer Cosmos |
| Authentication | Snowflake key-pair auth (RSA) |

## Project structure

```
dbt-dag/
├── dags/
│   ├── dbt_dag.py                 # Airflow DAG — runs the dbt project via Cosmos
│   └── dbt/data_pipeline/
│       ├── models/
│       │   ├── staging/           # 1:1 cleaned views of raw TPC-H sources
│       │   └── marts/             # Joined, tested, analysis-ready tables
│       ├── macros/                # Reusable SQL logic (e.g. discount calculation)
│       ├── tests/                 # Custom dbt data tests
│       └── dbt_project.yml
├── Dockerfile
├── requirements.txt                # astronomer-cosmos, apache-airflow-providers-snowflake
└── packages.txt
```

## Running it locally

**Prerequisites:** [Astronomer CLI](https://www.astronomer.io/docs/astro/cli/install-cli), Docker, a Snowflake account with key-pair authentication set up.

1. Clone the repo and install dependencies:
   ```bash
   git clone https://github.com/SipOfLatte/dbt-snowflake-airflow-pipeline.git
   cd dbt-snowflake-airflow-pipeline
   ```

2. Copy the example settings file and fill in your own Snowflake connection details:
   ```bash
   cp airflow_settings.yaml.example airflow_settings.yaml
   ```

3. Generate a Snowflake key pair and register the public key against your Snowflake user (see dbt's [key-pair auth docs](https://docs.getdbt.com/docs/core/connect-data-platform/snowflake-setup#key-pair-authentication)). Place the private key at `dags/rsa_key.p8` — this file is gitignored and never committed.

4. Start the environment:
   ```bash
   astro dev start
   ```

5. Open the Airflow UI at `localhost:8080` (default login: `admin` / `admin`) and trigger the `dbt_snowflake_dag`.

## What I learned

Building this from scratch (rather than just running pre-written code) meant working through the full stack of real-world friction: Snowflake authentication methods (SSO → password → key-pair), Python environment and dependency management, Docker networking issues between Airflow's containers, and how dbt's config and Airflow's DAG scanning actually behave under the hood. It's a small pipeline, but it touches every layer a real one does.

## Credit

Built while following along with [this tutorial](https://www.youtube.com/watch?v=OLXkGB7krGo), then adapted and debugged through to a working end-to-end deployment.
