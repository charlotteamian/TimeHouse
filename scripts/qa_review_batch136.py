#!/usr/bin/env python3
"""Batch 136 Final SeedExercises (remaining 14 with media): verify loaded catalog semantics, raw WebP decode, and review gate."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

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

media_names = [
    "motion_goblet_squat",
    "motion_glute_bridge",
    "motion_romanian_deadlift",
    "motion_step_up",
    "motion_dead_bug",
    "motion_plank",
    "motion_pallof_press",
    "motion_bird_dog",
    "motion_dumbbell_curl",
    "motion_inverted_row",
    "dataset_motion_0808",
    "dataset_motion_0426",
    "dataset_motion_0549",
    "dataset_motion_0662",
]

names = {
    "exercise_goblet_squat": "杯式深蹲",
    "exercise_glute_bridge": "臀桥",
    "exercise_romanian_deadlift": "罗马尼亚硬拉",
    "exercise_step_up": "台阶上步",
    "exercise_dead_bug": "死虫",
    "exercise_plank": "平板支撑",
    "exercise_pallof_press": "帕洛夫抗旋推",
    "exercise_bird_dog": "鸟狗",
    "exercise_dumbbell_curl": "哑铃弯举",
    "custom_inverted_row_unverified": "自定义倒立划船",
    "exercise_trx_row": "TRX 反向划船",
    "exercise_dumbbell_overhead_press": "哑铃推举",
    "exercise_kettlebell_swing": "壶铃摇摆",
    "exercise_pushup": "俯卧撑",
}

stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join(inspected),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    row = lambda x: catalog[x]

    verified_seed_ids = [x for x in inspected if x != "custom_inverted_row_unverified"]
    check(not any(x in known for x in inspected), "All 14 Batch 136 SeedExercises entries remain unreviewed during initial checks")
    check("supportReviewInvalidation=1" in raw, "Supporting equipment changes invalidate stale personal approval")
    check(
        row("exercise_goblet_squat")["equipment"] == ["哑铃", "壶铃"]
        and row("exercise_trx_row")["equipment"] == ["TRX 悬挂带"]
        and row("custom_inverted_row_unverified")["equipment"] == ["神秘器械"]
        and not row("custom_inverted_row_unverified")["safeWithRequiredEquipment"]
        and all(row(x)["available"][row(x)["equipment"][0]] and row(x)["safeWithRequiredEquipment"] for x in verified_seed_ids),
        "Batch 136 maps SeedExercises equipment accurately and keeps USER_UNVERIFIED blocked",
    )
    check(
        row("exercise_plank")["isHold"]
        and not any(row(x)["isHold"] for x in inspected if x != "exercise_plank")
        and row("exercise_step_up")["perSide"]
        and row("exercise_dead_bug")["perSide"]
        and not any(row(x)["perSide"] for x in inspected if x not in {"exercise_step_up", "exercise_dead_bug"}),
        "Plank stays isometric hold and step-up/dead-bug stay unilateral while others remain dynamic bilateral",
    )
    check(
        row("exercise_romanian_deadlift")["lower_back"] == "HIGH"
        and row("exercise_kettlebell_swing")["lower_back"] == "HIGH"
        and row("exercise_plank")["safeSevereShoulder"]
        and row("exercise_dead_bug")["safeSevereShoulder"]
        and row("exercise_goblet_squat")["safeSevereShoulder"]
        and not row("exercise_trx_row")["safeSevereShoulder"]
        and not row("exercise_dumbbell_overhead_press")["safeSevereShoulder"]
        and not row("exercise_pushup")["safeSevereShoulder"],
        "Joint stress screening reflects high lower-back load and severe-shoulder safety accurately",
    )

    decoded = adb(
        "shell", "am", "instrument", "-w",
        "-e", "media", ",".join(media_names),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    check("decodedAnimations=14" in decoded, "Android ImageDecoder decodes all 14 Batch 136 WebP animations")

    eq_str = "自重|哑铃|杠铃|壶铃|弹力带|固定器械|TRX 悬挂带|神秘器械"
    for eid in inspected:
        item = {
            "id": eid,
            "sets": 1,
            "reps": "10",
            "rpe": "7",
            "rest": 30,
            "kind": "HOLD" if row(eid)["isHold"] else "REPS",
            "hold": 30 if row(eid)["isHold"] else 0,
            "perSide": bool(row(eid)["perSide"]),
            "tempo": 3,
            "reason": "",
            "restAfter": 0,
        }
        workout = {"version": 1, "title": "种子门控验证136", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment=eq_str, workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[eid] + " remains blocked prior to approval by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND THIRTY-SIX INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
