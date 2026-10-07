#!/usr/bin/env python3
"""Generate deterministic articulated exercise GIFs for rows without licensed motion frames.

Style contract: white background, light "mannequin" figure with red target-muscle
tinting and slate equipment, matching the look of the app's photographic and
anatomical motion GIFs. Poses are authored as joint angles on a fixed-length
skeleton; frames interpolate angles (never raw pixels or XY joints), so limbs
keep their length and motion follows natural arcs. Wrists can be pinned to
fixed bars (pull-up bar, dip bars) through a two-bone IK solve.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw

SIZE = 480
FLOOR_Y = 442.0
CENTER_X = 240.0

BG = (255, 255, 255)
OUTLINE = (76, 70, 66)
BODY = (238, 233, 226)
BODY_FAR = (216, 209, 200)
RED = (211, 68, 53)
RED_FAR = (172, 55, 43)
HAIR = (62, 56, 53)
SHOE = (88, 82, 78)
SHOE_FAR = (72, 67, 63)
IRON = (84, 88, 94)
IRON_DARK = (58, 62, 68)
PAD = (108, 112, 118)
BAND = (47, 137, 106)
SHADOW = (233, 231, 228)
FLOOR_LINE = (224, 221, 217)

FRAME_COUNT = 16
FRAME_MS = 120

# Skeleton bone lengths (px).
TORSO = 112.0
NECK = 12.0
HEAD_R = 21.0
UA = 60.0
FA = 56.0
TH = 84.0
SH = 80.0
FOOT = 24.0

SHOULDER_W = 66.0  # front view
HIP_W = 44.0       # front view

Point = tuple[float, float]


# --------------------------------------------------------------------------- #
# Math helpers
# --------------------------------------------------------------------------- #

def rad(deg: float) -> float:
    return math.radians(deg)


def down_dir(deg: float, facing: float = 1.0) -> Point:
    """Unit vector for a limb angle: 0 = straight down, +90 = forward (facing)."""
    return (facing * math.sin(rad(deg)), math.cos(rad(deg)))


def up_dir(deg: float, facing: float = 1.0) -> Point:
    """Unit vector for the torso: 0 = straight up, +90 = forward (facing)."""
    return (facing * math.sin(rad(deg)), -math.cos(rad(deg)))


def add(p: Point, d: Point, length: float) -> Point:
    return (p[0] + d[0] * length, p[1] + d[1] * length)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def lerp_pt(a: Point, b: Point, t: float) -> Point:
    return (lerp(a[0], b[0], t), lerp(a[1], b[1], t))


def two_bone_ik(root: Point, target: Point, l1: float, l2: float,
                bend: float) -> tuple[Point, Point]:
    """(middle joint, clamped end) for a two-bone chain; bend=+1/-1 picks a side."""
    dx, dy = target[0] - root[0], target[1] - root[1]
    dist = max(1e-5, math.hypot(dx, dy))
    reach = min(max(dist, abs(l1 - l2) + 1e-4), l1 + l2 - 1e-4)
    scale = reach / dist
    dx, dy = dx * scale, dy * scale
    end = (root[0] + dx, root[1] + dy)
    a = (l1 * l1 - l2 * l2 + reach * reach) / (2 * reach)
    h = math.sqrt(max(0.0, l1 * l1 - a * a))
    mx, my = root[0] + dx * (a / reach), root[1] + dy * (a / reach)
    return (mx - bend * dy * (h / reach), my + bend * dx * (h / reach)), end


# --------------------------------------------------------------------------- #
# Pose model
# --------------------------------------------------------------------------- #

SIDE_DEFAULTS = {
    "torso": 0.0, "head": 0.0,
    "ua_n": 4.0, "fa_n": 6.0, "ua_f": 4.0, "fa_f": 6.0,
    "th_n": 0.0, "sh_n": 0.0, "th_f": 0.0, "sh_f": 0.0,
    "ft_n": 90.0, "ft_f": 90.0,
    "rootx": None, "rooty": None,   # explicit hip point; None => auto-grounded
    "rotate": 0.0,                  # whole-figure rotation about the hip (deg)
    "shiftx": 0.0, "shifty": 0.0,   # post-rotation translation
}

FRONT_DEFAULTS = {
    "lean": 0.0, "head": 0.0,
    "ua_l": 8.0, "fa_l": 4.0, "ua_r": 8.0, "fa_r": 4.0,
    "th_l": 7.0, "sh_l": -7.0, "th_r": 7.0, "sh_r": -7.0,
    "drop": 0.0,    # vertical hip drop with feet pinned via IK (squat family)
    "rise": 0.0,    # airborne hip lift, legs keep their authored angles
    "stance": 1.0,  # stance width multiplier
}


def make_pose(view: str, **kwargs) -> dict:
    base = dict(SIDE_DEFAULTS if view == "side" else FRONT_DEFAULTS)
    base["view"] = view
    for key, value in kwargs.items():
        if key not in base:
            raise KeyError(f"unknown pose key {key!r} for view {view}")
        base[key] = value
    return base


def interpolate_pose(a: dict, b: dict, t: float) -> dict:
    out = {}
    for key, va in a.items():
        vb = b[key]
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            out[key] = lerp(float(va), float(vb), t)
        elif va is None and vb is None:
            out[key] = None
        else:
            out[key] = va if t < 0.5 else vb
    return out


def solve_side(pose: dict, facing: float) -> dict[str, Point]:
    """Forward kinematics for the side view. Returns joint name -> point."""
    root = (pose["rootx"] if pose["rootx"] is not None else CENTER_X,
            pose["rooty"] if pose["rooty"] is not None else FLOOR_Y - (TH + SH))
    explicit = pose["rootx"] is not None or pose["rooty"] is not None
    hip = root
    j: dict[str, Point] = {"hip": hip}
    j["chest"] = add(hip, up_dir(pose["torso"], facing), TORSO)
    j["neck"] = add(j["chest"], up_dir(pose["torso"] + pose["head"], facing), NECK)
    j["head"] = add(j["neck"], up_dir(pose["torso"] + pose["head"], facing), HEAD_R)
    for side in ("n", "f"):
        j[f"elbow_{side}"] = add(j["chest"], down_dir(pose[f"ua_{side}"], facing), UA)
        j[f"wrist_{side}"] = add(j[f"elbow_{side}"], down_dir(pose[f"fa_{side}"], facing), FA)
        j[f"knee_{side}"] = add(hip, down_dir(pose[f"th_{side}"], facing), TH)
        j[f"ankle_{side}"] = add(j[f"knee_{side}"], down_dir(pose[f"sh_{side}"], facing), SH)
        j[f"toe_{side}"] = add(j[f"ankle_{side}"], down_dir(pose[f"ft_{side}"], facing), FOOT)

    theta = rad(pose["rotate"]) * facing
    if theta:
        cos_t, sin_t = math.cos(theta), math.sin(theta)
        for key, (x, y) in j.items():
            ox, oy = x - hip[0], y - hip[1]
            j[key] = (hip[0] + ox * cos_t - oy * sin_t, hip[1] + ox * sin_t + oy * cos_t)
    dx, dy = pose["shiftx"] * facing, pose["shifty"]
    if dx or dy:
        j = {key: (x + dx, y + dy) for key, (x, y) in j.items()}

    if not explicit and not theta:
        # Ground the stance: lowest foot contact sits on the floor line.
        low = max(j["toe_n"][1], j["toe_f"][1], j["ankle_n"][1] + 6, j["ankle_f"][1] + 6)
        j = {key: (x, y + FLOOR_Y - low) for key, (x, y) in j.items()}
    return j


def solve_front(pose: dict) -> dict[str, Point]:
    stance = pose["stance"]
    hip_c = (CENTER_X, FLOOR_Y - (TH + SH) * 0.985 + pose["drop"] - pose["rise"])
    j: dict[str, Point] = {"hip": hip_c}
    lean = pose["lean"]
    j["chest"] = add(hip_c, up_dir(lean), TORSO)
    j["neck"] = add(j["chest"], up_dir(lean + pose["head"]), NECK)
    j["head"] = add(j["neck"], up_dir(lean + pose["head"]), HEAD_R)
    for side, sgn in (("l", -1.0), ("r", 1.0)):
        shoulder = add(j["chest"], (sgn * math.cos(rad(lean)), sgn * math.sin(rad(lean))), SHOULDER_W / 2)
        hip_pt = (hip_c[0] + sgn * HIP_W / 2, hip_c[1])
        j[f"shoulder_{side}"] = shoulder
        j[f"hipp_{side}"] = hip_pt
        j[f"elbow_{side}"] = add(shoulder, down_dir(pose[f"ua_{side}"], sgn), UA)
        j[f"wrist_{side}"] = add(j[f"elbow_{side}"], down_dir(pose[f"fa_{side}"], sgn), FA)
        if pose["drop"] > 0.0 and pose["rise"] == 0.0:
            ankle = (hip_c[0] + sgn * (HIP_W / 2 + 34.0 * stance), FLOOR_Y - 8.0)
            knee, ankle = two_bone_ik(hip_pt, ankle, TH, SH, -sgn)
            j[f"knee_{side}"], j[f"ankle_{side}"] = knee, ankle
        else:
            j[f"knee_{side}"] = add(hip_pt, down_dir(pose[f"th_{side}"] * stance, sgn), TH)
            j[f"ankle_{side}"] = add(j[f"knee_{side}"], down_dir(pose[f"sh_{side}"] * stance, sgn), SH)
        ax, ay = j[f"ankle_{side}"]
        j[f"toe_{side}"] = (ax + sgn * 10.0, ay + 12.0)
    if pose["drop"] == 0.0 and pose["rise"] == 0.0:
        low = max(j["ankle_l"][1], j["ankle_r"][1]) + 14.0
        j = {key: (x, y + FLOOR_Y - low) for key, (x, y) in j.items()}
    return j


def pin_wrists(j: dict[str, Point], targets: dict[str, Point], view: str) -> None:
    """Re-solve elbows so wrists land exactly on fixed world points."""
    if view == "front":
        pairs = (("shoulder_l", "elbow_l", "wrist_l", -1.0), ("shoulder_r", "elbow_r", "wrist_r", 1.0))
    else:
        pairs = (("chest", "elbow_n", "wrist_n", 1.0), ("chest", "elbow_f", "wrist_f", 1.0))
    for shoulder_key, elbow_key, wrist_key, sgn in pairs:
        target = targets.get(wrist_key)
        if target is None:
            continue
        elbow, wrist = two_bone_ik(j[shoulder_key], target, UA, FA, sgn)
        j[elbow_key], j[wrist_key] = elbow, wrist


# --------------------------------------------------------------------------- #
# Drawing
# --------------------------------------------------------------------------- #

def capsule(draw: ImageDraw.ImageDraw, pts: list[Point], width: int,
            fill: tuple[int, int, int], outline: tuple[int, int, int] | None = OUTLINE,
            ow: int = 3) -> None:
    flat = [(float(x), float(y)) for x, y in pts]
    if outline is not None:
        w = width + 2 * ow
        draw.line(flat, fill=outline, width=w, joint="curve")
        for p in (flat[0], flat[-1]):
            r = w / 2
            draw.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=outline)
    draw.line(flat, fill=fill, width=width, joint="curve")
    for p in (flat[0], flat[-1]):
        r = width / 2
        draw.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=fill)


def disc(draw: ImageDraw.ImageDraw, center: Point, r: float, fill, outline=None, ow: int = 3) -> None:
    x, y = center
    if outline is not None:
        draw.ellipse((x - r - ow, y - r - ow, x + r + ow, y + r + ow), fill=outline)
    draw.ellipse((x - r, y - r, x + r, y + r), fill=fill)


class Highlight:
    """Which body parts get the red target tint."""

    def __init__(self, category: str, target: str):
        text = f"{category} {target}".lower()
        self.upper_arm = any(k in text for k in ("biceps", "triceps", "upper arms"))
        self.forearm = any(k in text for k in ("forearms", "lower arms", "wrist"))
        self.shoulder = "delts" in text or "shoulders" in text
        self.chest = any(k in text for k in ("pectorals", "chest", "serratus"))
        self.back = any(k in text for k in ("lats", "upper back", "back"))
        self.traps = "traps" in text or "levator" in text or "neck" in text
        self.abs = "abs" in text or "waist" in text or "spine" in text
        self.glutes = "glutes" in text
        self.thigh = any(k in text for k in ("quads", "hamstrings", "adductors", "abductors", "upper legs"))
        self.calf = "calves" in text or "lower legs" in text

    def arm_color(self, far: bool, part: str) -> tuple[int, int, int]:
        hot = self.upper_arm if part == "ua" else self.forearm
        if hot:
            return RED_FAR if far else RED
        return BODY_FAR if far else BODY

    def leg_color(self, far: bool, part: str) -> tuple[int, int, int]:
        hot = self.thigh if part == "th" else self.calf
        if hot:
            return RED_FAR if far else RED
        return BODY_FAR if far else BODY


def torso_axis(j: dict[str, Point], t0: float, t1: float) -> list[Point]:
    return [lerp_pt(j["hip"], j["chest"], t0), lerp_pt(j["hip"], j["chest"], t1)]


def draw_torso_side(draw: ImageDraw.ImageDraw, j: dict[str, Point], hl: Highlight) -> None:
    capsule(draw, [j["hip"], lerp_pt(j["hip"], j["chest"], 0.55), j["chest"]], 44, BODY)
    if hl.glutes:
        capsule(draw, torso_axis(j, 0.0, 0.1), 40, RED, outline=None)
    if hl.abs:
        capsule(draw, torso_axis(j, 0.16, 0.62), 34, RED, outline=None)
    if hl.chest or hl.back:
        capsule(draw, torso_axis(j, 0.55, 0.95), 38, RED, outline=None)
    if hl.traps:
        capsule(draw, torso_axis(j, 0.86, 1.0), 40, RED, outline=None)


def draw_head(draw: ImageDraw.ImageDraw, head: Point, mode: str) -> None:
    x, y = head
    disc(draw, head, HEAD_R, BODY, OUTLINE)
    box = (x - HEAD_R + 2, y - HEAD_R + 2, x + HEAD_R - 2, y + HEAD_R - 2)
    if mode == "front":
        draw.pieslice(box, 185, 355, fill=HAIR)
    elif mode == "left":
        draw.pieslice(box, 200, 25, fill=HAIR)
    else:
        draw.pieslice(box, 155, 340, fill=HAIR)


def draw_foot(draw: ImageDraw.ImageDraw, ankle: Point, toe: Point, far: bool) -> None:
    capsule(draw, [ankle, toe], 14, SHOE_FAR if far else SHOE)


def draw_limb(draw: ImageDraw.ImageDraw, a: Point, b: Point, c: Point,
              w_upper: int, w_lower: int, col_upper, col_lower) -> None:
    """Two-segment limb: shared outline, per-segment fill, clean joint."""
    flat = [(float(x), float(y)) for x, y in (a, b, c)]
    ow = 3
    w = w_upper + 2 * ow
    draw.line(flat, fill=OUTLINE, width=w, joint="curve")
    for p in (flat[0], flat[-1]):
        r = w / 2
        draw.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=OUTLINE)
    capsule(draw, [a, b], w_upper, col_upper, outline=None)
    capsule(draw, [b, c], w_lower, col_lower, outline=None)


def render_side(j: dict[str, Point], hl: Highlight, facing: float,
                equipment_layers, draw: ImageDraw.ImageDraw) -> None:
    equipment_layers("behind", draw, j)
    # far limbs
    draw_limb(draw, j["hip"], j["knee_f"], j["ankle_f"], 24, 19,
              hl.leg_color(True, "th"), hl.leg_color(True, "sh"))
    draw_foot(draw, j["ankle_f"], j["toe_f"], True)
    draw_limb(draw, j["chest"], j["elbow_f"], j["wrist_f"], 19, 15,
              hl.arm_color(True, "ua"), hl.arm_color(True, "fa"))
    equipment_layers("hand_far", draw, j)
    # torso, neck, head
    draw_torso_side(draw, j, hl)
    capsule(draw, [j["chest"], j["neck"]], 15, RED if hl.traps else BODY)
    draw_head(draw, j["head"], "right" if facing >= 0 else "left")
    if hl.shoulder:
        disc(draw, j["chest"], 15, RED, OUTLINE)
    # near limbs
    draw_limb(draw, j["hip"], j["knee_n"], j["ankle_n"], 26, 20,
              hl.leg_color(False, "th"), hl.leg_color(False, "sh"))
    draw_foot(draw, j["ankle_n"], j["toe_n"], False)
    draw_limb(draw, j["chest"], j["elbow_n"], j["wrist_n"], 20, 16,
              hl.arm_color(False, "ua"), hl.arm_color(False, "fa"))
    equipment_layers("front", draw, j)


def render_front(j: dict[str, Point], hl: Highlight, equipment_layers,
                 draw: ImageDraw.ImageDraw) -> None:
    equipment_layers("behind", draw, j)
    for side in ("l", "r"):
        draw_limb(draw, j[f"hipp_{side}"], j[f"knee_{side}"], j[f"ankle_{side}"], 24, 19,
                  hl.leg_color(False, "th"), hl.leg_color(False, "sh"))
        capsule(draw, [j[f"ankle_{side}"], j[f"toe_{side}"]], 14, SHOE)
    # torso
    ls, rs = j["shoulder_l"], j["shoulder_r"]
    lh, rh = j["hipp_l"], j["hipp_r"]
    draw.polygon([ls, rs, rh, lh], fill=BODY, outline=None)
    capsule(draw, [ls, rs], 30, BODY)
    capsule(draw, [lh, rh], 30, BODY)
    draw.line([ls, lh], fill=OUTLINE, width=3)
    draw.line([rs, rh], fill=OUTLINE, width=3)
    if hl.chest:
        disc(draw, lerp_pt(lerp_pt(ls, rs, 0.32), lerp_pt(lh, rh, 0.32), 0.16), 13, RED)
        disc(draw, lerp_pt(lerp_pt(ls, rs, 0.68), lerp_pt(lh, rh, 0.68), 0.16), 13, RED)
    if hl.abs:
        capsule(draw, [lerp_pt(lerp_pt(ls, rs, 0.5), lerp_pt(lh, rh, 0.5), 0.38),
                       lerp_pt(lerp_pt(ls, rs, 0.5), lerp_pt(lh, rh, 0.5), 0.9)], 26, RED, outline=None)
    if hl.back or hl.traps:
        capsule(draw, [lerp_pt(ls, rs, 0.28), lerp_pt(ls, rs, 0.72)], 24, RED, outline=None)
    capsule(draw, [j["chest"], j["neck"]], 15, RED if hl.traps else BODY)
    draw_head(draw, j["head"], "front")
    if hl.shoulder:
        disc(draw, ls, 13, RED, OUTLINE)
        disc(draw, rs, 13, RED, OUTLINE)
    for side in ("l", "r"):
        draw_limb(draw, j[f"shoulder_{side}"], j[f"elbow_{side}"], j[f"wrist_{side}"], 19, 15,
                  hl.arm_color(False, "ua"), hl.arm_color(False, "fa"))
    equipment_layers("front", draw, j)


# --------------------------------------------------------------------------- #
# Equipment
# --------------------------------------------------------------------------- #

LEG_CABLE_TEMPLATES = ("leg_curl", "kickback", "abduction", "adduction", "leg_extension")


def hand_points(j: dict[str, Point], view: str) -> list[Point]:
    if view == "front":
        return [j["wrist_l"], j["wrist_r"]]
    return [j["wrist_n"], j["wrist_f"]]


def make_equipment(equipment: str, template: str, view: str, mirror: bool, anchors: dict):
    """anchors: static geometry captured from frame 0 (bar_y, dip bars, ...)."""
    key = equipment.lower()
    cable_like = any(k in key for k in ("cable", "rope smith", "rope"))
    band_like = "band" in key
    machine_like = any(k in key for k in ("machine", "leverage", "assisted", "smith"))

    def attach_points(j: dict[str, Point]) -> list[Point]:
        if template in LEG_CABLE_TEMPLATES:
            return [j["ankle_n"] if view == "side" else j["ankle_r"]]
        return hand_points(j, view)

    def layers(stage: str, draw: ImageDraw.ImageDraw, j: dict[str, Point]) -> None:
        wrists = hand_points(j, view)
        if stage == "behind":
            if template == "pullup":
                bar_y = anchors["bar_y"]
                draw.line((70, bar_y, 410, bar_y), fill=IRON_DARK, width=10)
                draw.line((84, bar_y, 84, bar_y - 38), fill=IRON, width=8)
                draw.line((396, bar_y, 396, bar_y - 38), fill=IRON, width=8)
            if template == "dip":
                for x, y in anchors["dip_bars"]:
                    draw.line((x - 44, y, x + 44, y), fill=IRON_DARK, width=9)
                    draw.line((x, y, x, FLOOR_Y), fill=IRON, width=7)
            if cable_like or (machine_like and template in ("pulldown", "triceps", "row")):
                anchor = anchors["cable_anchor"]
                disc(draw, anchor, 8, IRON, IRON_DARK, 2)
                for p in attach_points(j):
                    draw.line((anchor, p), fill=IRON_DARK, width=4)
            elif band_like:
                anchor = anchors["cable_anchor"]
                for p in attach_points(j):
                    draw.line((anchor, p), fill=BAND, width=5)
            if "ball" in key:
                disc(draw, anchors["ball"], 54, (226, 232, 228), (150, 160, 154), 4)
            if machine_like and view == "side" and template not in (
                    "leg_extension", "dip", "bike", "run"):
                x = anchors["machine_x"]
                draw.line((x, 150, x, FLOOR_Y), fill=IRON, width=10)
                draw.rounded_rectangle((x - 17, FLOOR_Y - 108, x + 17, FLOOR_Y - 14),
                                       radius=6, fill=IRON, outline=IRON_DARK, width=3)
        elif stage in ("hand_far", "front"):
            far = stage == "hand_far"
            if view == "front":
                targets = [] if far else wrists
            else:
                targets = [wrists[1]] if far else [wrists[0]]
            if "dumbbell" in key:
                for w in targets:
                    if view == "side":
                        disc(draw, w, 15, IRON, IRON_DARK, 3)
                        disc(draw, w, 5, IRON_DARK)
                    else:
                        draw.line((w[0] - 17, w[1], w[0] + 17, w[1]), fill=IRON_DARK, width=5)
                        for dx in (-15, 15):
                            draw.rounded_rectangle((w[0] + dx - 6, w[1] - 11, w[0] + dx + 6, w[1] + 11),
                                                   radius=4, fill=IRON, outline=IRON_DARK, width=2)
            elif "kettlebell" in key:
                for w in targets:
                    disc(draw, (w[0], w[1] + 20), 16, IRON, IRON_DARK, 3)
                    draw.arc((w[0] - 12, w[1] - 4, w[0] + 12, w[1] + 22), 180, 360,
                             fill=IRON_DARK, width=5)
            elif any(k in key for k in ("barbell", "olympic", "trap bar")) and not far:
                if view == "front":
                    y = (wrists[0][1] + wrists[1][1]) / 2
                    left = min(w[0] for w in wrists) - 52
                    right = max(w[0] for w in wrists) + 52
                    draw.line((left, y, right, y), fill=IRON_DARK, width=7)
                    for x in (left + 10, right - 10):
                        draw.rounded_rectangle((x - 8, y - 26, x + 8, y + 26), radius=5,
                                               fill=IRON, outline=IRON_DARK, width=2)
                else:
                    disc(draw, wrists[0], 26, IRON, IRON_DARK, 3)
                    disc(draw, wrists[0], 6, IRON_DARK)
            elif "weighted" in key and not far:
                for w in targets:
                    disc(draw, w, 13, IRON, IRON_DARK, 3)

    return layers


def equipment_anchors(template: str, equipment: str, view: str, mirror: bool,
                      first: dict[str, Point]) -> dict:
    """Static equipment geometry derived from the first frame's joints."""
    key = equipment.lower()
    anchors: dict = {}
    wrists = hand_points(first, view)
    if template == "pullup":
        anchors["bar_y"] = min(w[1] for w in wrists)
    if template == "dip":
        anchors["dip_bars"] = [(w[0], w[1]) for w in wrists]
    # Cable/band anchor: overhead for pull-downs, floor for most standing moves,
    # behind at hip height for leg cable work.
    if template in ("pulldown", "triceps", "pullover"):
        anchors["cable_anchor"] = (CENTER_X, 58) if view == "front" else (
            (392, 92) if not mirror else (88, 92))
    elif template in LEG_CABLE_TEMPLATES:
        anchors["cable_anchor"] = (66, FLOOR_Y - 60) if not mirror else (414, FLOOR_Y - 60)
    elif template in ("row", "fly", "rotation"):
        anchors["cable_anchor"] = (60, FLOOR_Y - 130) if not mirror else (420, FLOOR_Y - 130)
    else:
        if view == "front":
            feet_x = (first["ankle_l"][0] + first["ankle_r"][0]) / 2
        else:
            feet_x = (first["ankle_n"][0] + first["ankle_f"][0]) / 2
        anchors["cable_anchor"] = (feet_x, FLOOR_Y - 2)
    if "ball" in key:
        if template in ("row", "hinge", "crunch", "plank", "bridge"):
            anchors["ball"] = (CENTER_X, FLOOR_Y - 54)
        else:
            anchors["ball"] = ((122 if not mirror else 358), FLOOR_Y - 54)
    anchors["machine_x"] = 66 if not mirror else 414
    return anchors


