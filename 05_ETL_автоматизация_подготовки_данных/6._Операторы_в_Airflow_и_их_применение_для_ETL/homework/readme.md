## Домашняя работа 6

### Задание:

- Установить Spark MySQL и Airflow;
- Запустить скрипт из первого и второго семинара;
- Запустить скрипты через Airflow

---

1. В Docker контейнере развернут `Spark`-`MySQL`-`Airflow`
с использованием файла [docker-compose](~/Programs/_Repository/00_Codes/26Docker/Spark-MySQL-Airflow/docker-compose.yaml)

2. Подключены папки:
    - `~/Programs/airflow/dags` : `/opt/airflow/dags`
    - `~/Programs/airflow/logs` : `/opt/airflow/logs`
    - `~/Programs/airflow/config` : `/opt/airflow/config`
    - `~/Programs/airflow/plugins` : `/opt/airflow/plugins`
    - `~/Programs/spark` : `/var/lib/mydir`
    - `~/Programs/spark/jars` : `/opt/spark/jars`


3. Добавлено соединение spark_default в Airflow через docker-compose.yaml. Для этого автоматически регистрируется соединение при запуске контейнера (секция airflow-init:).
   ```
   airflow connections add 'spark_default' --conn-type 'spark' --conn-host 'spark://spark:7077'
   ```

4. Для запуска используется команда:
    ```bash
    export AIRFLOW_UID=50000 && docker-compose up
    ```
   
4. Предоставить пользователю `user` доступ к базе `spark`

   ```bash
   docker exec -it mysql-db mysql -u root -p
   ```

   После ввода пароля и подключения к базе данных под рутом вводишь следующую команду:

   ```bash
   GRANT ALL PRIVILEGES ON spark.* TO 'user'@'%';
   FLUSH PRIVILEGES;
   ```

5. Установить Airflow Spark Provider

   ```bash
   docker exec -it spark-mysql-airflow-airflow-webserver-1 bash pip install apache-airflow-providers-apache-spark
   ```

6. Установить библиотеки python в образе `spark`:

   ```bash
   docker exec -it --user airflow spark-mysql-airflow-airflow-webserver-1 pip install cryptography pandas pymysql sqlalchemy matplotlib pyspark
   ```

6. Запуск контейнера с root-пользователем

   ```bash
   docker exec -it --user root spark-mysql-airflow-airflow-webserver-1 bash
   ```


6. Остановите сервисы:

   ```bash
   docker-compose down
   ```