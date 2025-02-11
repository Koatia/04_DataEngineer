/*
spark-submit --packages com.crealytics:spark-excel_2.12:3.5.1_0.20.4,mysql:mysql-connector-java:8.0.33 /var/lib/mydir/d1.scala

Конфигурация докер "/Users/kostia/Programs:/var/lib/mydir:rw"
*/

import org.apache.spark.sql.{DataFrame, SparkSession}
import java.sql.{Connection, DriverManager, ResultSet}

object MySQLExample {
  def main(args: Array[String]): Unit = {
    // Создаём SparkSession
    val spark = SparkSession.builder()
      .appName("MySQLExample")
      .config("spark.driver.extraJavaOptions", "-Dfile.encoding=utf-8")
      .getOrCreate()

    // Параметры подключения к MySQL
    val dbUrl = "jdbc:mysql://localhost:3306/spark"
    val dbUser = "user"
    val dbPassword = "password"
    val dbDriver = "com.mysql.cj.jdbc.Driver"

    // Читаем Excel
    val df1 = spark.read.format("com.crealytics.spark.excel")
      .option("sheetName", "Лист1") // Укажите имя листа
      .option("useHeader", "true") // Указывает, что есть заголовки
      .option("header", "true")
      .option("treatEmptyValuesAsNulls", "false")
      .option("inferSchema", "true")
      .option("startColumn", 0)
      .option("endColumn", 99)
      .option("timestampFormat", "MM-dd-yyyy HH:mm:ss")
      .load("/var/lib/mydir/d1.xlsx")

    df1.show()

    // Функция для записи DataFrame в MySQL
    def writeToMySQL(df: DataFrame, tableName: String): Unit = {
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

    // Подключение к базе данных
    var connection: Connection = null
    try {
      // Загружаем драйвер MySQL
      Class.forName(dbDriver)
      connection = DriverManager.getConnection(dbUrl, dbUser, dbPassword)
      println("✅ Подключение к MySQL успешно!")

      // Запись данных в таблицы MySQL
      writeToMySQL(df1.select("City_code", "Home_city").distinct(), "tabr1")
      writeToMySQL(df1.select("Job_Code", "Job").distinct(), "tabr2")
      writeToMySQL(df1.select("Employee_ID", "Name", "Job_Code").distinct(), "tabr3")
      writeToMySQL(df1.select("Employee_ID", "Name", "City_code").distinct(), "tabr4")

      println("✅ Данные успешно сохранены в MySQL.")

    } catch {
      case e: Exception => e.printStackTrace()
    } finally {
      if (connection != null) connection.close()
    }

    // Останавливаем Spark
    spark.stop()
  }
}