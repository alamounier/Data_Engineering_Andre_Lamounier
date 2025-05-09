from helpers.sessao_spark import get_spark_session
from helpers.paths import bronze_path, silver_path 
from delta.tables import DeltaTable
from pyspark.sql.functions import col, current_timestamp
from pyspark.sql.functions import col, length
from pyspark.sql.functions import col, length
from pyspark.sql.functions import coalesce, lit
import os
import shutil

def run_silver_etl():
    spark = get_spark_session("SilverLayer")

    # Tabela Delta da Bronze
    bronze_table = DeltaTable.forPath(spark, bronze_path)
    df_bronze = spark.read.format("delta").option("versionAsOf", 0).load(bronze_path)


    # Cria o DataFrame da camada Silver
    df_silver = df_bronze.select(
        "id", "name", "brewery_type", "address_1", "address_2", "address_3", 
        "city", "state_province", "postal_code", "country", 
        "longitude", "latitude", "phone", "website_url", 
        "state", "street"
    )
    
    # Valida dados inválidos
    invalid_records = df_silver.filter(
        (col("id").isNull()) | (length(col("id")) <= 1) |
        (col("name").isNull()) | (length(col("name")) <= 1)
    )

    if invalid_records.count() > 0:
        raise ValueError("Dados inválidos detectados: existem registros com 'id' "
                         "ou 'name' nulos ou com 1 caractere ou menos.")
    
    #para o particionamento, lidando com nulls
    df_silver = df_silver.withColumn("country", coalesce(col("country"), lit("unknown")))
    df_silver = df_silver.withColumn("state", coalesce(col("state"), lit("unknown")))
    df_silver = df_silver.withColumn("city", coalesce(col("city"), lit("unknown")))

    # Adiciona timestamp
    df_silver = df_silver.withColumn("silver_created_at", current_timestamp())

    # Excluir a pasta silver caso exista (alternativa para overwrite local)
    if os.path.exists(silver_path): 
        shutil.rmtree(silver_path) 

    # Escreve a tabela Silver particionada
    df_silver.write.format("delta") \
        .mode("overwrite") \
        .option("mergeSchema", "true") \
        .partitionBy("country", "state", "city") \
        .save(silver_path)

    print(f"✅ Dados gravados com CDF em: {silver_path}")
    spark.stop()

run_silver_etl()