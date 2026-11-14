#!/usr/bin/env python3
"""Batch one hundred and twenty-three deferred items: verify anatomy, dumbbell/support mapping, hold/perSide, and review gate."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["1723", "1724", "1725", "1726", "1727", "1728", "1744", "1745", "1747", "1748"]
per_side_ids = {"1723", "1727", "1745"}
bilateral_ids = set(inspected) - per_side_ids
ball_support_ids = {"1745", "1747"}
no_support_ids = set(inspected) - {"1725", "1745", "1747", "1748"}
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
        all(row(x)["primary"] == ["肱三头肌"] for x in inspected),
        "All ten Batch 123 triceps entries map cleanly to primary triceps",
    )
    check(
        row("1725")["requiredEquipment"] == ["上斜训练凳"]
        and all(row(x)["requiredEquipment"] == ["瑜伽球"] for x in ball_support_ids)
        and row("1745")["equipment"] == ["哑铃"]
        and row("1744")["equipment"] == ["瑜伽球"]
        and row("1748")["requiredEquipment"] == ["平板训练凳"]
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in no_support_ids),
        "Batch 123 enforces incline bench, stability ball, flat bench supports, and 1745 dumbbell equipment correction",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and all(not row(x)["perSide"] for x in bilateral_ids),
        "Batch 123 avoids hold triggers while activating unilateral perSide pacing on 1723, 1727, and 1745",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in inspected),
        "Joint stress screening reflects upper-arm triceps loading accurately",
    )

    for xid in inspected:
        item = {
            "id": "dataset_1324_" + xid,
            "sets": 1,
            "reps": "10",
            "rpe": "7",
            "rest": 30,
            "kind": "REPS",
            "hold": 0,
            "perSide": xid in per_side_ids,
            "tempo": 3,
            "reason": "",
            "restAfter": 0,
        }
        workout = {"version": 1, "title": "暂缓门控验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="上斜训练凳|瑜伽球|平板训练凳|哑铃|EZ 杠", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked prior to approval by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND TWENTY-THREE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
