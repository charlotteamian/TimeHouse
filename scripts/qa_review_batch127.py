#!/usr/bin/env python3
"""Batch one hundred and twenty-seven deferred items: verify anatomy, equipment, hold/perSide, and review gate."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["2297", "2311", "2315", "2318", "2328", "2330", "2331", "2334", "2335", "2364"]
cardio_ids = {"2311", "2331"}
calf_ids = {"2315", "2334", "2335"}
ball_ids = {"2297", "2328"}
lever_ids = {"2315", "2318", "2331", "2335", "2364"}
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
        row("2297")["primary"] == ["腹肌"]
        and all(row(x)["primary"] == ["心肺系统"] for x in cardio_ids)
        and all(row(x)["primary"] == ["小腿肌"] for x in calf_ids)
        and row("2318")["primary"] == ["三角肌"]
        and row("2328")["primary"] == ["肱三头肌"]
        and row("2330")["primary"] == ["背阔肌"]
        and row("2364")["primary"] == ["胸肌"],
        "Primary muscle groups match abs, cardio, calves, delts, triceps, lats, and pectorals",
    )
    check(
        all(row(x)["equipment"] == ["瑜伽球"] for x in ball_ids)
        and row("2311")["equipment"] == ["登阶机"]
        and row("2334")["equipment"] == ["雪橇机"]
        and all(row(x)["equipment"] == ["固定器械"] for x in lever_ids | {"2330"})
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in inspected),
        "Batch 127 maps stability ball, stepmill, sled, cable, and leverage machines cleanly",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and not any(row(x)["perSide"] for x in inspected),
        "All ten Batch 127 entries remain dynamic and bilateral",
    )
    check(
        row("2297")["shoulder"] == "NONE" and row("2297")["lower_back"] == "MEDIUM" and row("2297")["knee"] == "NONE"
        and all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "MEDIUM" for x in cardio_ids | calf_ids)
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in {"2318", "2328", "2364"})
        and row("2330")["shoulder"] == "MEDIUM" and row("2330")["lower_back"] == "MEDIUM" and row("2330")["knee"] == "NONE",
        "Joint stress screening reflects waist, cardio, calves, shoulders, triceps, chest, and back loadings accurately",
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
        state_with(reviewedOnlyV1=False, equipment="瑜伽球|登阶机|雪橇机|固定器械", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked prior to approval by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND TWENTY-SEVEN INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
