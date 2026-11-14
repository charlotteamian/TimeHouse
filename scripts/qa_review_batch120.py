#!/usr/bin/env python3
"""Batch one hundred and twenty candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["1634", "1635", "1636", "1637", "1638", "1639", "1640", "1641", "1642", "1643"]
per_side_ids = {"1635", "1640", "1642"}
bilateral_ids = set(inspected) - per_side_ids
no_support_ids = {"1636", "1638"}
preacher_ids = {"1635", "1639", "1640"}
flat_ids = {"1634", "1642"}
upright_ids = {"1641", "1643"}
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
        all(row(x)["primary"] == ["肱二头肌"] for x in inspected),
        "Primary muscle groups match biceps across all ten cable curl entries",
    )
    check(
        all(row(x)["requiredEquipment"] == ["平板训练凳"] for x in flat_ids)
        and all(row(x)["requiredEquipment"] == ["牧师凳"] for x in preacher_ids)
        and row("1637")["requiredEquipment"] == ["瑜伽球"]
        and all(row(x)["requiredEquipment"] == ["直立靠背训练凳"] for x in upright_ids)
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in no_support_ids),
        "All ten inspected entries enforce flat, preacher, ball, and upright bench supports cleanly",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and all(not row(x)["perSide"] for x in bilateral_ids),
        "Batch 120 avoids false hold triggers on 1635 and activates unilateral perSide pacing on 1635, 1640, and 1642",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in inspected),
        "Joint stress screening reflects conservative biceps shoulder loading across all ten entries",
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
        state_with(reviewedOnlyV1=False, equipment="平板训练凳|牧师凳|瑜伽球|直立靠背训练凳", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND TWENTY INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
