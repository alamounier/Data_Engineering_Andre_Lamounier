import requests
from datetime import datetime
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.functions import lit, to_timestamp
from etl_layers.utils import get_spark_session
from etl_layers.paths import bronze_path

def run_bronze_etl():
    # 1. Extrai os dados da API paginada
    base_url = "https://api.openbrewerydb.org/v1/breweries"
    all_data = []
    page = 1
    per_page = 50

    while True:
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

    # 2. Inicializa sessão Spark
    spark = get_spark_session("BronzeETL")

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

    # 4. Valida se todos os campos esperados estão presentes
    first_record_keys = set(all_data[0].keys())
    expected_keys = set(schema.fieldNames())
    if not expected_keys.issubset(first_record_keys):
        raise ValueError("Mudança no schema da API detectada!")

    # 5. Cria DataFrame
    df = spark.createDataFrame(all_data, schema=schema)

    # 6. Adiciona timestamps
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = df.withColumn("line_created_at", to_timestamp(lit(now_str))) \
           .withColumn("line_updated_at", to_timestamp(lit(now_str)))

    # 7. Grava no Delta com CDF habilitado
    df.write.format("delta") \
        .option("mergeSchema", "true") \
        .option("delta.enableChangeDataFeed", "true") \
        .mode("append") \
        .save(bronze_path)

    print(f"✅ Dados gravados com CDF em: {bronze_path}")
    spark.stop()