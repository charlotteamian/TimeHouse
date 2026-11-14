#!/usr/bin/env python3
"""Batch sixty candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["3533", "3664", "3543", "3888", "3544", "5201", "3552", "3561", "3582", "3636"]
per_side_ids = {"3664", "3888", "3544", "3552", "3561", "3582", "3636"}
hold_ids = {"3664", "3544"}
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
        row("3533")["primary"] == ["股四头肌"]
        and row("3664")["primary"] == ["上背"]
        and row("3543")["primary"] == ["心肺系统", "股四头肌"]
        and all(row(x)["primary"] == ["臀肌", "腘绳肌"] for x in ["3888", "3561"])
        and row("3544")["primary"] == ["腹肌", "腹斜肌"]
        and row("5201")["primary"] == ["肱二头肌", "前臂"]
        and all(row(x)["primary"] == ["心肺系统", "股四头肌"] for x in ["3552", "3582", "3636"]),
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        row("3636")["requiredEquipment"] == ["墙面"]
        and row("3636")["available"]["墙面"]
        and not row("3636")["available"]["自重"]
        and all(row(x)["requiredEquipment"] == [] for x in inspected if x != "3636"),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        all(row(x)["isHold"] for x in hold_ids)
        and not any(row(x)["isHold"] for x in inspected if x not in hold_ids)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 60 flags isometric side-plank variations as HOLD and configures unilateral snatch/lunges/kicks cleanly",
    )
    check(
        all(row(x)["knee"] == "MEDIUM" and row(x)["lower_back"] == "NONE" for x in ["3533", "3543", "3888", "3552", "3561", "3582", "3636"])
        and row("3544")["lower_back"] == "MEDIUM" and row("3544")["knee"] == "NONE"
        and all(row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["3664", "5201"]),
        "Joint stress screening reflects lower-body knee load, core side-bridge stress, and arm curl safety",
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
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|墙面", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH SIXTY INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
