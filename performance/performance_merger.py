from typing import List, Dict
from dataclasses import asdict
from .performance_schema import PerformanceNote


class PerformanceMerger:
    def merge(
        self,
        performance: List[Dict],
        emotions: List[Dict]
    ) -> List[Dict]:
        # index emotions by event_id
        emo_by_id = {e["event_id"]: e for e in emotions}
        enriched: List[Dict] = []

        for p in performance:
            e = emo_by_id.get(p["event_id"])
            out = dict(p)

            # defaults
            out.setdefault("delivery", {})
            out["delivery"].setdefault("pace_modifier", p.get("pace_modifier", 1.0))
            out["delivery"].setdefault("intensity", p.get("intensity", 0.5))
            out["delivery"].setdefault("emphasis_words", p.get("emphasis_words", []))
            out["delivery"].setdefault("pre_pause", 0.0)
            out["delivery"].setdefault("post_pause", 0.0)

            if e:
                emotions = e.get("emotions", [])
                confidence = e.get("confidence", 0.5)

                # apply rules
                if "fear" in emotions:
                    out["delivery"]["intensity"] = min(1.0, out["delivery"]["intensity"] + 0.2)
                    out["delivery"]["pace_modifier"] *= 0.9

                if "urgency" in emotions:
                    out["delivery"]["pace_modifier"] *= 1.15

                if "tension" in emotions:
                    out["delivery"]["intensity"] = min(1.0, out["delivery"]["intensity"] + 0.1)
                    out["delivery"]["post_pause"] = max(out["delivery"]["post_pause"], 0.1)

                if "hesitation" in emotions:
                    out["delivery"]["pace_modifier"] *= 0.9
                    out["delivery"]["pre_pause"] = max(out["delivery"]["pre_pause"], 0.2)

                if "uncertainty" in emotions:
                    out["delivery"]["pace_modifier"] *= 0.95

                out["delivery"]["emotion_confidence"] = confidence
                out["delivery"]["emotions"] = emotions

            enriched.append(out)

        return enriched
