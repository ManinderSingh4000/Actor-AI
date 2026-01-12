from models.blocks import Block


class Dialogue(Block):
    def __init__(
        self,
        block_id: str,
        order: int,
        character: str,
        text: str,
        parenthetical: dict | None = None
    ):
        super().__init__(
            block_id=block_id,
            order=order,
            type="dialogue",
            text=text,
            is_beat=False,
            character=character,
            parenthetical=parenthetical
        )
