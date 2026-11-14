#!/usr/bin/env python3
"""Batch 135 SeedExercises (first 14 with media): verify loaded catalog semantics, raw WebP decode, and review gate."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

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

media_names = [
    "motion_lat_pulldown",
    "motion_band_row",
    "motion_one_arm_dumbbell_row",
    "motion_seated_row",
    "motion_band_pulldown",
    "motion_bent_over_barbell_row",
    "motion_face_pull",
    "motion_wall_pushup",
    "motion_incline_pushup",
    "motion_dumbbell_bench_press",
    "motion_seated_chest_press",
    "motion_seated_shoulder_press",
    "motion_band_external_rotation",
    "motion_sit_to_stand",
]

names = {
    "exercise_lat_pulldown": "高位下拉",
    "exercise_band_row": "弹力带划船",
    "exercise_one_arm_dumbbell_row": "单臂哑铃划船",
    "exercise_seated_row": "坐姿划船",
    "exercise_band_pulldown": "弹力带下拉",
    "exercise_bent_over_barbell_row": "杠铃俯身划船",
    "exercise_face_pull": "面拉",
    "exercise_wall_pushup": "墙壁俯卧撑",
    "exercise_incline_pushup": "上斜俯卧撑",
    "exercise_dumbbell_bench_press": "哑铃卧推",
    "exercise_seated_chest_press": "坐姿推胸",
    "exercise_seated_shoulder_press": "坐姿肩推",
    "exercise_band_external_rotation": "弹力带外旋",
    "exercise_sit_to_stand": "坐站",
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

    check(not any(x in known for x in inspected), "All 14 Batch 135 SeedExercises entries remain unreviewed during initial checks")
    check("supportReviewInvalidation=1" in raw, "Supporting equipment changes invalidate stale personal approval")
    check(
        row("exercise_lat_pulldown")["equipment"] == ["高位下拉器", "固定器械"]
        and row("exercise_one_arm_dumbbell_row")["equipment"] == ["哑铃"]
        and row("exercise_dumbbell_bench_press")["equipment"] == ["哑铃"]
        and row("exercise_seated_shoulder_press")["equipment"] == ["哑铃", "固定器械"]
        and row("exercise_bent_over_barbell_row")["equipment"] == ["杠铃"]
        and all(row(x)["available"][row(x)["equipment"][0]] for x in inspected)
        and all(row(x)["safeWithRequiredEquipment"] for x in inspected),
        "Batch 135 SeedExercises equipment mappings and requiredEquipment availability match SeedExercises definitions",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and row("exercise_one_arm_dumbbell_row")["perSide"]
        and not any(row(x)["perSide"] for x in inspected if x != "exercise_one_arm_dumbbell_row"),
        "One-arm dumbbell row keeps perSide pacing while all 14 stay dynamic",
    )
    check(
        row("exercise_seated_shoulder_press")["shoulder"] == "HIGH"
        and row("exercise_bent_over_barbell_row")["lower_back"] == "HIGH"
        and not row("exercise_seated_shoulder_press")["safeSevereShoulder"]
        and not row("exercise_lat_pulldown")["safeSevereShoulder"]
        and row("exercise_band_external_rotation")["safeSevereShoulder"]
        and row("exercise_sit_to_stand")["safeSevereShoulder"],
        "Joint stress screening reflects high shoulder/lower-back constraints cleanly",
    )

    decoded = adb(
        "shell", "am", "instrument", "-w",
        "-e", "media", ",".join(media_names),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    check("decodedAnimations=14" in decoded, "Android ImageDecoder decodes all 14 Batch 135 WebP animations")

    eq_str = "自重|哑铃|弹力带|固定器械|高位下拉器|杠铃"
    for eid in inspected:
        item = {
            "id": eid,
            "sets": 1,
            "reps": "10",
            "rpe": "7",
            "rest": 30,
            "kind": "REPS",
            "hold": 0,
            "perSide": bool(row(eid)["perSide"]),
            "tempo": 3,
            "reason": "",
            "restAfter": 0,
        }
        workout = {"version": 1, "title": "种子门控验证135", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment=eq_str, workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[eid] + " remains blocked prior to approval by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND THIRTY-FIVE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
