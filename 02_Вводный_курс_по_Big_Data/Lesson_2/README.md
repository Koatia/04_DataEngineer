[Михаил Лебедев](https://github.com/MichaelSwanRu)

### Установка Hadoop

1. Скопируйте репозиторий:

```bash
git clone https://github.com/Wittline/apache-spark-docker.git
```

2. Перейдите в папку с файлом (docker-compose.jml), выполните команду:

```bash
docker compose up -d
```

```
[+] Running 13/13
 ✔ Network docker_default               Created                                        0.1s 
 ✔ Container database                   Started                                        0.9s 
 ✔ Container jupyterlab                 Started                                        0.9s 
 ✔ Container namenode                   Started                                        0.9s 
 ✔ Container hue                        Started                                        0.9s 
 ✔ Container datanode1                  Started                                        1.0s 
 ✔ Container datanode2                  Started                                        1.0s 
 ✔ Container hive-metastore-postgresql  Start...                                       1.0s 
 ✔ Container hive_metastore             Started                                        1.1s 
 ✔ Container hive-server                Started                                        1.1s 
 ✔ Container spark-master               Started                                        1.2s 
 ✔ Container spark-worker-2             Started                                        1.4s 
 ✔ Container spark-worker-1             Started                                        1.4s 
```


Подключаемся к БД в контейнере

```bash
docker exec -it hive-server beeline -u 'jdbc:hive2://localhost:10000/'
```

```
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/opt/hive/lib/log4j-slf4j-impl-2.6.2.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/opt/hadoop-2.7.4/share/hadoop/common/lib/slf4j-log4j12-1.7.10.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]
Connecting to jdbc:hive2://localhost:10000/
Connected to: Apache Hive (version 2.3.2)
Driver: Hive JDBC (version 2.3.2)
Transaction isolation: TRANSACTION_REPEATABLE_READ
Beeline version 2.3.2 by Apache Hive
0: jdbc:hive2://localhost:10000/> show tables;
+-------------+
|  tab_name   |
+-------------+
| hive_table  |
+-------------+
1 row selected (0.492 seconds)
0: jdbc:hive2://localhost:10000/> select * from hive_table limit 20;
+----------------+----------------+---------------------------------------------+-------------------+
| hive_table.c4  | hive_table.id  |                hive_table.c2                |   hive_table.c3   |
+----------------+----------------+---------------------------------------------+-------------------+
| PR             | 6680           | Cuylers Airport                             | Vega Baja         |
| MH             | 4650           | Utirik Airport                              | Utirik Island     |
| PR             | 349103         | Advanced Public Health of Isabela Heliport  | Isabela           |
| MP             | 4777           | Dynasty Heliport                            | San Jose, Tinian  |
| PR             | 7793           | Villamil-304 Ponce De Leon Heliport         | San Juan          |
| PR             | 330679         | Emp. Coco Beach Golf Club LLC Heliport      | Rio Grande        |
| PR             | 8626           | San Patricio Heliport                       | Guaynabo          |
| PR             | 9222           | La Concepcion Hospital Heliport             | San German        |
| PR             | 46121          | Caribbean Constr Main Office Heliport       | Guaynabo          |
| PR             | 346082         | PR Police-Ponce Area Heliport               | Ponce             |
| GU             | 328149         | Barrigada Readiness Center Heliport         | Barrigada         |
| PR             | 353053         | Cesar Castillo LLC Heliport                 | Guaynabo          |
| SO             | 324756         | Adado Airport                               | Adado             |
| AQ             | 30609          | Aer?dromo de Punto Rothera                  | Rothera Point     |
| GB             | 307979         | RAF Calveley                                | Cheshire          |
| GB             | 302247         | RNAS/RAF Calshot                            | Hampshire         |
| PG             | 301645         | Atkamba Airport                             | Atkamba Mission   |
| PG             | 321987         | Abau Airport                                | Abau              |
| PH             | 507217         | Woodland Airpark                            | Magalang          |
| CO             | 41025          | Arica Airport                               | Arica             |
+----------------+----------------+---------------------------------------------+-------------------+
20 rows selected (1.089 seconds)
```

```bash
docker compose down
```

```
[+] Running 13/13
 ✔ Container jupyterlab                 Removed               10.3s 
 ✔ Container spark-worker-2             Removed               10.3s 
 ✔ Container spark-worker-1             Removed               10.3s 
 ✔ Container hue                        Removed               10.3s 
 ✔ Container database                   Removed                1.5s 
 ✔ Container spark-master               Removed               10.2s 
 ✔ Container hive-server                Removed               10.2s 
 ✔ Container hive_metastore             Removed                0.6s 
 ✔ Container hive-metastore-postgresql  Removed                0.4s 
 ✔ Container datanode1                  Removed               10.3s 
 ✔ Container datanode2                  Removed               10.2s 
 ✔ Container namenode                   Removed               10.2s 
 ✔ Network docker_default               Removed                0.1s
 ```
