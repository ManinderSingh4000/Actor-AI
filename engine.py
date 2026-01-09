import time
from audio_player import play_audio_blocking
from mic_listener import listen_for_user
from models import Scene, SceneAssignment, SceneAssets

class SceneRuntimeEngine:

    def __init__(
        self,
        scene: Scene,
        assignment: SceneAssignment,
        assets: SceneAssets
    ):
        self.scene = scene
        self.assignment = assignment
        self.assets = assets

    # def run(self):
    #     print(f"\n\n 🎬 Scene start: {self.scene.heading}\n\n")

    #     for line in self.scene.dialogue:

    #         if line.character == self.assignment.ai_character:
    #             print(f"AI ({line.character}): {line.text}")
    #             audio_path = self.assets.ai_audio_map[line.dialogue_id]
    #             play_audio_blocking(audio_path)

    #         elif line.character == self.assignment.user_character:
    #             print(f"YOU ({line.character}): {line.text}")
    #             listen_for_user(duration=8.0)

    #         time.sleep(0.3)  # natural pause

    #     print("\n\n 🎬 Scene complete. \n\n ")

    #     matched = False

    #     for line in self.scene.dialogue:
    #         if line.character == self.assignment.ai_character:
    #             matched = True
    #             ...
    #         elif line.character == self.assignment.user_character:
    #             matched = True
    #             ...

    #     if not matched:
    #         raise RuntimeError(
    #             "No dialogue matched assignment. "
    #             "Check character names."
    #         )

    

    

    def run(self):
        print(f"🎬 Scene start: {self.scene.heading}")

        def group_dialogue(dialogue):
            groups = []
            current = None

            for line in dialogue:
                if not current or current["character"] != line.character:
                    current = {
                        "character": line.character,
                        "lines": [line]
                    }
                    groups.append(current)
                else:
                    current["lines"].append(line)

            return groups

        groups = group_dialogue(self.scene.dialogue)

        for group in groups:
            character = group["character"]
            lines = group["lines"]

            if character == self.assignment.ai_character:
                for line in lines:
                    print(f"AI ({character}): {line.text}")
                    play_audio_blocking(self.assets.ai_audio_map[line.dialogue_id])

                time.sleep(0.4)  # turn handoff pause

            elif character == self.assignment.user_character:
                for line in lines:
                    print(f"YOU ({character}): {line.text}")

                # ONE pause per turn, not per line
                total_words = sum(len(l.text.split()) for l in lines)
                pause = min(5.0, max(2.5, total_words * 0.35))
                time.sleep(pause)



        print("🎬 Scene complete.")
