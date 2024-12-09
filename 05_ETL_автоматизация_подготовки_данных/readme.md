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
