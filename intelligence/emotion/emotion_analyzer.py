import json
from typing import List, Dict
from .emotion_schema import EmotionNote


class EmotionAnalyzer:
    def infer(self, timeline: List[Dict], performance: Dict[int, Dict]) -> List[EmotionNote]:
        notes: List[EmotionNote] = []

        for event in timeline:
            if event["type"] != "dialogue":
                continue

            text = event["text"] or ""
            perf = performance.get(event["event_id"], {})
            intensity = perf.get("intensity", 0.0)

            emotions = set()
            confidence = 0.4

            # punctuation cues
            if "!" in text:
                emotions.add("urgency")
                confidence += 0.2
            if "?" in text:
                emotions.add("uncertainty")
                confidence += 0.1
            if "..." in text or "--" in text:
                emotions.add("hesitation")
                confidence += 0.1

            # lexical cues
            fear_words = ["found", "help", "now", "listen", "carefully", "safe"]
            if any(w in text.lower() for w in fear_words):
                emotions.add("fear")
                confidence += 0.2

            # pacing / intensity
            if intensity >= 0.8:
                emotions.add("tension")
                confidence += 0.1

            if not emotions:
                emotions.add("neutral")

            notes.append(
                EmotionNote(
                    event_id=event["event_id"],
                    emotions=sorted(emotions),
                    confidence=min(confidence, 1.0)
                )
            )

        return notes
