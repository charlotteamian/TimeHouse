#!/usr/bin/env python3
"""Newly reviewed Batch 28 entries must enter real training cleanly with correct per-side counts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
new = ["1167", "0418"]
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
    check(len(known) == 116 and all("dataset_1324_" + x in known for x in new), "Both new entries enter the final bundled 116-item ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in new),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        all(catalog["dataset_1324_" + x]["safeWithRequiredEquipment"] for x in new)
        and all(not catalog["dataset_1324_" + x]["safeSevereShoulder"] for x in new),
        "Both loaded candidates pass with full equipment and filter safely on severe shoulder pain",
    )

    for xid in new:
        per_side = xid == "0418"
        item = {"id": "dataset_1324_" + xid, "sets": 1, "reps": "8", "rpe": "7", "rest": 30, "kind": "REPS", "hold": 0, "perSide": per_side, "tempo": 3, "reason": "", "restAfter": 0}
        workout = {"version": 1, "title": "新复核动作开练验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(equipment="自重|哑铃", workoutDraft=json.dumps(workout, ensure_ascii=False))
        tap("查看课程 →")
        tap("开始这一练 →")
        check(draft()["active"] and draft()["items"][0]["id"] == "dataset_1324_" + xid, names[xid] + " enters normal training cleanly")
        snapshot(xid + "-session")
        if xid == "0418":
            tap("准备好了，开始这一组")
            deadline = time.monotonic() + 6
            while draft()["phase"] == "COUNT_IN" and time.monotonic() < deadline:
                time.sleep(0.25)
            check(
                draft()["phase"] == "WORK"
                and draft()["items"][0]["kind"] == "REPS"
                and draft()["items"][0]["perSide"],
                names[xid] + " enters unilateral standing concentration curl set after count-in",
            )

    print("ALL BATCH TWENTY-EIGHT FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
