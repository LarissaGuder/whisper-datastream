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

## How reproduce the results

In the code folder, check if in the `generate_array` file the dir path is `dir_path = r'../input/mp3/'`.
It will be necessary that you start the `spark_stream_evaluate` script.
They will start the spark engine, and will save the transcribed results into `output_txt` directory.
After that, run the `generate_array` script, and just wait.
When the process finished on the `spark_stream_evaluate`, you can run the `evaluate` script, where the results will be calculated.

The actual results are:
Precision: 0.41  
Recall: 0.33
F1-Score: 0.37