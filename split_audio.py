from pydub import AudioSegment
from pydub.silence import split_on_silence
import pydub
import numpy as np 
import time

sound = AudioSegment.from_mp3("./Recording (3).mp3")
chunks = split_on_silence(
    sound,

    # split on silences longer than 1000ms (1 sec)
    min_silence_len=500,

    # anything under -16 dBFS is considered silence
    silence_thresh=-40, 

)

# now recombine the chunks so that the parts are at least 90 sec long
target_length = 10 * 1000
# print(chunks)
output_chunks = [chunks[0]]
chunk_to_np = []
for chunk in chunks[1:]:
    if len(output_chunks[-1]) < target_length:
        output_chunks[-1] += chunk
    else:
        # if the last output chunk is longer than the target length,
        # we can start a new one
        output_chunks.append(chunk)

        # 


# OK isso aqui tem falhado miseravelmente na transcriçao.
# I'm going to start with the sound of the sound.
# I'm going to do a little bit of the same thing.
# I'm sorry.
# I'm going to do a little bit of the same thing.
# I'm going to do a little bit of the same thing.
# I'm going to use the same method as the other one.
for chunk in output_chunks:
    chunk_to_np.append(np.frombuffer(chunk.get_array_of_samples(), np.int16).flatten().astype(np.float32) / 32768.0)

# output_chunks = np.frombuffer(output_chunks.get_array_of_samples(), np.int16).flatten().astype(np.float32) / 32768.0

# for i, chunk in enumerate(output_chunks):
#    output_file = "./audio/chunk{0}.mp3".format(i)
#    print("Exporting file", output_file)
#    chunk.export(output_file, format="mp3")

start_time = time.time()

# print(output_chunks)
import whisper
model = whisper.load_model("base")

for i, chunk in enumerate(chunk_to_np):
    print(chunk)
    path = "./audio/chunk{0}.mp3".format(i)
# load audio and pad/trim it to fit 30 seconds
    # audio = whisper.load_audio(chunk)
    audio = whisper.pad_or_trim(chunk)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    # print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions(fp16 = False)
    result = whisper.decode(model, mel, options)

    # print the recognized text
    print(result.text)


print("--- %s seconds ---" % (time.time() - start_time))
