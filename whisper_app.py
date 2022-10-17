import whisper
import time
start_time = time.time()

# model = whisper.load_model("base")

# # load audio and pad/trim it to fit 30 seconds
# audio = whisper.load_audio("audio.mp3")
# audio = whisper.pad_or_trim(audio)

# # make log-Mel spectrogram and move to the same device as the model
# mel = whisper.log_mel_spectrogram(audio).to(model.device)

# # detect the spoken language
# _, probs = model.detect_language(mel)
# print(f"Detected language: {max(probs, key=probs.get)}")

# # decode the audio
# options = whisper.DecodingOptions(fp16 = False)
# result = whisper.decode(model, mel, options)

# # print the recognized text
# print(result.text)

model = whisper.load_model("base")
result = model.transcribe("Spark Streaming with Python under 12 minutes.mp3")
print(result["text"])

print("--- %s seconds ---" % (time.time() - start_time))