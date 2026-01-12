# models/block.py
from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class Block:
    block_id: str
    order: int

    type: str  # "action" | "dialogue" | "transition"

    text: str
    is_beat: bool = False

    character: Optional[str] = None
    parenthetical: Optional[Dict] = None
