/*
spark-shell -i /var/lib/mydir/dz2.scala --conf "spark.driver.extraJavaOptions=-Dfile.encoding=utf-8" --packages com.mysql:mysql-connector-j:8.0.33
*/

import org.apache.spark.internal.Logging
import org.apache.spark.sql.functions.{col, collect_list, concat_ws}
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.expressions.Window

val t1 = System.currentTimeMillis()
if (1 == 1) {
  // Чтение файла
  var df1 = spark.read.option("delimiter", ",")
    .option("header", "true")
    .csv("/var/lib/mydir/fifa_s2.csv")

  // Преобразование и очистка данных
  df1 = df1
    // Преобразование числовых колонок
    .withColumn("Age", col("Age").cast("int"))
    .withColumn("Overall", col("Overall").cast("int"))
    .withColumn("Potential", col("Potential").cast("int"))

    // Преобразование денежных колонок (удаление символов и преобразование в число)
    .withColumn("Value",
      regexp_replace(col("Value"), "[€,]", "").cast("double"))
    .withColumn("Wage",
      regexp_replace(col("Wage"), "[€,]", "").cast("double"))

  // Функция для определения возрастной группы
  def getAgeGroup = udf((age: Int) => {
    if (age < 20) "Less 20"
    else if (age >= 20 && age < 30) "From 20 to 30"
    else if (age >= 30 && age <= 36) "From 30 to 36"
    else "Older 36"
  })

  // Добавление колонки с возрастной группой
  df1 = df1.withColumn("AgeGroup", getAgeGroup(col("Age")))

  // Подсчет количества футболистов в каждой возрастной группе
  println("Number of football players in each age group:")
  df1.groupBy("AgeGroup")
    .agg(
      count("*").alias("PlayerCount"),
      avg("Overall").alias("AvgOverall"),
      avg("Potential").alias("AvgPotential")
    )
    .orderBy(col("PlayerCount").desc)
    .show()

  // Визуализация распределения возрастных групп
  println("\nProportion of football players in each age group:")
  df1.groupBy("AgeGroup")
    .agg(
      count("*").alias("PlayerCount"),
      (count("*") / df1.count() * 100).alias("Percentage")
    )
    .orderBy(col("PlayerCount").desc)
    .show()

  // Выбор наиболее релевантных колонок
  val columnsToKeep = Array(
    "ID", "Name", "Age", "AgeGroup", "Nationality",
    "Overall", "Potential", "Club",
    "Value", "Wage", "Position"
  )

  // Оставляем только выбранные колонки
  df1 = df1.select(columnsToKeep.map(col): _*)

  // Удаление строк с недостающими значениями
  df1 = df1.na.drop()

  // --------- Создаем базу данных "spark", если она не существует
  import java.sql.DriverManager
  // Устанавливаем соединение с MySQL
  val connection = DriverManager.getConnection("jdbc:mysql://mysql-db:3306/?user=root&password=root_password")
  val statement = connection.createStatement()
  // Проверяем, существует ли база данных "spark"
  val resultSet = statement.executeQuery("SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = 'spark'")
  // Если база данных не существует, создаем ее
  if (!resultSet.next()) {
    statement.executeUpdate("CREATE DATABASE spark")
    println("База данных 'spark' создана.")
  } else {
    println("База данных 'spark' уже существует.")
  }
  // Закрываем соединение
  statement.close()
  connection.close()

  // Сохранение в базу данных
  df1.write.format("jdbc")
    .option("url", "jdbc:mysql://mysql-db:3306/spark")
    .option("driver", "com.mysql.cj.jdbc.Driver")
    .option("user", "user")
    .option("password", "password")
    .option("dbtable", "fifa_players_age_groups")
    .mode("overwrite")
    .save()

  // Показ первых строк
  println("\nFirst lines after adding age groups:")
  df1.show()
}

val s0 = (System.currentTimeMillis() - t1) / 1000
val s = s0 % 60
val m = (s0 / 60) % 60
val h = (s0 / 60 / 60) % 24
println("%02d:%02d:%02d".format(h, m, s))
System.exit(0)