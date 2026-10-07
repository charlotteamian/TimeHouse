#!/usr/bin/env python3
"""Convert approved 3x2 anatomy start/end sheets into preview GIFs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

from generate_motion_gifs import fallback_frames, fit_frame, union_box


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "scripts" / "data" / "anatomy_sheet_manifest.json"
DEFAULT_OUTPUT = ROOT / "build" / "anatomy-motion-gifs"


def crop_pair(sheet: Image.Image, row: int) -> tuple[Image.Image, Image.Image]:
    if sheet.width * 2 != sheet.height * 3:
        raise ValueError(f"expected a 3:2 sheet, got {sheet.width}x{sheet.height}")
    cell_w = sheet.width // 2
    cell_h = sheet.height // 3
    inset = max(4, round(min(cell_w, cell_h) * 0.015))
    top = row * cell_h
    start = sheet.crop((inset, top + inset, cell_w - inset, top + cell_h - inset))
    end = sheet.crop((cell_w + inset, top + inset, sheet.width - inset, top + cell_h - inset))
    box = union_box(start, end)
    return fit_frame(start, box), fit_frame(end, box)


def save_gif(path: Path, start: Image.Image, end: Image.Image) -> None:
    frames, durations = fallback_frames(start, end)
    indexed = [frame.quantize(colors=128) for frame in frames]
    indexed[0].save(
        path,
        save_all=True,
        append_images=indexed[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--sheet-id", help="generate one manifest sheet only")
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    selected = [
        sheet for sheet in manifest["sheets"]
        if sheet["status"] in {"technical_passed", "qa_passed", "installed"}
        and (args.sheet_id is None or sheet["id"] == args.sheet_id)
    ]
    if args.sheet_id and not selected:
        raise SystemExit(f"no approved sheet found for {args.sheet_id!r}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    generated = 0
    for record in selected:
        path = ROOT / record["path"]
        sheet = Image.open(path).convert("RGB")
        for exercise in record["exercises"]:
            start, end = crop_pair(sheet, int(exercise["row"]))
            save_gif(args.output_dir / f"dataset_motion_{exercise['id']}.gif", start, end)
            generated += 1
    print(f"Generated {generated} anatomy preview GIFs in {args.output_dir}")


if __name__ == "__main__":
    main()
