from models.blocks import Block


class Action(Block):
    def __init__(
        self,
        block_id: str,
        order: int,
        text: str,
        is_beat: bool = False
    ):
        super().__init__(
            block_id=block_id,
            order=order,
            type="action",
            text=text,
            is_beat=is_beat,
            character=None,
            parenthetical=None
        )