# --------------------------------------------------------------------------- #
# Template pose library (side view unless noted)
# --------------------------------------------------------------------------- #

def S(**kw) -> dict:
    return make_pose("side", **kw)


def F(**kw) -> dict:
    return make_pose("front", **kw)


def supine(hipx: float = 232.0, hipy: float = 392.0, **kw) -> dict:
    """Lying on the back, head to the left: angles are pre-rotation (standing)."""
    return make_pose("side", rotate=-90.0, rootx=hipx, rooty=hipy, **kw)


def template_animation(template: str) -> dict:
    A = {"view": "side", "cycle": "pingpong", "floor": True, "shadow": True}

    if template == "curl":
        A["keyframes"] = [
            S(ua_n=-6, fa_n=8, ua_f=-6, fa_f=8),
            S(ua_n=-6, fa_n=138, ua_f=-6, fa_f=138),
        ]
    elif template == "wrist":
        A["keyframes"] = [
            S(ua_n=-4, fa_n=86, ua_f=-4, fa_f=86),
            S(ua_n=-4, fa_n=120, ua_f=-4, fa_f=120),
        ]
    elif template == "triceps":
        A["keyframes"] = [
            S(torso=6, ua_n=-10, fa_n=96, ua_f=-10, fa_f=96),
            S(torso=6, ua_n=-10, fa_n=6, ua_f=-10, fa_f=6),
        ]
    elif template == "row":
        A["keyframes"] = [
            S(torso=58, head=-30, th_n=-12, sh_n=6, th_f=-12, sh_f=6,
              ua_n=52, fa_n=66, ua_f=52, fa_f=66),
            S(torso=58, head=-30, th_n=-12, sh_n=6, th_f=-12, sh_f=6,
              ua_n=-24, fa_n=74, ua_f=-24, fa_f=74),
        ]
    elif template == "hinge":
        A["keyframes"] = [
            S(torso=4, ua_n=4, fa_n=4, ua_f=4, fa_f=4),
            S(torso=62, head=-34, th_n=-16, sh_n=8, th_f=-16, sh_f=8,
              ua_n=58, fa_n=62, ua_f=58, fa_f=62),
        ]
    elif template == "squat":
        A.update(view="front")
        A["keyframes"] = [
            F(ua_l=16, fa_l=118, ua_r=16, fa_r=118, drop=0.001),
            F(ua_l=16, fa_l=118, ua_r=16, fa_r=118, drop=62),
        ]
    elif template == "lunge":
        A["keyframes"] = [
            S(rootx=236, rooty=FLOOR_Y - 158, th_n=24, sh_n=-24, th_f=-20, sh_f=24, ft_f=78,
              ua_n=-4, fa_n=4, ua_f=6, fa_f=4),
            S(rootx=236, rooty=FLOOR_Y - 112, th_n=50, sh_n=-50, th_f=-24, sh_f=68, ft_f=58,
              ua_n=-4, fa_n=4, ua_f=6, fa_f=4),
        ]
    elif template == "calf_raise":
        A["keyframes"] = [
            S(),
            S(shifty=-18, ft_n=122, ft_f=122),
        ]
    elif template in ("pushup", "plank"):
        low = 40.0 if template == "pushup" else 6.0
        A["floor"] = False
        A["keyframes"] = [
            S(rotate=-84, rootx=196, rooty=330, th_n=4, sh_n=2, th_f=4, sh_f=2,
              ft_n=150, ft_f=150, ua_n=88, fa_n=92, ua_f=88, fa_f=92, head=24),
            S(rotate=-84, rootx=196, rooty=330 + low * 0.55, th_n=4, sh_n=2, th_f=4, sh_f=2,
              ft_n=150, ft_f=150, ua_n=88 + low, fa_n=92 - low * 0.2,
              ua_f=88 + low, fa_f=92 - low * 0.2, head=24),
        ]
    elif template == "pullup":
        A.update(view="front")
        A["floor"] = False
        A["pin"] = "bar"
        A["keyframes"] = [
            F(rise=-1, drop=0, ua_l=168, fa_l=176, ua_r=168, fa_r=176,
              th_l=4, sh_l=-26, th_r=4, sh_r=-26),
            F(rise=51, ua_l=118, fa_l=188, ua_r=118, fa_r=188,
              th_l=4, sh_l=-36, th_r=4, sh_r=-36),
        ]
    elif template == "pulldown":
        A.update(view="front")
        A["keyframes"] = [
            F(ua_l=162, fa_l=172, ua_r=162, fa_r=172),
            F(ua_l=112, fa_l=128, ua_r=112, fa_r=128),
        ]
    elif template == "overhead_press":
        A.update(view="front")
        A["keyframes"] = [
            F(ua_l=78, fa_l=168, ua_r=78, fa_r=168),
            F(ua_l=158, fa_l=175, ua_r=158, fa_r=175),
        ]
    elif template == "lateral_raise":
        A.update(view="front")
        A["keyframes"] = [
            F(ua_l=14, fa_l=10, ua_r=14, fa_r=10),
            F(ua_l=92, fa_l=88, ua_r=92, fa_r=88),
        ]
    elif template == "front_raise":
        A["keyframes"] = [
            S(ua_n=6, fa_n=8, ua_f=6, fa_f=8),
            S(ua_n=92, fa_n=94, ua_f=92, fa_f=94),
        ]
    elif template == "reverse_fly":
        A["keyframes"] = [
            S(torso=48, head=-26, th_n=-10, sh_n=6, th_f=-10, sh_f=6,
              ua_n=44, fa_n=54, ua_f=44, fa_f=54),
            S(torso=48, head=-26, th_n=-10, sh_n=6, th_f=-10, sh_f=6,
              ua_n=-18, fa_n=-6, ua_f=-18, fa_f=-6),
        ]
    elif template == "shrug":
        A["keyframes"] = [
            S(ua_n=0, fa_n=2, ua_f=0, fa_f=2),
            S(shifty=-9, ua_n=0, fa_n=2, ua_f=0, fa_f=2, head=6),
        ]
    elif template == "fly":
        A.update(view="front")
        A["keyframes"] = [
            F(ua_l=86, fa_l=96, ua_r=86, fa_r=96),
            F(ua_l=22, fa_l=118, ua_r=22, fa_r=118),
        ]
    elif template == "chest_press":
        A["floor"] = False
        A["bench"] = True
        A["keyframes"] = [
            supine(hipx=252, hipy=318, th_n=-62, sh_n=58, th_f=-62, sh_f=58,
                   ft_n=112, ft_f=112, ua_n=118, fa_n=32, ua_f=118, fa_f=32),
            supine(hipx=252, hipy=318, th_n=-62, sh_n=58, th_f=-62, sh_f=58,
                   ft_n=112, ft_f=112, ua_n=94, fa_n=92, ua_f=94, fa_f=92),
        ]
    elif template == "pullover":
        A["floor"] = False
        A["bench"] = True
        A["keyframes"] = [
            supine(hipx=252, hipy=318, th_n=-62, sh_n=58, th_f=-62, sh_f=58,
                   ft_n=112, ft_f=112, ua_n=176, fa_n=178, ua_f=176, fa_f=178),
            supine(hipx=252, hipy=318, th_n=-62, sh_n=58, th_f=-62, sh_f=58,
                   ft_n=112, ft_f=112, ua_n=96, fa_n=98, ua_f=96, fa_f=98),
        ]
    elif template == "crunch":
        A["floor"] = False
        A["keyframes"] = [
            supine(torso=-6, head=10, th_n=-58, sh_n=62, th_f=-58, sh_f=62,
                   ft_n=112, ft_f=112, ua_n=150, fa_n=118, ua_f=150, fa_f=118),
            supine(torso=-38, head=16, th_n=-58, sh_n=62, th_f=-58, sh_f=62,
                   ft_n=112, ft_f=112, ua_n=150, fa_n=104, ua_f=150, fa_f=104),
        ]
    elif template == "leg_raise":
        A["floor"] = False
        A["keyframes"] = [
            supine(th_n=-84, sh_n=4, th_f=-84, sh_f=4, ft_n=24, ft_f=24,
                   ua_n=120, fa_n=150, ua_f=120, fa_f=150),
            supine(th_n=-172, sh_n=6, th_f=-172, sh_f=6, ft_n=-60, ft_f=-60,
                   ua_n=120, fa_n=150, ua_f=120, fa_f=150),
        ]
    elif template == "bridge":
        A["floor"] = False
        A["keyframes"] = [
            supine(hipx=252, hipy=396, th_n=-64, sh_n=64, th_f=-64, sh_f=64,
                   ft_n=112, ft_f=112, ua_n=-24, fa_n=-22, ua_f=-24, fa_f=-22),
            supine(hipx=246, hipy=352, torso=-23, th_n=-46, sh_n=80, th_f=-46, sh_f=80,
                   ft_n=112, ft_f=112, ua_n=-46, fa_n=-44, ua_f=-46, fa_f=-44),
        ]
    elif template in ("bird_dog", "kickback"):
        base = dict(rootx=186, rooty=352, torso=68, head=-46,
                    ua_n=6, fa_n=8, ua_f=6, fa_f=8,
                    th_n=-6, sh_n=-86, th_f=-6, sh_f=-86, ft_n=64, ft_f=64)
        start = make_pose("side", **base)
        if template == "bird_dog":
            end = make_pose("side", **{**base, "ua_f": 100, "fa_f": 102,
                                       "th_n": -96, "sh_n": -92, "ft_n": -20})
        else:
            end = make_pose("side", **{**base, "th_n": -78, "sh_n": -110, "ft_n": -40})
        A["keyframes"] = [start, end]
    elif template == "crawl":
        A["cycle"] = "loop"
        base = dict(rootx=186, rooty=336, torso=74, head=-50,
                    ua_n=10, fa_n=12, ua_f=10, fa_f=12,
                    th_n=24, sh_n=-70, th_f=24, sh_f=-70, ft_n=64, ft_f=64)
        a = make_pose("side", **base)
        b = make_pose("side", **{**base, "ua_n": 42, "fa_n": 30, "ua_f": -18, "fa_f": -6,
                                 "th_n": -10, "sh_n": -60, "th_f": 48, "sh_f": -78})
        c = make_pose("side", **{**base, "ua_n": -18, "fa_n": -6, "ua_f": 42, "fa_f": 30,
                                 "th_n": 48, "sh_n": -78, "th_f": -10, "sh_f": -60})
        A["keyframes"] = [a, b, a, c]
    elif template == "leg_curl":
        A["keyframes"] = [
            S(torso=8, ua_n=18, fa_n=22, ua_f=18, fa_f=22),
            S(torso=8, ua_n=18, fa_n=22, ua_f=18, fa_f=22, th_n=-6, sh_n=-118, ft_n=-24),
        ]
    elif template == "leg_extension":
        A["floor"] = False
        A["seat"] = True
        A["keyframes"] = [
            S(rootx=232, rooty=300, torso=-10, th_n=82, sh_n=-4, th_f=82, sh_f=-4,
              ft_n=76, ft_f=76, ua_n=22, fa_n=34, ua_f=22, fa_f=34),
            S(rootx=232, rooty=300, torso=-10, th_n=82, sh_n=78, th_f=82, sh_f=78,
              ft_n=160, ft_f=160, ua_n=22, fa_n=34, ua_f=22, fa_f=34),
        ]
    elif template in ("abduction", "adduction"):
        A.update(view="front")
        wide = F(th_l=34, sh_l=-30, th_r=7, sh_r=-7, ua_l=18, fa_l=8, ua_r=18, fa_r=8)
        narrow = F(ua_l=18, fa_l=8, ua_r=18, fa_r=8)
        A["keyframes"] = [narrow, wide] if template == "abduction" else [wide, narrow]
    elif template == "side_bend":
        A.update(view="front")
        A["keyframes"] = [
            F(lean=-16, ua_l=6, fa_l=4, ua_r=14, fa_r=10),
            F(lean=18, ua_l=6, fa_l=4, ua_r=14, fa_r=10),
        ]
    elif template == "rotation":
        A["keyframes"] = [
            S(torso=12, ua_n=66, fa_n=84, ua_f=66, fa_f=84, th_n=6, sh_n=-4, th_f=-8, sh_f=6),
            S(torso=-14, ua_n=-52, fa_n=-38, ua_f=-52, fa_f=-38, th_n=-4, sh_n=2, th_f=10, sh_f=-6),
        ]
    elif template == "neck":
        A["keyframes"] = [S(head=-26), S(head=30)]
    elif template == "dip":
        A["floor"] = False
        A["pin"] = "dip"
        A["keyframes"] = [
            S(rootx=CENTER_X, rooty=250, th_n=-22, sh_n=-58, th_f=-22, sh_f=-58,
              ft_n=24, ft_f=24, ua_n=-14, fa_n=10, ua_f=-14, fa_f=10),
            S(rootx=CENTER_X, rooty=292, torso=12, th_n=-30, sh_n=-66, th_f=-30, sh_f=-66,
              ft_n=24, ft_f=24, ua_n=-56, fa_n=48, ua_f=-56, fa_f=48),
        ]
    elif template == "run":
        A["cycle"] = "loop"
        base = dict(torso=8, head=2)
        a = make_pose("side", **base, ua_n=42, fa_n=118, ua_f=-38, fa_f=36,
                      th_n=42, sh_n=-32, ft_n=110, th_f=-30, sh_f=54, ft_f=140)
        b = make_pose("side", **base, ua_n=-38, fa_n=36, ua_f=42, fa_f=118,
                      th_n=-30, sh_n=54, ft_n=140, th_f=42, sh_f=-32, ft_f=110)
        A["keyframes"] = [a, b]
    elif template == "bike":
        A["cycle"] = "loop"
        A["floor"] = False
        A["seat"] = "bike"
        base = dict(rootx=228, rooty=300, torso=38, head=-20, ua_n=64, fa_n=58, ua_f=64, fa_f=58)
        a = make_pose("side", **base, th_n=14, sh_n=34, ft_n=96, th_f=62, sh_f=-24, ft_f=96)
        b = make_pose("side", **base, th_n=62, sh_n=-24, ft_n=96, th_f=14, sh_f=34, ft_f=96)
        A["keyframes"] = [a, b]
    elif template == "jump":
        A.update(view="front")
        A["cycle"] = "loop"
        A["keyframes"] = [
            F(ua_l=14, fa_l=8, ua_r=14, fa_r=8),
            F(drop=52, ua_l=30, fa_l=26, ua_r=30, fa_r=26),
            F(rise=58, ua_l=132, fa_l=150, ua_r=132, fa_r=150,
              th_l=16, sh_l=-12, th_r=16, sh_r=-12),
            F(drop=26, ua_l=24, fa_l=20, ua_r=24, fa_r=20),
        ]
    elif template == "burpee":
        A["cycle"] = "loop"
        A["floor"] = False
        stand = S(rootx=214, rooty=FLOOR_Y - (TH + SH))
        crouch = S(rootx=214, rooty=FLOOR_Y - 65, torso=66, head=-30,
                   th_n=64, sh_n=-74, th_f=64, sh_f=-74, ft_n=110, ft_f=110,
                   ua_n=20, fa_n=12, ua_f=20, fa_f=12)
        plank = S(rotate=-84, rootx=196, rooty=330, th_n=4, sh_n=2, th_f=4, sh_f=2,
                  ft_n=150, ft_f=150, ua_n=88, fa_n=92, ua_f=88, fa_f=92, head=24)
        air = S(rootx=214, rooty=FLOOR_Y - (TH + SH) - 44, ua_n=-22, fa_n=-26,
                ua_f=-22, fa_f=-26, ft_n=118, ft_f=118)
        A["keyframes"] = [stand, crouch, plank, crouch, air]
    else:  # "stretch" and any unmapped fallback: overhead reach
        A["keyframes"] = [
            S(ua_n=8, fa_n=10, ua_f=8, fa_f=10),
            S(ua_n=168, fa_n=176, ua_f=168, fa_f=176, head=6),
        ]
    return A


