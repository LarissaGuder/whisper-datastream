import json
import numpy as np
import os
import ffmpeg
import json

# dir_path = r'../audio/'
dir_path = r'../input/mp3/'

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
    path_csv = "../files/" + path + ".json"
    with open(path_csv, 'w') as f:
        json.dump({'audio': audio.tolist(), 'file': path}, f, ensure_ascii=False)
