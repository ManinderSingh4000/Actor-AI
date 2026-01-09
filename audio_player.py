import sounddevice as sd
import soundfile as sf

def play_audio_blocking(path: str):
    data, samplerate = sf.read(path)
    sd.play(data, samplerate)
    sd.wait()
