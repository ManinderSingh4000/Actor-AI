import sounddevice as sd
import numpy as np

def listen_for_user(duration: float = 10.0):
    samplerate = 44100
    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1
    )
    sd.wait()
    return audio
