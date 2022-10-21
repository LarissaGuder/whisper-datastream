from pydub import AudioSegment
from pydub.silence import split_on_silence
import pydub
import numpy as np 
import time
import whisper
model = whisper.load_model("base")

sound = AudioSegment.from_wav("./audio2.wav")
# sound = AudioSegment.from_mp3("./Gusttavo Lima é o SUS do sertanejo _ Choque de Cultura - Ambiente de Música #CORTE.mp3")

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

start_time = time.time()

target_length = 10 * 1000
# print(chunks)
# output_chunks = [chunks[0]]
# for chunk in chunks[1:]:
#     if len(output_chunks[-1]) < target_length:
#         output_chunks[-1] += chunk
#     else:
#         # if the last output chunk is longer than the target length,
#         # we can start a new one
#         output_chunks.append(chunk)

for chunk in chunks:
    audio = np.frombuffer(chunk.get_array_of_samples(), np.int16).flatten().astype(np.float32) / 32768.0
    audio = whisper.pad_or_trim(audio)
    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    # detect the spoken language
    # _, probs = model.detect_language(mel)
    # print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    #  to define the language >> language = 'portuguese'
    options = whisper.DecodingOptions(fp16 = False)
    result = whisper.decode(model, mel, options)

    # print the recognized text
    print(result.text)


print("--- %s seconds ---" % (time.time() - start_time))
