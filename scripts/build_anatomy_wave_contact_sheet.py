#!/usr/bin/env python3
"""Build a compact visual-QA contact sheet for one generated wave."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from build_anatomy_generation_queue import ROOT


DEFAULT_OUTPUT_DIR = ROOT / "build" / "anatomy-wave-contacts"
CELL_W = 768
CELL_H = 512


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wave", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    wave = json.loads(args.wave.read_text(encoding="utf-8"))
    available = [batch for batch in wave["batches"] if (ROOT / batch["destination"]).exists()]
    if not available:
        raise SystemExit(f"no generated assets found for {args.wave}")
    columns = 2
    rows = math.ceil(len(available) / columns)
    canvas = Image.new("RGB", (columns * CELL_W, rows * CELL_H), (246, 246, 246))
    font = ImageFont.load_default(size=18)
    for index, batch in enumerate(available):
        image = Image.open(ROOT / batch["destination"]).convert("RGB")
        image.thumbnail((CELL_W, CELL_H - 28), Image.Resampling.LANCZOS)
        x = (index % columns) * CELL_W + (CELL_W - image.width) // 2
        y = (index // columns) * CELL_H + 28 + (CELL_H - 28 - image.height) // 2
        canvas.paste(image, (x, y))
        draw = ImageDraw.Draw(canvas)
        draw.text(((index % columns) * CELL_W + 8, (index // columns) * CELL_H + 5),
                  batch["id"], fill=(45, 45, 45), font=font)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / f"wave_{int(wave['wave']):04d}.png"
    canvas.save(output)
    print(output)


if __name__ == "__main__":
    main()
