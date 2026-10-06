import os
from datetime import datetime

from airflow import DAG  # noqa: F401
from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import SnowflakePrivateKeyPemProfileMapping

with open(os.path.join(os.path.dirname(__file__), "rsa_key.p8")) as f:
    private_key_content = f.read()

profile_config = ProfileConfig(
    profile_name="data_pipeline",
    target_name="dev",
    profile_mapping=SnowflakePrivateKeyPemProfileMapping(
        conn_id="snowflake_conn",
        profile_args={
            "database": "dbt_db",
            "schema": "dbt_schema",
            "private_key": private_key_content,
        },
    ),
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
)
