import os
from datetime import datetime

from airflow import DAG  # noqa: F401
from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import SnowflakePrivateKeyPemProfileMapping

profile_config = ProfileConfig(
    profile_name="data_pipeline",
    target_name="dev",
    # Account, database, schema, warehouse and the private key (extra.private_key_content)
    # all come from the snowflake_conn Airflow connection.
    profile_mapping=SnowflakePrivateKeyPemProfileMapping(conn_id="snowflake_conn"),
)

dbt_snowflake_dag = DbtDag(
    project_config=ProjectConfig(
        dbt_project_path=os.path.join(os.path.dirname(__file__), "dbt", "data_pipeline")
    ),
    operator_args={"install_deps": True},
    profile_config=profile_config,
    execution_config=ExecutionConfig(
        dbt_executable_path=os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "dbt_venv", "bin", "dbt"
        )
    ),
    schedule="@daily",
    start_date=datetime(2026, 9, 3),
    catchup=False,
    dag_id="dbt_snowflake_dag",
    tags=["dbt", "snowflake"],
    default_args={"retries": 2},
)
