#!/usr/bin/env python3
"""Newly reviewed Batch 125 exercise (2138) enters reviewed ledger and training cleanly while 9 deferred stay blocked."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
new = ["2138"]
inspected = ["2138", "2139", "2141", "2142", "2144", "2186", "2187", "2202", "2203", "2204"]
deferred = [x for x in inspected if x not in new]
names = {
    e["id"]: e["name_zh"]
    for e in json.loads(Path("app/src/main/assets/exercises_1324.json").read_text())["exercises"]
}
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)


def tap(label):
    for attempt in range(6):
        for n in ui().iter("node"):
            if n.get("text") == label or n.get("content-desc") == label:
                x1, y1, x2, y2 = map(int, re.findall(r"-?\d+", n.get("bounds")))
                screen = re.findall(r"(\d+)x(\d+)", adb("shell", "wm", "size").decode())[-1]
                if 40 <= y1 < y2 <= int(screen[1]) - 20 and x2 > x1:
                    adb("shell", "input", "tap", str((x1 + x2) // 2), str((y1 + y2) // 2))
                    time.sleep(0.35)
                    return
        size = re.findall(r"(\d+)x(\d+)", adb("shell", "wm", "size").decode())[-1]
        width, height = map(int, size)
        adb("shell", "input", "swipe", str(width // 2), str(int(height * 0.72)),
            str(width // 2), str(int(height * 0.32)), "750")
        time.sleep(0.35)
    raise AssertionError("Missing UI control: " + label)


try:
    check(len(known) == 140 and all("dataset_1324_" + x in known for x in new), "New entry 2138 enters the final bundled 140-item ledger")
    check(not any("dataset_1324_" + x in known for x in deferred), "Nine deferred Batch 125 items stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in inspected),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_2138"]["equipment"] == ["动感单车"]
        and catalog["dataset_1324_2138"]["requiredEquipment"] == []
        and catalog["dataset_1324_2138"]["safeWithRequiredEquipment"]
        and not catalog["dataset_1324_2138"]["available"]["自重"]
        and not catalog["dataset_1324_2138"]["perSide"]
        and not catalog["dataset_1324_2138"]["isHold"]
        and catalog["dataset_1324_2138"]["primary"] == ["心肺系统"],
        "Loaded 2138 stationary bike binds 动感单车 equipment and uses bilateral cardio mode",
    )

    item = {"id": "dataset_1324_2138", "sets": 1, "reps": "12", "rpe": "7", "rest": 30, "kind": "REPS", "hold": 0, "perSide": False, "tempo": 3, "reason": "", "restAfter": 0}
    w = {"version": 1, "title": "新复核动感单车骑行验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
    state_with(equipment="动感单车", workoutDraft=json.dumps(w, ensure_ascii=False))
    tap("查看课程 →")
    tap("开始这一练 →")
    check(draft()["active"] and draft()["items"][0]["id"] == "dataset_1324_2138" and not draft()["items"][0]["perSide"], names["2138"] + " enters training cleanly with 动感单车")
    snapshot("2138-session")

    print("ALL BATCH ONE HUNDRED AND TWENTY-FIVE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
