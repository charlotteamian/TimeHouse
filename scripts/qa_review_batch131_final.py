#!/usr/bin/env python3
"""Newly reviewed Batch 131 exercise (3144) enters reviewed ledger and training cleanly while 9 deferred stay blocked."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
new = ["3144"]
inspected = ["3144", "3194", "3195", "3200", "3235", "3236", "3237", "3281", "3286", "3290"]
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
    check(len(known) == 141 and all("dataset_1324_" + x in known for x in new), "New entry 3144 enters the final bundled 141-item ledger")
    check(not any("dataset_1324_" + x in known for x in deferred), "Nine deferred Batch 131 items stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in inspected),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    row_3144 = catalog["dataset_1324_3144"]
    check(
        bool(row_3144["equipment"])
        and row_3144["requiredEquipment"] == []
        and row_3144["safeWithRequiredEquipment"]
        and not row_3144["perSide"]
        and not row_3144["isHold"]
        and bool(row_3144["primary"]),
        "Loaded 3144 resistance band row clears safety checks and uses dynamic bilateral pulling mode",
    )

    item = {"id": "dataset_1324_3144", "sets": 1, "reps": "12", "rpe": "7", "rest": 30, "kind": "REPS", "hold": 0, "perSide": False, "tempo": 3, "reason": "", "restAfter": 0}
    w = {"version": 1, "title": "新复核阻力带划船验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
    state_with(equipment="|".join(row_3144["equipment"]), workoutDraft=json.dumps(w, ensure_ascii=False))
    tap("查看课程 →")
    tap("开始这一练 →")
    check(draft()["active"] and draft()["items"][0]["id"] == "dataset_1324_3144" and not draft()["items"][0]["perSide"], names["3144"] + " enters training cleanly")
    snapshot("3144-session")

    print("ALL BATCH ONE HUNDRED AND THIRTY-ONE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
