import sounddevice as sd
import numpy as np
import requests
import wave
import io
import queue

from vosk import Model, KaldiRecognizer

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def play_streaming_wav(url):
    # Open a streaming GET request
    response = requests.get(url, stream=True)
    
    if response.status_code != 200:
        print(f"Failed to access the stream. Status code: {response.status_code}")
        return

    # Create a buffer for the initial audio data
    buffer = io.BytesIO()

    # Read the first chunk to get WAV header information
    for chunk in response.iter_content(chunk_size=1024):
        buffer.write(chunk)
        if buffer.tell() > 44:  # Minimum WAV header size
            break

    buffer.seek(0)

    # Read WAV properties
    with wave.open(buffer, 'rb') as wf:
        channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        framerate = wf.getframerate()

    print(f"Channels: {channels}, Sample Width: {sample_width}, Framerate: {framerate}")

    # Start the audio stream
    stream = sd.OutputStream(
        samplerate=framerate,
        channels=channels,
        dtype='int16'
    )
    model = Model(lang="en-us")

    stream.start()

    try:
        # Continue reading and playing the audio data
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                callback(chunk)
                audio_data = np.frombuffer(chunk, dtype=np.int16)
                rec = KaldiRecognizer(model, 1024)
                data = q.get()
                if rec.AcceptWaveform(data):
                    print(rec.Result())
                else:
                    print(rec.PartialResult())
                    stream.write(audio_data)
    except KeyboardInterrupt:
        print("Playback stopped by user")
    finally:
        stream.stop()
        stream.close()

# Usage
play_streaming_wav('http://192.168.0.102:8080/audio.wav')