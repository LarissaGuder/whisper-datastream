from pydub import AudioSegment
from pydub.silence import split_on_silence


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
for chunk in chunks[1:]:
    if len(output_chunks[-1]) < target_length:
        output_chunks[-1] += chunk
    else:
        # if the last output chunk is longer than the target length,
        # we can start a new one
        output_chunks.append(chunk)

# print(output_chunks)

for i, chunk in enumerate(output_chunks):
   output_file = "./audio/chunk{0}.mp3".format(i)
   print("Exporting file", output_file)
   chunk.export(output_file, format="mp3")
