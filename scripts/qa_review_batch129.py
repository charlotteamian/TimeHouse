#!/usr/bin/env python3
"""Batch one hundred and twenty-nine deferred items: verify anatomy, equipment, hold/perSide, and review gate."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["2611", "2612", "2616", "2736", "2741", "2798", "2799", "2800", "2810", "2987"]
per_side_ids = {"2611", "2810"}
bilateral_ids = set(inspected) - per_side_ids
barbell_ids = {"2798", "2799", "2800", "2810"}
flat_bench_ids = {"2799", "2800"}
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
        row("2611")["primary"] == ["臀肌"]
        and row("2612")["primary"] == ["心肺系统"]
        and all(row(x)["primary"] == ["背阔肌"] for x in {"2616", "2736", "2987"})
        and row("2741")["primary"] == ["肱二头肌"]
        and all(row(x)["primary"] == ["股四头肌"] for x in {"2798", "2810"})
        and all(row(x)["primary"] == ["腹肌"] for x in flat_bench_ids),
        "Primary muscle groups match glutes, cardio, lats, biceps, quads, and abs",
    )
    check(
        all(row(x)["equipment"] == ["固定器械"] for x in {"2611", "2616", "2736"})
        and bool(row("2612")["equipment"])
        and row("2741")["equipment"] == ["EZ 杠"]
        and all(row(x)["equipment"] == ["杠铃"] for x in barbell_ids)
        and row("2987")["equipment"] == ["负重"]
        and all(row(x)["requiredEquipment"] == ["平板训练凳"] and not row(x)["available"]["平板训练凳"] for x in flat_bench_ids)
        and row("2987")["requiredEquipment"] == ["单杠"]
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in set(inspected) - flat_bench_ids - {"2987"}),
        "Batch 129 maps equipment and flat-bench / pull-up-bar support requirements consistently",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and all(not row(x)["perSide"] for x in bilateral_ids),
        "Batch 129 avoids hold triggers while enabling unilateral perSide pacing on 2611 and 2810",
    )
    check(
        all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "MEDIUM" for x in {"2611", "2612", "2798", "2810"})
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in {"2616", "2736", "2987"})
        and row("2741")["shoulder"] == "MEDIUM" and row("2741")["lower_back"] == "NONE" and row("2741")["knee"] == "NONE"
        and all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in flat_bench_ids),
        "Joint stress screening reflects lower-body, cardio, back, biceps, and abs loadings accurately",
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
        state_with(reviewedOnlyV1=False, equipment="平板训练凳|单杠|杠铃|EZ 杠|负重|固定器械", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked prior to approval by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND TWENTY-NINE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
