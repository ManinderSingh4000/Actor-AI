from scene_loader import load_scene
from engine import SceneRuntimeEngine
from models import SceneAssignment
from speech_trigger import wait_for_action
from audio_mapper import build_ai_audio_map

scene = load_scene("output_pdf.json")

assignment = SceneAssignment(
    ai_character="JOHN",
    user_character="MARY"
)

# assets = SceneAssets(
#     ai_audio_map={
#         "dlg_d40cdce6": "audio_clips/1.wav",
#         "dlg_cde0c43c": "audio_clips/2.wav",
#         # add all AI dialogue lines
#     }
# )

assets = build_ai_audio_map(
    scene=scene,
    assignment=assignment,
    audio_dir="audio_clips"
)


if wait_for_action():
    engine = SceneRuntimeEngine(scene, assignment, assets)
    engine.run()
