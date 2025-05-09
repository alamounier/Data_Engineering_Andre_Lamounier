from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from docker.types import Mount


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
    start_date=days_ago(1),
    tags=["etl", "brewery", "delta"],
) as dag:

    bronze_task = DockerOperator(
        task_id="bronze_etl",
        image="pyspark_image",  
        container_name="bronze_etl_container_{{ ts_nodash }}",
        command='python3 /code/layer_bronze.py', 
        docker_url='tcp://docker-socket-proxy:2375',
        mount_tmp_dir=False,
        mounts=[
            Mount(source=r"C:\Users\andre-lamounier\Desktop\airflow-docker\meu-projeto\src\outputs", target="/code/outputs", type="bind")
        ],   
        network_mode="bridge",
        auto_remove=True
    )

    silver_task = DockerOperator(
        task_id="silver_etl",
        image="pyspark_image",
        container_name="silver_etl_container_{{ ts_nodash }}",
        command='python3 /code/layer_silver.py',
        docker_url='tcp://docker-socket-proxy:2375',
        mount_tmp_dir=False,
                mounts=[
            Mount(source=r"C:\Users\andre-lamounier\Desktop\airflow-docker\meu-projeto\src\outputs", target="/code/outputs", type="bind")
        ], 
        network_mode="bridge",
        auto_remove=True
    )

    gold_task = DockerOperator(
        task_id="gold_etl",
        image="pyspark_image",
        container_name="gold_etl_container_{{ ts_nodash }}",
        command='python3 /code/layer_gold.py',
        docker_url='tcp://docker-socket-proxy:2375',
        mount_tmp_dir=False,
        mounts=[
            Mount(source=r"C:\Users\andre-lamounier\Desktop\airflow-docker\meu-projeto\src\outputs", target="/code/outputs", type="bind")
        ],  
        network_mode="bridge",
        auto_remove=True
    )

    bronze_task >> silver_task >> gold_task