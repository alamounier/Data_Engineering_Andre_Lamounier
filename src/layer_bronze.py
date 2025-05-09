import requests
from datetime import datetime
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from helpers.sessao_spark import get_spark_session
from helpers.paths import bronze_path
from pyspark.sql.functions import current_timestamp


def run_bronze_etl():
    
    spark = get_spark_session("BronzeETL")

    # 1. Extrai os dados da API paginada
    base_url = "https://api.openbrewerydb.org/v1/breweries"
    all_data = []
    page = 1
    per_page = 50

    #while True:
    while page < 10:
        response = requests.get(base_url, params={"page": page, "per_page": per_page})
        if response.status_code != 200:
            print(f"Erro na página {page}: {response.status_code}")
            break

        page_data = response.json()
        if not page_data:
            break

        all_data.extend(page_data)
        print(f"Página {page} com {len(page_data)} registros coletada.")
        page += 1

    if not all_data:
        print("Nenhum dado extraído da API.")
        return

    # 3. Define o schema
    schema = StructType([
        StructField("id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("brewery_type", StringType(), True),
        StructField("address_1", StringType(), True),
        StructField("address_2", StringType(), True),
        StructField("address_3", StringType(), True),
        StructField("city", StringType(), True),
        StructField("state_province", StringType(), True),
        StructField("postal_code", StringType(), True),
        StructField("country", StringType(), True),
        StructField("longitude", DoubleType(), True),
        StructField("latitude", DoubleType(), True),
        StructField("phone", StringType(), True),
        StructField("website_url", StringType(), True),
        StructField("state", StringType(), True),
        StructField("street", StringType(), True)
    ])

    df = spark.createDataFrame(all_data, schema=schema)
    df = df.withColumn("line_created_at", current_timestamp()) \
        .withColumn("line_updated_at", current_timestamp())

    # 7. Grava no Delta com CDF habilitado
    df = df.coalesce(1)
    df.write.format("delta") \
        .option("mergeSchema", "true") \
        .option("delta.enableChangeDataFeed", "true") \
        .mode("overwrite") \
        .save(bronze_path)
    
    print(f"✅ Dados gravados com CDF em: {bronze_path}")
    spark.stop()

run_bronze_etl()