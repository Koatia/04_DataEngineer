/*
spark-submit --packages com.crealytics:spark-excel_2.12:3.5.1_0.20.4,mysql:mysql-connector-java:8.0.33 /var/lib/mydir/d1.scala

Конфигурация докер "/Users/kostia/Programs:/var/lib/mydir:rw"
*/

import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions._
import java.util.Properties

object MySQLExample {
  def main(args: Array[String]): Unit = {
    // Создаем SparkSession
    val spark = SparkSession.builder()
      .appName("MySQLExample")
      .config("spark.driver.extraJavaOptions", "-Dfile.encoding=UTF-8")
      .getOrCreate()

    // Параметры подключения к MySQL
    val dbUrl = "jdbc:mysql://mysql-db:3306/spark?serverTimezone=UTC"
    val dbUser = "airflow"
    val dbPassword = "airflow"
    val dbDriver = "com.mysql.cj.jdbc.Driver"

    // Читаем Excel-файл
    val df1 = spark.read
      .format("com.crealytics.spark.excel")
      .option("sheetName", "Лист1")
      .option("useHeader", "true")
      .option("header", "true")
      .option("treatEmptyValuesAsNulls", "false")
      .option("inferSchema", "true")
      .option("startColumn", 0)
      .option("endColumn", 99)
      .option("timestampFormat", "MM-dd-yyyy HH:mm:ss")
      .load("/var/lib/mydir/d1.xlsx")

    df1.show()

    // Настройки для соединения с MySQL
    val connectionProperties = new Properties()
    connectionProperties.put("user", dbUser)
    connectionProperties.put("password", dbPassword)
    connectionProperties.put("driver", dbDriver)

    // Функция для записи DataFrame в MySQL
    def writeToMySQL(df: DataFrame, tableName: String): Unit = {
      try {
        df.write
          .mode("append")
          .jdbc(dbUrl, tableName, connectionProperties)
        println(s"✅ Данные успешно записаны в таблицу $tableName.")
      } catch {
        case e: Exception =>
          println(s"❌ Ошибка при записи в таблицу $tableName: ${e.getMessage}")
      }
    }

    // Запись данных в таблицы MySQL
    try {
      println("📊 Загружаем данные в MySQL...")

      writeToMySQL(df1.select("City_code", "Home_city").distinct(), "tabr1")
      writeToMySQL(df1.select("Job_Code", "Job").distinct(), "tabr2")
      writeToMySQL(df1.select("Employee_ID", "Name", "Job_Code").distinct(), "tabr3")
      writeToMySQL(df1.select("Employee_ID", "Name", "City_code").distinct(), "tabr4")

      println("✅ Данные успешно сохранены в MySQL.")

    } catch {
      case e: Exception =>
        println(s"❌ Ошибка при работе с MySQL: ${e.getMessage}")
    } finally {
      // Закрываем SparkSession
      println("🛑 Остановка SparkSession...")
      spark.stop()
    }
  }
}