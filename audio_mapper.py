import os
from models import Scene, SceneAssignment, SceneAssets

# def build_ai_audio_map(
#     scene: Scene,
#     assignment: SceneAssignment,
#     audio_dir: str = "audio_clips"
# ) -> SceneAssets:

#     ai_audio_map = {}

#     # Filter only AI dialogue lines, in correct order
#     ai_lines = [
#         line for line in scene.dialogue
#         if line.character == assignment.ai_character
#     ]
#     all_lines = scene.dialogue

#     for index, line in enumerate(ai_lines, start=1):
#         audio_path = os.path.join(audio_dir, f"{index}.wav")

#         if not os.path.exists(audio_path):
#             raise FileNotFoundError(
#                 f"Missing AI audio file: expected {audio_path} "
#                 f"for dialogue_id={line.dialogue_id}"
#             )

#         ai_audio_map[line.dialogue_id] = audio_path
#         print(f"Mapped {len(ai_audio_map)} AI audio clips")

# #-----------------------------------------------
#         print(f"Total dialogues: {len(scene.dialogue)}")
#         print(f"AI dialogues: {len(ai_lines)}")
# #-----------------------------------------------

#     return SceneAssets(ai_audio_map=ai_audio_map)


def build_ai_audio_map(scene, assignment, audio_dir="audio_clips"):
    audio_map = {}

    for index, line in enumerate(scene.dialogue, start=1):
        audio_path = os.path.join(audio_dir, f"{index}.wav")

        if not os.path.exists(audio_path):
            raise FileNotFoundError(
                f"Missing audio file: {audio_path} "
                f"for dialogue_id={line.dialogue_id}"
            )

        audio_map[line.dialogue_id] = audio_path
        print(f"Mapped {len(audio_map)} audio clips")

    return SceneAssets(ai_audio_map=audio_map)
