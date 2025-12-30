from typing import List, Dict
from .tts_schema import TTSRequest
from .voice_router import VoiceRouter


class TTSAdapter:
    def __init__(self):
        self.voice_router = VoiceRouter()
        self._rid = 0

    def _next_id(self) -> int:
        self._rid += 1
        return self._rid

    def build_requests(
        self,
        timeline: List[Dict],
        performance_enriched: List[Dict]
    ) -> List[TTSRequest]:

        perf_by_event = {p["event_id"]: p for p in performance_enriched}
        requests: List[TTSRequest] = []

        for event in timeline:
            if event["type"] != "dialogue":
                continue

            perf = perf_by_event.get(event["event_id"])
            if not perf:
                continue

            delivery = perf.get("delivery", {})
            voice_id = self.voice_router.route(event["character"])

            requests.append(
                TTSRequest(
                    request_id=self._next_id(),
                    event_id=event["event_id"],
                    character=event["character"],
                    text=event["text"],
                    voice_id=voice_id,
                    pace=delivery.get("pace_modifier", 1.0),
                    intensity=delivery.get("intensity", perf.get("intensity", 0.5)),
                    pre_pause=delivery.get("pre_pause", 0.0),
                    post_pause=delivery.get("post_pause", 0.0),
                    emotions=delivery.get("emotions", [])
                )
            )

        return requests
