from typing import List
from timeline.timeline_schema import TimelineEvent
from .character_registry import CharacterRegistry


class CharacterAnalyzer:
    def analyze(self, timeline: List[TimelineEvent]) -> CharacterRegistry:
        registry = CharacterRegistry()

        for event in timeline:
            if not event.character:
                continue

            profile = registry.get_or_create(event.character)

            if event.scene_id not in profile.scenes_present:
                profile.scenes_present.append(event.scene_id)

            if event.type == "dialogue":
                profile.dialogue_count += 1
                parenthetical = event.metadata.get("parenthetical")
                if parenthetical:
                    mode = parenthetical.get("raw")
                    if mode and mode not in profile.delivery_modes:
                        profile.delivery_modes.append(mode)

            if event.type == "action":
                profile.action_mentions += 1

            if profile.first_event_id == 0:
                profile.first_event_id = event.event_id

            profile.last_event_id = event.event_id

        return registry
