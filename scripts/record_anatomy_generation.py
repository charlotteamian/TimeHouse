#!/usr/bin/env python3
"""Validate, copy, and atomically record one generated anatomy sheet."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

from build_anatomy_generation_queue import ROOT, SHEET_MANIFEST


ACCEPTED_SOURCE_STATUSES = {"generated", "technical_passed", "qa_passed", "installed"}


def cell(sheet: Image.Image, row: int, column: int) -> Image.Image:
    cell_w = sheet.width // 2
    cell_h = sheet.height // 3
    return sheet.crop((column * cell_w, row * cell_h, (column + 1) * cell_w, (row + 1) * cell_h))


def content_fraction(image: Image.Image) -> float:
    # Ignore the sheet dividers and faint off-white background texture. A bbox
    # is unsuitable here because one pale divider can span the entire cell.
    inset_x = max(4, round(image.width * 0.025))
    inset_y = max(4, round(image.height * 0.025))
    interior = image.crop((inset_x, inset_y, image.width - inset_x, image.height - inset_y))
    white = Image.new("RGB", interior.size, (255, 255, 255))
    diff = ImageChops.difference(interior.convert("RGB"), white).convert("L")
    histogram = diff.histogram()
    foreground = sum(histogram[25:])
    return foreground / (interior.width * interior.height)


def validate_sheet(path: Path, batch: dict) -> tuple[int, int]:
    with Image.open(path) as source:
        sheet = source.convert("RGB")
    if sheet.width * 2 != sheet.height * 3:
        raise SystemExit(f"{path}: expected 3:2 sheet, got {sheet.width}x{sheet.height}")
    if sheet.width < 1200 or sheet.height < 800:
        raise SystemExit(f"{path}: source is too small at {sheet.width}x{sheet.height}")
    for exercise in batch["exercises"]:
        row = int(exercise["row"])
        start = cell(sheet, row, 0)
        end = cell(sheet, row, 1)
        for label, frame in (("start", start), ("end", end)):
            fraction = content_fraction(frame)
            if not 0.008 <= fraction <= 0.75:
                raise SystemExit(
                    f"{path}: {exercise['id']} {label} content fraction {fraction:.3f} is implausible"
                )
        delta = ImageStat.Stat(ImageChops.difference(start, end)).rms
        if sum(delta) / len(delta) < 2.0:
            raise SystemExit(f"{path}: {exercise['id']} start/end cells are effectively identical")
    return sheet.size


def atomic_write(path: Path, payload: dict) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wave", required=True, type=Path)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--source", required=True, type=Path)
    args = parser.parse_args()

    wave = json.loads(args.wave.read_text(encoding="utf-8"))
    matches = [batch for batch in wave["batches"] if batch["id"] == args.batch_id]
    if len(matches) != 1:
        raise SystemExit(f"expected one batch {args.batch_id!r}, found {len(matches)}")
    batch = matches[0]
    manifest = json.loads(SHEET_MANIFEST.read_text(encoding="utf-8"))
    existing = [sheet for sheet in manifest["sheets"] if sheet["id"] == args.batch_id]
    if existing:
        print(f"Already recorded {args.batch_id}")
        return

    recorded_ids = {
        str(exercise["id"])
        for sheet in manifest["sheets"]
        if sheet.get("status") in ACCEPTED_SOURCE_STATUSES
        for exercise in sheet["exercises"]
    }
    duplicate_ids = recorded_ids & {str(item["id"]) for item in batch["exercises"]}
    if duplicate_ids:
        raise SystemExit(f"exercise IDs already recorded: {sorted(duplicate_ids)}")

    width, height = validate_sheet(args.source, batch)
    destination = ROOT / batch["destination"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise SystemExit(f"refusing to overwrite existing asset: {destination}")
    shutil.copy2(args.source, destination)

    manifest["sheets"].append({
        "id": batch["id"],
        "path": batch["destination"],
        "status": "technical_passed",
        "generator": "built-in-imagegen",
        "prompt_version": "v2-auto",
        "prompt_sha256": batch["prompt_sha256"],
        "wave": int(wave["wave"]),
        "source_size": [width, height],
        "exercises": batch["exercises"],
    })
    atomic_write(SHEET_MANIFEST, manifest)
    print(f"Recorded {args.batch_id}: {destination}")


if __name__ == "__main__":
    main()
