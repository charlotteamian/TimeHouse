#!/usr/bin/env python3
"""Batch fifty-nine candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["3419", "3546", "3420", "3547", "3433", "3548", "3470", "3560", "3523", "3635"]
per_side_ids = {"3546", "3433", "3548", "3470", "3560", "3635"}
hold_ids = {"3419", "3420"}
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
        all(row(x)["primary"] == ["腹肌", "髋屈肌群"] for x in ["3419", "3420"])
        and all(row(x)["primary"] == ["三角肌"] for x in ["3546", "3548"])
        and row("3547")["primary"] == ["肱二头肌", "肩部"]
        and row("3560")["primary"] == ["肱二头肌", "前臂"]
        and all(row(x)["primary"] == ["臀肌", "腘绳肌"] for x in ["3433", "3523"])
        and all(row(x)["primary"] == ["臀肌", "股四头肌"] for x in ["3470", "3635"]),
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        all(row(x)["requiredEquipment"] == ["平板训练凳"] and row(x)["available"]["平板训练凳"] and not row(x)["available"]["自重"] for x in ["3523"])
        and row("3546")["requiredEquipment"] == ["平板训练凳"]
        and row("3546")["available"]["哑铃|平板训练凳"]
        and not row("3546")["available"]["哑铃"]
        and row("3547")["requiredEquipment"] == ["直立靠背训练凳"]
        and row("3547")["available"]["哑铃|直立靠背训练凳"]
        and not row("3547")["available"]["哑铃"]
        and all(row(x)["requiredEquipment"] == [] for x in ["3419", "3420", "3433", "3548", "3470", "3560", "3635"]),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        all(row(x)["isHold"] for x in hold_ids)
        and not any(row(x)["isHold"] for x in inspected if x not in hold_ids)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 59 flags isometric L-sit and V-sit as HOLD and configures unilateral presses/lunges/kicks cleanly",
    )
    check(
        all(row(x)["lower_back"] == "MEDIUM" for x in ["3419", "3420"])
        and all(row(x)["knee"] == "MEDIUM" for x in ["3433", "3470", "3523", "3635"])
        and all(row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["3546", "3547", "3548", "3560"]),
        "Joint stress screening reflects core L/V-sit low-back stress, lower-body knee load, and arm/shoulder safety",
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
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|平板训练凳|直立靠背训练凳", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH FIFTY-NINE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
