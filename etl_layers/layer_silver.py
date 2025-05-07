from etl_layers.utils import get_spark_session
from etl_layers.paths import bronze_path, silver_path, control_path  # mova control_path para paths.py
from delta.tables import DeltaTable
from pyspark.sql.functions import col, lower, current_timestamp, max as spark_max
from datetime import datetime
from pyspark.sql import Row

def get_last_processed_version(spark):
    try:
        df = spark.read.format("delta").load(control_path)
        return df.agg(spark_max("version")).first()[0] or -1
    except:
        return -1

def save_last_processed_version(spark, version):
    df = spark.createDataFrame([Row(version=version, timestamp=datetime.now())])
    df.write.format("delta").mode("append").save(control_path)

def run_silver_etl():
    spark = get_spark_session("SilverLayer")

    # Tabela Delta da Bronze
    bronze_table = DeltaTable.forPath(spark, bronze_path)
    latest_version = bronze_table.history(1).select("version").first()["version"]
    last_processed = get_last_processed_version(spark)

    if latest_version == last_processed:
        print("Nenhuma nova mudança na Bronze.")
        spark.stop()
        return

    # Leitura apenas das mudanças via CDF
    df_changes = spark.read.format("delta") \
        .option("readChangeData", "true") \
        .option("startingVersion", last_processed + 1) \
        .option("endingVersion", latest_version) \
        .load(bronze_path)

    df_changes = df_changes.filter(col("_change_type").isin("insert", "update_postimage"))

    if df_changes.rdd.isEmpty():
        print("Nenhum dado relevante para processar.")
        spark.stop()
        return

    # Transformações
    df_silver = df_changes.select(
        "id", "name", "brewery_type", "city", "state", "country",
        "longitude", "latitude", "phone", "website_url",
        "line_created_at", "line_updated_at"
    ).dropna(subset=["id", "name", "brewery_type", "state", "city"])

    df_silver = df_silver.withColumn("city", lower(col("city"))) \
                         .withColumn("state", lower(col("state"))) \
                         .withColumn("country", lower(col("country"))) \
                         .withColumn("silver_loaded_at", current_timestamp())

    df_silver.write.format("delta") \
        .mode("append") \
        .partitionBy("country", "state", "city") \
        .save(silver_path)

    save_last_processed_version(spark, latest_version)
    print(f"Silver atualizado com mudanças da versão {last_processed + 1} até {latest_version}")
    spark.stop()