/*
chcp 65001 && \
spark-shell --packages com.crealytics:spark-excel_2.12:3.5.1_0.20.4,org.postgresql:postgresql:42.6.0 -i /var/lib/mydir/d1.scala --conf "spark.driver.extraJavaOptions=-Dfile.encoding=utf-8"
*/

/*
Конфигурация докер "/Users/kostia/Programs:/var/lib/mydir:rw"
*/

//import org.apache.spark.internal.Logging
//import org.apache.spark.sql.functions.{col, collect_list, concat_ws}
//import org.apache.spark.sql.{DataFrame, SparkSession}

import org.apache.spark.sql.{DataFrame, SparkSession}

// Настройки подключения к PostgreSQL
val dbUrl = "jdbc:postgresql://postgres-db:5432/mydb" // Укажите хост, порт и имя базы данных
val dbUser = "user"
val dbPassword = "password"
val dbDriver = "org.postgresql.Driver"

// Читаем Excel
val df1 = spark.read.format("com.crealytics.spark.excel")
  .option("sheetName", "Лист1") // Укажите имя листа
  .option("useHeader", "true") // Обязательно указать этот параметр
  .option("header", "true") // Указывает, есть ли заголовки в первой строке
  .option("treatEmptyValuesAsNulls", "false")
  .option("inferSchema", "true")
  .option("startColumn", 0)
  .option("endColumn", 99)
  .option("timestampFormat", "MM-dd-yyyy HH:mm:ss")
  .load("/var/lib/mydir/d1.xlsx")

df1.show()

// Функция для записи DataFrame в PostgreSQL
def writeToPostgres(df: DataFrame, tableName: String): Unit = {
  df.write
    .format("jdbc")
    .option("url", dbUrl)
    .option("dbtable", tableName)
    .option("user", dbUser)
    .option("password", dbPassword)
    .option("driver", dbDriver)
    .mode("append") // Можно использовать "overwrite" для перезаписи
    .save()
}

// Запись данных в таблицы PostgreSQL
writeToPostgres(df1.select("City_code", "Home_city").distinct(), "tabr1")
writeToPostgres(df1.select("Job_Code", "Job").distinct(), "tabr2")
writeToPostgres(df1.select("Employee_ID", "Name", "Job_Code").distinct(), "tabr3")
writeToPostgres(df1.select("Employee_ID", "Name", "City_code").distinct(), "tabr4")

println("Данные успешно сохранены в PostgreSQL.")
System.exit(0)