# --------------------------------------------------------------------------- #
# Classification (same taxonomy as before; two ordering fixes:
# "reverse fly"/"rear delt" now win over generic "fly", and crunch-style names
# win over "bike" so "bicycle crunch" animates as a crunch)
# --------------------------------------------------------------------------- #

def classify(name: str, category: str, target: str) -> str:
    text = name.lower().replace("_", " ")
    if any(term in text for term in ("push-up", "push up", "pushup")):
        return "pushup"
    if any(term in text for term in ("pull-up", "pull up", "pullup", "chin-up", "chin up")):
        return "pullup"
    if "burpee" in text:
        return "burpee"
    if "all fours" in text:
        return "bird_dog"
    if any(term in text for term in ("mountain climber", "bear crawl", "crab walk", "inchworm")):
        return "crawl"
    if any(term in text for term in ("jump", "hop", "skipping", "jack")):
        return "jump"
    if re.search(r"\b(run|running|walk|walking|jog|jogging|sprint|quick feet)\b", text):
        return "run"
    if any(term in text for term in ("crunch", "sit-up", "sit up", "curl-up", "curl up", "cocoon")):
        return "crunch"
    if any(term in text for term in ("bike", "bicycle", "cycling", "cycle")):
        return "bike"
    if "squat" in text or "sit-to-stand" in text or "sit to stand" in text:
        return "squat"
    if any(term in text for term in ("lunge", "split squat", "step-up", "step up")):
        return "lunge"
    if any(term in text for term in ("deadlift", "good morning", "hip hinge")):
        return "hinge"
    if any(term in text for term in ("kettlebell swing", "tire flip")):
        return "hinge"
    if any(term in text for term in ("sledge hammer", "hammer strike")):
        return "rotation"
    if "hip thrust" in text or "glute bridge" in text or text == "bridge":
        return "bridge"
    if "kickback" in text or "donkey kick" in text:
        return "kickback"
    if "leg curl" in text or "hamstring curl" in text:
        return "leg_curl"
    if "leg extension" in text:
        return "leg_extension"
    if "calf raise" in text or "heel raise" in text:
        return "calf_raise"
    if any(term in text for term in ("abduction", "abductor", "side leg raise")):
        return "abduction"
    if any(term in text for term in ("adduction", "adductor", "inner thigh")):
        return "adduction"
    if re.search(r"\b(row|rowing)\b", text):
        return "row"
    if any(term in text for term in ("pulldown", "pull down", "straight arm pull")):
        return "pulldown"
    if "shrug" in text:
        return "shrug"
    if any(term in text for term in ("bench press", "chest press", "floor press")):
        return "chest_press"
    if "reverse fly" in text or "rear delt" in text:
        return "reverse_fly"
    if any(term in text for term in ("fly", "crossover", "cross-over")):
        return "fly"
    if "pullover" in text:
        return "pullover"
    if any(term in text for term in ("shoulder press", "military press", "overhead press", "push press")):
        return "overhead_press"
    if "front raise" in text or "forward raise" in text:
        return "front_raise"
    if any(term in text for term in ("lateral raise", "side raise", "upright row")):
        return "lateral_raise"
    if "wrist" in text or "finger curl" in text:
        return "wrist"
    if "curl" in text and "leg" not in text:
        return "curl"
    if "dip" in text:
        return "dip"
    if any(term in text for term in ("triceps extension", "pushdown", "push-down", "skull crusher")):
        return "triceps"
    if any(term in text for term in ("leg raise", "knee raise", "toes to bar", "toe touch")):
        return "leg_raise"
    if "plank" in text or "side bridge" in text:
        return "plank"
    if "bird dog" in text:
        return "bird_dog"
    if any(term in text for term in ("rotation", "twist", "wood chop", "russian")):
        return "rotation"
    if "side bend" in text or "windmill" in text:
        return "side_bend"
    if "neck" in text or category == "neck":
        return "neck"
    if any(term in text for term in ("stretch", "mobility", "circle", "roll")):
        return "stretch"
    if category == "back":
        return "row"
    if category == "chest":
        return "chest_press"
    if category == "shoulders":
        return "lateral_raise"
    if category == "upper arms":
        return "triceps" if target.lower() == "triceps" else "curl"
    if category == "lower arms":
        return "wrist"
    if category == "upper legs":
        return "squat"
    if category == "lower legs":
        return "calf_raise"
    if category == "waist":
        return "crunch"
    if category == "cardio":
        return "run"
    return "stretch"


