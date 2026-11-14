#!/usr/bin/env python3
"""Batch eighty-four candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["0248", "0271", "0272", "0445", "0446", "0447", "0448", "0449", "0450", "0451"]
per_side_ids = set()
flat_bench_ids = {"0248", "0450"}
stability_ball_ids = {"0271", "0272"}
decline_bench_ids = {"0448"}
incline_bench_ids = {"0449"}
no_support_ids = {"0445", "0446", "0447", "0451"}
names = {
    e["id"]: e["name_zh"]
    for e in json.loads(Path("app/src/main/assets/exercises_1324.json").read_text())["exercises"]
}

stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + s for s in inspected),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    row = lambda x: catalog["dataset_1324_" + x]

    check(not any("dataset_1324_" + x in known for x in inspected), "All ten inspected entries remain unreviewed during initial checks")
    check("supportReviewInvalidation=1" in raw, "Supporting equipment changes invalidate stale personal approval")
    check(
        row("0248")["primary"] == ["上背"]
        and all(row(x)["primary"] == ["腹肌"] for x in stability_ball_ids)
        and row("0445")["primary"] == ["三角肌"]
        and all(row(x)["primary"] == ["肱二头肌"] for x in ["0446", "0447", "0451"])
        and all(row(x)["primary"] == ["肱三头肌"] for x in ["0448", "0449", "0450"]),
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        all(row(x)["requiredEquipment"] == ["平板训练凳"] and row(x)["safeWithRequiredEquipment"] for x in flat_bench_ids)
        and all(row(x)["requiredEquipment"] == ["瑜伽球"] and row(x)["safeWithRequiredEquipment"] for x in stability_ball_ids)
        and all(row(x)["requiredEquipment"] == ["带勾脚的下斜训练凳"] and row(x)["safeWithRequiredEquipment"] for x in decline_bench_ids)
        and all(row(x)["requiredEquipment"] == ["上斜训练凳"] and row(x)["safeWithRequiredEquipment"] for x in incline_bench_ids)
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in no_support_ids),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and not any(row(x)["perSide"] for x in inspected),
        "Batch 84 avoids hold triggers and configures bilateral rep pacing cleanly",
    )
    check(
        row("0248")["shoulder"] == "MEDIUM" and row("0248")["lower_back"] == "MEDIUM" and row("0248")["knee"] == "NONE"
        and all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in stability_ball_ids)
        and row("0445")["shoulder"] == "MEDIUM" and row("0445")["lower_back"] == "NONE" and row("0445")["knee"] == "NONE"
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["0446", "0447", "0448", "0449", "0450", "0451"]),
        "Joint stress screening reflects shoulder and back loading for cambered bar rows, back loading for stability ball crunches, and shoulder loading for ez barbell presses, curls, and triceps extensions",
    )

    for xid in inspected:
        item = {
            "id": "dataset_1324_" + xid,
            "sets": 1,
            "reps": "8",
            "rpe": "7",
            "rest": 30,
            "kind": "REPS",
            "hold": 0,
            "perSide": False,
            "tempo": 3,
            "reason": "",
            "restAfter": 0,
        }
        workout = {"version": 1, "title": "暂缓项门控验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="自由重量|平板训练凳|瑜伽球|上斜训练凳|带勾脚的下斜训练凳", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH EIGHTY-FOUR INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
