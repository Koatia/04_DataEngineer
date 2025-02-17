import sys
import os
import pandas as pd
from pandas.io import sql
from pyspark.sql.functions import col, lit, to_date
from pyspark.sql.session import SparkSession
from sqlalchemy import create_engine
from pyspark.sql.window import Window
from pyspark.sql.functions import sum as sum1

# Настройки подключения к MySQL
MYSQL_USER = "airflow"
MYSQL_PASSWORD = "airflow"
MYSQL_HOST = "mysql-db"  # Имя контейнера MySQL
MYSQL_DB = "spark"
MYSQL_JDBC_DRIVER = "com.mysql.cj.jdbc.Driver"

# Подключение к MySQL через SQLAlchemy
try:
    engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}")
    connection = engine.connect()
    print("✅ Подключение к MySQL установлено!")
except Exception as e:
    print(f"❌ Ошибка подключения к MySQL: {e}")
    sys.exit(1)

# Создание SparkSession с загрузкой необходимых JAR-пакетов
spark = SparkSession.builder \
    .appName("Excel Processing") \
    .config("spark.jars.packages",
            "com.crealytics:spark-excel_2.12:3.5.1_0.20.4,mysql:mysql-connector-java:8.0.33") \
    .config("spark.driver.extraClassPath", "/opt/bitnami/spark/jars/mysql-connector-java-8.0.33.jar") \
    .config("spark.executor.extraClassPath", "/opt/bitnami/spark/jars/mysql-connector-java-8.0.33.jar") \
    .getOrCreate()

print("✅ SparkSession создан!")

# Пример SQL-запроса
try:
    with engine.connect() as connection:
        pd.io.sql.execute("DROP TABLE IF EXISTS spark.`tasketl4b`", connection)
        print("✅ Таблица 'tasketl4b' успешно удалена (если существовала)")
        pd.io.sql.execute("""CREATE TABLE if not exists spark.`tasketl4b` (
                            `№` INT(10) NULL DEFAULT NULL,
                            `Месяц` DATE NULL DEFAULT NULL,
                            `Сумма платежа` FLOAT NULL DEFAULT NULL,
                            `Платеж по основному долгу` FLOAT NULL DEFAULT NULL,
                            `Платеж по процентам` FLOAT NULL DEFAULT NULL,
                            `Остаток долга` FLOAT NULL DEFAULT NULL,
                            `проценты` FLOAT NULL DEFAULT NULL,
                            `долг` FLOAT NULL DEFAULT NULL
                                                )
                            COLLATE='utf8mb4_0900_ai_ci'
                            ENGINE=InnoDB""", connection)
        print("✅ Таблица 'tasketl4b' успешно создана")
except Exception as e:
    print(f"❌ Ошибка при создании таблицы: {e}")

# Окно для вычисления суммарных значений
w = Window.partitionBy(lit(1)).orderBy("№").rowsBetween(Window.unboundedPreceding, Window.currentRow)

# Проверка наличия Excel-файла
excel_path = "/var/lib/mydir/s4_2.xlsx"

if os.path.exists(excel_path):
    print(f"✅ Файл {excel_path} найден. Начинаем обработку...")
    try:
        df1 = spark.read.format("com.crealytics.spark.excel") \
            .option("sheetName", "Sheet1") \
            .option("useHeader", "false") \
            .option("treatEmptyValuesAsNulls", "false") \
            .option("inferSchema", "true") \
            .option("addColorColumns", "true") \
            .option("usePlainNumberFormat", "true") \
            .option("startColumn", 0) \
            .option("endColumn", 99) \
            .option("timestampFormat", "MM-dd-yyyy HH:mm:ss") \
            .option("maxRowsInMemory", 20) \
            .option("excerptSize", 10) \
            .option("header", "true") \
            .format("excel") \
            .load(excel_path).limit(1000) \
            .withColumn("проценты", sum1(col("Платеж по процентам")).over(w)) \
            .withColumn("долг", sum1(col("Платеж по основному долгу")).over(w))

        df1 = df1.withColumn("Месяц", to_date(col("Месяц")))  # Приведение типа к `DATE`
        print("✅ Данные загружены в Spark DataFrame")

    except Exception as e:
        print(f"❌ Ошибка при загрузке Excel файла: {e}")
else:
    print(f"❌ Файл {excel_path} не найден!")
    sys.exit(1)

# Запись данных в MySQL
try:
    df1.write \
        .format("jdbc") \
        .option("url", f"jdbc:mysql://{MYSQL_HOST}/{MYSQL_DB}") \
        .option("dbtable", "tasketl4b") \
        .option("user", MYSQL_USER) \
        .option("password", MYSQL_PASSWORD) \
        .option("driver", MYSQL_JDBC_DRIVER) \
        .mode("overwrite") \
        .save()

    print("✅ Данные успешно записаны в MySQL!")

except Exception as e:
    print(f"❌ Ошибка при записи в MySQL: {e}")

# Завершаем сессию
spark.stop()
print("✅ SparkSession завершен!")
