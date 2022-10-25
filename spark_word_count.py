from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

# PARA EXECUTAR: EM UM TERMINAL:
# nc -lk 9999
# NO OUTRO TERMINAL
# python spark_word_count.py localhost 9999
# Para testar, só escrever e dar enter no terminal com o netcat

# Exemplo:
# $ nc -lk 9999
# Eu sou o douglas
# SAIDA >>>>>>>>>>>>
# -------------------------------------------                                     
# Batch: 1
# -------------------------------------------
# +-------+-----+
# |   word|count|
# +-------+-----+
# |     Eu|    1|
# |    sou|    1|
# |      o|    1|
# |douglas|    1|
# +-------+-----+
spark = SparkSession \
    .builder \
    .appName("StructuredNetworkWordCount") \
    .getOrCreate()

# Create DataFrame representing the stream of input lines from connection to localhost:9999
lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# Split the lines into words
words = lines.select(
   explode(
       split(lines.value, " ")
   ).alias("word")
)

# Generate running word count
wordCounts = words.groupBy("word").count()

 # Start running the query that prints the running counts to the console
query = wordCounts \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()