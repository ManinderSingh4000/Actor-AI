from typing import List
from timeline.timeline_schema import TimelineEvent
from .performance_schema import PerformanceNote


class PerformanceAnalyzer:
    def analyze(self, timeline: List[TimelineEvent]) -> List[PerformanceNote]:
        notes: List[PerformanceNote] = []

        for event in timeline:
            if event.type != "dialogue":
                continue

            intensity = min(1.0, event.estimated_duration / 2)

            notes.append(
                PerformanceNote(
                    event_id=event.event_id,
                    emotion="neutral",
                    intensity=intensity,
                    pace_modifier=1.0,
                    emphasis_words=[]
                )
            )

        return notes
