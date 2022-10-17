import pandas as pd
from pyspark.sql.functions import pandas_udf
from pyspark.sql import SparkSession
import whisper
from pyspark.ml import Pipeline
from pyspark import SparkConf, SparkContext
#  https://www.analyticsvidhya.com/blog/2019/11/build-machine-learning-pipelines-pyspark/


def main(spark):
    # conf = SparkConf().setAppName("Whisper")
    # sc = SparkContext(conf=spark)

    # lista = ["https://mmlspark.blob.core.windows.net/datasets/Speech/audio2.wav",
    #                        "https://mmlspark.blob.core.windows.net/datasets/Speech/audio3.mp3"]
    # distLista = sc.parallelize(lista)
    # # Create a dataframe with our audio URLs, tied to the column called "url"
    # df = spark.createDataFrame([("https://mmlspark.blob.core.windows.net/datasets/Speech/audio2.wav",),
    #                        ("https://mmlspark.blob.core.windows.net/datasets/Speech/audio3.mp3",)
    #                        ], ["url"])

    # a = df.limit(1).toPandas()
    
    # print(a['url'][0])

    model = whisper.load_model("base")

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio("Spark Streaming with Python under 12 minutes.mp3")
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    for x in audio:
        print(x)
        # mel = whisper.log_mel_spectrogram(x).to(model.device)

        # # detect the spoken language
        # _, probs = model.detect_language(mel)
        # print(f"Detected language: {max(probs, key=probs.get)}")

        # # decode the audio
        # options = whisper.DecodingOptions(fp16 = False)
        # result = whisper.decode(model, mel, options)

        # # print the recognized text
        # print(result.text)

if __name__ == "__main__":
    main(SparkSession.builder.getOrCreate())