from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from etl_layers.layer_bronze import run_bronze_etl
from etl_layers.layer_silver import run_silver_etl
from etl_layers.layer_gold import run_gold_etl

default_args = {
    "owner": "andre",
    "depends_on_past": False,
    "start_date": datetime(2025, 5, 7),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="brewery_etl_dag",
    default_args=default_args,
    schedule_interval=None,  # ou "0 2 * * *" para rodar diariamente às 2h da manhã
    catchup=False,
    tags=["etl", "brewery", "delta"],
) as dag:

    bronze_task = PythonOperator(
        task_id="bronze_etl",
        python_callable=run_bronze_etl,
    )

    silver_task = PythonOperator(
        task_id="silver_etl",
        python_callable=run_silver_etl,
    )

    gold_task = PythonOperator(
        task_id="gold_etl",
        python_callable=run_gold_etl,
    )

    # Define a ordem de execução
    bronze_task >> silver_task >> gold_task