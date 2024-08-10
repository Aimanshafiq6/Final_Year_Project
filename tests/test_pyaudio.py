import pyaudio
import wave
import requests
import io
import struct
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
    model = Model(lang="en-us")
    if response.status_code != 200:
        print(f"Failed to access the stream. Status code: {response.status_code}")
        return

    buffer = io.BytesIO()
    
    # Read the WAV header
    for chunk in response.iter_content(chunk_size=44):
        if chunk:
            buffer.write(chunk)
            if buffer.tell() >= 44:
                break

    buffer.seek(0)
    
    with wave.open(buffer, 'rb') as wf:
        p = pyaudio.PyAudio()
        
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        
        print(f"Channels: {wf.getnchannels()}, Sample Width: {wf.getsampwidth()}, Framerate: {wf.getframerate()}")
        
        try:

            # Continue reading the audio data
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    rec = KaldiRecognizer(model, chunk)
                    while True:
                        data = q.get()
                        if rec.AcceptWaveform(data):
                            print(rec.Result())
                        else:
                            print(rec.PartialResult())
                        

                    stream.write(chunk)
        except KeyboardInterrupt:
            print("Playback stopped by user")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

# Usage
play_streaming_wav('http://192.168.0.102:8080/audio.wav')