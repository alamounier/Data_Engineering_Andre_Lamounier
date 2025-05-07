from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

def get_spark_session(app_name="ETLApp") -> SparkSession:
    builder = SparkSession.builder \
        .appName(app_name) \
        .master("local[4]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "2g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.default.parallelism", "4") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.jars", "/opt/spark/jars/hadoop-aws-3.3.1.jar,/opt/spark/jars/aws-java-sdk-bundle-1.11.901.jar") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.multipart.size", "64M") \
        .config("spark.hadoop.fs.s3a.fast.upload", "true") \
        .config("spark.hadoop.fs.s3a.fast.upload.buffer", "disk") \
        .config("spark.hadoop.fs.s3a.fast.upload.active.blocks", "2")

    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    return spark




# from pyspark.sql import SparkSession
# from delta import configure_spark_with_delta_pip

# def get_spark_session(app_name="ETLApp") -> SparkSession:
#     return SparkSession.builder \
#         .appName(app_name) \
#         .master("local[4]") \
#         .config("spark.driver.memory", "2g") \
#         .config("spark.executor.memory", "2g") \
#         .config("spark.sql.shuffle.partitions", "4") \
#         .config("spark.default.parallelism", "4") \
#         .config("spark.jars", "/opt/spark/jars/delta-core_2.12-2.4.0.jar,/opt/spark/jars/hadoop-aws-3.3.1.jar,/opt/spark/jars/aws-java-sdk-bundle-1.11.901.jar") \
#         .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
#         .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
#         .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
#         .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
#         .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
#         .config("spark.hadoop.fs.s3a.path.style.access", "true") \
#         .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
#         .config("spark.hadoop.fs.s3a.multipart.size", "64M") \
#         .config("spark.hadoop.fs.s3a.fast.upload", "true") \
#         .config("spark.hadoop.fs.s3a.fast.upload.buffer", "disk") \
#         .config("spark.hadoop.fs.s3a.fast.upload.active.blocks", "2") \
#         .getOrCreate()
