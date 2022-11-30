from bert_NER import NER
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.sql.types import *
import whisper
model = whisper.load_model("base")
import time
start_time = time.time()

spark = SparkSession \
    .builder \
    .appName("WhisperStreaming") \
    .getOrCreate()
# StructField("languagesAtWork",ArrayType(StringType()),True),
schema = StructType().add("audio", ArrayType(
    FloatType(), False)).add("file", StringType())
spark.conf.get("spark.sql.adaptive.enabled")
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

print(f"Streaming DataFrame: {df.isStreaming}")


sentence_dictionary = {}


def transcribe(df, epochId):
    audio = df.collect()[0][0]
    path = df.collect()[0][1]

    audio = np.array(audio, dtype=np.float32)

    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    # print(f"Language: {max(probs, key=probs.get)}")

    # decode the audio
    #  to define the language >> language = 'portuguese'
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)
    # ner_results = nlp(result.text)
    ner = NER(result.text)

    persons = []
    final = result.text
    for token in ner.ents:
        if token.label_ == 'PERSON':
            persons.append(token.text)
            if token.text in sentence_dictionary:
                sentence_dictionary[token.text] += 1
            else:
                sentence_dictionary[token.text] = 1
    
    for person in persons:
        final = final.replace(person, "|" + person +"]")
    
    # for item in ner:
    #     print(item)
    #     if item['entity'] == 'B-PER':
    #         if item['word'] in sentence_dictionary:
    #             sentence_dictionary[item['word']] += 1
    #         else:
    #             sentence_dictionary[item['word']] = 1
    # print the recognized text
    path = path.replace('.mp3', '.txt')
    with open("../output_txt/"+path, 'w') as f:
        f.write(final.upper())
    print(f"Lang: {max(probs, key=probs.get)} >>>> ")
    print("-------------------------------------------")
    print(f" | {result.text} | ")
    print("-------------------------------------------")

    print(f" | PERSON cited >>  {sentence_dictionary} | ")
    print(f"--- seconds ---  {(time.time() - start_time)}")

    return (result.text)


df.writeStream.foreachBatch(transcribe).start().awaitTermination()
