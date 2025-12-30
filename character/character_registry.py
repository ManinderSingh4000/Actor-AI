from dataclasses import dataclass, field
from typing import Dict
from .character_schema import CharacterProfile


@dataclass
class CharacterRegistry:
    characters: Dict[str, CharacterProfile] = field(default_factory=dict)

    def get_or_create(self, character_id: str) -> CharacterProfile:
        if character_id not in self.characters:
            self.characters[character_id] = CharacterProfile(character_id=character_id)
        return self.characters[character_id]
