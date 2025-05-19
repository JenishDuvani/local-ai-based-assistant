import sounddevice as sd
import queue
import sys
import json
from vosk import Model, KaldiRecognizer

# Load the model (adjust path if necessary)
model = Model("models/vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# Start the stream
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    print("🎙️ Speak now... (Ctrl+C to stop)")
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print("📝 Recognized:", result.get("text", ""))
        else:
            partial = json.loads(rec.PartialResult())
            print("...listening:", partial.get("partial", ""), end='\r')
