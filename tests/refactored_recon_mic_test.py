import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
Model_path = "..\\extra\\vosk-model-small-en-us-0.15"

class SpeechRecognizer:
    def __init__(self, language="en-us", device=None, samplerate=None):
        self.language = language
        self.device = device
        self.samplerate = samplerate
        self.model = None
        self.recognizer = None
        self.stream = None
        self.queue = queue.Queue()
        self.is_running = False

    def initialize(self):
        
        if self.samplerate is None:
            device_info = sd.query_devices(self.device, "input")
            self.samplerate = int(device_info["default_samplerate"])
        
        self.model = Model(model_path=Model_path,lang=self.language)
        self.recognizer = KaldiRecognizer(self.model, self.samplerate)
    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.queue.put(bytes(indata))

    def start(self):
        if not self.model:
            self.initialize()
        
        self.stream = sd.RawInputStream(
            samplerate=self.samplerate,
            blocksize=8000,
            device=self.device,
            dtype="int16",
            channels=1,
            callback=self.callback
        )
        self.stream.start()
        self.is_running = True

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
        self.is_running = False

    def process_audio(self):
        if not self.is_running:
            return None
        
        data = self.queue.get()
        if self.recognizer.AcceptWaveform(data):
            result = self.recognizer.Result()
            return result
        else:
            partial = self.recognizer.PartialResult()
            return partial

    @staticmethod
    def list_devices():
        return sd.query_devices()

# Example usage:
if __name__ == "__main__":
    recognizer = SpeechRecognizer(language="en-us")
    recognizer.start()
    import json
    try:
        while True:
            result = recognizer.process_audio()
            if result:
                try:
                    print(json.loads(result)["text"])
                except KeyError:
                    pass
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        recognizer.stop()

