Ваш скрипт Spark выполняет множество операций: чтение Excel-файла, обработка данных и взаимодействие с MySQL базой данных. Вот основные шаги и комментарии:

Основные компоненты:

	1.	Чтение Excel-файла:

val df1 = spark.read.format("com.crealytics.spark.excel")
    .option("sheetName", "Sheet1")
    .option("useHeader", "false")
    .option("treatEmptyValuesAsNulls", "false")
    .option("inferSchema", "true")
    .option("addColorColumns", "true")
    .option("usePlainNumberFormat", "true")
    .option("startColumn", 0)
    .option("endColumn", 99)
    .option("timestampFormat", "MM-dd-yyyy HH:mm:ss")
    .option("maxRowsInMemory", 20)
    .option("excerptSize", 10)
    .option("header", "true")
    .format("excel")
    .load("/var/lib/mydir/d1.xlsx")
df1.show()

	•	Используется библиотека com.crealytics.spark.excel для чтения Excel-файла.
	•	Опции задают параметры чтения, такие как имя листа, наличие заголовков, формат временных меток и диапазон колонок.
	•	Проверьте, что файл Excel находится в указанной директории /var/lib/mydir/d1.xlsx.

	2.	Фильтрация и запись данных в MySQL:

df1.filter(df1("Employee_ID").isNotNull)
    .select("Employee_ID", "Name", "Job_Code", "Job", "City_code", "Home_city")
    .write.format("jdbc")
    .option("url", "jdbc:mysql://localhost:3306/spark?user=root&password=root")
    .option("driver", "com.mysql.cj.jdbc.Driver")
    .option("dbtable", "tabr")
    .mode("overwrite")
    .save()

	•	Данные фильтруются по Employee_ID, затем записываются в таблицу tabr базы данных spark.
	•	Проверьте, что MySQL запущен, и параметры подключения (user, password, url) корректны.

	3.	Создание таблиц в MySQL:
	•	Используется метод sqlexecute для выполнения SQL-команд на стороне MySQL:

sqlexecute("CREATE TABLE `tabr1` (...)")
sqlexecute("CREATE TABLE `tabr2` (...)")
sqlexecute("CREATE TABLE `tabr3` (...)")
sqlexecute("CREATE TABLE `tabr4` (...)")


	•	Убедитесь, что права доступа к базе данных позволяют создавать и удалять таблицы.

	4.	Запись данных в MySQL по таблицам:

df1.select("City_code", "Home_city").distinct()
    .write.format("jdbc")
    .option("url", "jdbc:mysql://localhost:3306/spark?user=root&password=root")
    .option("driver", "com.mysql.cj.jdbc.Driver")
    .option("dbtable", "tabr1")
    .mode("append")
    .save()

	•	Аналогично для tabr2, tabr3, tabr4. Используются методы .distinct() для удаления дубликатов.

	5.	Вывод времени выполнения:

val s0 = (System.currentTimeMillis() - t1) / 1000
val s = s0 % 60
val m = (s0 / 60) % 60
val h = (s0 / 60 / 60) % 24
println("%02d:%02d:%02d".format(h, m, s))

	•	Показывает время выполнения в формате чч:мм:сс.

	6.	Завершение работы:

System.exit(0)



Примечания:

	1.	Проверка библиотек:
	•	Убедитесь, что библиотека com.crealytics.spark.excel доступна в проекте (добавьте в зависимости).
	•	Подключите JDBC-драйвер MySQL (например, mysql-connector-java).
	2.	Разрешения и настройки:
	•	Проверьте разрешения на чтение/запись для директории /var/lib/mydir.
	•	Убедитесь, что пользователь MySQL имеет доступ к базе данных spark.

Если возникнут ошибки, напишите, чтобы я мог помочь!