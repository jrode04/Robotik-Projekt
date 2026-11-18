import sys
import whisper

audio_file = sys.argv[1]

model = whisper.load_model("base", device="cpu")
result = model.transcribe(audio_file, fp16=False)

with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])

print("Done. The text is in transcription.txt")