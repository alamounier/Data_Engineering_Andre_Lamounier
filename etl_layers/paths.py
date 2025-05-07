# Prefixo do bucket MinIO
bucket = "meu-bucket"

# Caminhos para as camadas do data lake
bronze_path = f"s3a://{bucket}/bronze/list_breweries/"
silver_path = f"s3a://{bucket}/silver/list_breweries/"
gold_path = f"s3a://{bucket}/gold/agg_breweries/"
