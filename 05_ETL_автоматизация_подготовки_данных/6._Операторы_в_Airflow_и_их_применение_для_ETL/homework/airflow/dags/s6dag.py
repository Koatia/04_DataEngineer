from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'Kostia',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 1),
    'email': ['alex@alex.ru'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}

dag1 = DAG('Kostia001',
           default_args=default_args,
           description="seminar_6",
           catchup=False,
           schedule_interval='0 6 * * *')

# Устанавливаем все системные зависимости
task1 = BashOperator(
    task_id='install_dependencies',
    bash_command="""
    docker exec -u root spark sh -c "
    apt-get update && \
    apt-get install -y gnupg curl && \
    curl -fsSL https://packages.adoptium.net/artifactory/api/gpg/key/public | gpg --dearmor > /usr/share/keyrings/adoptium-keyring.gpg && \
    echo 'deb [signed-by=/usr/share/keyrings/adoptium-keyring.gpg] https://packages.adoptium.net/artifactory/deb bookworm main' > /etc/apt/sources.list.d/adoptium.list && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y openjdk-17-jdk scala curl telnet && \
    chmod -R 755 /opt/bitnami/spark/jars/
    "
    """,
    dag=dag1
)

# Устанавливаем Python-библиотеки
task2 = BashOperator(
    task_id='pip_install',
    bash_command="""
    docker exec spark sh -c "
    pip install --no-cache-dir cryptography pandas pymysql sqlalchemy pyspark
    "
    """,
    dag=dag1
)

# Запускаем Python-скрипт PySpark
task3 = BashOperator(
    task_id='pyspark',
    bash_command="""
    docker exec spark sh -c "
    if test -f /var/lib/mydir/s6.py; then \
      python /var/lib/mydir/s6.py; \
    else \
      echo 's6.py not found!' && exit 1; \
    fi
    "
    """,
    dag=dag1
)

task4 = BashOperator(
    task_id='scala',
    bash_command="""
    docker exec spark sh -c "
    # export JAVA_HOME=/opt/bitnami/java && \
    # export PATH=$JAVA_HOME/bin:$PATH && \
    echo 'Using JAVA_HOME='$JAVA_HOME && \
    javac -version && \
    cd /var/lib/mydir && \
    if test -f s6s1.scala; then \
      scalac -encoding UTF-8 -J-Xmx4g -J-Xms2g -classpath '/opt/bitnami/spark/jars/*' -d s6s1.jar s6s1.scala && \
      jar cf s6s1.jar *.class && \
      echo '✅ Scala script compiled successfully.'; \
    else \
      echo '❌ Scala script not found!' && exit 1; \
    fi
    "
    """,
    dag=dag1
)

task5 = BashOperator(
    task_id='run_spark',
    bash_command="""
    docker exec spark sh -c "
    cd /var/lib/mydir && \
    if test -f s6s1.jar; then \
      /opt/bitnami/spark/bin/spark-submit --driver-memory 4g --executor-memory 4g \
      --class MySQLExample \
      --packages com.crealytics:spark-excel_2.12:3.5.1_0.20.4,mysql:mysql-connector-java:8.0.33 \
      /var/lib/mydir/s6s1.jar; \
    else \
      echo 'Scala JAR file not found!' && exit 1; \
    fi
    "
    """,
    dag=dag1
)

task1 >> task2 >> task3 >> task4 >> task5
