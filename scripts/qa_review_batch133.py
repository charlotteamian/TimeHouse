#!/usr/bin/env python3
"""Batch one hundred and thirty-three deferred items: verify anatomy, equipment, hold/perSide, and review gate."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["3670", "3697", "3758", "3759", "3760"]
machine_ids = {"3697", "3758", "3759", "3760"}
waist_ids = {"3670", "3760"}
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

    check(not any("dataset_1324_" + x in known for x in inspected), "All five inspected entries remain unreviewed during initial checks")
    check("supportReviewInvalidation=1" in raw, "Supporting equipment changes invalidate stale personal approval")
    check(
        all(row(x)["primary"] == ["腹肌"] for x in waist_ids)
        and row("3697")["primary"] == ["三角肌"]
        and row("3758")["primary"] == ["胸肌"]
        and row("3759")["primary"] == ["臀肌"],
        "Primary muscle groups match abs, delts, pectorals, and glutes",
    )
    check(
        row("3670")["equipment"] == ["负重"]
        and all(row(x)["equipment"] == ["固定器械"] for x in machine_ids)
        and row("3670")["requiredEquipment"] == ["带勾脚的下斜训练凳"]
        and not row("3670")["available"]["带勾脚的下斜训练凳"]
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in machine_ids),
        "Batch 133 maps weighted/cable/leverage equipment and 3670 decline-hook bench requirement accurately",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and not any(row(x)["perSide"] for x in inspected),
        "Batch 133 stays dynamic and bilateral",
    )
    check(
        all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in waist_ids)
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in {"3697", "3758"})
        and row("3759")["shoulder"] == "NONE" and row("3759")["lower_back"] == "NONE" and row("3759")["knee"] == "MEDIUM",
        "Joint stress screening reflects waist, delts, pectorals, and glutes loadings accurately",
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
            "perSide": False,
            "tempo": 3,
            "reason": "",
            "restAfter": 0,
        }
        workout = {"version": 1, "title": "暂缓门控验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="带勾脚的下斜训练凳|负重|固定器械", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked prior to approval by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND THIRTY-THREE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
