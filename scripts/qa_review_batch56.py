#!/usr/bin/env python3
"""Batch fifty-six candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["3297", "2403", "3298", "2470", "3299", "2705", "3300", "2706", "3301", "2796"]
per_side_ids = {"2403", "2796"}
hold_ids = {"3297", "3298", "3299", "3300", "3301"}
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
        row("3297")["primary"] == ["上背"]
        and row("2403")["primary"] == ["肱二头肌", "前臂"]
        and all(row(x)["primary"] == ["腹肌"] for x in ["3298", "3299", "3300", "3301"])
        and row("2470")["primary"] == ["三角肌"]
        and all(row(x)["primary"] == ["前臂"] for x in ["2705", "2706"])
        and row("2796")["primary"] == ["股四头肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        row("3297")["requiredEquipment"] == ["单杠"]
        and row("3297")["available"]["单杠"]
        and not row("3297")["available"]["自重"]
        and row("2796")["requiredEquipment"] == ["稳固踏台"]
        and row("2796")["safeWithRequiredEquipment"]
        and not row("2796")["available"]["哑铃"]
        and all(row(x)["requiredEquipment"] == [] for x in ["2403", "3298", "2470", "3299", "2705", "3300", "2706", "3301"]),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        all(row(x)["isHold"] for x in hold_ids)
        and not any(row(x)["isHold"] for x in inspected if x not in hold_ids)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 56 flags isometric back-lever and planches as HOLD and configures unilateral curls and step-ups cleanly",
    )
    check(
        all(row(x)["lower_back"] == "MEDIUM" for x in ["3297", "3298", "3299", "3300", "3301"])
        and row("2796")["knee"] == "MEDIUM"
        and all(row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["2403", "2470", "2705", "2706"]),
        "Joint stress screening reflects lever/planche low-back load, step-up knee load, and arm-day safety",
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
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|单杠|稳固踏台", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH FIFTY-SIX INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
