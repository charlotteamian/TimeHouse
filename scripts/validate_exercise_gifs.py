#!/usr/bin/env python3
"""Validate every generated exercise animation against the app's contract.

Media is animated WebP (or legacy GIF); both decode via Android ImageDecoder.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageChops


def webp_durations(path: Path) -> list[int]:
    """Per-frame durations (ms) parsed from a WebP's ANMF chunks.

    Pillow 12 reads animated-WebP frames but reports their durations as None, so
    read them from the container directly (Android's ImageDecoder does the same).
    """
    data = path.read_bytes()
    durations: list[int] = []
    i = 12  # past the RIFF/WEBP header
    while i < len(data) - 8:
        fourcc = data[i:i + 4]
        size = int.from_bytes(data[i + 4:i + 8], "little")
        if fourcc == b"ANMF":
            payload = data[i + 8:i + 8 + size]
            durations.append(int.from_bytes(payload[12:15], "little"))
        i += 8 + size + (size & 1)
    return durations


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--expected-count", type=int, default=1324)
    parser.add_argument("--prefix", default="dataset_motion_")
    args = parser.parse_args()

    paths = sorted([*args.directory.glob(f"{args.prefix}*.webp"),
                    *args.directory.glob(f"{args.prefix}*.gif")])
    if len(paths) != args.expected_count:
        raise SystemExit(f"Expected {args.expected_count} animations, got {len(paths)}")

    # Two animation contracts coexist, keyed by total loop duration: the
    # photographic frame-pair GIFs keep the original 2360 ms envelope, the
    # procedural mannequin GIFs use the smoother 1920 ms envelope. Frame counts
    # may fall below the authored 10/16 because GIF optimization merges
    # pixel-identical neighbours while preserving total duration.
    counts = {2360: 0, 1920: 0}
    stills = 0
    for path in paths:
        with Image.open(path) as image:
            if image.size != (480, 480):
                raise SystemExit(f"{path.name}: expected 480x480, got {image.size}")
            if image.n_frames == 1:
                # Deliberate still: an isometric hold whose two source photos
                # are identical. Displayed as a static drawable by the app.
                stills += 1
                continue
            # 2 frames = the deliberate two-pose flip (used when a GPT sheet
            # redrew the scene too differently to interpolate safely).
            if not 2 <= image.n_frames <= 16:
                raise SystemExit(f"{path.name}: expected 2-16 frames, got {image.n_frames}")
            if image.info.get("loop", 0) != 0:
                raise SystemExit(f"{path.name}: not configured to loop forever")
            webp = path.suffix == ".webp"
            file_durations = webp_durations(path) if webp else None
            durations = []
            frames = []
            for index in range(image.n_frames):
                image.seek(index)
                durations.append(file_durations[index] if webp else image.info.get("duration", 0))
                frames.append(image.convert("RGB"))
            total_ms = sum(durations)
            if total_ms not in counts:
                raise SystemExit(f"{path.name}: expected a 2360 or 1920 ms loop, got {total_ms} ms")
            # A real animation moves: some frame must differ from the first.
            # (Cyclic loops can revisit the start pose mid-loop, so compare
            # against every frame rather than a single fixed index.)
            if all(ImageChops.difference(frames[0], other).getbbox() is None
                   for other in frames[1:]):
                raise SystemExit(f"{path.name}: every frame is identical (static)")
            counts[total_ms] += 1

    webp = sum(1 for p in paths if p.suffix == ".webp")
    print(f"ExerciseAnim: {len(paths)} validated ({webp} webp, {len(paths) - webp} gif; "
          f"{counts[2360]} @2.36s, {counts[1920]} @1.92s, {stills} stills)")


if __name__ == "__main__":
    main()
