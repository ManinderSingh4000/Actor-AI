# normalizer/script_normalizer.py

from models.scene import Scene as CanonicalScene
from models.blocks import Block
from models.action import Action
from models.dialogue import Dialogue
from models.schema import Script , Transition
from models.schema import uid


def normalize_script_to_canonical(script: Script) -> list[CanonicalScene]:
    canonical_scenes: list[CanonicalScene] = []

    for scene in script.scenes:
        canonical_scene = CanonicalScene(
            scene_id=scene.scene_id,
            heading={
                "raw": scene.heading
            }
        )

        order = 1

        # merge action + dialogue by order heuristic
        timeline = []

        for a in scene.action:
            timeline.append(("action", a))

        for d in scene.dialogue:
            timeline.append(("dialogue", d))

        for t in scene.transitions:
            timeline.append(("transition", t))

        # dialogue already has order → use it
        timeline.sort(
            key=lambda x: x[1].order if x[0] == "dialogue" else 10_000
        )

        for kind, item in timeline:
            if kind == "action":
                canonical_scene.blocks.append(
                    Action(
                        block_id=uid("blk"),
                        order=order,
                        text=item.text,
                        is_beat=item.is_beat
                    )
                )

            elif kind == "dialogue":
                canonical_scene.blocks.append(
                    Dialogue(
                        block_id=item.dialogue_id,
                        order=order,
                        character=item.character,
                        text=item.text,
                        parenthetical=(
                            vars(item.parenthetical)
                            if item.parenthetical else None
                        )
                    )
                )
            else:
                canonical_scene.blocks.append(
                    Block(
                        block_id=uid("blk"),
                        order=order,
                        type="transition",
                        text=item.text,
                        is_beat=True
                    )
                )


            order += 1

        canonical_scenes.append(canonical_scene)

    return canonical_scenes
