import logging
import requests
from datetime import datetime
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from helpers.sessao_spark import get_spark_session
from helpers.paths import bronze_path
from pyspark.sql.functions import current_timestamp

# Configuração básica do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def run_bronze_etl():
    # Etapa 1: Inicia a sessão Spark
    logging.info("Inicializando sessão Spark.")
    spark = get_spark_session("BronzeETL")

    # Etapa 2: Configurações da API e variáveis de controle
    base_url = "https://api.openbrewerydb.org/v1/breweries"
    all_data = []
    page = 1
    per_page = 50

    # Etapa 3: Extração paginada de dados da API
    logging.info("Iniciando extração da API paginada.")
    while page < 10:
        logging.info(f"Requisitando página {page}...")
        response = requests.get(base_url, params={"page": page, "per_page": per_page})
        if response.status_code != 200:
            logging.error(f"Erro na página {page}: {response.status_code}")
            break

        page_data = response.json()
        if not page_data:
            logging.info("Nenhum dado retornado. Encerrando paginação.")
            break

        all_data.extend(page_data)
        logging.info(f"Página {page} com {len(page_data)} registros coletada.")
        page += 1

    if not all_data:
        logging.warning("Nenhum dado extraído da API.")
        return

    # Etapa 4: Criação do DataFrame com schema explícito
    logging.info("Definindo schema e criando DataFrame.")
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

    # Etapa 5: Adiciona colunas técnicas de controle (timestamp)
    df = df.withColumn("line_created_at", current_timestamp()) \
           .withColumn("line_updated_at", current_timestamp())

    # Etapa 6: Escrita no caminho Bronze em formato Delta com CDF
    logging.info("Escrevendo dados no Delta com CDF.")
    df = df.coalesce(1)
    df.write.format("delta") \
        .option("mergeSchema", "true") \
        .option("delta.enableChangeDataFeed", "true") \
        .mode("overwrite") \
        .save(bronze_path)

    # Etapa 7: Finaliza a sessão Spark
    logging.info(f"✅ Dados gravados com sucesso em: {bronze_path}")
    spark.stop()
    logging.info("Sessão Spark finalizada.")

# Dispara o processo
run_bronze_etl()