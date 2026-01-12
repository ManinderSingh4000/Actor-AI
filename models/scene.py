from typing import List
from models.blocks import Block


class Scene:
    def __init__(self, scene_id: str, heading: dict):
        self.scene_id = scene_id
        self.heading = heading

        # CANONICAL TIMELINE
        self.blocks: List[Block] = []
