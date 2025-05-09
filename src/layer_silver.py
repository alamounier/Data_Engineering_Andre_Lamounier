import logging
import os
import shutil
from helpers.sessao_spark import get_spark_session
from helpers.paths import bronze_path, silver_path 
from delta.tables import DeltaTable
from pyspark.sql.functions import col, current_timestamp, length, coalesce, lit

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def run_silver_etl():
    # Etapa 1: Inicia a sessão Spark
    logging.info("Inicializando sessão Spark para camada Silver.")
    spark = get_spark_session("SilverLayer")

    # Etapa 2: Lê dados da camada Bronze (versão 0 por controle de versionamento)
    logging.info("Lendo dados da camada Bronze (versionAsOf = 0).")
    bronze_table = DeltaTable.forPath(spark, bronze_path)
    df_bronze = spark.read.format("delta").option("versionAsOf", 0).load(bronze_path)

    # Etapa 3: Seleciona e organiza as colunas relevantes
    logging.info("Selecionando colunas relevantes para a camada Silver.")
    df_silver = df_bronze.select(
        "id", "name", "brewery_type", "address_1", "address_2", "address_3", 
        "city", "state_province", "postal_code", "country", 
        "longitude", "latitude", "phone", "website_url", 
        "state", "street"
    )
    
    # Etapa 4: Validação de registros inválidos (nulos ou muito curtos)
    logging.info("Validando registros nulos ou com IDs/Nomes inválidos.")
    invalid_records = df_silver.filter(
        (col("id").isNull()) | (length(col("id")) <= 1) |
        (col("name").isNull()) | (length(col("name")) <= 1)
    )

    if invalid_records.count() > 0:
        logging.error("❌ Dados inválidos encontrados.")
        raise ValueError("Dados inválidos detectados: existem registros com 'id' ou 'name' nulos ou muito curtos.")
    
    # Etapa 5: Trata valores nulos para colunas de particionamento
    logging.info("Tratando valores nulos para colunas de particionamento.")
    df_silver = df_silver.withColumn("country", coalesce(col("country"), lit("unknown")))
    df_silver = df_silver.withColumn("state", coalesce(col("state"), lit("unknown")))
    df_silver = df_silver.withColumn("city", coalesce(col("city"), lit("unknown")))

    # Etapa 6: Adiciona coluna de timestamp
    logging.info("Adicionando coluna de timestamp (silver_created_at).")
    df_silver = df_silver.withColumn("silver_created_at", current_timestamp())

    # Etapa 7: Limpa a pasta silver se já existir (overwrite local)
    if os.path.exists(silver_path): 
        logging.warning(f"Pasta '{silver_path}' já existe. Excluindo antes de sobrescrever.")
        shutil.rmtree(silver_path)

    # Etapa 8: Escreve os dados da Silver particionando por país, estado e cidade
    logging.info("Gravando dados no Delta particionados por country/state/city.")
    df_silver.write.format("delta") \
        .mode("overwrite") \
        .option("mergeSchema", "true") \
        .partitionBy("country", "state", "city") \
        .save(silver_path)

    logging.info(f"✅ Dados gravados com sucesso na camada Silver: {silver_path}")
    spark.stop()
    logging.info("Sessão Spark finalizada.")

# Dispara o processo
run_silver_etl()