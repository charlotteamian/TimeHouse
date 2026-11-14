#!/usr/bin/env python3
"""Batch one hundred and twenty-two deferred items: verify anatomy corrections, supports, hold/perSide pacing, and review gate."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["1712", "1713", "1714", "1716", "1717", "1718", "1719", "1720", "1721", "1722"]
quad_ids = {"1713", "1714"}
tricep_ids = {"1718", "1719", "1720", "1721", "1722"}
per_side_ids = {"1712", "1713", "1714"}
bilateral_ids = set(inspected) - per_side_ids
flat_bench_ids = {"1718", "1720", "1721"}
no_support_ids = {"1713", "1714", "1717", "1722"}
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
        row("1712")["primary"] == ["大腿内收肌群"]
        and all(row(x)["primary"] == ["股四头肌"] for x in quad_ids)
        and row("1716")["primary"] == ["胸肌"]
        and row("1717")["primary"] == ["背阔肌"]
        and all(row(x)["primary"] == ["肱三头肌"] for x in tricep_ids),
        "Primary muscle groups match adductors, quads (including fixed 1714), pectorals, lats, and triceps",
    )
    check(
        row("1712")["requiredEquipment"] == ["稳固踏台"]
        and row("1716")["requiredEquipment"] == ["瑜伽球"]
        and all(row(x)["requiredEquipment"] == ["平板训练凳"] for x in flat_bench_ids)
        and row("1719")["requiredEquipment"] == ["上斜训练凳"]
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in no_support_ids),
        "All ten inspected entries enforce step box, stability ball, flat bench, and incline bench supports",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and all(not row(x)["perSide"] for x in bilateral_ids),
        "Batch 122 avoids hold triggers while activating unilateral perSide pacing on 1712, 1713, and 1714",
    )
    check(
        all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "MEDIUM" for x in {"1712", "1713", "1714"})
        and row("1716")["shoulder"] == "MEDIUM" and row("1716")["lower_back"] == "NONE" and row("1716")["knee"] == "NONE"
        and row("1717")["shoulder"] == "MEDIUM" and row("1717")["lower_back"] == "MEDIUM" and row("1717")["knee"] == "NONE"
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in tricep_ids),
        "Joint stress screening reflects lower-body, chest, back, and triceps loadings accurately",
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
        state_with(reviewedOnlyV1=False, equipment="稳固踏台|瑜伽球|平板训练凳|上斜训练凳", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked prior to approval by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND TWENTY-TWO INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
