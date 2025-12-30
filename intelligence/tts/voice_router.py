class VoiceRouter:
    def route(self, character: str) -> str:
        # deterministic placeholder voices
        if character.upper() == "MARY":
            return "female_soft"
        if character.upper() == "JOHN":
            return "male_neutral"
        return "neutral_default"
