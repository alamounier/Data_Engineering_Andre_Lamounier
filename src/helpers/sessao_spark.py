from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip


def get_spark_session(app_name="ETLApp") -> SparkSession:
    """
    Cria e retorna uma SparkSession configurada para uso local com suporte ao Delta Lake.

    Parâmetros:
    -----------
    app_name : str
        Nome do aplicativo Spark (default: "ETLApp").

    Configurações aplicadas:
    -------------------------
    - master("local[*]"): Executa o Spark localmente utilizando todos os núcleos disponíveis.
    - spark.driver.memory: Define 2 GB de memória para o driver.
    - spark.executor.memory: Define 2 GB de memória para o executor.
    - spark.sql.shuffle.partitions: Define o número de partições para operações de shuffle (join, groupBy etc.) como 4.
    - spark.default.parallelism: Define o grau padrão de paralelismo como 4.
    - spark.sql.extensions: Habilita a extensão Delta Lake no Spark.
    - spark.sql.catalog.spark_catalog: Define o catálogo Delta como padrão para operações SQL.
    - spark.databricks.delta.retentionDurationCheck.enabled: Desabilita a verificação de retenção para operações como `vacuum`.
    - spark.hadoop.fs.file.impl: Usa `RawLocalFileSystem` para evitar a criação de arquivos `.crc` ao escrever localmente.

    Retorna:
    --------
    SparkSession
        Instância configurada da SparkSession pronta para uso com Delta Lake.
    """
    builder = SparkSession.builder \
        .appName(app_name) \
        .master("local[*]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "2g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.default.parallelism", "4") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.databricks.delta.retentionDurationCheck.enabled", "false") \
        .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.RawLocalFileSystem")  # <- evita arquivos .crc

    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    return spark