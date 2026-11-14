#!/usr/bin/env python3
"""Batch eighty-one candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["0218", "0219", "0220", "0221", "0222", "0223", "0224", "0225", "0226", "0227"]
per_side_ids = {"0221", "0222", "0223"}
flat_bench_ids = {"0218"}
bosu_ball_ids = {"0221"}
no_support_ids = {"0219", "0220", "0222", "0223", "0224", "0225", "0226", "0227"}
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
        row("0218")["primary"] == ["上背"]
        and all(row(x)["primary"] == ["三角肌"] for x in ["0219", "0225"])
        and row("0220")["primary"] == ["斜方肌"]
        and all(row(x)["primary"] == ["腹肌"] for x in ["0221", "0222", "0223", "0226"])
        and row("0224")["primary"] == ["前臂"]
        and row("0227")["primary"] == ["胸肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        all(row(x)["requiredEquipment"] == ["平板训练凳"] and row(x)["safeWithRequiredEquipment"] for x in flat_bench_ids)
        and all(row(x)["requiredEquipment"] == ["半圆平衡球"] and row(x)["safeWithRequiredEquipment"] for x in bosu_ball_ids)
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in no_support_ids),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 81 avoids hold triggers and configures unilateral side bends and crunches cleanly",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in ["0218", "0220"])
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["0219", "0225", "0227"])
        and all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in ["0221", "0222", "0223", "0226"])
        and row("0224")["shoulder"] == "NONE" and row("0224")["lower_back"] == "NONE" and row("0224")["knee"] == "NONE",
        "Joint stress screening reflects shoulder and back loading for cable rows and shrugs, shoulder loading for overhead presses, reverse flys, and chest flys, back loading for waist twists and crunches, and zero stress for wrist curls",
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
            "perSide": xid in per_side_ids,
            "tempo": 3,
            "reason": "",
            "restAfter": 0,
        }
        workout = {"version": 1, "title": "暂缓项门控验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="固定器械|平板训练凳|半圆平衡球", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH EIGHTY-ONE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
