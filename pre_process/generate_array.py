import pandas as pd
import json
from pydub import AudioSegment
from pydub.silence import split_on_silence
import pydub
from pydub.utils import make_chunks
import numpy as np
import time
import whisper
import os
import ffmpeg
import json

# model = whisper.load_model("base")

dir_path = r'../audio/'

# list to store files
res = []
SAMPLE_RATE = 16000


def load_audio(file: str, sr: int = SAMPLE_RATE):
    """
    Open an audio file and read as mono waveform, resampling as necessary

    Parameters
    ----------
    file: str
        The audio file to open

    sr: int
        The sample rate to resample the audio if necessary

    Returns
    -------
    A NumPy array containing the audio waveform, in float32 dtype.
    """
    try:
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        out, _ = (
            ffmpeg.input(file, threads=0)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
            .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0


# Iterate directory
for path in os.listdir(dir_path):
    audio = load_audio(dir_path+path)
    listao = ""
    # for i in audio.tolist():
    #     listao = listao + str(i) + ","
    
    path_csv = "../files/i" + path + ".json"
    # print(path_csv)
    # f = open(path_csv,'w')
    # f.write(listao) #Give your csv text here.
    # ## Python will convert \n to os.linesep
    # f.close()

    with open(path_csv, 'w') as f:
        # temp = 'audio'
        json.dump({'audio': audio.tolist()}, f, ensure_ascii=False)
    # df = pd.DataFrame(listao)
    # # Save this shit to file
    # df.to_csv(path_csv, index=False)

    # np.savetxt(path_csv, audio, delimiter=",")
    #    audio = whisper.pad_or_trim(audio)
