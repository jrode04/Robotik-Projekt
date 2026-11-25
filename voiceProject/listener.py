import queue
import re
import threading
from collections import deque

import numpy as np
import sounddevice as sd
import whisper

SAMPLE_RATE = 16000        # Whisper needs 16000 samples per second
BLOCK_SECONDS = 0.1        # length of one audio block
THRESHOLD = 0.04           # loudness limit for speech
SILENCE_SECONDS = 0.8      # silence that ends a phrase
MIN_SPEECH_SECONDS = 0.3   # shorter sounds are ignored
MAX_SPEECH_SECONDS = 15.0  # longest phrase
STOP_WORD = "finish"
MODEL_NAME = "base"


class Listener:
    def __init__(self):
        self.model = whisper.load_model(MODEL_NAME, device="cpu")
        self.audio_queue = queue.Queue()
        self.text_queue = queue.Queue()
        self.running = False
        self.stream = None
        self.thread = None

    def on_audio(self, indata, frames, time_info, status):
        if status:
            print("Audio status:", status)
        self.audio_queue.put(indata[:, 0].copy())

    def start(self):
        self.running = True
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            blocksize=int(SAMPLE_RATE * BLOCK_SECONDS),
            callback=self.on_audio,
        )
        self.stream.start()
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        if self.thread is not None:
            self.thread.join(timeout=30)

    def loop(self):
        pre_roll = deque(maxlen=3)
        speech = []
        silent_blocks = 0
        max_silent = int(SILENCE_SECONDS / BLOCK_SECONDS)
        min_blocks = int(MIN_SPEECH_SECONDS / BLOCK_SECONDS)
        max_blocks = int(MAX_SPEECH_SECONDS / BLOCK_SECONDS)

        while self.running:
            try:
                block = self.audio_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            loud = np.sqrt(np.mean(block ** 2)) > THRESHOLD

            if loud:
                if not speech:
                    speech.extend(pre_roll)
                speech.append(block)
                silent_blocks = 0
            elif speech:
                speech.append(block)
                silent_blocks += 1
            else:
                pre_roll.append(block)

            if speech and (silent_blocks >= max_silent or len(speech) >= max_blocks):
                if len(speech) - silent_blocks >= min_blocks:
                    self.process(speech)
                speech = []
                silent_blocks = 0
                pre_roll.clear()

    def process(self, speech):
        audio = np.concatenate(speech)
        result = self.model.transcribe(audio, fp16=False, language="en")
        text = result["text"].strip()
        if not text:
            return

        print("Heard:", text)
        self.text_queue.put(text)

        words = re.sub(r"[^a-z ]", "", text.lower()).split()
        if STOP_WORD in words:
            self.running = False


if __name__ == "__main__":
    listener = Listener()
    listener.start()
    print(f"Listening. Say '{STOP_WORD}' to stop.")
    try:
        while listener.running:
            try:
                listener.text_queue.get(timeout=0.5)
            except queue.Empty:
                pass
    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
        print("Listener stopped.")