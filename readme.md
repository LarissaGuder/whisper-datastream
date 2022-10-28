## Requirements 
Python 3.8.10

### for whisper

`pip install git+https://github.com/openai/whisper.git`

`pip install setuptools-rust`

`choco install ffmpeg`

### Req for spark

`pip install pyspark`

### All dependencies

`pip3 install -r requirements.txt`

## How it works
In the code folder, we have 3 files.

You can start the `spark_stream` when you want. They will wait to have json files in the files folder.

In another terminal, you must run `load_and_split_audio`. They will create .wav files in the audio folder.
This audios will be processed by the `generate_array`.
When you run they, json files with the np.array of the audio files will be created, and feed the stream input. 
