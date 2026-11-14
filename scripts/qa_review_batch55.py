#!/usr/bin/env python3
"""Batch fifty-five candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["3292", "2321", "3293", "2327", "3294", "2397", "3295", "2401", "3296", "2402"]
per_side_ids = {"3293", "3294"}
hold_ids = {"3296"}
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
        all(row(x)["primary"] == ["上背"] for x in ["3292", "2327", "3295"])
        and all(row(x)["primary"] == ["肱二头肌", "前臂"] for x in ["2321", "2401", "2402"])
        and row("3293")["primary"] == ["背阔肌"]
        and row("3294")["primary"] == ["胸肌"]
        and row("2397")["primary"] == ["三角肌"]
        and row("3296")["primary"] == ["腹肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        all(row(x)["requiredEquipment"] == ["单杠"] and row(x)["available"]["单杠"] and not row(x)["available"]["自重"] for x in ["3293", "3295", "3296"])
        and row("2397")["requiredEquipment"] == ["直立靠背训练凳"]
        and row("2397")["available"]["哑铃|直立靠背训练凳"]
        and not row("2397")["available"]["哑铃"]
        and all(row(x)["requiredEquipment"] == [] for x in ["3292", "2321", "2327", "3294", "2401", "2402"]),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        all(row(x)["isHold"] for x in hold_ids)
        and not any(row(x)["isHold"] for x in inspected if x not in hold_ids)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 55 distinguishes front-lever isometric hold from dynamic reps and sets unilateral archer modes cleanly",
    )
    check(
        all(row(x)["lower_back"] == "MEDIUM" for x in ["3292", "3293", "2327", "3295", "3296"])
        and all(row(x)["lower_back"] == "NONE" for x in ["2321", "3294", "2397", "2401", "2402"])
        and all(row(x)["knee"] == "NONE" for x in inspected),
        "Joint stress screening reflects back/waist axial pull load and arm/chest/shoulder safety",
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
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|单杠|直立靠背训练凳", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH FIFTY-FIVE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
