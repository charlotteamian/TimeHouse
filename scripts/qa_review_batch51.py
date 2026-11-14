#!/usr/bin/env python3
"""Batch fifty-one candidates: verify all ten stay unreviewed while anatomy, supports, and steps update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["3204", "1737", "3212", "1738", "3213", "1739", "3214", "1740", "3215", "1741"]
per_side_ids = {"1738", "3214", "1740"}
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
        row("3204")["primary"] == ["腹肌"]
        and row("3213")["primary"] == ["腹肌", "腹斜肌"]
        and all(row(x)["primary"] == ["肱三头肌"] for x in ["1737", "1738", "1739", "1740", "1741"])
        and all(row(x)["primary"] == ["臀肌", "腘绳肌"] for x in ["3212", "3214", "3215"]),
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        all(row(x)["requiredEquipment"] == ["平板训练凳"] and row(x)["available"]["哑铃|平板训练凳"] and not row(x)["available"]["哑铃"] for x in ["1737", "1738"])
        and all(row(x)["requiredEquipment"] == [] for x in ["3204", "3212", "3213", "1739", "3214", "1740", "3215", "1741"]),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in ["3204", "1737", "3212", "3213", "1739", "3215", "1741"]),
        "Batch 51 avoids hold triggers while configuring unilateral/bilateral rep modes accurately",
    )
    check(
        all(row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["1737", "1738", "1739", "1740", "1741"])
        and all(row(x)["knee"] == "MEDIUM" for x in ["3212", "3214", "3215"])
        and all(row(x)["lower_back"] == "MEDIUM" for x in ["3204", "3213"]),
        "Joint stress screening reflects lower-leg toe-touch knee load, sit-up axial load, and triceps low-back safety",
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
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|平板训练凳", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH FIFTY-ONE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
