import json
import wave
import os
from typing import List, Dict
from .silence import generate_silence


class AudioAssembler:
    def __init__(self, sample_rate: int = 22050):
        self.sample_rate = sample_rate

    def _append_wav(self, out_wav, in_path: str):
        with wave.open(in_path, "rb") as wf:
            out_wav.writeframes(wf.readframes(wf.getnframes()))

    def assemble(
        self,
        audio_requests: List[Dict],
        clips_dir: str,
        output_path: str
    ):
        if not audio_requests:
            raise ValueError("No audio requests to assemble.")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        temp_silence = "_temp_silence.wav"

        with wave.open(output_path, "w") as out_wav:
            # initialize from first clip format
            first_clip = os.path.join(clips_dir, f"{audio_requests[0]['request_id']}.wav")
            with wave.open(first_clip, "rb") as wf:
                out_wav.setnchannels(wf.getnchannels())
                out_wav.setsampwidth(wf.getsampwidth())
                out_wav.setframerate(wf.getframerate())

            for req in audio_requests:
                # pre-pause
                if req["pre_pause"] > 0:
                    generate_silence(
                        temp_silence,
                        req["pre_pause"],
                        sample_rate=self.sample_rate
                    )
                    self._append_wav(out_wav, temp_silence)

                # dialogue clip
                clip_path = os.path.join(clips_dir, f"{req['request_id']}.wav")
                if not os.path.exists(clip_path):
                    raise FileNotFoundError(f"Missing clip: {clip_path}")

                self._append_wav(out_wav, clip_path)

                # post-pause
                if req["post_pause"] > 0:
                    generate_silence(
                        temp_silence,
                        req["post_pause"],
                        sample_rate=self.sample_rate
                    )
                    self._append_wav(out_wav, temp_silence)

        if os.path.exists(temp_silence):
            os.remove(temp_silence)
