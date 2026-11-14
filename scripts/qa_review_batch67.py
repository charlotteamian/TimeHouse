#!/usr/bin/env python3
"""Batch sixty-seven candidates: verify all ten stay unreviewed while anatomy, supports, and hold/perSide update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["0050", "0051", "0052", "0053", "0054", "0055", "0056", "0057", "0058", "0059"]
per_side_ids = {"0054"}
flat_bench_ids = {"0052", "0055", "0056", "0057", "0058"}
incline_bench_ids = {"0050"}
preacher_ids = {"0059"}
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
        row("0050")["primary"] == ["前锯肌"]
        and all(row(x)["primary"] == ["臀肌", "股四头肌"] for x in ["0051", "0053", "0054"])
        and all(row(x)["primary"] == ["肱三头肌"] for x in ["0052", "0055", "0056", "0057"])
        and row("0058")["primary"] == ["臀肌", "腘绳肌"]
        and row("0059")["primary"] == ["肱二头肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        all(row(x)["requiredEquipment"] == ["平板训练凳"] and row(x)["safeWithRequiredEquipment"] for x in flat_bench_ids)
        and all(row(x)["requiredEquipment"] == ["上斜训练凳"] and row(x)["safeWithRequiredEquipment"] for x in incline_bench_ids)
        and all(row(x)["requiredEquipment"] == ["牧师凳"] and row(x)["safeWithRequiredEquipment"] for x in preacher_ids)
        and all(row(x)["requiredEquipment"] == [] for x in inspected if x not in flat_bench_ids and x not in incline_bench_ids and x not in preacher_ids),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in inspected if x not in per_side_ids),
        "Batch 67 avoids hold triggers and configures unilateral alternating lunges cleanly",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" for x in ["0050", "0052", "0055", "0056", "0057", "0059"])
        and all(row(x)["knee"] == "MEDIUM" and row(x)["lower_back"] == "NONE" for x in ["0051", "0053", "0054", "0058"]),
        "Joint stress screening reflects shoulder loading for presses/extensions and lower-body knee stress for squats/lunges/bridges",
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
        state_with(reviewedOnlyV1=False, equipment="杠铃|平板训练凳|上斜训练凳|牧师凳", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH SIXTY-SEVEN INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
