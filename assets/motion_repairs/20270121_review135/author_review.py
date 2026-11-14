#!/usr/bin/env python3
"""Author Batch 135 inspection of the first 14 SeedExercises with bundled media (0 approved, 14 deferred to 待修图)."""
from pathlib import Path
import argparse
import hashlib
import json

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20270121_review135"
VERSION = "1.2.140"
VERSION_CODE = 2027012201

inspected = [
    "exercise_lat_pulldown",
    "exercise_band_row",
    "exercise_one_arm_dumbbell_row",
    "exercise_seated_row",
    "exercise_band_pulldown",
    "exercise_bent_over_barbell_row",
    "exercise_face_pull",
    "exercise_wall_pushup",
    "exercise_incline_pushup",
    "exercise_dumbbell_bench_press",
    "exercise_seated_chest_press",
    "exercise_seated_shoulder_press",
    "exercise_band_external_rotation",
    "exercise_sit_to_stand",
]
review_candidates = []
registered_media = []
definition_updates = {}

pending = {
    "exercise_lat_pulldown": "待修图 · SeedExercises 动图 motion_lat_pulldown.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、T:14/B:11<15、y>=370 IoU=0.4367<0.96 且中段叠影残影），另步骤一含“保持”且 primaryMuscles 为空，待重制标准 4 帧循环图。",
    "exercise_band_row": "待修图 · SeedExercises 动图 motion_band_row.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、L:14/R:13<15、y>=370 IoU=0.6943<0.96 且中段渐隐拖影），另步骤含两处“保持”且 primaryMuscles 为空，待重制。",
    "exercise_one_arm_dumbbell_row": "待修图 · SeedExercises 动图 motion_one_arm_dumbbell_row.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、L:12/R:14<15、y>=370 IoU=0.7786<0.96），另步骤提及“一手支撑”却缺 requiredEquipment 且 primaryMuscles 为空，待重制。",
    "exercise_seated_row": "待修图 · SeedExercises 动图 motion_seated_row.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、L:14/R:14<15、y>=370 IoU=0.3544<0.96），另步骤三含“保持”且 primaryMuscles 为空，待重制。",
    "exercise_band_pulldown": "待修图 · SeedExercises 动图 motion_band_pulldown.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、顶部几乎贴边 T:2/B:14<15、y>=370 IoU=0.1116<0.96），另 primaryMuscles 为空，待重制。",
    "exercise_bent_over_barbell_row": "待修图 · SeedExercises 动图 motion_bent_over_barbell_row.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、T:8/B:14<15、y>=370 IoU=0.3847<0.96），另步骤含两处“保持”且 primaryMuscles 为空，待重制。",
    "exercise_face_pull": "待修图 · SeedExercises 动图 motion_face_pull.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、L:14/R:14<15、y>=370 IoU=0.1706<0.96 且中段叠影），另 primaryMuscles 为空，待重制。",
    "exercise_wall_pushup": "待修图 · SeedExercises 动图 motion_wall_pushup.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、L:14/R:14<15、y>=370 IoU=0.3908<0.96），另缺 requiredEquipment=[\"墙面\"]、步骤三含“保持”且 primaryMuscles 为空，待重制。",
    "exercise_incline_pushup": "待修图 · SeedExercises 动图 motion_incline_pushup.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、L:12/R:13<15、y>=370 IoU=0.4353<0.96），另缺稳固踏台/上斜训练凳支撑要求、步骤含“保持”且 primaryMuscles 为空，待重制。",
    "exercise_dumbbell_bench_press": "待修图 · SeedExercises 动图 motion_dumbbell_bench_press.webp（同 0289 原图）存在底色偏灰 ([253,253,253]) 与右侧脚尖贴边 R=3<15 px；另 SeedExercises 缺 requiredEquipment=[\"平板训练凳\"] 且 primaryMuscles 为空，待扩边距重制并补齐元数据。",
    "exercise_seated_chest_press": "待修图 · SeedExercises 动图 motion_seated_chest_press.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、T:14/B:14<15、y>=370 IoU=0.5392<0.96），另 primaryMuscles 为空，待重制。",
    "exercise_seated_shoulder_press": "待修图 · SeedExercises 动图 motion_seated_shoulder_press.webp（4 帧 380ms，同 0405）底区域 y>=370 IoU=0.9234<0.96（y>=415 IoU=0.8392）、F3 头部与靠背等比缩放约 12-16 px；另器材混标 fixed machine 且缺 requiredEquipment=[\"直立靠背训练凳\"] 与 primaryMuscles，待重制。",
    "exercise_band_external_rotation": "待修图 · SeedExercises 动图 motion_band_external_rotation.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、L:13/R:13<15、y>=370 IoU=0.1959<0.96），另 primaryMuscles 为空，待重制。",
    "exercise_sit_to_stand": "待修图 · SeedExercises 动图 motion_sit_to_stand.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、T:12/B:7<15、y>=370 IoU=0.1652<0.96），另步骤要求稳定椅子却缺支撑件标定且 primaryMuscles 为空，待重制。",
}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text(encoding="utf-8"))
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review135-20270121",
    "inspected": inspected,
    "review_candidates": review_candidates,
    "registered_media": registered_media,
    "definition_updates": definition_updates,
    "pending": pending,
    "sources": {},
    "review_notes": {},
    "image_generation_calls": 0,
    "generated_images_imported": 0,
}
(B / "review-result.json").write_text(json.dumps(review_result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

code_paths = [
    "app/src/main/java",
    "scripts/validate_exercise_dataset.sh",
    "scripts/build_android_debug.sh",
]
baseline = {}
for rel in code_paths:
    p = R / rel
    if p.is_file():
        baseline[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    else:
        for f in sorted(p.rglob("*")):
            if f.is_file():
                baseline[str(f.relative_to(R))] = hashlib.sha256(f.read_bytes()).hexdigest()
(B / "code-baseline.json").write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

qa_spec = {
    "batch": BATCH_ID,
    "expected_checks": 20,
    "expected_reviewed_after_approve": reviewed_count,
    "candidate_ids": [],
    "candidate_required_equipment": {},
    "expected_per_side_ids": ["exercise_one_arm_dumbbell_row"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

parser = argparse.ArgumentParser()
parser.add_argument("--stage", action="store_true")
args = parser.parse_args()

if args.stage:
    reviews_path = R / "app/src/main/assets/exercise_reviews.json"
    reviews = json.loads(reviews_path.read_text(encoding="utf-8"))
    existing_pending = {item["id"]: i for i, item in enumerate(reviews["pending"])}
    for eid in inspected:
        entry = {"id": eid, "note": pending[eid]}
        if eid in existing_pending:
            reviews["pending"][existing_pending[eid]] = entry
        else:
            reviews["pending"].append(entry)
    reviews_path.write_text(json.dumps(reviews, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    state_path = R / "assets/motion_repairs/review-workflow-state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["active_batch"] = None
    state["last_updated"] = "2027-01-21"
    deferred = state.get("deferred_ids", [])
    for eid in inspected:
        if eid not in deferred:
            deferred.append(eid)
    state["deferred_ids"] = deferred
    pending_batches = state.get("apk_qa_pending_batches", [])
    if BATCH_ID not in pending_batches:
        pending_batches.append(BATCH_ID)
    state["apk_qa_pending_batches"] = pending_batches
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Staged {len(inspected)} pending 待修图 seed entries and queued {BATCH_ID} for APK QA")
else:
    print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
