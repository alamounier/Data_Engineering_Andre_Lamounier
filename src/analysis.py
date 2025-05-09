from pyspark.sql.functions import desc, countDistinct, col

from helpers.paths import gold_path
from helpers.sessao_spark import get_spark_session

spark = get_spark_session()

# Read the Delta table
df = spark.read.format("delta").load(gold_path)

# 1. Sort by the brewery_count column from highest to lowest and show the city with the highest brewery_count
city_with_most_breweries = df.orderBy(desc("brewery_count")).first()
print(f"City with the most breweries: {city_with_most_breweries['city']} ({city_with_most_breweries['brewery_count']})")

# 2. The country that appears the most and the one that appears the least
most_common_country = df.groupBy("country").count().orderBy(desc("count")).first()
least_common_country = df.groupBy("country").count().orderBy("count").first()

print(f"Country that appears the most: {most_common_country['country']} ({most_common_country['count']})")
print(f"Country that appears the least: {least_common_country['country']} ({least_common_country['count']})")

# 3. Number of distinct cities
distinct_cities_count = df.select(countDistinct("city")).collect()[0][0]
print(f"Number of distinct cities: {distinct_cities_count}")

# 4. Show the top 10 cities sorted by brewery_count
df.orderBy(desc("brewery_count")).show(10)