def apply_variants(anim: dict, name: str) -> None:
    lower = name.lower()
    single = any(term in lower for term in ("single arm", "one arm", "one-arm", "unilateral", "alternate"))
    if single and anim["view"] == "side" and "pin" not in anim:
        first = anim["keyframes"][0]
        for frame in anim["keyframes"][1:]:
            frame["ua_f"] = first["ua_f"]
            frame["fa_f"] = first["fa_f"]
    if single and anim["view"] == "front" and "pin" not in anim:
        first = anim["keyframes"][0]
        for frame in anim["keyframes"][1:]:
            frame["ua_l"] = first["ua_l"]
            frame["fa_l"] = first["fa_l"]
    if "wide" in lower and anim["view"] == "front":
        for frame in anim["keyframes"]:
            frame["ua_l"] += 10
            frame["ua_r"] += 10
            frame["stance"] = frame.get("stance", 1.0) + 0.35


# --------------------------------------------------------------------------- #
# Frame assembly
# --------------------------------------------------------------------------- #

def sample_cycle(anim: dict) -> list[dict]:
    keyframes = anim["keyframes"]
    poses = []
    if anim["cycle"] == "pingpong":
        segments = len(keyframes) - 1
        for i in range(FRAME_COUNT):
            phase = i / FRAME_COUNT
            wave = 0.5 - 0.5 * math.cos(2 * math.pi * phase)   # 0 -> 1 -> 0, eased
            spot = min(wave * segments, segments - 1e-6)
            idx = int(spot)
            poses.append(interpolate_pose(keyframes[idx], keyframes[idx + 1], spot - idx))
    else:  # loop over keyframes cyclically with eased segments
        segs = len(keyframes)
        for i in range(FRAME_COUNT):
            spot = (i / FRAME_COUNT) * segs
            idx = int(spot) % segs
            local = spot - int(spot)
            eased = 0.5 - 0.5 * math.cos(math.pi * local)
            poses.append(interpolate_pose(keyframes[idx], keyframes[(idx + 1) % segs], eased))
    return poses


