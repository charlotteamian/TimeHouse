#!/usr/bin/env python3
"""Batch one hundred and thirty-one candidate (3144) & deferred items: semantics, playback, supports, and review gate."""
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageChops, ImageOps

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])

new = ["3144"]
inspected = ["3144", "3194", "3195", "3200", "3235", "3236", "3237", "3281", "3286", "3290"]
per_side_ids = {"3237", "3290"}
bilateral_ids = set(inspected) - per_side_ids
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
        row("3144")["primary"] == row("3200")["primary"] and bool(row("3144")["primary"])
        and all(row(x)["primary"] == ["臀肌"] for x in {"3194", "3236", "3281"})
        and all(row(x)["primary"] == ["腘绳肌"] for x in {"3195", "3235"})
        and row("3237")["primary"] == ["三角肌"]
        and all(row(x)["primary"] == ["背阔肌"] for x in {"3286", "3290"}),
        "Primary muscle groups match upper back, glutes, hamstrings, delts, and lats",
    )
    check(
        row("3144")["equipment"] == row("3236")["equipment"] and bool(row("3144")["equipment"])
        and all(row(x)["equipment"] == ["杠铃"] for x in {"3194", "3237"})
        and all(row(x)["equipment"] == ["固定器械"] for x in {"3195", "3200", "3235"})
        and row("3281")["equipment"] == ["史密斯机"]
        and all(row(x)["equipment"] == ["负重"] for x in {"3286", "3290"})
        and row("3235")["requiredEquipment"] == ["平板训练凳"]
        and all(row(x)["requiredEquipment"] == ["单杠"] for x in {"3286", "3290"})
        and all(row(x)["requiredEquipment"] == [] and row(x)["safeWithRequiredEquipment"] for x in set(inspected) - {"3235", "3286", "3290"}),
        "Batch 131 maps resistance band, barbell, cable/leverage, Smith, and flat bench / pull-up bar supports accurately",
    )
    check(
        not any(row(x)["isHold"] for x in inspected)
        and all(row(x)["perSide"] for x in per_side_ids)
        and all(not row(x)["perSide"] for x in bilateral_ids),
        "Batch 131 avoids hold triggers while enabling unilateral perSide pacing on 3237 and 3290",
    )
    check(
        all(row(x)["shoulder"] == "MEDIUM" and row(x)["lower_back"] == "MEDIUM" and row(x)["knee"] == "NONE" for x in {"3144", "3200", "3286", "3290"})
        and all(row(x)["shoulder"] == "NONE" and row(x)["lower_back"] == "NONE" and row(x)["knee"] == "MEDIUM" for x in {"3194", "3195", "3235", "3236", "3281"})
        and row("3237")["shoulder"] == "MEDIUM" and row("3237")["lower_back"] == "NONE" and row("3237")["knee"] == "NONE",
        "Joint stress screening reflects back, lower-body, and shoulder loadings accurately",
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
        for i, im in enumerate(frames):
            sheet.paste(ImageOps.pad(im, (300, 300), color="white"), ((i % 4) * 300, (i // 4) * 300))
        sheet.save(out / f"{xid}-playback-contact.jpg", quality=92)

    eq_str = "|".join(set(row("3144")["equipment"]) | {"杠杆器械", "杠铃", "固定器械", "史密斯机", "负重", "平板训练凳", "单杠"})
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
        workout = {"version": 1, "title": "候选前门控验证", "intensity": "MEDIUM", "reason": "QA", "safety": "QA", "limited": False, "notes": [], "budget": 0, "active": False, "items": [item]}
        state_with(reviewedOnlyV1=False, equipment=eq_str, workoutDraft=json.dumps(workout, ensure_ascii=False))
        check(not draft() and prefs().get("unreviewedWorkoutDraft"), names[xid] + " remains blocked prior to approval by mandatory 1.2.14 review gate")

    print("ALL BATCH ONE HUNDRED AND THIRTY-ONE INITIAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
