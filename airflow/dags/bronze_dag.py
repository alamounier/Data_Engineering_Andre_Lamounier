from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from etl_layers.bronze_layer import run_bronze_etl

default_args = {
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

with DAG("bronze_dag",
         default_args=default_args,
         schedule_interval="@daily",
         catchup=False) as dag:

    extract_and_store_bronze = PythonOperator(
        task_id="extract_and_store_bronze",
        python_callable=run_bronze_etl
    )
