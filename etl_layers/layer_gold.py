from etl_layers.utils import get_spark_session
from etl_layers.paths import silver_path, gold_path
from pyspark.sql.functions import count

def run_gold():
    spark = get_spark_session("GoldLayer")

    # Lê os dados da camada Silver
    df_silver = spark.read.parquet(silver_path)

    # Agregação: quantidade de cervejarias por tipo e localidade
    df_gold = df_silver.groupBy("brewery_type", "country", "state", "city") \
        .agg(count("*").alias("brewery_count"))

    df_gold.write.mode("overwrite").parquet(gold_path)

    spark.stop()