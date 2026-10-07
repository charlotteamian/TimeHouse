#!/usr/bin/env python3
"""Convert packaged animated GIFs to animated WebP (smaller, ImageDecoder-native).

Re-encodes every dataset_motion_*.gif / motion_*.gif under res/raw as WebP with
the same frames and per-frame timing, then removes the .gif so no two resources
share an R.raw name. Idempotent: already-converted names are skipped.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageSequence

QUALITY = 80


def convert(gif: Path) -> int:
    frames, durations = [], []
    with Image.open(gif) as im:
        for frame in ImageSequence.Iterator(im):
            frames.append(frame.convert("RGB"))
            durations.append(int(frame.info.get("duration", 100)))
    out = gif.with_suffix(".webp")
    frames[0].save(out, format="WEBP", save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, quality=QUALITY, method=4)
    gif.unlink()
    return out.stat().st_size


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("directory", type=Path)
    ap.add_argument("--globs", nargs="+", default=["dataset_motion_*.gif", "motion_*.gif"])
    args = ap.parse_args()

    paths = sorted({p for g in args.globs for p in args.directory.glob(g)})
    total = 0
    for p in paths:
        total += convert(p)
    print(f"converted {len(paths)} GIFs to WebP ({total / 1048576:.0f} MB) in {args.directory}")


if __name__ == "__main__":
    main()
