from pyspark.sql.functions import count
from helpers.sessao_spark import get_spark_session
from helpers.paths import silver_path, gold_path

def run_gold_etl():
       spark = get_spark_session("GoldETL")

       # Lê os dados da camada Silver
       df_silver = spark.read.format("delta").load(silver_path)

       # Agrega: quantidade de cervejarias por tipo e localização
       df_gold = df_silver.groupBy("country", "state", "city", "brewery_type") \
                            .agg(count("*").alias("brewery_count"))

       # Grava como Delta na camada Gold particionando por localização
       df_gold.write.format("delta") \
              .mode("overwrite") \
              .partitionBy("country", "state", "city") \
              .save(gold_path)

       print("✅ Gold Layer atualizada com agregações por tipo e local.")

       spark.stop()

run_gold_etl()