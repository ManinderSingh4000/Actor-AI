from typing import List
from models.blocks import Block


class Scene:
    def __init__(self, scene_id: str, heading: dict):
        self.scene_id = scene_id
        self.heading = heading
        self.blocks: List[Block] = []

    def to_dict(self):
        return {
            "scene_id": self.scene_id,
            "heading": self.heading,
            "blocks": [block.__dict__ for block in self.blocks]
        }
