from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 2, 10),
    "catchup": False,
}

dag = DAG(
    dag_id="spark_scala_dag",
    default_args=default_args,
    schedule_interval=None  # Запуск только вручную
)

submit_scala_job = SparkSubmitOperator(
    task_id="run_scala_script",
    application="/var/lib/mydir/d1.scala",  # Путь к файлу внутри контейнера
    conn_id="spark_default",
    dag=dag,
)

submit_scala_job