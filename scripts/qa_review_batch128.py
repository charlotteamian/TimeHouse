#!/usr/bin/env python3
"""Batch one hundred and twenty-eight deferred items: verify anatomy, equipment, hold/perSide, and review gate."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["2371", "2399", "2404", "2405", "2406", "2407", "2414", "2432", "2459", "2464"]
per_side_ids = {"2399", "2414", "2464"}
bilateral_ids = set(inspected) - per_side_ids
biceps_ids = {"2404", "2407", "2414"}
triceps_ids = {"2405", "2406", "2432"}
cable_ids = {"2399", "2405", "2406", "2464"}
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
        all(row(x)["primary"] == ["腹肌"] for x in {"2371", "2399"})
        and all(row(x)["primary"] == ["肱二头肌"] for x in biceps_ids)
        and all(row(x)["primary"] == ["肱三头肌"] for x in triceps_ids)
        and row("2459")["primary"] == ["臀肌"]
        and row("2464")["primary"] == ["背阔肌"],
        "Primary muscle groups match abs, biceps, triceps, glutes, and lats",
    )
    check(
        row("2371")["equipment"] == ["负重"]
        and all(row(x)["equipment"] == ["固定器械"] for x in cable_ids)
        and all(row(x)["equipment"] == ["杠铃"] for x in {"2407", "2414"})
        and all(row(x)["equipment"] == ["EZ 杠"] for x in {"2404", "2432"})
        and row("2459")["equipment"] == ["轮胎"]
        and row("2432")["requiredEquipment"] == ["平板训练凳"]
        and not row("2432")["available"]["平板训练凳"]
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in set(inspected) - {"2432"}),
        "Batch 128 maps weighted/cable/barbell/EZ-bar/tire equipment and 2432 flat-bench support requirement consistently",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and all(not row(x)["perSide"] for x in bilateral_ids),
        "Batch 128 stays dynamic while enabling unilateral perSide pacing on 2399, 2414, and 2464",
    )
    check(
        all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in {"2371", "2399"})
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in biceps_ids | triceps_ids)
        and row("2459")["shoulder"] == "NONE" and row("2459")["lower_back"] == "NONE" and row("2459")["knee"] == "MEDIUM"
        and row("2464")["shoulder"] == "MEDIUM" and row("2464")["lower_back"] == "MEDIUM" and row("2464")["knee"] == "NONE",
        "Joint stress screening reflects waist, biceps, triceps, glutes, and back loadings accurately",
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
        state_with(reviewedOnlyV1=False, equipment="平板训练凳|负重|固定器械|杠铃", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked prior to approval by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND TWENTY-EIGHT INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
