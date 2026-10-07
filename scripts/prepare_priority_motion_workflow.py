#!/usr/bin/env python3
"""Prepare the resumable priority-equipment regeneration workflow.

The current app contains older 2/10-frame demonstrations for every dataset
exercise.  This script turns each existing animation into a compact 2x2
movement guide and pairs it with one reviewed 2026-09-10 quality anchor.  The
image model therefore receives the motion semantics as pixels instead of a
long, hand-written prompt for every exercise.

Five dataset rows are true duplicates of another row in the same equipment
class. Four upstream rows are explicitly excluded because their equipment
fields are wrong: two machine-resisted leg movements, one treadmill movement,
and one ab-wheel movement. The strict eight-class scope therefore contains 721
unrepaired rows and requires exactly 716 new source images.

Run with the project Python that contains Pillow:

    /opt/homebrew/Caskroom/miniforge/base/bin/python3 \
      scripts/prepare_priority_motion_workflow.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "app/src/main/assets/exercises_1324.json"
RAW = ROOT / "app/src/main/res/raw"
REPAIRS = ROOT / "assets/motion_repairs"
DEFAULT_BATCH = "20260910_720"

# These are the eight user-facing equipment classes.  Both upstream band
# spellings map to the single in-app label 弹力带.
EQUIPMENT_LABELS = {
    "body weight": "自重",
    "band": "弹力带",
    "resistance band": "弹力带",
    "dumbbell": "哑铃",
    "kettlebell": "壶铃",
    "stability ball": "瑜伽球",
    "bosu ball": "BOSU 球",
    "stationary bike": "动感单车",
}

# Visually and biomechanically equivalent duplicate rows.  Generate the value
# once (right side), then install it for the duplicate id (left side).
REUSE = {
    "0296": "1731",  # dumbbell close-grip press
    "0513": "0514",  # jump squat v2
    "0656": "0655",  # push-up on stability ball (identical source steps)
    "0658": "0659",  # wall push-up v2
    "1680": "0422",  # one-arm curl over incline bench
}

# These upstream records are tagged as body weight, but their names,
# instructions, and source animations require equipment outside the user's
# eight allowed classes. Keep the exceptions explicit so they cannot silently
# re-enter the batch.
SCOPE_EXCLUSIONS = {
    "2400": "upstream equipment is mislabeled as body weight; movement requires a pull-in cable machine",
    "0684": "upstream equipment is mislabeled as body weight; run (equipment) is shown on a treadmill",
    "3637": "upstream equipment is mislabeled as body weight; wheel run requires an ab wheel",
    "1766": "upstream equipment is mislabeled as body weight; instructions and guide require a leg-curl machine",
}

STYLE_ANCHORS = {
    "body weight": REPAIRS / "20260910/0500.png",
    "band": REPAIRS / "20260910/3144.png",
    "resistance band": REPAIRS / "20260910/3144.png",
    "dumbbell": REPAIRS / "20260910/0313.png",
    "kettlebell": REPAIRS / "20260910/0549.png",
    "stability ball": REPAIRS / "20260910/0271.png",
    "bosu ball": REPAIRS / "20260910/1705.png",
    "stationary bike": REPAIRS / "20260910/2138.png",
}


def repaired_ids() -> set[str]:
    result: set[str] = set()
    for path in sorted(REPAIRS.glob("*/manifest.json")):
        result.update(str(row["id"]) for row in json.loads(path.read_text()))
    return result


def flatten(frame: Image.Image) -> Image.Image:
    rgba = frame.convert("RGBA")
    background = Image.new("RGBA", rgba.size, "white")
    background.alpha_composite(rgba)
    return background.convert("RGB")


def frame_indices(count: int) -> list[int]:
    if count <= 1:
        return [0, 0, 0, 0]
    if count == 2:
        # The source provides endpoints only.  Repetition makes that limitation
        # explicit instead of inventing a blurry local cross-fade.
        return [0, 1, 1, 0]
    return [round(index * (count - 1) / 3) for index in range(4)]


def make_guide(source: Path, destination: Path) -> dict:
    image = Image.open(source)
    indexes = frame_indices(getattr(image, "n_frames", 1))
    canvas = Image.new("RGB", (1024, 1024), "white")
    for cell, frame_index in enumerate(indexes):
        image.seek(frame_index)
        frame = flatten(image.copy())
        frame.thumbnail((492, 492), Image.Resampling.LANCZOS)
        x0 = (cell % 2) * 512 + (512 - frame.width) // 2
        y0 = (cell // 2) * 512 + (512 - frame.height) // 2
        canvas.paste(frame, (x0, y0))
    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, optimize=True)
    return {"source_frames": getattr(image, "n_frames", 1), "guide_frames": indexes}


def prompt(row: dict) -> str:
    steps = [str(value).strip() for value in row.get("instructions_zh", []) if str(value).strip()]
    cue = " ".join(steps)
    return (
        "Use case: scientific-educational. Asset: production 2x2 exercise-animation sprite sheet. "
        "Image 1 is the exclusive visual-quality and anatomy-style reference. Image 2 is only the "
        "movement, viewpoint, and equipment guide; redraw it cleanly and do not copy its artifacts. "
        f"Exercise: {row['name']} ({row.get('name_zh', '')}); equipment: "
        f"{EQUIPMENT_LABELS[row['equipment']]}; primary target: {row.get('target', '')}. "
        f"Movement cue: {cue} If the old guide or translated steps conflict with the English exercise "
        "name, follow the named exercise and standard biomechanics. Create one square image with "
        "exactly four equal cells in reading order: setup immediately before the active range, a true "
        "halfway pose, the clearly different peak endpoint, then an exact repeat of the halfway pose. "
        "Do not substitute duplicate poses for real joint motion. Show the same adult male grayscale "
        "anatomical model, black shorts, and the same "
        "camera, scale, support points, grip points, and fixed equipment in every cell. Use a pure "
        "white background and tint only active primary muscles muted coral red. Full body and all "
        "equipment must remain visible. No text, arrows, labels, borders, watermark, scenery, extra "
        "people, extra limbs, floating equipment, camera motion, duplicate phases, or impossible joints."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", default=DEFAULT_BATCH)
    parser.add_argument("--refresh-guides", action="store_true")
    args = parser.parse_args()
    if not args.batch.replace("_", "").isalnum():
        raise SystemExit("batch must contain only letters, numbers, and underscores")

    batch = REPAIRS / args.batch
    guides = batch / "guides"
    batch.mkdir(parents=True, exist_ok=True)
    guides.mkdir(parents=True, exist_ok=True)

    exercises = json.loads(DATASET.read_text(encoding="utf-8"))["exercises"]
    completed = repaired_ids()
    candidates = [
        row for row in exercises
        if row.get("equipment") in EQUIPMENT_LABELS
        and str(row["id"]) not in completed
        and str(row["id"]) not in SCOPE_EXCLUSIONS
    ]
    candidate_ids = {str(row["id"]) for row in candidates}
    for duplicate, source in REUSE.items():
        if duplicate not in candidate_ids or source not in candidate_ids:
            raise SystemExit(f"reuse pair is no longer pending: {duplicate} <- {source}")

    generated = [row for row in candidates if str(row["id"]) not in REUSE]
    if len(candidates) != 721 or len(generated) != 716:
        raise SystemExit(
            f"scope drift: expected 721 pending rows / 716 generated images, "
            f"got {len(candidates)} / {len(generated)}"
        )

    specs = []
    for row in generated:
        exercise_id = str(row["id"])
        source = RAW / f"dataset_motion_{exercise_id}.webp"
        if not source.exists():
            raise FileNotFoundError(source)
        style = STYLE_ANCHORS[row["equipment"]]
        if not style.exists():
            raise FileNotFoundError(style)
        guide = guides / f"{exercise_id}.png"
        if args.refresh_guides or not guide.exists():
            guide_info = make_guide(source, guide)
        else:
            old = Image.open(source)
            guide_info = {
                "source_frames": getattr(old, "n_frames", 1),
                "guide_frames": frame_indices(getattr(old, "n_frames", 1)),
            }
        text = prompt(row)
        specs.append({
            "id": exercise_id,
            "name": row.get("name_zh") or row["name"],
            "name_en": row["name"],
            "equipment": EQUIPMENT_LABELS[row["equipment"]],
            "equipment_source": row["equipment"],
            "target": row.get("target", ""),
            "style_reference": str(style.resolve()),
            "movement_guide": str(guide.resolve()),
            "prompt": text,
            "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "status": "generated" if (batch / f"{exercise_id}.png").exists() else "pending",
            **guide_info,
        })

    (batch / "prompts.json").write_text(
        json.dumps(specs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (batch / "reuse.json").write_text(
        json.dumps(REUSE, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (batch / "scope-exclusions.json").write_text(
        json.dumps(SCOPE_EXCLUSIONS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    summary = {
        "version": 1,
        "mode": "built-in-imagegen",
        "batch": args.batch,
        "equipment": list(dict.fromkeys(EQUIPMENT_LABELS.values())),
        "scope_pending_before_workflow": len(candidates),
        "new_images": len(specs),
        "exact_duplicate_reuses": len(REUSE),
        "scope_exclusions": len(SCOPE_EXCLUSIONS),
        "covered_rows": len(specs) + len(REUSE),
        "already_repaired": len(completed),
        "status_counts": dict(Counter(row["status"] for row in specs)),
        "prompt_strategy": "one quality anchor plus one local movement guide plus full source movement cue",
    }
    (batch / "workflow.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    shutil.copy2(STYLE_ANCHORS["dumbbell"], batch / "QUALITY_ANCHOR.png")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