def draw_bench(draw: ImageDraw.ImageDraw) -> None:
    draw.rounded_rectangle((66, 334, 400, 358), radius=10, fill=PAD, outline=IRON_DARK, width=3)
    for x in (104, 362):
        draw.line((x, 358, x, 422), fill=IRON, width=9)
        draw.line((x - 22, 422, x + 22, 422), fill=IRON_DARK, width=7)


def draw_seat(draw: ImageDraw.ImageDraw) -> None:
    # leg-extension chair: backrest on the left, seat under the thighs
    draw.rounded_rectangle((170, 188, 196, 322), radius=9, fill=PAD, outline=IRON_DARK, width=3)
    draw.rounded_rectangle((176, 306, 306, 330), radius=8, fill=PAD, outline=IRON_DARK, width=3)
    draw.line((240, 330, 240, 424), fill=IRON, width=10)
    draw.line((204, 424, 276, 424), fill=IRON_DARK, width=7)


def draw_bike(draw: ImageDraw.ImageDraw) -> None:
    disc(draw, (196, 400), 36, BG, IRON_DARK, 6)
    disc(draw, (196, 400), 5, IRON_DARK)
    draw.line((196, 400, 236, 316), fill=IRON, width=8)      # seat post
    draw.line((214, 316, 258, 316), fill=IRON_DARK, width=8)  # saddle
    draw.line((196, 400, 300, 356), fill=IRON, width=8)      # frame
    draw.line((300, 356, 300, 302), fill=IRON, width=7)      # head tube
    draw.line((286, 300, 322, 300), fill=IRON_DARK, width=7)  # handlebar
    draw.line((160, 436, 330, 436), fill=IRON_DARK, width=8)  # floor base


