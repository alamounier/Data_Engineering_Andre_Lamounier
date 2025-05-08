from etl_layers.layer_bronze import run_bronze_etl
from etl_layers.layer_silver import run_silver_etl
from etl_layers.layer_gold import run_gold_etl

run_bronze_etl()
run_silver_etl()
run_gold_etl()


# import os
# import requests
# from datetime import datetime
# from pyspark.sql import SparkSession
# from pyspark.sql.types import StructType, StructField, StringType, DoubleType
# from pyspark.sql.functions import lit, to_timestamp

# # Horário atual formatado no padrão brasileiro
# now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
# print(now_str)

# # Configurações do MinIO
# minio_endpoint = "http://minio:9000"
# access_key = "minioadmin"
# secret_key = "minioadmin"
# bucket_name = "meu-bucket"
# file_name = "list_breweries_bronze"

# # URL base da API
# base_url = "https://api.openbrewerydb.org/v1/breweries"
# all_data = []
# page = 1
# per_page = 50  # Número máximo por página que a API permite

# while True:
#     response = requests.get(base_url, params={"page": page, "per_page": per_page})
#     if response.status_code != 200:
#         print(f"Erro na página {page}: {response.status_code}")
#         break
#     page_data = response.json()
#     if not page_data:
#         break  # Sai do loop se não houver dados (última página)
#     all_data.extend(page_data)
#     print(f"Página {page} com {len(page_data)} registros coletada.")
#     page += 1


# # Inicializa Spark

# spark = SparkSession.builder \
#     .appName("ExemploMinIO") \
#     .master("local[4]") \
#     .config("spark.driver.memory", "2g") \
#     .config("spark.executor.memory", "2g") \
#     .config("spark.sql.shuffle.partitions", "4") \
#     .config("spark.default.parallelism", "4") \
#     .config("spark.jars", "/opt/spark/jars/hadoop-aws-3.3.1.jar,/opt/spark/jars/aws-java-sdk-bundle-1.11.901.jar") \
#     .config("spark.hadoop.fs.s3a.endpoint", minio_endpoint) \
#     .config("spark.hadoop.fs.s3a.access.key", access_key) \
#     .config("spark.hadoop.fs.s3a.secret.key", secret_key) \
#     .config("spark.hadoop.fs.s3a.path.style.access", "true") \
#     .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
#     .config("spark.hadoop.fs.s3a.multipart.size", "64M") \
#     .config("spark.hadoop.fs.s3a.fast.upload", "true") \
#     .config("spark.hadoop.fs.s3a.fast.upload.buffer", "disk") \
#     .config("spark.hadoop.fs.s3a.fast.upload.active.blocks", "2") \
#     .getOrCreate()


# # Define o schema com base nos campos retornados pela API
# schema = StructType([
#     StructField("id", StringType(), True),
#     StructField("name", StringType(), True),
#     StructField("brewery_type", StringType(), True),
#     StructField("address_1", StringType(), True),
#     StructField("address_2", StringType(), True),
#     StructField("address_3", StringType(), True),
#     StructField("city", StringType(), True),
#     StructField("state_province", StringType(), True),
#     StructField("postal_code", StringType(), True),
#     StructField("country", StringType(), True),
#     StructField("longitude", DoubleType(), True),
#     StructField("latitude", DoubleType(), True),
#     StructField("phone", StringType(), True),
#     StructField("website_url", StringType(), True),
#     StructField("state", StringType(), True),
#     StructField("street", StringType(), True)
# ])

# # Cria o DataFrame Spark
# df = spark.createDataFrame(all_data, schema=schema)

# # Adiciona colunas com timestamp atual
# df = df \
#     .withColumn("line_created_at", to_timestamp(lit(now_str), "yyyy-MM-dd HH:mm:ss")) \
#     .withColumn("line_updated_at", to_timestamp(lit(now_str), "yyyy-MM-dd HH:mm:ss"))

# # Exibe os dados
# #df.show(truncate=False)

# # Escrever no MinIO
# df.write.mode("overwrite").parquet(f"s3a://{bucket_name}/{file_name}")

# # Ler de volta
# df_lido = spark.read.parquet(f"s3a://{bucket_name}/{file_name}")
# df_lido.show(truncate=False)