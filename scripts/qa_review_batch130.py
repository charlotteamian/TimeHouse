#!/usr/bin/env python3
"""Batch one hundred and thirty deferred items: verify anatomy, equipment, hold/perSide, and review gate."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["3006", "3007", "3010", "3017", "3116", "3117", "3122", "3123", "3124", "3142"]
per_side_ids = {"3007"}
bilateral_ids = set(inspected) - per_side_ids
res_band_ids = {"3006", "3007", "3122", "3123", "3124"}
flat_bench_ids = {"3010", "3117", "3122", "3123"}
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
        bool(row("3006")["primary"])
        and row("3007")["primary"] == ["股四头肌"]
        and all(row(x)["primary"] == ["背阔肌"] for x in {"3010", "3116", "3117"})
        and bool(row("3017")["primary"])
        and row("3122")["primary"] == ["三角肌"]
        and row("3123")["primary"] == ["肱二头肌"]
        and row("3124")["primary"] == ["胸肌"]
        and row("3142")["primary"] == ["臀肌"],
        "Primary muscle groups match quads, lats, delts, biceps, pectorals, glutes, abductors, and upper back",
    )
    check(
        len({tuple(row(x)["equipment"]) for x in res_band_ids}) == 1 and bool(row("3006")["equipment"])
        and all(row(x)["equipment"] == ["弹力带"] for x in {"3116", "3117"})
        and row("3010")["equipment"] == ["EZ 杠"]
        and row("3017")["equipment"] == ["杠铃"]
        and row("3142")["equipment"] == ["史密斯机"]
        and row("3007")["requiredEquipment"] == ["稳固立柱"]
        and all(row(x)["requiredEquipment"] == ["平板训练凳"] for x in flat_bench_ids)
        and row("3124")["requiredEquipment"] == ["直立靠背训练凳"]
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in {"3006", "3017", "3116", "3142"}),
        "Batch 130 maps equipment and upright/flat bench and post supporting gear accurately",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and row("3007")["perSide"]
        and all(not row(x)["perSide"] for x in bilateral_ids),
        "Batch 130 avoids hold triggers while activating unilateral perSide pacing on 3007",
    )
    check(
        all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "MEDIUM" for x in {"3006", "3007", "3142"})
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in {"3010", "3017", "3116", "3117"})
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "NONE" for x in {"3122", "3123", "3124"}),
        "Joint stress screening reflects leg, back, shoulder, biceps, and chest loadings accurately",
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
        state_with(reviewedOnlyV1=False, equipment="稳固立柱|平板训练凳|直立靠背训练凳|弹力带|杠铃|EZ 杠|史密斯机", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked prior to approval by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND THIRTY INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
