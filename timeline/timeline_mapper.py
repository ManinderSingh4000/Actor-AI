from typing import List
from .timeline_schema import TimelineEvent


class TimelineMapper:
    def __init__(self):
        self._event_counter = 0

    def _next_id(self) -> int:
        self._event_counter += 1
        return self._event_counter

    def map_scene(self, scene: dict) -> List[TimelineEvent]:
        events: List[TimelineEvent] = []

        for action in scene.get("action", []):
            events.append(
                TimelineEvent(
                    event_id=self._next_id(),
                    type="beat" if action.get("is_beat") else "action",
                    scene_id=scene["scene_id"],
                    character=action.get("character_ref"),
                    text=action.get("text"),
                    estimated_duration=1.2 if action.get("is_beat") else 2.0,
                    metadata={}
                )
            )

        for dlg in scene.get("dialogue", []):
            events.append(
                TimelineEvent(
                    event_id=self._next_id(),
                    type="dialogue",
                    scene_id=scene["scene_id"],
                    character=dlg["character"],
                    text=dlg["text"],
                    estimated_duration=max(0.6, len(dlg["text"].split()) * 0.3),
                    metadata={
                        "parenthetical": dlg.get("parenthetical")
                    }
                )
            )

        return events
