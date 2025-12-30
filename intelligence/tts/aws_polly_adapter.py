import os
import json
import boto3 
from typing import List, Dict

import wave

def pcm_to_wav(pcm_bytes: bytes, path: str, sample_rate: int = 16000):
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_bytes)



class AWSPollyAdapter:
    def __init__(
        self,
        region_name: str = "us-east-1",
        output_dir: str = "audio_clips",
        sample_rate: str = "16000"
    ):
        self.client = boto3.client("polly", region_name=region_name)
        self.output_dir = output_dir
        self.sample_rate = sample_rate
        os.makedirs(self.output_dir, exist_ok=True)

    def _build_ssml(self, text: str, pace: float) -> str:
        """
        Convert pace modifier into SSML prosody rate.
        pace: 0.85–1.15 typical
        """
        rate_pct = int(pace * 100)
        return f"""
        <speak>
            <prosody rate="{rate_pct}%">
                {text}
            </prosody>
        </speak>
        """

    def synthesize(self, requests: List[Dict]):
        for req in requests:
            request_id = req["request_id"]
            text = req["text"]
            voice_id = self._map_voice(req["voice_id"])
            pace = req.get("pace", 1.0)

            ssml = self._build_ssml(text, pace)
            out_path = os.path.join(self.output_dir, f"{request_id}.wav")

            response = self.client.synthesize_speech(
                Engine="neural",
                VoiceId=voice_id,
                OutputFormat="pcm",
                TextType="ssml",
                Text=ssml,
                SampleRate=self.sample_rate
            )

            pcm_bytes = response["AudioStream"].read()
            pcm_to_wav(pcm_bytes, out_path, int(self.sample_rate))

            print(f"[Polly] Generated {out_path}")

    def _map_voice(self, internal_voice: str) -> str:
        """
        Map your internal voice IDs → Polly voices
        """
        mapping = {
            "female_soft": "Joanna",
            "male_neutral": "Matthew",
            "neutral_default": "Joanna"
        }
        return mapping.get(internal_voice, "Joanna")