def render_frame(anim: dict, pose: dict, hl: Highlight, equipment_layers,
                 mirror: bool, pins: dict[str, Point] | None) -> Image.Image:
    image = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(image)

    facing = -1.0 if mirror else 1.0
    j = solve_side(pose, facing) if anim["view"] == "side" else solve_front(pose)
    if mirror:
        j = {key: (SIZE - x, y) for key, (x, y) in j.items()}
    if pins:
        pin_wrists(j, pins, anim["view"])

    if anim.get("shadow", True):
        xs = [p[0] for p in j.values()]
        cx = (min(xs) + max(xs)) / 2
        draw.ellipse((cx - 96, FLOOR_Y - 4, cx + 96, FLOOR_Y + 16), fill=SHADOW)
    if anim.get("floor", True):
        draw.line((56, FLOOR_Y + 6, 424, FLOOR_Y + 6), fill=FLOOR_LINE, width=5)

    if anim.get("bench"):
        draw_bench(draw)
    if anim.get("seat") == "bike":
        draw_bike(draw)
    elif anim.get("seat"):
        draw_seat(draw)

    if anim["view"] == "side":
        render_side(j, hl, facing, equipment_layers, draw)
    else:
        render_front(j, hl, equipment_layers, draw)
    return image


def build_frames(row: dict[str, object]) -> tuple[list[Image.Image], str]:
    name = str(row["name"])
    category = str(row["category"])
    target = str(row.get("target", ""))
    equipment = str(row.get("equipment", ""))

    template = classify(name, category, target)
    anim = template_animation(template)
    apply_variants(anim, name)
    hl = Highlight(category, target)
    mirror = int(hashlib.sha1(str(row["id"]).encode("utf-8")).hexdigest()[-1], 16) % 2 == 1
    if anim["view"] == "front":
        mirror = False

    poses = sample_cycle(anim)
    first_pose = anim["keyframes"][0]
    first_j = solve_side(first_pose, -1.0 if mirror else 1.0) if anim["view"] == "side" \
        else solve_front(first_pose)
    if mirror:
        first_j = {key: (SIZE - x, y) for key, (x, y) in first_j.items()}
    anchors = equipment_anchors(template, equipment, anim["view"], mirror, first_j)
    equipment_layers = make_equipment(equipment, template, anim["view"], mirror, anchors)

    pins: dict[str, Point] | None = None
    if anim.get("pin") == "bar":
        pins = {"wrist_l": first_j["wrist_l"], "wrist_r": first_j["wrist_r"]}
    elif anim.get("pin") == "dip":
        pins = {"wrist_n": first_j["wrist_n"], "wrist_f": first_j["wrist_f"]}

    frames = [render_frame(anim, pose, hl, equipment_layers, mirror, pins) for pose in poses]
    return frames, template


