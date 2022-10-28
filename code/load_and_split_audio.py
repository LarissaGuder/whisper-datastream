import pandas as pd
import json
from pydub import AudioSegment
from pydub.silence import split_on_silence
import pydub
from pydub.utils import make_chunks
import numpy as np
import time
import whisper
start_time = time.time()

model = whisper.load_model("base")

# sound = AudioSegment.from_wav("./audio2.wav")
sound = AudioSegment.from_mp3(
    "../Watch Barack Obama’s Full Speech At The 2020 DNC _ NBC News.mp3")

# Set to mono
sound = sound.set_channels(1)

# Split audio on silence.
chunks = split_on_silence(
    sound,
    # split on silences longer than 1000ms (1 sec)
    min_silence_len=500,
    # anything under -16 dBFS is considered silence
    silence_thresh=-40,
)


target_length = 30 * 1000

output_chunks = [chunks[0]]
for chunk in chunks[1:]:
    if len(output_chunks[-1]) < target_length:
        output_chunks[-1] += chunk
    else:
        # if the last output chunk is longer than the target length,
        # we can start a new one
        output_chunks.append(chunk)


for i, chunk in enumerate(chunks):
    output_file = "../audio/chunk{0}.wav".format(i)
    print("Exporting file", output_file)
    chunk.export(output_file, format="wav")

print("--- %s seconds to pre process---" % (time.time() - start_time))
