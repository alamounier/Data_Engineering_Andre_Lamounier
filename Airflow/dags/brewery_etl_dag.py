from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

default_args = {
    "owner": "andre",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="brewery_etl_dag",
    default_args=default_args,
    schedule_interval="@daily",
    start_date= days_ago(1),
    tags=["etl", "brewery", "delta"],
) as dag:

    bronze_task = DockerOperator(
        task_id="bronze_etl",
        image="pyspark_image",  
        container_name="bronze_etl_container",
        auto_remove=True,
        command= 'python3 /code/etl_layers/layer_bronze.py', 
        docker_url= 'tcp://docker-socket-proxy:2375',
        network_mode="bridge",
    )

    silver_task = DockerOperator(
        task_id="silver_etl",
        image="pyspark_image",
        container_name="silver_etl_container",
        auto_remove=True,
        command='python3 /code/etl_layers/layer_silver.py',
        docker_url= 'tcp://docker-socket-proxy:2375',
        network_mode="bridge",
    )

    gold_task = DockerOperator(
        task_id="gold_etl",
        image="pyspark_image",
        container_name="gold_etl_container",
        auto_remove=True,
        command='python3 /code/etl_layers/layer_gold.py',
        docker_url= 'tcp://docker-socket-proxy:2375',
        network_mode="bridge",
    )

    bronze_task >> silver_task >> gold_task