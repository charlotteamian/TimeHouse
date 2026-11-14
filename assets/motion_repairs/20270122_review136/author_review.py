#!/usr/bin/env python3
"""Author Final Batch 136 inspection of the remaining 14 SeedExercises with bundled media (0 approved, 14 deferred to 待修图; 待核逻辑 -> 0)."""
from pathlib import Path
import argparse
import hashlib
import json

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20270122_review136"
VERSION = "1.2.140"
VERSION_CODE = 2027012201

inspected = [
    "exercise_goblet_squat",
    "exercise_glute_bridge",
    "exercise_romanian_deadlift",
    "exercise_step_up",
    "exercise_dead_bug",
    "exercise_plank",
    "exercise_pallof_press",
    "exercise_bird_dog",
    "exercise_dumbbell_curl",
    "custom_inverted_row_unverified",
    "exercise_trx_row",
    "exercise_dumbbell_overhead_press",
    "exercise_kettlebell_swing",
    "exercise_pushup",
]
review_candidates = []
registered_media = []
definition_updates = {}

pending = {
    "exercise_goblet_squat": "待修图 · SeedExercises 动图 motion_goblet_squat.webp（4 帧 380ms，同 1760）虽白底清晰，但底缘支撑区 y>=370 IoU=0.7052<0.96（双脚 y>=415 IoU=0.9100<0.96，F3 前掌外移 +6..12 px）；另器械混标“哑铃/壶铃”、步骤三含“保持”且 primaryMuscles 为空，待锁定双足对齐并完善元数据。",
    "exercise_glute_bridge": "待修图 · SeedExercises 动图 motion_glute_bridge.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、L:14/R:14<15 且中段轮廓模糊叠影），另混标杠铃且 primaryMuscles 为空，待重制。",
    "exercise_romanian_deadlift": "待修图 · SeedExercises 动图 motion_romanian_deadlift.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、T:14/B:14<15、y>=370 IoU=0.1838<0.96 且中段重影），另步骤二含“保持”且 primaryMuscles 为空，待重制。",
    "exercise_step_up": "待修图 · SeedExercises 动图 motion_step_up.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、T:13/B:13<15、y>=370 IoU=0.1581<0.96），另缺 requiredEquipment=[\"稳固踏台\"]、步骤三含“保持”且 primaryMuscles 为空，待重制。",
    "exercise_dead_bug": "待修图 · SeedExercises 动图 motion_dead_bug.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、L:14/R:14<15 且中段四肢半透明叠影），另步骤三含“保持”且 primaryMuscles 为空，待重制。",
    "exercise_plank": "待修图 · SeedExercises 动图 motion_plank.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、L:13/R:12<15 且帧间几乎静止 mean_d02=0.66），另 primaryMuscles 为空，待重制为标准 4 帧静态核心图。",
    "exercise_pallof_press": "待修图 · SeedExercises 动图 motion_pallof_press.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、L:14/R:13<15、y>=370 IoU=0.0368<0.96 且横向偏移），另 primaryMuscles 为空，待重制。",
    "exercise_bird_dog": "待修图 · SeedExercises 动图 motion_bird_dog.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、L:14/R:13<15 且中段手脚叠影），另对侧交替动作缺“双侧”标记（perSide=false）、步骤含“保持”且 primaryMuscles 为空，待重制。",
    "exercise_dumbbell_curl": "待修图 · SeedExercises 动图 motion_dumbbell_curl.webp（4 帧 380ms，同 0294）存在非纯白角落 ([254,254,254]) 及头部顶缘贴边 T=4<15 px；另 primaryMuscles 为空，待扩边距重制。",
    "custom_inverted_row_unverified": "待修图 · SeedExercises 未核验条目“自定义倒立划船”配图 motion_inverted_row.webp 为 10 帧 70ms 程序插值轮廓图（边角 [253,253,253]、L:13/R:12<15、y>=370 IoU=0.3750<0.96），且为 USER_UNVERIFIED 占位（器材“神秘器械”、步骤“尚未审核”），待补齐正规动作定义并重制。",
    "exercise_trx_row": "待修图 · SeedExercises 动图 dataset_motion_0808.webp（4 帧 380ms）存在底脚位移 y>=370 IoU=0.8734<0.96（y>=415 IoU=0.8558<0.96，F1 鞋底高于 F2-F4 约 28 px 且 F3 墙面锚点上跳 8 px）；另步骤一含“保持”且 primaryMuscles 为空，待修正锚点与双足重制。",
    "exercise_dumbbell_overhead_press": "待修图 · SeedExercises 动图 dataset_motion_0426.webp（4 帧 380ms）存在角落偏灰 ([253,253,252])、T:0/B:1<15 px（F3 顶缘触边 y=0、F1 底缘触边 y=478）及 y>=370 IoU=0.8993<0.96；另步骤含“保持”且 primaryMuscles 为空，待扩边距重制。",
    "exercise_kettlebell_swing": "待修图 · SeedExercises 动图 dataset_motion_0549.webp（4 帧 380ms）存在底缘大幅位移 y>=370 IoU=0.9465<0.96（y>=415 IoU=0.0000，F1 底缘 y=451 较 F2-F4 y=406 下移 45 px 致脚踝与壶铃高度漂移），另 primaryMuscles 为空，待重制。",
    "exercise_pushup": "待修图 · SeedExercises 动图 dataset_motion_0662.webp（4 帧 380ms）存在边角偏灰 ([254,254,254]/[254,255,254]) 且 F3 右侧脚尖距边缘仅 R=2<15 px；另步骤一含“保持”且 primaryMuscles 为空，待扩边距重制。",
}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text(encoding="utf-8"))
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review136-20270122",
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
    "expected_per_side_ids": ["exercise_step_up", "exercise_dead_bug"],
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
    state["last_updated"] = "2027-01-22"
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
