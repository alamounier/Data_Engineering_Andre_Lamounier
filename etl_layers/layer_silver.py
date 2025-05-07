from etl_layers.utils import get_spark_session
from etl_layers.paths import bronze_path, silver_path
from pyspark.sql.functions import col, lower

def run_silver():
    spark = get_spark_session("SilverLayer")

    # Lê os dados da camada Bronze
    df_bronze = spark.read.parquet(bronze_path)

    # Limpeza e transformação (exemplo)
    df_silver = df_bronze.select(
        "id", "name", "brewery_type", "city", "state", "country",
        "longitude", "latitude", "phone", "website_url",
        "line_created_at", "line_updated_at"
    ).dropna(subset=["id", "name", "brewery_type", "state", "city"])

    # Exemplo de padronização de campos
    df_silver = df_silver.withColumn("city", lower(col("city"))) \
                         .withColumn("state", lower(col("state"))) \
                         .withColumn("country", lower(col("country")))

    # Escrita com particionamento por localização
    df_silver.write.mode("overwrite") \
        .partitionBy("country", "state", "city") \
        .parquet(silver_path)

    spark.stop()