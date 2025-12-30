from timeline.timeline_mapper import TimelineMapper
from character.character_analyzer import CharacterAnalyzer
from narrative.narrative_analyzer import NarrativeAnalyzer
from performance.performance_analyzer import PerformanceAnalyzer

class IntelligencePipeline:
    def run(self, script: dict):
        mapper = TimelineMapper()
        timeline = []

        for scene in script["scenes"]:
            timeline.extend(mapper.map_scene(scene))

        characters = CharacterAnalyzer().analyze(timeline)
        narrative = NarrativeAnalyzer().analyze(timeline)
        performance = PerformanceAnalyzer().analyze(timeline)

        return {
            "timeline": timeline,
            "characters": characters,
            "narrative": narrative,
            "performance": performance
        }