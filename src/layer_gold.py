from pyspark.sql.functions import count
from helpers.sessao_spark import get_spark_session
from helpers.paths import silver_path, gold_path
from pyspark.sql.functions import current_timestamp
import os
import shutil

def run_gold_etl():
       spark = get_spark_session("GoldETL")

       # Lê os dados da camada Silver
       df_silver = spark.read.format("delta").load(silver_path)

       # Agrega: quantidade de cervejarias por tipo e localização
       df_gold = df_silver.groupBy("country", "state", "city", "brewery_type") \
                            .agg(count("*").alias("brewery_count"))
       
       df_gold = df_gold.withColumn("updated_at",current_timestamp())

       # Excluir a pasta silver caso exista (alternativa para overwrite local)
       if os.path.exists(gold_path): 
              shutil.rmtree(gold_path)

       # Grava como Delta na camada Gold particionando por localização
       df_gold.write.format("delta") \
              .mode("overwrite") \
              .option("mergeSchema", "true") \
              .save(gold_path)

       print("✅ Gold Layer atualizada com agregações por tipo e local.")

       spark.stop()

run_gold_etl()