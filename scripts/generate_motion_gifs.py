#!/usr/bin/env python3
"""Build packaged exercise motion GIFs for the Android app.

Most motions come from ExerciseGymGifsDB, which already provides real exercise
animation frames. The importer normalizes them onto a fixed white square canvas
and keeps the source rhythm: held poses stay on screen long, crossfade
transition frames flash briefly. The crossfades are double exposures baked into
the source material, so giving them equal screen time (as an earlier version
did) makes the playback look smeared with ghost trails.

Two rehab-style motions are not present in the public GIF set, so they fall back
to the existing local anatomical start/end sheets with optical-flow
interpolation. Each interpolated frame warps a single source image (never a
blend of two warps) to avoid the same double-exposure ghosting.
"""

from __future__ import annotations

import math
import urllib.request
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageOps, ImageSequence


ROOT = Path(__file__).resolve().parents[1]
SHEETS = ROOT / "assets" / "motion_sheets"
SOURCE_CACHE = ROOT / "assets" / "motion_sources"
RAW = ROOT / "app" / "src" / "main" / "res" / "raw"

SIZE = 480
PADDING = 12
# Source GIFs are two held poses (1000ms each) bridged by short crossfade
# frames (100ms each). The crossfades are literal double exposures, so they
# must stay on screen only briefly: long holds + fast transitions keep the
# ghosting below perception instead of dominating the loop.
HOLD_MS = 900
TRANSITION_MS = 70
HOLD_THRESHOLD_MS = 400
BG = (255, 255, 255)
GIF_BASE = "https://cdn.jsdelivr.net/gh/JahelCuadrado/ExerciseGymGifsDB@v1.1.0"


GIF_SOURCES: Dict[str, str] = {
    "lat_pulldown": "lats/cable-lat-pulldown-full-range-of-motion.gif",
    "band_row": "upper-back/resistance-band-seated-straight-back-row.gif",
    "one_arm_dumbbell_row": "upper-back/dumbbell-one-arm-bent-over-row.gif",
    "seated_row": "upper-back/cable-seated-row.gif",
    "band_pulldown": "lats/band-close-grip-pulldown.gif",
    "bent_over_barbell_row": "upper-back/barbell-bent-over-row.gif",
    "face_pull": "delts/cable-standing-rear-delt-row-with-rope.gif",
    "wall_pushup": "pectorals/push-up-wall.gif",
    "incline_pushup": "pectorals/incline-push-up.gif",
    "dumbbell_bench_press": "pectorals/dumbbell-bench-press.gif",
    "seated_chest_press": "pectorals/lever-chest-press.gif",
    "seated_shoulder_press": "delts/dumbbell-seated-shoulder-press.gif",
    "band_external_rotation": "delts/cable-standing-shoulder-external-rotation.gif",
    "goblet_squat": "quads/dumbbell-goblet-squat.gif",
    "glute_bridge": "glutes/low-glute-bridge-on-floor.gif",
    "romanian_deadlift": "glutes/dumbbell-romanian-deadlift.gif",
    "step_up": "glutes/dumbbell-step-up.gif",
    "dead_bug": "abs/dead-bug.gif",
    "plank": "abs/front-plank-with-twist.gif",
    "pallof_press": "abs/band-horizontal-pallof-press.gif",
    "dumbbell_curl": "biceps/dumbbell-standing-biceps-curl.gif",
    "inverted_row": "upper-back/inverted-row.gif",
}

SHEET_FALLBACKS: Dict[str, Tuple[str, int]] = {
    "sit_to_stand": ("sheet_legs_1.png", 0),
    "bird_dog": ("sheet_core_1.png", 2),
}


def fetch_source(key: str, source_path: str) -> Path:
    SOURCE_CACHE.mkdir(parents=True, exist_ok=True)
    local = SOURCE_CACHE / f"{key}.gif"
    if local.exists() and local.stat().st_size > 0:
        return local
    url = f"{GIF_BASE}/{source_path}"
    urllib.request.urlretrieve(url, local)
    return local


def frame_content_box(frames: Iterable[Image.Image]) -> Tuple[int, int, int, int]:
    boxes: List[Tuple[int, int, int, int]] = []
    for frame in frames:
        white = Image.new("RGB", frame.size, BG)
        diff = ImageChops.difference(frame.convert("RGB"), white).convert("L")
        mask = diff.point(lambda value: 255 if value > 18 else 0)
        box = mask.getbbox()
        if box is not None:
            boxes.append(box)
    if not boxes:
        return (0, 0, SIZE, SIZE)
    left = min(box[0] for box in boxes)
    top = min(box[1] for box in boxes)
    right = max(box[2] for box in boxes)
    bottom = max(box[3] for box in boxes)
    pad = 8
    return (
        max(0, left - pad),
        max(0, top - pad),
        min(frames[0].width if isinstance(frames, list) else right, right + pad),
        min(frames[0].height if isinstance(frames, list) else bottom, bottom + pad),
    )


