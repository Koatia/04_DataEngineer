from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def print_hello():
    return 'Привет, Мир! Первый запуск Airflow DAG!'


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2017, 3, 20),
    'retries': 1,
}

dag = DAG(
    dag_id='my_first_dag',
    description='Добро пожаловать, Konstantin! С вами DAG',
    schedule_interval='0 12 * * *',
    catchup=False,
    default_args=default_args
)

hello_operator = PythonOperator(
    task_id='hello_task',
    python_callable=print_hello,
    dag=dag
)

hello_operator