def generate(row: dict[str, object], output: Path) -> str:
    frames, template = build_frames(row)
    palette = frames[0].quantize(colors=64, method=Image.Quantize.MEDIANCUT)
    indexed = [palette]
    indexed.extend(frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames[1:])
    indexed[0].save(output, format="GIF", save_all=True, append_images=indexed[1:],
                    duration=FRAME_MS, loop=0, optimize=True, disposal=2)
    return template


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def preview_sheet(rows: list[dict], out_path: Path) -> None:
    """One tile per template: frames 0, N/4, N/2 side by side."""
    by_template: dict[str, dict] = {}
    for row in rows:
        template = classify(str(row["name"]), str(row["category"]), str(row.get("target", "")))
        by_template.setdefault(template, row)
    names = sorted(by_template)
    cols = 3
    tile_w, tile_h = 3 * 240 + 16, 240 + 30
    rows_n = math.ceil(len(names) / cols)
    sheet = Image.new("RGB", (cols * tile_w, rows_n * tile_h), (244, 242, 238))
    from PIL import ImageFont
    font = ImageFont.load_default(size=17)
    for i, template in enumerate(names):
        row = by_template[template]
        frames, _ = build_frames(row)
        cell_x = (i % cols) * tile_w
        cell_y = (i // cols) * tile_h
        for k, f_idx in enumerate((0, FRAME_COUNT // 4, FRAME_COUNT // 2)):
            frame = frames[f_idx].resize((240, 240), Image.Resampling.LANCZOS)
            sheet.paste(frame, (cell_x + k * 240 + 8, cell_y + 26))
        d = ImageDraw.Draw(sheet)
        label = f"{template} | {row['name']} | {row.get('equipment', '')}"
        d.text((cell_x + 10, cell_y + 4), label[:64], fill=(60, 60, 60), font=font)
    sheet.save(out_path)
    print(f"Preview sheet: {out_path} ({len(names)} templates)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True, type=Path)
    parser.add_argument("--exact-media-map", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--preview", type=Path, help="render a per-template contact sheet and exit")
    args = parser.parse_args()

    rows = json.loads(args.dataset.read_text(encoding="utf-8"))["exercises"]
    exact_ids = set(json.loads(args.exact_media_map.read_text(encoding="utf-8")))
    procedural_rows = [row for row in rows if str(row["id"]) not in exact_ids]

    if args.preview:
        preview_sheet(procedural_rows, args.preview)
        return

    if not args.output_dir or not args.manifest:
        raise SystemExit("--output-dir and --manifest are required unless --preview is used")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, dict[str, str]] = {}
    counts: Counter[str] = Counter()
    for row in procedural_rows:
        exercise_id = str(row["id"])
        template = generate(row, args.output_dir / f"dataset_motion_{exercise_id}.gif")
        manifest[exercise_id] = {"template": template, "name": str(row["name"])}
        counts[template] += 1

    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(manifest)} procedural exercise GIFs across {len(counts)} motion templates")
    print("Template counts: " + ", ".join(f"{key}={counts[key]}" for key in sorted(counts)))


if __name__ == "__main__":
    main()
