#!/usr/bin/env python3
"""Prepare the next resumable built-in-imagegen wave for anatomy motion sheets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

from build_anatomy_generation_queue import (
    DATASET,
    EXACT_MEDIA,
    REFERENCE_BY_CATEGORY,
    ROOT,
    SHEET_MANIFEST,
)


WAVES_DIR = ROOT / "assets" / "anatomy_motion_sheets" / "waves"
OUTPUT_DIR = ROOT / "assets" / "anatomy_motion_sheets" / "generated"
REFERENCE_DIR = ROOT / "assets" / "motion_sheets"
COMPLETE_STATUSES = {"generated", "technical_passed", "qa_passed", "installed"}
GENERAL_REFERENCES = [
    "sheet_back_1.png",
    "sheet_core_1.png",
    "sheet_legs_1.png",
    "sheet_push_1.png",
    "sheet_core_arms_2.png",
]

COMMON_PROMPT = """Use case: scientific-educational
Asset type: production source sheet for exercise animation start/end frames
Input images: all supplied images are style and layout references only. Match their visual language very closely; do not edit or collage them.
Primary request: Create one new anatomical exercise motion sheet containing exactly three start/end pose pairs in a strict 3-row by 2-column grid. Each row is one exercise. The left cell is START and the right cell is END.
Canvas/layout: landscape 3:2 ratio like the references; equal-size cells; very thin pale-gray center divider and row dividers; pure white background; generous consistent padding; no cropping; no captions or labels.
Subject/style: use the same adult male anatomical fitness model across every cell, grayscale exposed-muscle medical illustration, realistic proportions, close-cropped dark hair, black shorts, barefoot. Equipment is matte black and gray; resistance bands may be muted green. Only the anatomically active primary target muscles are tinted muted coral red. Fine gray anatomical linework, clean educational rendering, soft minimal grounding shadow only.
Movement interpretation: follow the exercise name and source movement instructions. The left cell shows the setup immediately before the active range of motion; the right cell shows the peak contraction, peak stretch, or defining end position. For unilateral or alternating movements, demonstrate one consistent side. If source metadata conflicts with established biomechanics, preserve the named movement and show the anatomically active muscles rather than coloring an incorrect muscle.
Scientific constraints: anatomically plausible joint positions and equipment interaction; exactly one complete body per cell; correct number of limbs, hands, and feet; matching identity, scale, viewpoint, equipment anchors, and camera within each pair; clearly different start and end range of motion.
Avoid: any text, arrows, numbers, logos, watermark, labels, decorative background, gym room, extra props, helper people, extra limbs, floating equipment, cut-off body parts, skeletal X-ray look, blue muscles, glossy plastic skin, inconsistent camera, or mixed exercise poses."""


def slug(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return cleaned or "mixed"


def completed_ids(manifest: dict) -> set[str]:
    return {
        str(exercise["id"])
        for sheet in manifest["sheets"]
        if sheet.get("status") in COMPLETE_STATUSES
        for exercise in sheet["exercises"]
    }


def completed_sheet_ids(manifest: dict) -> set[str]:
    return {str(sheet["id"]) for sheet in manifest["sheets"]}


def next_wave_number() -> int:
    numbers = []
    for path in WAVES_DIR.glob("wave_*.json"):
        match = re.fullmatch(r"wave_(\d+)\.json", path.name)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


def exercise_prompt(row_number: int, row: dict) -> str:
    instructions = " ".join(str(item) for item in row.get("instructions_zh", []))
    return (
        f"Row {row_number} exercise: {row['name']} ({row.get('name_zh', '')}).\n"
        f"Primary target metadata: {row.get('target', '')}; supporting muscle group: "
        f"{row.get('muscle_group', '')}; equipment: {row.get('equipment', '')}.\n"
        f"Source movement instructions: {instructions}\n"
        "Choose the clearest instructional viewpoint for this movement. Keep the full body and all "
        "equipment visible. Make START and END biomechanically distinct while keeping camera, body "
        "identity, equipment anchors, grip points, and support points identical. Highlight only the "
        "anatomically active primary muscles in muted coral red."
    )


def filler_prompt(row_number: int) -> str:
    return (
        f"Row {row_number} calibration row: repeat a neutral standing anatomical model in both cells "
        "at identical scale and viewpoint, arms relaxed by the sides, no equipment and no highlighted "
        "muscles. This row is layout filler only."
    )


def make_batch(category: str, rows: list[dict]) -> dict:
    ids = [str(row["id"]) for row in rows]
    category_slug = slug(category)
    batch_id = f"auto_{category_slug}_{'_'.join(ids)}"
    filename = f"sheet_{batch_id}.png"
    references = REFERENCE_BY_CATEGORY.get(category, GENERAL_REFERENCES)
    prompt_parts = [COMMON_PROMPT]
    for index, row in enumerate(rows, start=1):
        prompt_parts.append(exercise_prompt(index, row))
    for index in range(len(rows) + 1, 4):
        prompt_parts.append(filler_prompt(index))
    prompt = "\n\n".join(prompt_parts)
    return {
        "id": batch_id,
        "category": category,
        "destination": str((OUTPUT_DIR / filename).relative_to(ROOT)),
        "references": [str((REFERENCE_DIR / name).resolve()) for name in references[:5]],
        "prompt": prompt,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "exercises": [
            {
                "row": index,
                "id": str(row["id"]),
                "name": row["name"],
                "name_zh": row.get("name_zh", ""),
            }
            for index, row in enumerate(rows)
        ],
    }


def unresolved_wave(manifest: dict) -> Path | None:
    recorded = completed_sheet_ids(manifest)
    for path in sorted(WAVES_DIR.glob("wave_*.json"), reverse=True):
        wave = json.loads(path.read_text(encoding="utf-8"))
        if any(batch["id"] not in recorded for batch in wave["batches"]):
            return path
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=6, help="maximum sheets in this wave")
    parser.add_argument("--force-new", action="store_true", help="ignore an unresolved prior wave")
    args = parser.parse_args()
    if args.count < 1:
        raise SystemExit("--count must be positive")

    WAVES_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(SHEET_MANIFEST.read_text(encoding="utf-8"))
    if not args.force_new:
        existing = unresolved_wave(manifest)
        if existing is not None:
            print(existing)
            return

    dataset = json.loads(DATASET.read_text(encoding="utf-8"))["exercises"]
    exact_ids = set(json.loads(EXACT_MEDIA.read_text(encoding="utf-8")))
    done = completed_ids(manifest)
    pending = [row for row in dataset if str(row["id"]) not in exact_ids | done]
    if not pending:
        print("complete")
        return

    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in pending:
        grouped[str(row["category"])].append(row)

    full_groups: list[tuple[str, list[dict]]] = []
    leftovers: list[dict] = []
    for category in sorted(grouped):
        rows = grouped[category]
        full_count = len(rows) // 3
        for index in range(full_count):
            full_groups.append((category, rows[index * 3:(index + 1) * 3]))
        leftovers.extend(rows[full_count * 3:])

    selected = full_groups[:args.count]
    if len(selected) < args.count:
        remaining_slots = args.count - len(selected)
        for index in range(0, len(leftovers), 3):
            if remaining_slots <= 0:
                break
            selected.append(("mixed", leftovers[index:index + 3]))
            remaining_slots -= 1

    wave_number = next_wave_number()
    path = WAVES_DIR / f"wave_{wave_number:04d}.json"
    payload = {
        "version": 1,
        "wave": wave_number,
        "mode": "built-in-imagegen",
        "batches": [make_batch(category, rows) for category, rows in selected],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
