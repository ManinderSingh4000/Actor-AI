from models.blocks import Block
from models.dialogue import Dialogue
from models.action import Action
from models.scene import Scene


class CanonicalNormalizer:
    """
    Converts parser-specific output (PDF / Fountain)
    into a single canonical blocks[] timeline.
    """

    def normalize_scene(self, raw_scene) -> list[Block]:
        blocks: list[Block] = []
        order = 0

        for item in raw_scene:
            order += 1

            if item["type"] == "dialogue":
                blocks.append(
                    Dialogue(
                        block_id=item["id"],
                        order=order,
                        character=item["character"],
                        text=item["text"],
                        parenthetical=item.get("parenthetical")
                    )
                )

            elif item["type"] == "action":
                blocks.append(
                    Action(
                        block_id=item["id"],
                        order=order,
                        text=item["text"],
                        is_beat=item.get("is_beat", False)
                    )
                )

            elif item["type"] == "transition":
                blocks.append(
                    Block(
                        block_id=item["id"],
                        order=order,
                        type="transition",
                        text=item["text"],
                        is_beat=True
                    )
                )

        return blocks
