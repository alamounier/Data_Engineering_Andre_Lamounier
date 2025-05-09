import logging
import os
import shutil
from pyspark.sql.functions import count, current_timestamp
from helpers.sessao_spark import get_spark_session
from helpers.paths import silver_path, gold_path

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def run_gold_etl():
    # Etapa 1: Inicia a sessão Spark
    logging.info("Iniciando sessão Spark para camada Gold.")
    spark = get_spark_session("GoldETL")

    # Etapa 2: Lê os dados da camada Silver
    logging.info(f"Lendo dados da camada Silver a partir de: {silver_path}")
    df_silver = spark.read.format("delta").load(silver_path)

    # Etapa 3: Agrega a contagem de cervejarias por localização e tipo
    logging.info("Agregando quantidade de cervejarias por tipo e localização.")
    df_gold = df_silver.groupBy("country", "state", "city", "brewery_type") \
                       .agg(count("*").alias("brewery_count"))

    # Etapa 4: Adiciona timestamp da última atualização
    logging.info("Adicionando coluna 'updated_at' com timestamp atual.")
    df_gold = df_gold.withColumn("updated_at", current_timestamp())

    # Etapa 5: Remove a pasta gold caso exista (overwrite local)
    if os.path.exists(gold_path): 
        logging.warning(f"Pasta '{gold_path}' já existe. Excluindo antes de sobrescrever.")
        shutil.rmtree(gold_path)

    # Etapa 6: Escreve os dados no formato Delta
    logging.info("Gravando dados agregados na camada Gold.")
    df_gold.write.format("delta") \
           .mode("overwrite") \
           .option("mergeSchema", "true") \
           .save(gold_path)

    logging.info("✅ Camada Gold atualizada com sucesso.")
    spark.stop()
    logging.info("Sessão Spark finalizada.")

# Dispara o processo
run_gold_etl()