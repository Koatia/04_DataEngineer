Запускаем PostgreSQL
Используем стандартный образ PostgreSQL с открытым портом для внешнего подключения:

```shell
docker run -d \
  --name postgres-db \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  postgres:latest
```

Запускаем Spark в Docker:

```bash
docker run -d \
  --name spark-master \
  -p 7077:7077 \
  -p 8080:8080 \
  -v /Users/kostia/Programs:/var/lib/mydir \
  bitnami/spark:latest \
  ./bin/spark-class org.apache.spark.deploy.master.Master
```


Создаем новую сеть Docker:

```bash
docker network create spark-postgres-network
```


2. Перезапустите контейнеры и подключите их к новой сети

Переподключите PostgreSQL и Spark к созданной сети:

Подключение PostgreSQL:

Если контейнер PostgreSQL уже запущен, отключите его и снова запустите, подключив к новой сети:

docker network connect spark-postgres-network <имя_контейнера_postgres>

Подключение Spark:

Для контейнера Spark:

docker network connect spark-postgres-network <имя_контейнера_spark>

3. Убедитесь, что оба контейнера находятся в одной сети

Проверьте, что оба контейнера находятся в одной сети:

docker network inspect spark-postgres-network

В выводе команды вы должны увидеть оба контейнера (PostgreSQL и Spark) под одним и тем же идентификатором сети.

4. Проверьте подключение

Выполните внутри контейнера Spark тестовый telnet на порт PostgreSQL:

docker exec -it <имя_контейнера_spark> bash
telnet postgres-db 5432

Если соединение успешно, значит контейнеры теперь могут взаимодействовать.

5. Проверьте URL JDBC

Теперь в вашем скрипте Scala используйте имя сервиса PostgreSQL как хост:

val jdbcUrl = "jdbc:postgresql://postgres-db:5432/mydb"

Попробуйте снова выполнить ваш скрипт Spark. Если возникнут ошибки, поделитесь новыми логами, и мы их разберем.




Запускаем скрипт с указанием библиотеки
```bash
spark-shell --packages com.crealytics:spark-excel_2.12:3.5.1_0.20.4 -i /var/lib/mydir/d1.scala --conf "spark.driver.extraJavaOptions=-Dfile.encoding=utf-8"
```