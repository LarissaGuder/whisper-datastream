import pyaudio
import wave
import numpy as np
import json
import time
import os
def exact_div(x, y):
    assert x % y == 0
    return x // y

SAMPLE_RATE = 16000
N_FFT = 400
N_MELS = 80
HOP_LENGTH = 160
CHUNK_LENGTH = 30
N_SAMPLES = CHUNK_LENGTH * SAMPLE_RATE  # 480000: number of samples in a chunk
CHUNK = exact_div(N_SAMPLES, HOP_LENGTH)  # 3000: number of frames in a mel spectrogram input

# CHUNK = 44100
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 30
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
 
number_file = 0
while True:
    print("* recording") 

    frames = []

    for i in range(0, int(RATE / CHUNK * 10)):
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16).flatten().astype(np.float32) / 32768.0
        frames.extend(audio_data)

    # data = stream.read(CHUNK)
    # audio_data = np.frombuffer(data, dtype=np.int16).flatten().astype(np.float32) / 32768.0
    path_json = "../temp/live" + str(number_file) + ".json"
    json.dump({'audio': np.array(frames).tolist()}, open(path_json, "w"), ensure_ascii=False)
    # with open(path_csv, 'w') as f:
    #     json.dump({'audio': np.array(frames).tolist()}, f, ensure_ascii=False)
    os.rename(path_json, "../files/live" + str(number_file) + ".json")
    print("* done recording")
    number_file+=1

stream.stop_stream()
stream.close()
p.terminate()