def fit_frame(frame: Image.Image, box: Tuple[int, int, int, int]) -> Image.Image:
    crop = frame.convert("RGB").crop(box)
    contained = ImageOps.contain(crop, (SIZE - PADDING * 2, SIZE - PADDING * 2), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (SIZE, SIZE), BG)
    canvas.paste(contained, ((SIZE - contained.width) // 2, (SIZE - contained.height) // 2))
    return canvas


def read_gif_frames(path: Path) -> Tuple[List[Image.Image], List[int]]:
    image = Image.open(path)
    frames: List[Image.Image] = []
    durations: List[int] = []
    for frame in ImageSequence.Iterator(image):
        base = Image.new("RGBA", image.size, BG + (255,))
        base.alpha_composite(frame.convert("RGBA"))
        frames.append(base.convert("RGB"))
        durations.append(int(frame.info.get("duration", 100)))
    if not frames:
        raise ValueError(f"No frames found in {path}")
    return frames, durations


def retime_frames(
    frames: List[Image.Image], durations: List[int]
) -> Tuple[List[Image.Image], List[int]]:
    """Long holds, fast crossfades; drop the deepest (50/50) blend frame."""
    if not any(duration >= HOLD_THRESHOLD_MS for duration in durations):
        return frames, [max(duration, 100) for duration in durations]
    out_frames: List[Image.Image] = []
    out_durations: List[int] = []
    index = 0
    while index < len(frames):
        if durations[index] >= HOLD_THRESHOLD_MS:
            out_frames.append(frames[index])
            out_durations.append(HOLD_MS)
            index += 1
            continue
        run_end = index
        while run_end < len(frames) and durations[run_end] < HOLD_THRESHOLD_MS:
            run_end += 1
        run = list(range(index, run_end))
        if len(run) >= 5:
            run.pop(len(run) // 2)
        for keep in run:
            out_frames.append(frames[keep])
            out_durations.append(TRANSITION_MS)
        index = run_end
    return out_frames, out_durations


def normalized_source_frames(path: Path) -> Tuple[List[Image.Image], List[int]]:
    frames, durations = read_gif_frames(path)
    box = frame_content_box(frames)
    fitted = [fit_frame(frame, box) for frame in frames]
    return retime_frames(fitted, durations)


def sheet_pair(sheet_name: str, row: int) -> Tuple[Image.Image, Image.Image]:
    sheet = Image.open(SHEETS / sheet_name).convert("RGB")
    cell_w = sheet.width // 2
    cell_h = sheet.height // 3
    inset = 8
    top = row * cell_h
    start = sheet.crop((inset, top + inset, cell_w - inset, top + cell_h - inset))
    end = sheet.crop((cell_w + inset, top + inset, cell_w * 2 - inset, top + cell_h - inset))
    box = union_box(start, end)
    return fit_frame(start, box), fit_frame(end, box)


def union_box(start: Image.Image, end: Image.Image) -> Tuple[int, int, int, int]:
    start_box = frame_content_box([start])
    end_box = frame_content_box([end])
    return (
        min(start_box[0], end_box[0]),
        min(start_box[1], end_box[1]),
        max(start_box[2], end_box[2]),
        max(start_box[3], end_box[3]),
    )


def warp(image: np.ndarray, flow: np.ndarray, factor: float) -> np.ndarray:
    height, width = flow.shape[:2]
    grid_x, grid_y = np.meshgrid(np.arange(width), np.arange(height))
    map_x = (grid_x + flow[..., 0] * factor).astype(np.float32)
    map_y = (grid_y + flow[..., 1] * factor).astype(np.float32)
    return cv2.remap(image, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def fallback_frames(start: Image.Image, end: Image.Image) -> List[Image.Image]:
    first = np.array(start.convert("RGB"))
    last = np.array(end.convert("RGB"))
    first_gray = cv2.cvtColor(first, cv2.COLOR_RGB2GRAY)
    last_gray = cv2.cvtColor(last, cv2.COLOR_RGB2GRAY)

    flow = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    flow.setFinestScale(1)
    flow.setGradientDescentIterations(40)
    flow.setVariationalRefinementIterations(10)
    forward = flow.calc(first_gray, last_gray, None)
    backward = flow.calc(last_gray, first_gray, None)

    diff = cv2.absdiff(first, last).max(axis=2)
    motion_mask = (diff > 28).astype(np.uint8) * 255
    motion_mask = cv2.morphologyEx(motion_mask, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8), iterations=1)
    motion_mask = cv2.dilate(motion_mask, np.ones((11, 11), np.uint8), iterations=1)
    motion_mask = cv2.GaussianBlur(motion_mask, (23, 23), 0).astype(np.float32) / 255.0
    motion_mask = motion_mask[..., None]

    frames: List[Image.Image] = []
    durations: List[int] = []
    static = first.astype(np.float32)
    transitions = [0.2, 0.4, 0.6, 0.8]
    schedule = (
        [(0.0, HOLD_MS)]
        + [(t, TRANSITION_MS) for t in transitions]
        + [(1.0, HOLD_MS)]
        + [(t, TRANSITION_MS) for t in reversed(transitions)]
    )
    for t, duration in schedule:
        eased = 0.5 - 0.5 * math.cos(math.pi * t)
        # Warp a single source image per frame: cross-blending two warps
        # double-exposes wherever the flows disagree and leaves ghost trails.
        if eased <= 0.5:
            moving = warp(first, forward, -eased)
        else:
            moving = warp(last, backward, -(1 - eased))
        frame = static * (1 - motion_mask) + moving.astype(np.float32) * motion_mask
        frames.append(Image.fromarray(frame.clip(0, 255).astype(np.uint8)))
        durations.append(duration)
    return frames, durations


def save_gif(key: str, frames: List[Image.Image], durations: List[int]) -> None:
    out = RAW / f"motion_{key}.gif"
    palette_frames = [frame.quantize(colors=128) for frame in frames]
    palette_frames[0].save(
        out,
        save_all=True,
        append_images=palette_frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)

    for key, source_path in GIF_SOURCES.items():
        source = fetch_source(key, source_path)
        frames, durations = normalized_source_frames(source)
        save_gif(key, frames, durations)

    for key, (sheet_name, row) in SHEET_FALLBACKS.items():
        frames, durations = fallback_frames(*sheet_pair(sheet_name, row))
        save_gif(key, frames, durations)


if __name__ == "__main__":
    main()
