#!/usr/bin/env python3
"""Batch twenty-six candidates: catalog semantics, required supports, real loops and review gate."""
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageChops, ImageOps

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

new = ["0403", "0408"]
inspected = ["0795", "0403", "0803", "0404", "0812", "0405", "0813", "0407", "0814", "0408"]
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
        row("0795")["primary"] == ["腘绳肌"]
        and row("0403")["primary"] == ["肱二头肌"]
        and row("0803")["primary"] == ["胸肌"]
        and all(row(x)["primary"] == ["三角肌"] for x in ["0404", "0405", "0408"])
        and all(row(x)["primary"] == ["肱三头肌"] for x in ["0812", "0813", "0814"])
        and row("0407")["primary"] == ["腹肌"],
        "Primary muscle groups match corrected anatomical targets for all ten inspected entries",
    )
    check(
        row("0403")["requiredEquipment"] == ["平板训练凳"]
        and row("0403")["available"]["哑铃|平板训练凳"]
        and not row("0403")["available"]["哑铃"]
        and all(row(x)["requiredEquipment"] == ["直立靠背训练凳"] and row(x)["available"]["哑铃|直立靠背训练凳"] and not row(x)["available"]["哑铃"] for x in ["0404", "0405"])
        and all(row(x)["requiredEquipment"] == ["平板训练凳"] and row(x)["available"]["平板训练凳"] and not row(x)["available"]["自重"] for x in ["0812", "0813", "0814"])
        and all(row(x)["requiredEquipment"] == [] for x in ["0795", "0803", "0407", "0408"]),
        "All ten inspected entries enforce exact required supporting equipment",
    )
    check(
        all(row(x)["perSide"] for x in ["0795", "0403", "0407", "0408"])
        and not any(row(x)["perSide"] for x in ["0803", "0404", "0812", "0405", "0813", "0814"])
        and not any(row(x)["isHold"] for x in inspected),
        "Single-arm/single-leg entries count per side while bilateral presses, dips and push-ups count bilaterally",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" for x in ["0403", "0803", "0404", "0812", "0405", "0813", "0814", "0408"])
        and row("0803")["lower_back"] == "MEDIUM"
        and all(row(x)["lower_back"] == "LOW" for x in ["0795", "0407"]),
        "Joint stress screening reflects high-plank, dip, overhead press, side bend, and leg curl loads",
    )

    for xid in new:
        state_with(favorites="dataset_1324_" + xid)
        tap("动作库")
        tap("已标心")
        tap(names[xid])
        check("暂停示范" in texts() and any("未复核" in s for s in texts()), names[xid] + " plays while retaining its unreviewed label")
        snapshot(xid + "-detail")
        node = next(n for n in ui().iter("node") if n.get("class") == "android.widget.ImageView")
        bounds = tuple(map(int, re.findall(r"-?\d+", node.get("bounds"))))
        frames = []
        for i in range(12):
            im = Image.open(BytesIO(adb("exec-out", "screencap", "-p"))).convert("RGB").crop(bounds)
            im.save(out / f"{xid}-play-{i}.png")
            frames.append(im)
            time.sleep(0.28)
        check(any(ImageChops.difference(frames[0], im).getbbox() for im in frames[1:]), names[xid] + " changes poses during captured Android loops")
        frames[0].save(out / f"{xid}-android-loop.gif", save_all=True, append_images=frames[1:], duration=400, loop=0)
        sheet = Image.new("RGB", (1200, 900), "white")
        for i, f in enumerate(frames):
            sheet.paste(ImageOps.pad(f, (300, 300), color="white"), ((i % 4) * 300, (i // 4) * 300))
        sheet.save(out / f"{xid}-playback-contact.jpg")
        item = {"id": "dataset_1324_" + xid, "sets": 1, "reps": "8", "rpe": "7", "rest": 30, "kind": "REPS", "hold": 0, "perSide": True, "tempo": 3, "reason": "", "restAfter": 0}
        workout = {"version": 1, "title": "候选门控核查", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment="自重|哑铃|平板训练凳", workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " cannot bypass 1.2.14 mandatory review gate")

    decoded = adb("shell", "am", "instrument", "-w", "-e", "media", ",".join("dataset_motion_" + x for x in new), "com.restartday.fitness.qa/.UiSnapshot").decode()
    check("decodedAnimations=2" in decoded, "Android decodes both candidate demonstrations as animations")
    print("ALL BATCH TWENTY-SIX INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
