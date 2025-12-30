# create_dummy_clips.py
import wave, struct, os, json

os.makedirs("audio_clips", exist_ok=True)

with open("intelligence/artifacts/audio_requests.json") as f:
    reqs = json.load(f)

for r in reqs:
    path = f"audio_clips/{r['request_id']}.wav"
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(22050)
        frames = int(22050 * 0.3)
        wf.writeframes(struct.pack("<h", 500) * frames)
