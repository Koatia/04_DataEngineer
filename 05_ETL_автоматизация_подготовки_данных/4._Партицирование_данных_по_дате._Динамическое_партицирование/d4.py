# docker exec -it spark spark-submit \
#   --jars /opt/spark/jars/spark-excel_2.12-3.5.1_0.20.4.jar,/opt/spark/jars/mysql-connector-j-9.2.0.jar \
#   /var/lib/mydir/d4.py

# docker exec -it spark pip install cryptography pandas pymysql sqlalchemy matplotlib pyspark

import os
import sys
import time
import warnings

import matplotlib.pyplot as plt
from pandas.io import sql
from pyspark.sql.functions import col, lit
from pyspark.sql.session import SparkSession
from sqlalchemy import create_engine, text

from pyspark.sql.window import Window
from pyspark.sql.functions import sum as sum1

warnings.filterwarnings("ignore")
t0 = time.time()

DATABASE_URL = "mysql+pymysql://user:password@mysql-db:3306/mydb"
con = create_engine(DATABASE_URL)

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

spark = SparkSession.builder \
    .appName("Excel Processing") \
    .config("spark.jars", "/opt/spark/jars/spark-excel_2.12-3.5.1_0.20.4.jar") \
    .config("spark.driver.extraClassPath", "/opt/spark/jars/spark-excel_2.12-3.5.1_0.20.4.jar") \
    .config("spark.executor.extraClassPath", "/opt/spark/jars/spark-excel_2.12-3.5.1_0.20.4.jar") \
    .getOrCreate()

connection = con.connect()
connection.execute(text("DROP TABLE IF EXISTS spark.d4_1"))
connection.execute(text("""CREATE TABLE if not exists spark.d4_1 (
	`№` INT(10) NULL DEFAULT NULL,
	`Месяц` DATE NULL DEFAULT NULL,
	`Сумма платежа` FLOAT NULL DEFAULT NULL,
	`Платеж по основному долгу` FLOAT NULL DEFAULT NULL,
	`Платеж по процентам` FLOAT NULL DEFAULT NULL,
	`Остаток долга` FLOAT NULL DEFAULT NULL,
	`Проценты` FLOAT NULL DEFAULT NULL,
	`Долг` FLOAT NULL DEFAULT NULL)
"""))


w = Window.partitionBy(lit(1)).orderBy("№").rowsBetween(Window.unboundedPreceding, Window.currentRow)
df1 = spark.read.format("com.crealytics.spark.excel") \
    .option("sheetName", "Sheet1") \
    .option("useHeader", "false") \
    .option("treatEmptyValuesAsNulls", "false") \
    .option("inferSchema", "true").option("addColorColumns", "true") \
    .option("usePlainNumberFormat", "true") \
    .option("startColumn", 0) \
    .option("endColumn", 99) \
    .option("timestampFormat", "MM-dd-yyyy HH:mm:ss") \
    .option("maxRowsInMemory", 20) \
    .option("excerptSize", 10) \
    .option("header", "true") \
    .format("excel") \
    .load("/var/lib/mydir/d4_1.xlsx").limit(1000) \
    .withColumn("проценты", sum1(col("Платеж по процентам")).over(w)) \
    .withColumn("долг", sum1(col("Платеж по основному долгу")).over(w))

df1.write.format("jdbc").option("url", "jdbc:mysql://mysql-db:3306/spark?user=root&password=root_password") \
    .option("driver", "com.mysql.cj.jdbc.Driver").option("dbtable", "d4_1") \
    .mode("append").save()

df2 = df1.toPandas()
# Get current axis 
ax = plt.gca()
ax.ticklabel_format(style='plain')
# bar plot
df2.plot(kind='line',
         x='№',
         y='долг',
         color='green', ax=ax)
df2.plot(kind='line',
         x='№',
         y='проценты',
         color='red', ax=ax)


connection.execute(text("DROP TABLE IF EXISTS spark.d4_2"))
connection.execute(text("""CREATE TABLE if not exists spark.d4_2 (
	`№` INT(10) NULL DEFAULT NULL,
	`Месяц` DATE NULL DEFAULT NULL,
	`Сумма платежа` FLOAT NULL DEFAULT NULL,
	`Платеж по основному долгу` FLOAT NULL DEFAULT NULL,
	`Платеж по процентам` FLOAT NULL DEFAULT NULL,
	`Остаток долга` FLOAT NULL DEFAULT NULL,
	`проценты` FLOAT NULL DEFAULT NULL,
	`долг` FLOAT NULL DEFAULT NULL)
"""))


