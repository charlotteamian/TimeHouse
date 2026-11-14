#!/usr/bin/env python3
"""Batch one hundred and twenty-six deferred items: verify anatomy, equipment, hold/perSide, and review gate."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

inspected = ["2205", "2206", "2207", "2208", "2209", "2285", "2286", "2287", "2288", "2289"]
glute_ids = {"2205", "2286"}
lat_ids = {"2207", "2285"}
roller_ids = {"2205", "2206", "2207", "2208", "2209"}
machine_ids = {"2285", "2286", "2287", "2288", "2289"}
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
        all(row(x)["primary"] == ["臀肌"] for x in glute_ids)
        and row("2206")["primary"] == ["腹肌"]
        and all(row(x)["primary"] == ["背阔肌"] for x in lat_ids)
        and row("2208")["primary"] == ["脊柱"]
        and row("2209")["primary"] == ["胸肌"]
        and row("2287")["primary"] == ["股四头肌"]
        and row("2288")["primary"] == ["前臂"]
        and row("2289")["primary"] == ["小腿肌"],
        "Primary muscle groups match glutes, abs, lats, spine, chest, quads, forearms, and calves",
    )
    check(
        all(row(x)["equipment"] == ["健腹轮 / 滚轮"] for x in roller_ids)
        and all(row(x)["equipment"] == ["固定器械"] for x in machine_ids)
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in inspected),
        "Batch 126 maps roller and leverage machine equipment consistently",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and not any(row(x)["perSide"] for x in inspected),
        "All ten Batch 126 entries remain dynamic and bilateral",
    )
    check(
        all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "MEDIUM" for x in {"2205", "2286", "2287", "2289"})
        and row("2206")["shoulder"] == "NONE" and row("2206")["lower_back"] == "MEDIUM" and row("2206")["knee"] == "NONE"
        and all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in {"2207", "2208", "2285"})
        and row("2209")["shoulder"] == "MEDIUM" and row("2209")["lower_back"] == "NONE" and row("2209")["knee"] == "NONE"
        and row("2288")["shoulder"] == "NONE" and row("2288")["lower_back"] == "NONE" and row("2288")["knee"] == "NONE",
        "Joint stress screening reflects lower-body, abs, back, chest, and forearm loadings accurately",
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
        state_with(reviewedOnlyV1=False, equipment="健腹轮 / 滚轮|固定器械", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked prior to approval by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND TWENTY-SIX INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
