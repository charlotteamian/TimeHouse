#!/usr/bin/env python3
"""Batch forty-three candidates: verify all ten stay unreviewed while metadata/supports update cleanly."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["1773", "1651", "1774", "1652", "1775", "1653", "2271", "1654", "2298", "1655"]
per_side_ids = {"1773", "1774", "1652", "1775", "1653", "2271"}
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
        all(row(x)["primary"] == ["上背"] for x in ["1773", "2298"])
        and all(row(x)["primary"] == ["肱二头肌"] for x in ["1651", "1652", "1653", "1654", "1655"])
        and row("1774")["primary"] == ["髋外展肌群", "臀肌"]
        and row("1775")["primary"] == ["大腿内收肌群"]
        and row("2271")["primary"] == ["三角肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        row("1773")["requiredEquipment"] == ["毛巾", "稳固立柱"] and row("1773")["safeWithRequiredEquipment"] and not row("1773")["available"]["自重"]
        and row("1652")["requiredEquipment"] == ["瑜伽球"] and row("1652")["safeWithRequiredEquipment"] and not row("1652")["available"]["哑铃"]
        and row("2298")["requiredEquipment"] == ["平板训练凳"] and row("2298")["available"]["平板训练凳"] and not row("2298")["available"]["自重"]
        and all(row(x)["requiredEquipment"] == [] for x in ["1651", "1774", "1775", "1653", "2271", "1654", "1655"]),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and not any(row(x)["perSide"] for x in ["1651", "1654", "2298", "1655"]),
        "Batch 43 avoids hold triggers while configuring unilateral/bilateral rep modes accurately",
    )
    check(
        all(row(x)["lower_back"] == "NONE" for x in ["1651", "1652", "1653", "1654", "1655"])
        and all(row(x)["lower_back"] == "MEDIUM" for x in ["1773", "2298"])
        and row("2271")["shoulder"] == "MEDIUM"
        and row("1774")["knee"] == "MEDIUM" and row("1775")["knee"] == "MEDIUM"
        and row("1773")["knee"] == "NONE",
        "Joint stress screening reflects row lower-back loads, punch shoulder load, and hip-lift knee loads",
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
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|平板训练凳|瑜伽球", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked by mandatory 1.2.14 review gate")

    print("ALL BATCH FORTY-THREE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
