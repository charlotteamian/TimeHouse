#!/usr/bin/env python3
"""Batch eighty candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["0207", "0208", "0209", "0210", "0211", "0212", "0213", "0214", "0215", "0216"]
per_side_ids = {"0214", "0216"}
flat_bench_ids = {"0208", "0210", "0213", "0214", "0215", "0216"}
preacher_bench_ids = {"0209"}
stability_ball_ids = {"0211"}
no_support_ids = {"0207", "0212"}
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
        row("0207")["primary"] == ["肱三头肌"]
        and all(row(x)["primary"] == ["上背"] for x in ["0208", "0214"])
        and row("0209")["primary"] == ["肱二头肌"]
        and row("0210")["primary"] == ["前臂"]
        and all(row(x)["primary"] == ["腹肌"] for x in ["0211", "0212"])
        and row("0213")["primary"] == ["背阔肌"]
        and all(row(x)["primary"] == ["三角肌"] for x in ["0215", "0216"]),
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        all(row(x)["requiredEquipment"] == ["平板训练凳"] and row(x)["safeWithRequiredEquipment"] for x in flat_bench_ids)
        and all(row(x)["requiredEquipment"] == ["牧师凳"] and row(x)["safeWithRequiredEquipment"] for x in preacher_bench_ids)
        and all(row(x)["requiredEquipment"] == ["瑜伽球"] and row(x)["safeWithRequiredEquipment"] for x in stability_ball_ids)
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in no_support_ids),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 80 avoids hold triggers and configures unilateral rows and rotations cleanly",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in ["0207", "0209", "0215", "0216"])
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in ["0208", "0213", "0214"])
        and all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in ["0211", "0212"])
        and row("0210")["shoulder"] == "NONE" and row("0210")["lower_back"] == "NONE" and row("0210")["knee"] == "NONE",
        "Joint stress screening reflects shoulder and back loading for cable rows, shoulder loading for arm curls and raises, back loading for waist twists and crunches, and zero stress for wrist curls",
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
        state_with(reviewedOnlyV1=False, equipment="固定器械|平板训练凳|牧师凳|瑜伽球", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH EIGHTY INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
