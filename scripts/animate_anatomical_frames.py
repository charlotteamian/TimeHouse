#!/usr/bin/env python3
"""Animate anatomical exercise loops from GPT-drawn start/end frame pairs.

Given two anatomical frames (a start pose and an end pose of the *same* figure),
produce the app's looping animation: 480x480 white canvas, 2.36 s, infinite loop.

The bulk GPT sheets redraw the whole scene between the two poses — figure and
equipment land shifted, rescaled, occasionally re-angled. Warping naively
between such frames smears the machine into ghost trails and makes the
background swim. Measurement on the hand-built seed sheets shows DIS flow never
truly *tracks* these drawings anyway — the old recipe looked good only where
the two frames were already aligned, because 70 ms warp flashes read as motion
blur regardless of flow accuracy. The design follows from that:

1. REGISTER (native resolution, before any letterboxing) — undo the END
   frame's whole-scene drift with the best of several guarded candidates
   (ORB similarity / full affine, dense-flow RANSAC refinements), judged by
   an edge-alignment score and required to keep all content on canvas.
2. DECIDE — after registration, measure the *static* residual: the median
   flow left on content pixels outside the moving mask. Near zero means the
   scene truly matches and warp flashes are safe; several px means the gear
   was redrawn and any warp would wobble it, so fall back to a clean
   two-pose flip (no warp, no blend — nothing can smear or ghost).
3. COMPOSITE — in warp mode the first half of the loop rides on the pure
   START frame and the second half on the pure registered END frame; only
   the moving parts (flow components kept by mean travel, so a dumbbell
   survives and redraw noise does not) are repainted, each frame warped from
   a SINGLE source image (never a blend — blends are double exposures by
   construction). Both held poses are therefore the artist's true drawings,
   and every prop lands exactly where it was drawn.

Input modes (see `main`):
  * --pair START.png END.png OUT.gif
  * --manifest manifest.json  (batch; entries pick frames from files or sheets)
  * --sheet SHEET.png --row R OUT.gif   (2 columns [start|end] x 3 rows)
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import List, Optional, Tuple

import cv2
import numpy as np
from PIL import Image, ImageOps

SIZE = 480
PAD = 14
BG = (255, 255, 255)
DARK_THRESH = 14          # (255 - max(RGB)) above this => content, not white bg

# Loop rhythm: dwell on the two clean poses, pass through the in-betweens as a
# fast flash so residual limb deformation reads as motion blur, not melting.
# The exact 0.5 midpoint (deepest warp, ugliest frame) is never shown.
HOLD_MS = 900
TRANSITION_MS = 70
TRANSITIONS = [0.2, 0.4, 0.6, 0.8]
LOOP_MS = 2 * HOLD_MS + 8 * TRANSITION_MS          # 2360, the app contract
FLIP_DURATIONS = [LOOP_MS // 2, LOOP_MS // 2]      # two-pose fallback, same loop

# Registration guardrails: reject transforms implying an implausible redraw.
REG_SCALE_RANGE = (0.72, 1.35)
REG_MAX_SHEAR = 0.15      # |shear|/scale for the full-affine candidates
REG_MIN_KEPT = 0.975      # content pixels that must survive the warp on-canvas

# Motion mask thresholds (px of optical-flow travel at 480x480).
STATIC_MAX_FLOW = 2.5     # peak in-content flow under this => poses barely differ
MASK_MIN_FLOW = 2.0       # absolute floor for "this pixel moved"
MASK_REL_FLOW = 0.25      # ... or this fraction of the peak, whichever is larger
COMP_MIN_AREA = 140       # ignore speckle components smaller than this
COMP_MEAN_KEEP = 0.30     # keep components whose mean travel >= this * best mean
MASK_DILATE = 13          # grow to cover the swept corridor
MASK_FEATHER = 11         # gaussian feather (px) for a seamless composite edge

# Warp-trust gates (calibrated on the seed sheets vs. the failed bulk pairs):
# warp only when the registered statics genuinely overlap — otherwise flip.
# The bar is deliberately high: the 24 hand-picked seed animations that looked
# good were real multi-frame source GIFs, not 2-frame warps, so a warped
# in-between has to *earn* its place; the flip is always artifact-free.
WARP_MIN_EDGE_ALIGN = 0.62   # registration quality floor
WARP_MAX_STATIC_RESID = 2.0  # median px of flow on static content after reg
FLIP_PEAK_FLOW = 150.0       # px; DIS cannot track farther without mush


# --------------------------------------------------------------------------- #
# Framing: normalize a raw frame onto the fixed white canvas
# --------------------------------------------------------------------------- #

def _content_box(img: Image.Image) -> Tuple[int, int, int, int]:
    """Tight bounds of the figure, ignoring sparse edge noise / faint bg tint."""
    arr = np.asarray(img.convert("RGB")).astype(np.int16)
    dark = (255 - arr.max(axis=2)) > DARK_THRESH
    col_hits = dark.sum(axis=0)
    row_hits = dark.sum(axis=1)
    col_thresh = max(2, int(0.02 * img.height))
    row_thresh = max(2, int(0.02 * img.width))
    xs = np.where(col_hits > col_thresh)[0]
    ys = np.where(row_hits > row_thresh)[0]
    if len(xs) == 0 or len(ys) == 0:
        return (0, 0, img.width, img.height)
    return (int(xs[0]), int(ys[0]), int(xs[-1]) + 1, int(ys[-1]) + 1)


def normalize_pair(start: Image.Image, end: Image.Image,
                   pad: int = PAD) -> Tuple[Image.Image, Image.Image]:
    """Crop both frames to a *shared* content box, then letterbox onto SIZE.

    `pad` is the white margin kept around the content. Registration runs on a
    version with a much wider margin so a shifted END frame never clips.
    """
    sb, eb = _content_box(start), _content_box(end)
    box = (min(sb[0], eb[0]), min(sb[1], eb[1]), max(sb[2], eb[2]), max(sb[3], eb[3]))

    def fit(img: Image.Image) -> Image.Image:
        crop = img.convert("RGB").crop(box)
        contained = ImageOps.contain(crop, (SIZE - pad * 2, SIZE - pad * 2), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (SIZE, SIZE), BG)
        canvas.paste(contained, ((SIZE - contained.width) // 2, (SIZE - contained.height) // 2))
        return canvas

    return fit(start), fit(end)


def sheet_pair(sheet_path: Path, row: int, cols: int = 2, rows: int = 3,
               inset: int = 8) -> Tuple[Image.Image, Image.Image]:
    """Slice a start|end pair from a multi-cell sheet (default 2 cols x 3 rows)."""
    sheet = Image.open(sheet_path).convert("RGB")
    cw, ch = sheet.width // cols, sheet.height // rows
    top = row * ch
    start = sheet.crop((inset, top + inset, cw - inset, top + ch - inset))
    end = sheet.crop((cw + inset, top + inset, cw * 2 - inset, top + ch - inset))
    return start, end


# --------------------------------------------------------------------------- #
# Registration: undo the END frame's whole-scene drift (native resolution)
# --------------------------------------------------------------------------- #

def _content_mask(rgb: np.ndarray) -> np.ndarray:
    return (255 - rgb.max(axis=2)) > DARK_THRESH


def _edge_alignment(first_gray: np.ndarray, other_gray: np.ndarray) -> float:
    """Fraction of `other` edge pixels landing within ~2px of a `first` edge.

    Cheap chamfer-style score used to pick between candidate registrations.
    The moving limb caps the attainable maximum equally for every candidate,
    so relative comparison is fair.
    """
    e1 = cv2.Canny(first_gray, 40, 120)
    e2 = cv2.Canny(other_gray, 40, 120)
    n2 = int(np.count_nonzero(e2))
    if n2 == 0:
        return 0.0
    near = cv2.dilate(e1, np.ones((5, 5), np.uint8))
    return float(np.count_nonzero((near > 0) & (e2 > 0))) / n2


def _decompose_ok(matrix: np.ndarray, shape: Tuple[int, int]) -> bool:
    """Sanity-check a 2x3 affine: bounded scale/shear/translation."""
    if matrix is None or not np.all(np.isfinite(matrix)):
        return False
    a = matrix[:, :2].astype(np.float64)
    sx = float(np.hypot(a[0, 0], a[1, 0]))
    if sx < 1e-6:
        return False
    # QR-style decomposition: rotation * [[sx, sh], [0, sy]]
    cos_t, sin_t = a[0, 0] / sx, a[1, 0] / sx
    sh = cos_t * a[0, 1] + sin_t * a[1, 1]
    sy = cos_t * a[1, 1] - sin_t * a[0, 1]
    h, w = shape
    max_shift = 0.35 * max(h, w)
    return (REG_SCALE_RANGE[0] <= sx <= REG_SCALE_RANGE[1]
            and REG_SCALE_RANGE[0] <= abs(sy) <= REG_SCALE_RANGE[1]
            and sy > 0
            and abs(sh) / sx <= REG_MAX_SHEAR
            and abs(matrix[0, 2]) < max_shift and abs(matrix[1, 2]) < max_shift)


def _apply_affine(img: np.ndarray, matrix: np.ndarray, border: str = "white") -> np.ndarray:
    h, w = img.shape[:2]
    if border == "replicate":  # photos: extend edge pixels instead of white
        return cv2.warpAffine(img, matrix, (w, h), flags=cv2.INTER_LINEAR,
                              borderMode=cv2.BORDER_REPLICATE)
    return cv2.warpAffine(img, matrix, (w, h), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=BG)


def _content_kept(last: np.ndarray, warped: np.ndarray) -> float:
    """Share of END's content that is still on canvas after warping."""
    before = int(_content_mask(last).sum())
    if before == 0:
        return 1.0
    return int(_content_mask(warped).sum()) / before


