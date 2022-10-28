import librosa
from itertools import cycle
import IPython.display as ipd
import librosa.display
import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
import whisper
from glob import glob

model = whisper.load_model("base")


def exact_div(x, y):
    assert x % y == 0
    return x // y


# sns.set_theme(style="white", palette=None)
# color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]
# color_cycle = cycle(plt.rcParams["axes.prop_cycle"].by_key()["color"])
plt.use('tkagg')

# Load file
# y, sr = librosa.load("./Gusttavo Lima é o SUS do sertanejo _ Choque de Cultura - Ambiente de Música #CORTE.mp3")
y, sr = librosa.load("./audio2.wav")
print(f'y: {y[:10]}')
print(f'shape y: {y.shape}')
print(f'sr: {sr}')

print("_______________")
# short time fourier transform
# (n_fft and hop lenght dertermine frequency/time resolution)
n_fft = 2048
hop_length = n_fft//2

S = librosa.stft(y, n_fft=n_fft, hop_length=n_fft//2)
print(S.shape)
D = librosa.amplitude_to_db(np.abs(S), ref=np.max)
print(np.max(abs(D)))

non_mute_sections = librosa.effects.split(y)
print(non_mute_sections)

# hard-coded audio hyperparameters THIS IS FROM WHISPER
SAMPLE_RATE = 16000
N_FFT = 400
N_MELS = 80
HOP_LENGTH = 160
CHUNK_LENGTH = 30
N_SAMPLES = CHUNK_LENGTH * SAMPLE_RATE  # 480000: number of samples in a chunk
# 3000: number of frames in a mel spectrogram input
N_FRAMES = exact_div(N_SAMPLES, HOP_LENGTH)

filename = librosa.ex('libri2')
sr = 16000

# librosa streaming
stream = librosa.stream(filename, block_length=N_FRAMES,
                        frame_length=N_FFT,
                        hop_length=HOP_LENGTH,
                        mono=True,
                        fill_value=0,
                        duration=CHUNK_LENGTH)


for y_block in stream:
    D_block = librosa.stft(y_block, center=False)
    mel = whisper.log_mel_spectrogram(y_block).to(model.device)
    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    #  to define the language >> language = 'portuguese'
    options = whisper.DecodingOptions(fp16 = False, language = 'portuguese')
    result = whisper.decode(model, mel, options)

    # print the recognized text
    print(result.text)
