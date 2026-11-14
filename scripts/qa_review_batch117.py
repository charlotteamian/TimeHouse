#!/usr/bin/env python3
"""Batch one hundred and seventeen candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["1439", "1451", "1452", "1456", "1457", "1458", "1461", "1462", "1463", "1464"]
leg_ids = {"1461", "1462", "1463", "1464"}
shoulder_ids = {"1456", "1457"}
no_support_ids = set(inspected) - {"1458"}
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
        row("1439")["primary"] == ["斜方肌"]
        and row("1451")["primary"] == ["肱三头肌"]
        and row("1452")["primary"] == ["腹肌"]
        and all(row(x)["primary"] == ["三角肌"] for x in shoulder_ids)
        and row("1458")["primary"] == ["肱二头肌"]
        and all(row(x)["primary"] == ["臀肌"] for x in leg_ids),
        "Primary muscle groups match traps, triceps, abs, delts, biceps, and glutes cleanly",
    )
    check(
        row("1458")["requiredEquipment"] == ["平板训练凳"]
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in no_support_ids),
        "All ten inspected entries enforce flat bench support on 1458",
    )
    check(
        not any(row(x)["isHold"] or row(x)["perSide"] for x in inspected),
        "All ten bilateral exercises stay dynamic REPS with zero false hold or perSide triggers",
    )
    check(
        row("1439")["shoulder"] == "MEDIUM" and row("1439")["lower_back"] == "MEDIUM" and row("1439")["knee"] == "NONE"
        and row("1452")["shoulder"] == "NONE" and row("1452")["lower_back"] == "MEDIUM" and row("1452")["knee"] == "NONE"
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in {"1451", "1456", "1457", "1458"})
        and all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "MEDIUM" for x in leg_ids),
        "Joint stress screening reflects traps, waist, upper body, and lower body loadings accurately",
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
            "perSide": False,
            "tempo": 3,
            "reason": "",
            "restAfter": 0,
        }
        workout = {"version": 1, "title": "暂缓项门控验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="平板训练凳|固定器械|杠铃|曲杆杠铃|雪橇倒蹬机", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND SEVENTEEN INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
