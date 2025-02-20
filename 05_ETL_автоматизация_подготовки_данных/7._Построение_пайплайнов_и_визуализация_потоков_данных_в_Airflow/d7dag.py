import os
import logging
import pandas as pd
from airflow.operators.bash import BashOperator
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pendulum

# Настройки логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

default_args = {
    'owner': 'Kostia',
    'depends_on_past': False,
    'start_date': pendulum.datetime(2024, 6, 1, tz='Europe/Moscow'),
    'email': ['dom@dom.ru'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}

dag2 = DAG('Kostia002',
           default_args=default_args,
           description="seminar_7",
           catchup=False,
           schedule_interval='0 8 * * *')


def percent(**kwargs):
    files = ['/opt/airflow/dags/d4_1.xlsx', '/opt/airflow/dags/d4_2.xlsx', '/opt/airflow/dags/d4_3.xlsx']

    # Настройки подключения к MySQL
    MYSQL_USER = "airflow"
    MYSQL_PASSWORD = "airflow"
    MYSQL_HOST = "mysql-db"
    MYSQL_DB = "spark"

    # Подключение к MySQL через SQLAlchemy с таймаутом
    con = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DB}",
                        connect_args={'connect_timeout': 10})

    for file in files:
        if not os.path.exists(file):
            logger.error(f"❌ Файл {file} не найден!")
            raise FileNotFoundError(f"Файл {file} не найден!")

        logger.info(f"📂 Обработка файла {file}")
        df = pd.read_excel(file, engine='openpyxl')

        required_columns = ['Платеж по основному долгу', 'Платеж по процентам']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"❌ В файле {file} отсутствует колонка {col}!")
                raise KeyError(f"Ошибка: в файле {file} отсутствует колонка {col}!")

        df['долг'] = df['Платеж по основному долгу'].cumsum().round(2)
        df['проценты'] = df['Платеж по процентам'].cumsum().round(2)

        # Проверка существования таблицы перед заменой
        try:
            table_exists = con.dialect.has_table(con.connect(), "credit", schema="spark")
            if not table_exists or os.path.basename(file) == "d4_1.xlsx":
                df.to_sql('credit', con, schema='spark', if_exists='replace', index=False, chunksize=500)
            else:
                df.to_sql('credit', con, schema='spark', if_exists='append', index=False, chunksize=500)
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при записи в БД: {e}")
            raise


# Устанавливаем Python-библиотеки
task1 = BashOperator(
    task_id='pip_install',
    bash_command="""
    pip install --no-cache-dir cryptography pandas pymysql sqlalchemy openpyxl pendulum
    """,
    dag=dag2
)

# Этот DAG автоматизирует обработку платежных данных из Excel-файлов
task2 = PythonOperator(
    task_id='python3',
    dag=dag2,
    python_callable=percent
)

task1 >> task2  # Устанавливаем порядок выполнения
