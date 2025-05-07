import requests
from datetime import datetime
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
from pyspark.sql.functions import lit, to_timestamp, col
from etl_layers.utils import get_spark_session
from etl_layers.paths import bronze_path
from delta.tables import DeltaTable


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

    # 4. Cria DataFrame
    df = spark.createDataFrame(all_data, schema=schema)

    # 5. Adiciona timestamps
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = df.withColumn("line_created_at", to_timestamp(lit(now_str))) \
        .withColumn("line_updated_at", to_timestamp(lit(now_str)))

    # 6. Cria/atualiza camada Bronze Delta com CDC
    if DeltaTable.isDeltaTable(spark, bronze_path):
        bronze_delta = DeltaTable.forPath(spark, bronze_path)

        # Faz merge baseado no ID
        # Se algum campo relevante tiver mudado, insere nova linha (append)
        existing_df = bronze_delta.toDF()
        updated_df = df.alias("new")

        # Join para encontrar diferenças
        join_condition = "existing.id = new.id"
        changes_df = updated_df.join(
            existing_df.alias("existing"), on="id", how="left_outer"
        ).filter(
            (col("existing.id").isNull()) |  # novo ID
            (col("new.name") != col("existing.name")) |
            (col("new.city") != col("existing.city")) |
            (col("new.postal_code") != col("existing.postal_code"))
            # adicione mais comparações se necessário
        ).select("new.*")

        if changes_df.count() > 0:
            changes_df.write.format("delta").mode("append").save(bronze_path)
            print(f"Novos dados inseridos via CDC em: {bronze_path}")
        else:
            print("Nenhuma alteração detectada.")
    else:
        df.write.format("delta").mode("overwrite").save(bronze_path)
        print(f"Camada Bronze inicial criada em: {bronze_path}")