import customtkinter as ctk
import pyaudio
import wave
import threading

class AudioRecorder(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Audio Recorder")
        self.geometry("300x200")

        self.recording = False
        self.frames = []

        self.record_button = ctk.CTkButton(self, text="Start Recording", command=self.toggle_recording)
        self.record_button.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="Not recording")
        self.status_label.pack(pady=10)

    def toggle_recording(self):
        if not self.recording:
            self.recording = True
            self.record_button.configure(text="Stop Recording")
            self.status_label.configure(text="Recording...")
            threading.Thread(target=self.record_audio).start()
        else:
            self.recording = False
            self.record_button.configure(text="Start Recording")
            self.status_label.configure(text="Recording stopped")

    def record_audio(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        self.frames = []

        while self.recording:
            data = stream.read(CHUNK)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        self.save_audio()

    def save_audio(self):
        WAVE_OUTPUT_FILENAME = "output.wav"

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        self.status_label.configure(text=f"Saved as {WAVE_OUTPUT_FILENAME}")

if __name__ == "__main__":
    app = AudioRecorder()
    app.mainloop()