#!/usr/bin/env python3
"""Batch sixty-one candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["3637", "3638", "3639", "3640", "3645", "3655", "3656", "3662", "3663", "3665"]
per_side_ids = {"3638", "3639", "3640", "3645", "3655", "3663", "3665"}
hold_ids = set()
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
        all(row(x)["primary"] == ["心肺系统", "股四头肌"] for x in ["3638", "3655", "3656"])
        and row("3637")["primary"] == ["腹肌", "核心肌群"]
        and row("3639")["primary"] == ["腹肌", "腹斜肌"]
        and row("3640")["primary"] == ["腹肌", "髋屈肌群"]
        and row("3645")["primary"] == ["臀肌", "腘绳肌"]
        and row("3662")["primary"] == ["胸肌"]
        and row("3663")["primary"] == ["腹肌", "臀肌"]
        and row("3665")["primary"] == ["腹肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        all(row(x)["requiredEquipment"] == [] for x in inspected),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 61 configures dynamic alternating reps without hold triggers and sets unilateral climbers/twists/lunges cleanly",
    )
    check(
        all(row(x)["knee"] == "MEDIUM" for x in ["3638", "3645", "3655", "3656"])
        and all(row(x)["lower_back"] == "MEDIUM" for x in ["3637", "3639", "3640", "3663", "3665"])
        and row("3662")["lower_back"] == "NONE" and row("3662")["knee"] == "NONE",
        "Joint stress screening reflects lower-body knee load, core low-back stress, and chest push-up safety",
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
        state_with(reviewedOnlyV1=False, equipment="自重", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH SIXTY-ONE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
