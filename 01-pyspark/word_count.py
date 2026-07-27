from pyspark.sql import SparkSession
from pyspark.sql.functions import explode,split

spark = SparkSession.builder.appName("WordCount").GetOrCreate()

df = spark.read.text("input.txt")

df_words = df.select(explode(split(df.value," ")).alias("word"))

result = df_words.groupBy("word").count()

result.show()

spark.stop()
