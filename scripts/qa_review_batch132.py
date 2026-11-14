#!/usr/bin/env python3
"""Batch one hundred and thirty-two deferred items: verify anatomy, equipment, hold/perSide, and review gate."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["3305", "3312", "3313", "3562", "3563", "3641", "3642", "3643", "3644", "3666"]
per_side_ids = {"3563"}
bilateral_ids = set(inspected) - per_side_ids
weighted_ids = {"3312", "3313", "3641", "3642", "3643", "3644"}
glute_ids = {"3562", "3642", "3643", "3644"}
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
        all(row(x)["primary"] == ["三角肌"] for x in {"3305", "3641"})
        and all(row(x)["primary"] == ["背阔肌"] for x in {"3312", "3563"})
        and row("3313")["primary"] == ["胸肌"]
        and all(row(x)["primary"] == ["臀肌"] for x in glute_ids)
        and row("3666")["primary"] == ["心肺系统"],
        "Primary muscle groups match delts, lats, pectorals, glutes, and cardio",
    )
    check(
        all(row(x)["equipment"] == ["杠铃"] for x in {"3305", "3562"})
        and all(row(x)["equipment"] == ["负重"] for x in weighted_ids)
        and all(row(x)["equipment"] == ["固定器械"] for x in {"3563", "3666"})
        and row("3312")["requiredEquipment"] == ["单杠"]
        and row("3313")["requiredEquipment"] == ["双杠"]
        and row("3562")["requiredEquipment"] == ["平板训练凳"] and not row("3562")["available"]["平板训练凳"]
        and row("3666")["requiredEquipment"] == ["跑步机"]
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in {"3305", "3563", "3641", "3642", "3643", "3644"}),
        "Batch 132 maps barbell/weighted/machine equipment and pull-up bar, parallel bars, flat bench, and treadmill supports accurately",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and row("3563")["perSide"]
        and all(not row(x)["perSide"] for x in bilateral_ids),
        "Batch 132 stays dynamic while enabling unilateral perSide pacing on 3563",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in {"3305", "3313", "3641"})
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in {"3312", "3563"})
        and all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "MEDIUM" for x in glute_ids | {"3666"}),
        "Joint stress screening reflects shoulder/chest, back, lower-body, and cardio loadings accurately",
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
        state_with(reviewedOnlyV1=False, equipment="单杠|双杠|平板训练凳|跑步机|杠铃|负重|固定器械", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked prior to approval by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND THIRTY-TWO INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
