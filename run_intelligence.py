import json
# from intelligence.intelligence_pipeline import IntelligencePipeline
# from dataclasses import asdict
# from  pathlib import Path

# ---------------------------
# Setup artifact directory
# ---------------------------
# ARTIFACT_DIR = Path("artifacts")
# ARTIFACT_DIR.mkdir(exist_ok=True)

# def save_json(path: Path, data):
#     with open(path, "w") as f:
#         json.dump(data, f, indent=2)



# # Load parsed script JSON
# with open("output_updated_01.json", "r") as f:
#     script = json.load(f)

# pipeline = IntelligencePipeline()
# result = pipeline.run(script)

# # ---------------------------
# # SAVE ARTIFACTS (NEW PART)
# # ---------------------------

# save_json(
#     ARTIFACT_DIR / "timeline.json",
#     [asdict(e) for e in result["timeline"]]
# )

# save_json(
#     ARTIFACT_DIR / "characters.json",
#     {k: asdict(v) for k, v in result["characters"].characters.items()}
# )

# save_json(
#     ARTIFACT_DIR / "narrative.json",
#     [asdict(n) for n in result["narrative"]]
# )

# save_json(
#     ARTIFACT_DIR / "performance.json",
#     [asdict(p) for p in result["performance"]]
# )

# print("\nArtifacts saved to /artifacts")

# ================================================= #

from intelligence.emotion.emotion_analyzer import EmotionAnalyzer
from dataclasses import asdict

# Load saved artifacts
# with open("intelligence/artifacts/timeline.json", "r") as f:
#     timeline = json.load(f)

# with open("intelligence/artifacts/performance.json", "r") as f:
#     performance_list = json.load(f)

# # index performance by event_id
# performance = {p["event_id"]: p for p in performance_list}

# emotion_notes = EmotionAnalyzer().infer(timeline, performance)

# # save emotions
# with open("intelligence/artifacts/emotions.json", "w") as f:
#     json.dump([asdict(e) for e in emotion_notes], f, indent=2)

# print("\n--- EMOTIONS ---")
# for e in emotion_notes[:5]:
#     print(e)

# ================================================= #

# ---- MERGE EMOTIONS INTO PERFORMANCE ----
# from performance.performance_merger import PerformanceMerger

# with open("intelligence/artifacts/performance.json", "r") as f:
#     performance = json.load(f)

# with open("intelligence/artifacts/emotions.json", "r") as f:
#     emotions = json.load(f)

# enriched = PerformanceMerger().merge(performance, emotions)

# with open("intelligence/artifacts/performance_enriched.json", "w") as f:
#     json.dump(enriched, f, indent=2)

# print("\n--- PERFORMANCE (ENRICHED) ---")
# for e in enriched[:5]:
#     print(e)



# ================================================= #

# ---- BUILD TTS REQUESTS ----
from intelligence.tts.tts_adapter import TTSAdapter
from dataclasses import asdict

# with open("intelligence/artifacts/timeline.json", "r") as f:
#     timeline = json.load(f)

# with open("intelligence/artifacts/performance_enriched.json", "r") as f:
#     perf_enriched = json.load(f)

# tts_requests = TTSAdapter().build_requests(timeline, perf_enriched)

# with open("intelligence/artifacts/audio_requests.json", "w") as f:
#     json.dump([asdict(r) for r in tts_requests], f, indent=2)

# print("\n--- TTS REQUESTS ---")
# for r in tts_requests[:5]:
#     print(r)


# ---- AUDIO ASSEMBLY ----
# from intelligence.audio.audio_assembler import AudioAssembler

# with open("intelligence/artifacts/audio_requests.json", "r") as f:
#     audio_requests = json.load(f)

# assembler = AudioAssembler(sample_rate=22050)

# assembler.assemble(
#     audio_requests=audio_requests,
#     clips_dir="audio_clips",  # put WAVs here
#     output_path="intelligence/artifacts/assembled_audio.wav"
# )

# print("\nAssembled audio written to intelligence/artifacts/assembled_audio.wav")

# ---- AWS POLLY TTS ----
from intelligence.tts.aws_polly_adapter import AWSPollyAdapter

with open("intelligence/artifacts/audio_requests.json", "r") as f:
    audio_requests = json.load(f)

polly = AWSPollyAdapter(
    region_name="us-east-1",
    output_dir="audio_clips"
)

polly.synthesize(audio_requests)

# ---- AUDIO ASSEMBLY ----
from intelligence.audio.audio_assembler import AudioAssembler

with open("intelligence/artifacts/audio_requests.json", "r") as f:
    audio_requests = json.load(f)

assembler = AudioAssembler(sample_rate=16000)  # MUST match Polly

assembler.assemble(
    audio_requests=audio_requests,
    clips_dir="audio_clips",
    output_path="intelligence/artifacts/assembled_audio.wav"
)

print("\nAssembled audio written to intelligence/artifacts/assembled_audio.wav")
