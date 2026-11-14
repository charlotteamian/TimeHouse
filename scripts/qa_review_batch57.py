#!/usr/bin/env python3
"""Batch fifty-seven candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["3302", "2803", "3303", "2805", "3304", "2808", "3314", "2812", "3315", "3234"]
per_side_ids = {"2805", "2812"}
hold_ids = {"3302", "3303", "3314", "3315"}
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
        row("3302")["primary"] == ["肱三头肌"]
        and all(row(x)["primary"] == ["股四头肌"] for x in ["2803", "2812"])
        and row("3303")["primary"] == ["腹肌", "腹斜肌"]
        and all(row(x)["primary"] == ["臀肌", "腘绳肌"] for x in ["2805", "2808"])
        and row("3304")["primary"] == ["上背"]
        and all(row(x)["primary"] == ["腹肌"] for x in ["3314", "3315"])
        and row("3234")["primary"] == ["胸肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        row("3303")["requiredEquipment"] == ["稳固立柱"]
        and row("3303")["safeWithRequiredEquipment"]
        and not row("3303")["available"]["自重"]
        and all(row(x)["requiredEquipment"] == ["稳固踏台"] and row(x)["safeWithRequiredEquipment"] and not row(x)["available"]["哑铃"] for x in ["2805", "2812"])
        and row("3304")["requiredEquipment"] == ["单杠"]
        and row("3304")["available"]["单杠"]
        and not row("3304")["available"]["自重"]
        and all(row(x)["requiredEquipment"] == ["吊环"] and row(x)["safeWithRequiredEquipment"] and not row(x)["available"]["自重"] for x in ["3314", "3315"])
        and row("3234")["requiredEquipment"] == ["平板训练凳"]
        and row("3234")["available"]["哑铃|平板训练凳"]
        and not row("3234")["available"]["哑铃"]
        and all(row(x)["requiredEquipment"] == [] for x in ["3302", "2803", "2808"]),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        all(row(x)["isHold"] for x in hold_ids)
        and not any(row(x)["isHold"] for x in inspected if x not in hold_ids)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 57 flags isometric handstand, flag, and ring maltese as HOLD and configures unilateral step-ups and deadlifts cleanly",
    )
    check(
        all(row(x)["knee"] == "MEDIUM" and row(x)["lower_back"] == "NONE" for x in ["2803", "2805", "2808", "2812"])
        and all(row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in ["3303", "3304", "3314", "3315"])
        and all(row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["3302", "3234"]),
        "Joint stress screening reflects squat/deadlift knee load, lever/ring low-back stress, and handstand/fly safety",
    )

    for xid in inspected:
        is_hold = xid in hold_ids
        item = {
            "id": "dataset_1324_" + xid,
            "sets": 1,
            "reps": "20" if is_hold else "8",
            "rpe": "7",
            "rest": 30,
            "kind": "HOLD" if is_hold else "REPS",
            "hold": 20 if is_hold else 0,
            "perSide": xid in per_side_ids,
            "tempo": 3,
            "reason": "",
            "restAfter": 0,
        }
        workout = {"version": 1, "title": "暂缓项门控验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|单杠|稳固踏台|稳固立柱|吊环|平板训练凳", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH FIFTY-SEVEN INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
