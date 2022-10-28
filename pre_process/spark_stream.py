from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.sql.types import *
from pyspark.ml import Pipeline
import whisper
model = whisper.load_model("base")
import numpy as np
# https://medium.com/analytics-vidhya/apache-spark-structured-streaming-with-pyspark-b4a054a7947d

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
# StructField("languagesAtWork",ArrayType(StringType()),True),
schema = StructType().add("audio", ArrayType(FloatType(), False))

# schema = StructType().add("languagesAtSchool", ArrayType(FloatType))
# Create DataFrame representing the stream of input lines from connection to localhost:9999
df = (spark
      .readStream
      .format("json")
      .schema(schema)
      .option("maxFilesPerTrigger", 1)
      .json("../files/*")
      )
df.isStreaming

df.printSchema()
print(df.collect())

print(f"Streaming DataFrame: {df.isStreaming}")

df.writeStream.format("console").start().awaitTermination();

# # arr = np.ndarray(df['audio'])
# a = df.collect()[0][0]

# print(mvv)
def transcribe(audio):
    print(type(audio))
    # audio = whisper.pad_or_trim(audio)
    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    #  to define the language >> language = 'portuguese'
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)

    # print the recognized text
    return (result.text)

# texto = transcribe(arr)

# query = df \
#     .writeStream \
#     .outputMode("complete") \
#     .format("console") \
#     .start().awaitTermination()

# query
# print("Streaming DataFrame : " + df.isStreaming)
# lines = spark \
#     .readStream \
#     .format("socket") \
#     .option("host", "localhost") \
#     .option("port", 9999) \
#     .load()

# # Split the lines into words
# words = lines.select(
#    explode(
#        split(lines.value, " ")
#    ).alias("word")
# )

# # Generate running word count
# wordCounts = words.groupBy("word").count()


#  # Start running the query that prints the running counts to the console

