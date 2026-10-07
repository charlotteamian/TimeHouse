#!/usr/bin/env python3
"""Build app-owned looping animations from two public-domain exercise photos.

The two free-exercise-db photos per exercise are the start and end pose shot
from a (mostly) fixed camera. Earlier versions cross-faded between them, which
double-exposes the athlete into a ghost during every transition frame. Now the
loop is a registered two-pose flip: align the second photo onto the first with
a guarded similarity fit, then alternate the two clean frames — no blend, no
ghosting, and any camera drift between the shots is cancelled instead of
animated.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops

sys.path.insert(0, str(Path(__file__).resolve().parent))
import animate_anatomical_frames as anim  # noqa: E402

SIZE = (480, 480)
BACKGROUND = (250, 248, 242)
DURATIONS_MS = list(anim.FLIP_DURATIONS)  # [1180, 1180] — the 2360 ms contract


def prepared_frame(path: Path) -> Image.Image:
    with Image.open(path) as source:
        image = source.convert("RGB")
    image.thumbnail((456, 456), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", SIZE, BACKGROUND)
    canvas.paste(image, ((SIZE[0] - image.width) // 2, (SIZE[1] - image.height) // 2))
    return canvas


def build_animation(first_path: Path, second_path: Path, output: Path) -> dict:
    first = prepared_frame(first_path)
    second = prepared_frame(second_path)
    if ImageChops.difference(first, second).getbbox() is None:
        # Some static-hold exercises publish the same pose twice: it is an
        # isometric hold, and the honest demonstration is a still image. (The
        # old zoom "breathing" made the whole scene swim, and a subtle exposure
        # pulse gets deduplicated away by lossy WebP anyway.)
        frames = [first]
        info = {"mode": "still-photo"}
    else:
        a = np.array(first)
        b = np.array(second)
        registered, reg = anim.register_end_to_start(a, b, border="replicate")
        frames = [first, Image.fromarray(registered)]
        info = {"mode": "flip-photo", **reg}
    durations = DURATIONS_MS[:len(frames)]
    if output.suffix.lower() == ".gif":
        anim.save_gif(frames, durations, output)
    else:
        anim.save_webp(frames, durations, output)
    return info


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matches", required=True, type=Path)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--ext", default=".gif", choices=[".gif", ".webp"])
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    with args.matches.open(encoding="utf-8", newline="") as handle:
        for row in csv.reader(handle, delimiter="\t"):
            if len(row) != 4:
                raise ValueError(f"Expected 4 columns in media match row, got {len(row)}: {row}")
            _, exercise_id, first_relative, second_relative = row
            info = build_animation(
                args.source_root / "exercises" / first_relative,
                args.source_root / "exercises" / second_relative,
                args.output_dir / f"dataset_motion_{exercise_id}{args.ext}",
            )
            count += 1
            print(f"dataset_motion_{exercise_id}: {info.get('mode')} "
                  f"align={info.get('edge_align', '-')}")
    print(f"Generated {count} looping exercise animations")


if __name__ == "__main__":
    main()