def _orb_candidates(first_gray: np.ndarray, last_gray: np.ndarray,
                    shape: Tuple[int, int]) -> List[Tuple[str, np.ndarray]]:
    """Coarse end->start similarity + full-affine from sparse features."""
    orb = cv2.ORB_create(nfeatures=3000, fastThreshold=12)
    k1, d1 = orb.detectAndCompute(first_gray, None)
    k2, d2 = orb.detectAndCompute(last_gray, None)
    if d1 is None or d2 is None or len(k1) < 12 or len(k2) < 12:
        return []
    matches = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(d2, d1)
    if len(matches) < 12:
        return []
    matches = sorted(matches, key=lambda m: m.distance)[:300]
    src = np.float32([k2[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst = np.float32([k1[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    out: List[Tuple[str, np.ndarray]] = []
    sim, sim_in = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC,
                                              ransacReprojThreshold=4.0)
    if sim is not None and sim_in is not None and int(sim_in.sum()) >= 10 \
            and _decompose_ok(sim, shape):
        out.append(("orb-sim", sim))
    aff, aff_in = cv2.estimateAffine2D(src, dst, method=cv2.RANSAC,
                                       ransacReprojThreshold=4.0)
    if aff is not None and aff_in is not None and int(aff_in.sum()) >= 12 \
            and _decompose_ok(aff, shape):
        out.append(("orb-aff", aff))
    return out


def _flow_refinements(first_gray: np.ndarray, warped_gray: np.ndarray,
                      content: np.ndarray, shape: Tuple[int, int],
                      flow_engine) -> List[Tuple[str, np.ndarray]]:
    """Residual similarity/affine fitted on the dense flow start->warped-end.

    Every static pixel votes for the leftover global drift; the moving limb is
    a RANSAC outlier. Far denser than ORB on these smoothly-shaded drawings.
    """
    flow = flow_engine.calc(first_gray, warped_gray, None)
    ys, xs = np.where(content)
    if len(xs) < 400:
        return []
    step = max(1, len(xs) // 4000)
    xs, ys = xs[::step], ys[::step]
    src = np.float32(np.stack([xs, ys], axis=1)).reshape(-1, 1, 2)
    dst = src + np.float32(flow[ys, xs]).reshape(-1, 1, 2)
    # dst = where start-content sits in the warped end; we need the transform
    # taking the end geometry back onto start, i.e. dst -> src.
    out: List[Tuple[str, np.ndarray]] = []
    sim, sim_in = cv2.estimateAffinePartial2D(dst, src, method=cv2.RANSAC,
                                              ransacReprojThreshold=1.8)
    if sim is not None and sim_in is not None and int(sim_in.sum()) >= 0.25 * len(src) \
            and _decompose_ok(sim, shape):
        out.append(("flow-sim", sim))
    aff, aff_in = cv2.estimateAffine2D(dst, src, method=cv2.RANSAC,
                                       ransacReprojThreshold=1.8)
    if aff is not None and aff_in is not None and int(aff_in.sum()) >= 0.25 * len(src) \
            and _decompose_ok(aff, shape):
        out.append(("flow-aff", aff))
    return out


def _compose(m2: np.ndarray, m1: np.ndarray) -> np.ndarray:
    """Affine composition m2∘m1 for 2x3 matrices."""
    a1 = np.vstack([m1, [0, 0, 1]])
    a2 = np.vstack([m2, [0, 0, 1]])
    return np.float32((a2 @ a1)[:2])


def register_end_to_start(first: np.ndarray, last: np.ndarray,
                          border: str = "white") -> Tuple[np.ndarray, dict]:
    """Warp END onto START's geometry; return (registered_end, info).

    Candidates: identity, ORB similarity/affine, then dense-flow refinements of
    the running best. The winner is whichever makes END's edges overlap START's
    best while keeping all content on canvas — never worse than doing nothing.
    `border` picks the fill for revealed margins: white for drawings,
    "replicate" for photographs.
    """
    h, w = first.shape[:2]
    shape = (h, w)
    fg = cv2.cvtColor(first, cv2.COLOR_RGB2GRAY)
    lg = cv2.cvtColor(last, cv2.COLOR_RGB2GRAY)

    flow_engine = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    flow_engine.setFinestScale(1)
    flow_engine.setGradientDescentIterations(40)
    flow_engine.setVariationalRefinementIterations(10)

    identity = np.float32([[1, 0, 0], [0, 1, 0]])
    identity_score = _edge_alignment(fg, lg)
    best = (identity_score, "identity", identity, last)

    def consider(name: str, matrix: np.ndarray) -> None:
        nonlocal best
        warped = _apply_affine(last, matrix, border)
        if border == "white" and _content_kept(last, warped) < REG_MIN_KEPT:
            return
        score = _edge_alignment(fg, cv2.cvtColor(warped, cv2.COLOR_RGB2GRAY))
        if score > best[0]:
            best = (score, name, matrix, warped)

    for name, matrix in _orb_candidates(fg, lg, shape):
        consider(name, matrix)

    # Dense-flow refinement of the current winner (captures sub-ORB drift and
    # anisotropic redraw like a bar drawn taller/narrower).
    for _ in range(2):
        prev_name = best[1]
        content = _content_mask(first) | _content_mask(best[3])
        wg = cv2.cvtColor(best[3], cv2.COLOR_RGB2GRAY)
        for name, matrix in _flow_refinements(fg, wg, content, shape, flow_engine):
            consider(f"{prev_name}+{name}", _compose(matrix, best[2]))
        if best[1] == prev_name:
            break

    # Prefer identity when it is essentially as good — don't move a frame that
    # already lines up (guards against locking onto a rigidly-moving body).
    if best[1] != "identity" and identity_score >= best[0] - 0.01:
        best = (identity_score, "identity", identity, last)

    info = {"reg": best[1], "edge_align": round(best[0], 4),
            "edge_align_identity": round(identity_score, 4)}
    return best[3], info


# --------------------------------------------------------------------------- #
# Motion analysis on the registered, normalized pair
# --------------------------------------------------------------------------- #

def _moving_mask(first: np.ndarray, last: np.ndarray, forward: np.ndarray,
                 backward: np.ndarray) -> Tuple[Optional[np.ndarray], dict]:
    """Soft [0,1] mask of everything that genuinely travels, plus stats.

    Components are kept by MEAN travel, not by area: a moving dumbbell is a
    small blob with a high mean and must stay; a slightly-redrawn machine is a
    big blob with a low mean and must go. Returns (None, stats) when the poses
    barely differ. stats["static_resid"] is the median flow left on content
    OUTSIDE the mask — the direct predictor of gear wobble under warping.
    """
    mag = np.maximum(np.linalg.norm(forward, axis=2), np.linalg.norm(backward, axis=2))
    content = _content_mask(first) | _content_mask(last)
    stats = {"peak_flow": 0.0, "mask_frac": 0.0, "static_resid": 0.0}
    if not content.any():
        return None, stats
    peak = float(np.percentile(mag[content], 99.0))
    stats["peak_flow"] = round(peak, 2)
    if peak < STATIC_MAX_FLOW:
        return None, stats

    thresh = max(MASK_MIN_FLOW, peak * MASK_REL_FLOW)
    binary = ((mag > thresh) & content).astype(np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), 1)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8), 1)

    num, labels, cstats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)
    if num <= 1:
        return None, stats
    means = np.zeros(num, dtype=np.float64)
    for idx in range(1, num):
        if cstats[idx, cv2.CC_STAT_AREA] >= COMP_MIN_AREA:
            means[idx] = float(mag[labels == idx].mean())
    best_mean = means.max()
    if best_mean <= 0:
        return None, stats
    keep = np.where(means >= max(MASK_MIN_FLOW, best_mean * COMP_MEAN_KEEP))[0]
    binary = np.isin(labels, keep).astype(np.uint8)

    stats["mask_frac"] = round(float(binary.sum()) / max(1, int(content.sum())), 3)
    static = content & (binary == 0)
    if static.any():
        stats["static_resid"] = round(float(np.median(mag[static])), 2)

    # Solid core, thin feathered edge: the core must stay fully opaque across
    # the whole swept corridor or the base frame ghosts through mid-transition.
    binary = cv2.dilate(binary, np.ones((MASK_DILATE, MASK_DILATE), np.uint8), 1)
    soft = cv2.GaussianBlur(binary.astype(np.float32), (0, 0), MASK_FEATHER)
    soft = np.clip((soft - 0.5) / 0.4 + 0.5, 0.0, 1.0)
    return soft, stats


def _warp(image: np.ndarray, flow: np.ndarray, factor: float) -> np.ndarray:
    h, w = flow.shape[:2]
    gx, gy = np.meshgrid(np.arange(w), np.arange(h))
    map_x = (gx + flow[..., 0] * factor).astype(np.float32)
    map_y = (gy + flow[..., 1] * factor).astype(np.float32)
    return cv2.remap(image, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def _flip_frames(first: np.ndarray, last: np.ndarray) -> Tuple[List[Image.Image], List[int]]:
    """Two clean poses, no in-betweens. Nothing can smear, ghost, or drift."""
    return ([Image.fromarray(first), Image.fromarray(last)], list(FLIP_DURATIONS))


def _pulse_frames(first: np.ndarray) -> Tuple[List[Image.Image], List[int]]:
    """Poses are pixel-identical (isometric hold drawn twice): emphasize the
    highlighted muscle slightly so the loop is alive but nothing 'moves'."""
    rgb = first.astype(np.float32)
    red = (rgb[..., 0] - np.maximum(rgb[..., 1], rgb[..., 2])) > 24
    pulsed = rgb.copy()
    pulsed[red] = np.clip(rgb[red] * np.float32([1.0, 0.82, 0.82]), 0, 255)
    return ([Image.fromarray(first), Image.fromarray(pulsed.astype(np.uint8))],
            list(FLIP_DURATIONS))


def interpolate_frames(start: Image.Image, end: Image.Image,
                       collect: Optional[dict] = None,
                       reg_info: Optional[dict] = None) -> Tuple[List[Image.Image], List[int]]:
    """Build the loop from a *registered*, normalized pair."""
    info: dict = dict(reg_info or {})
    first = np.array(start.convert("RGB"))
    last = np.array(end.convert("RGB"))

    flow_engine = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    flow_engine.setFinestScale(1)
    flow_engine.setGradientDescentIterations(40)
    flow_engine.setVariationalRefinementIterations(10)
    fg = cv2.cvtColor(first, cv2.COLOR_RGB2GRAY)
    lg = cv2.cvtColor(last, cv2.COLOR_RGB2GRAY)
    forward = flow_engine.calc(fg, lg, None)
    backward = flow_engine.calc(lg, fg, None)

    mask, stats = _moving_mask(first, last, forward, backward)
    info.update(stats)

    def done(frames, durations, mode):
        info["mode"] = mode
        if collect is not None:
            collect.update(info)
        return frames, durations

    if mask is None:
        if np.array_equal(first, last):
            return done(*_pulse_frames(first), "pulse")
        # Registered poses barely differ geometrically (colour shift, or a
        # sub-threshold nudge): alternate the two real drawings.
        return done(*_flip_frames(first, last), "flip-static")

    aligned = (info.get("edge_align", 1.0) >= WARP_MIN_EDGE_ALIGN
               and stats["static_resid"] <= WARP_MAX_STATIC_RESID
               and stats["peak_flow"] <= FLIP_PEAK_FLOW)
    if not aligned:
        # The leftover "motion" includes a whole-scene redraw (or is untrackably
        # large) — warping would wobble or melt the gear. Show two honest poses.
        return done(*_flip_frames(first, last), "flip")

    # Warp mode. First half rides on the pure START frame, second half on the
    # pure registered END frame, so both holds are the artist's real drawings
    # and every prop lands where it belongs. Each in-between repaints only the
    # moving mask, warped from the SINGLE nearer pose (never a blend).
    mask3 = mask[..., None]
    schedule = ([(0.0, HOLD_MS)] + [(t, TRANSITION_MS) for t in TRANSITIONS]
                + [(1.0, HOLD_MS)] + [(t, TRANSITION_MS) for t in reversed(TRANSITIONS)])
    frames: List[Image.Image] = []
    durations: List[int] = []
    for t, dur in schedule:
        if t == 0.0:
            frames.append(Image.fromarray(first))
        elif t == 1.0:
            frames.append(Image.fromarray(last))
        else:
            eased = 0.5 - 0.5 * math.cos(math.pi * t)
            if eased <= 0.5:
                base = first.astype(np.float32)
                moving = _warp(first, forward, -eased).astype(np.float32)
            else:
                base = last.astype(np.float32)
                moving = _warp(last, backward, -(1 - eased)).astype(np.float32)
            frame = base * (1 - mask3) + moving * mask3
            frames.append(Image.fromarray(frame.clip(0, 255).astype(np.uint8)))
        durations.append(dur)
    return done(frames, durations, "warp")


WEBP_QUALITY = 80


def save_gif(frames: List[Image.Image], durations: List[int], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    palette = frames[0].quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    indexed = [palette] + [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames[1:]]
    indexed[0].save(out, format="GIF", save_all=True, append_images=indexed[1:],
                    duration=durations, loop=0, optimize=True, disposal=2)


def save_webp(frames: List[Image.Image], durations: List[int], out: Path,
              quality: int = WEBP_QUALITY) -> None:
    # Animated WebP: ~4x smaller than palette GIF at higher (true-color) quality.
    # Decoded natively by Android's ImageDecoder (API 28+).
    out.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(out, format="WEBP", save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, quality=quality, method=4)


REG_PAD = 44  # working-space margin: room for registration shifts, no clipping


def _common_canvas(start: Image.Image, end: Image.Image) -> Tuple[Image.Image, Image.Image]:
    """Both frames on an identical canvas so shared-box cropping is valid."""
    if start.size == end.size:
        return start.convert("RGB"), end.convert("RGB")
    w = max(start.width, end.width)
    h = max(start.height, end.height)

    def place(img: Image.Image) -> Image.Image:
        canvas = Image.new("RGB", (w, h), BG)
        canvas.paste(img.convert("RGB"), ((w - img.width) // 2, (h - img.height) // 2))
        return canvas

    return place(start), place(end)


def animate(start: Image.Image, end: Image.Image, out: Path,
            also: Optional[List[Path]] = None) -> dict:
    """Render one animation to `out` (and optional extra encodings). Returns
    a metrics dict: mode, registration choice/score, flow stats."""
    start, end = _common_canvas(start, end)
    # Working space: full 480 resolution with a wide margin, so features are
    # dense enough for ORB and a registration shift can never clip content.
    ws, we = normalize_pair(start, end, pad=REG_PAD)
    first_w = np.array(ws)
    registered_w, reg_info = register_end_to_start(first_w, np.array(we))
    # Final framing: re-crop the *registered* pair to the standard margin.
    ns, ne = normalize_pair(Image.fromarray(first_w), Image.fromarray(registered_w), pad=PAD)
    collect: dict = {}
    frames, durations = interpolate_frames(ns, ne, collect, reg_info)
    for target in [out] + list(also or []):
        if target.suffix.lower() == ".gif":
            save_gif(frames, durations, target)
        else:
            save_webp(frames, durations, target)
    return collect


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def _resolve_frames(entry: dict, roots: dict) -> Tuple[Image.Image, Image.Image]:
    if "sheet" in entry:
        return sheet_pair(roots["sheets"] / entry["sheet"], int(entry["row"]),
                          entry.get("cols", 2), entry.get("rows", 3))
    start = Image.open(roots["frames"] / entry["start"])
    end = Image.open(roots["frames"] / entry["end"])
    return start, end


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="mode", required=True)

    p = sub.add_parser("pair", help="animate one start/end file pair")
    p.add_argument("start", type=Path)
    p.add_argument("end", type=Path)
    p.add_argument("out", type=Path)

    s = sub.add_parser("sheet", help="animate one row of a start|end sheet")
    s.add_argument("sheet", type=Path)
    s.add_argument("row", type=int)
    s.add_argument("out", type=Path)

    m = sub.add_parser("manifest", help="batch-animate from a JSON manifest")
    m.add_argument("manifest", type=Path)
    m.add_argument("--frames-root", type=Path, default=Path("."))
    m.add_argument("--sheets-root", type=Path, default=Path("assets/motion_sheets"))
    m.add_argument("--output-dir", type=Path, required=True)

    args = ap.parse_args()
    if args.mode == "pair":
        info = animate(Image.open(args.start), Image.open(args.end), args.out)
        print(f"wrote {args.out}  {info}")
    elif args.mode == "sheet":
        info = animate(*sheet_pair(args.sheet, args.row), args.out)
        print(f"wrote {args.out}  {info}")
    else:
        roots = {"frames": args.frames_root, "sheets": args.sheets_root}
        entries = json.loads(args.manifest.read_text(encoding="utf-8"))
        for entry in entries:
            start, end = _resolve_frames(entry, roots)
            out = args.output_dir / f"{entry['out']}.gif"
            info = animate(start, end, out)
            print(f"wrote {out.name}  mode={info.get('mode')}")
        print(f"done: {len(entries)} GIFs")


if __name__ == "__main__":
    main()
