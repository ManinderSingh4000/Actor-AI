from typing import List
from timeline.timeline_schema import TimelineEvent
from .narrative_schema import NarrativeInsight


class NarrativeAnalyzer:
    def analyze(self, timeline: List[TimelineEvent]) -> List[NarrativeInsight]:
        insights = {}
        tension = 0.0

        for event in timeline:
            tension += 0.05 if event.type == "dialogue" else 0.02

            scene = insights.setdefault(
                event.scene_id,
                NarrativeInsight(
                    scene_id=event.scene_id,
                    tension_curve=[],
                    pacing="normal",
                    dominant_emotions=[]
                )
            )
            scene.tension_curve.append(min(tension, 1.0))

        return list(insights.values())
