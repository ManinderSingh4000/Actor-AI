import wave
import struct


def generate_silence(
    path: str,
    duration_sec: float,
    sample_rate: int = 22050,
    channels: int = 1,
    sample_width: int = 2
):
    frames = int(sample_rate * duration_sec)
    silence_frame = struct.pack("<h", 0)

    with wave.open(path, "w") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(silence_frame * frames)
