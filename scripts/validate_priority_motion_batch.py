#!/usr/bin/env python3
"""Technical/style gate for the 720-image priority motion batch."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BATCH = "20260910_720"


def flatten(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    background = Image.new("RGBA", rgba.size, "white")
    background.alpha_composite(rgba)
    return background.convert("RGB")


def inspect_source(path: Path) -> dict:
    image = flatten(Image.open(path))
    width, height = image.size
    reasons: list[str] = []
    if abs(width - height) > 2 or min(width, height) < 900:
        reasons.append("source_not_square_or_too_small")
    array = np.asarray(image.resize((1024, 1024), Image.Resampling.LANCZOS))
    cells = [
        array[row * 512:(row + 1) * 512, col * 512:(col + 1) * 512]
        for row, col in ((0, 0), (0, 1), (1, 0), (1, 1))
    ]
    metrics = []
    for cell in cells:
        nonwhite = np.any(cell < 242, axis=2)
        red = (cell[:, :, 0] > cell[:, :, 1] * 1.12) & (cell[:, :, 0] > 125)
        ys, xs = np.where(nonwhite)
        coverage = float(nonwhite.mean())
        red_fraction = float(red.mean())
        margin = 512 if len(xs) == 0 else int(min(xs.min(), ys.min(), 511 - xs.max(), 511 - ys.max()))
        metrics.append({
            "foreground_fraction": round(coverage, 5),
            "coral_fraction": round(red_fraction, 5),
            "minimum_margin": margin,
        })
        if coverage < 0.025:
            reasons.append("empty_cell")
        if coverage > 0.68:
            reasons.append("background_or_overcrowding")
        if margin < 2:
            reasons.append("cropped_or_cell_border")
        if red_fraction < 0.0004:
            reasons.append("missing_coral_highlight")
    start_end_delta = float(np.mean(np.abs(cells[0].astype(np.int16) - cells[2].astype(np.int16))))
    if start_end_delta < 2.0:
        reasons.append("start_end_too_similar")
    return {
        "id": path.stem,
        "size": [width, height],
        "cells": metrics,
        "start_end_delta": round(start_end_delta, 3),
        "status": "pass" if not reasons else "review",
        "reasons": sorted(set(reasons)),
    }


def inspect_asset(path: Path) -> dict:
    image = Image.open(path)
    reasons = []
    if image.size != (480, 480):
        reasons.append("asset_wrong_size")
    if getattr(image, "n_frames", 1) != 4:
        reasons.append("asset_wrong_frame_count")
    return {
        "id": path.stem.removeprefix("dataset_motion_"),
        "size": list(image.size),
        "frames": getattr(image, "n_frames", 1),
        "status": "pass" if not reasons else "review",
        "reasons": reasons,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", default=DEFAULT_BATCH)
    parser.add_argument("--assets", action="store_true", help="validate installed app assets")
    args = parser.parse_args()
    batch = ROOT / "assets/motion_repairs" / args.batch
    specs = json.loads((batch / "prompts.json").read_text())
    reuse = json.loads((batch / "reuse.json").read_text())
    expected = [str(row["id"]) for row in specs]
    if args.assets:
        ids = expected + list(reuse)
        results = [inspect_asset(ROOT / f"app/src/main/res/raw/dataset_motion_{xid}.webp") for xid in ids]
        output = batch / "asset-qa.json"
    else:
        results = []
        for exercise_id in expected:
            source = batch / f"{exercise_id}.png"
            if source.exists():
                results.append(inspect_source(source))
            else:
                results.append({"id": exercise_id, "status": "missing", "reasons": ["source_missing"]})
        output = batch / "source-qa.json"
    payload = {
        "batch": args.batch,
        "expected": len(results),
        "status_counts": dict(Counter(row["status"] for row in results)),
        "results": results,
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({**payload, "results": "omitted"}, ensure_ascii=False))
    if any(row["status"] != "pass" for row in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