w = Window.partitionBy(lit(1)).orderBy("№").rowsBetween(Window.unboundedPreceding, Window.currentRow)
df3 = spark.read.format("com.crealytics.spark.excel") \
    .option("sheetName", "Sheet1") \
    .option("useHeader", "false") \
    .option("treatEmptyValuesAsNulls", "false") \
    .option("inferSchema", "true").option("addColorColumns", "true") \
    .option("usePlainNumberFormat", "true") \
    .option("startColumn", 0) \
    .option("endColumn", 99) \
    .option("timestampFormat", "MM-dd-yyyy HH:mm:ss") \
    .option("maxRowsInMemory", 20) \
    .option("excerptSize", 10) \
    .option("header", "true") \
    .format("excel") \
    .load("/var/lib/mydir/d4_2.xlsx").limit(1000) \
    .withColumn("проценты", sum1(col("Платеж по процентам")).over(w)) \
    .withColumn("долг", sum1(col("Платеж по основному долгу")).over(w))
df3.write.format("jdbc").option("url", "jdbc:mysql://mysql-db:3306/spark?user=root&password=root_password") \
    .option("driver", "com.mysql.cj.jdbc.Driver").option("dbtable", "d4_2") \
    .mode("append").save()
df4 = df3.toPandas()
ax.ticklabel_format(style='plain')
# bar plot
df4.plot(kind='line',
         x='№',
         y='долг',
         color='blue', ax=ax)
df4.plot(kind='line',
         x='№',
         y='проценты',
         color='cyan', ax=ax)


connection.execute(text("DROP TABLE IF EXISTS spark.d4_3"))
connection.execute(text("""CREATE TABLE if not exists spark.d4_3 (
	`№` INT(10) NULL DEFAULT NULL,
	`Месяц` DATE NULL DEFAULT NULL,
	`Сумма платежа` FLOAT NULL DEFAULT NULL,
	`Платеж по основному долгу` FLOAT NULL DEFAULT NULL,
	`Платеж по процентам` FLOAT NULL DEFAULT NULL,
	`Остаток долга` FLOAT NULL DEFAULT NULL,
	`проценты` FLOAT NULL DEFAULT NULL,
	`долг` FLOAT NULL DEFAULT NULL)
"""))
connection.close()  # Закрываем соединение после всех операций


w = Window.partitionBy(lit(1)).orderBy("№").rowsBetween(Window.unboundedPreceding, Window.currentRow)
df5 = spark.read.format("com.crealytics.spark.excel") \
    .option("sheetName", "Sheet1") \
    .option("useHeader", "true") \
    .option("treatEmptyValuesAsNulls", "false") \
    .option("inferSchema", "true").option("addColorColumns", "true") \
    .option("usePlainNumberFormat", "true") \
    .option("startColumn", 0) \
    .option("endColumn", 99) \
    .option("timestampFormat", "MM-dd-yyyy HH:mm:ss") \
    .option("maxRowsInMemory", 20) \
    .option("excerptSize", 10) \
    .option("header", "true") \
    .format("excel") \
    .load("/var/lib/mydir/d4_3.xlsx").limit(1000) \
    .withColumn("проценты", sum1(col("Платеж по процентам")).over(w)) \
    .withColumn("долг", sum1(col("Платеж по основному долгу")).over(w))
df5.write.format("jdbc").option("url", "jdbc:mysql://mysql-db:3306/spark?user=root&password=root_password") \
    .option("driver", "com.mysql.cj.jdbc.Driver").option("dbtable", "d4_3") \
    .mode("append").save()
df6 = df5.toPandas()
ax.ticklabel_format(style='plain')
# bar plot
df6.plot(kind='line',
         x='№',
         y='долг',
         color='magenta', ax=ax)
df6.plot(kind='line',
         x='№',
         y='проценты',
         color='yellow', ax=ax)

# show the plot
plt.legend(['долг_86689', 'проценты_86689', 'долг_120000', 'проценты_120000', 'долг_150000', 'проценты_150000'])
plt.show()

spark.stop()
t1 = time.time()
print('finished', time.strftime('%H:%M:%S', time.gmtime(round(t1 - t0))))
