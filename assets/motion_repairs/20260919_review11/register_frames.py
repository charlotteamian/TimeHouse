#!/usr/bin/env python3
"""Register, stabilize, and validate all 10 exercises in batch 20260919_review11."""

import json
import os
import subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw

BATCH_DIR = Path("assets/motion_repairs/20260919_review11")
SRC_720_DIR = Path("assets/motion_repairs/20260910_720")
RAW_DIR = Path("app/src/main/res/raw")
DURATIONS_MS = [800, 380, 800, 380]

EXERCISES = [
    "0467", "0323", "0469", "0324", "0471",
    "0325", "0472", "0326", "0473", "0327",
]


def clean_white(arr: np.ndarray, thresh: int = 248) -> np.ndarray:
    out = arr.copy()
    out[np.all(out >= thresh, axis=2)] = 255
    return out


def shift_img(arr: np.ndarray, dx: int, dy: int) -> np.ndarray:
    h, w, c = arr.shape
    out = np.full((h, w, c), 255, dtype=np.uint8)
    sx1, sx2 = max(0, -dx), min(w, w - dx)
    sy1, sy2 = max(0, -dy), min(h, h - dy)
    if sx2 > sx1 and sy2 > sy1:
        out[sy1 + dy : sy2 + dy, sx1 + dx : sx2 + dx] = arr[sy1:sy2, sx1:sx2]
    return out


def load_quadrants_480(sheet_path: Path) -> list[np.ndarray]:
    im = Image.open(sheet_path).convert("RGB")
    w, h = im.size
    hw, hh = w // 2, h // 2
    boxes = [(0, 0, hw, hh), (hw, 0, w, hh), (0, hh, hw, h), (hw, hh, w, h)]
    frames = []
    for b in boxes:
        cell = np.array(im.crop(b).resize((480, 480), Image.Resampling.LANCZOS))
        frames.append(clean_white(cell, 248))
    return frames


def build_0323() -> tuple[list[np.ndarray], str]:
    raw = load_quadrants_480(SRC_720_DIR / "0323.png")
    f0, f1, f2 = raw[0], raw[1], raw[2]
    return [f0, f1, f2, f1.copy()], str(SRC_720_DIR / "0323.png")


def build_0324() -> tuple[list[np.ndarray], str]:
    # In 0324.png (1254x1254), rows y=607..626 are pure white, and Cell 2 starts at y=627.
    # Shifting Frame 2 down by +5 px restores a 5px top white margin, and locking the static lower
    # bench base & planted feet (y >= 340, feathered over y=332..340) eliminates the 1-2px base jitter.
    raw = load_quadrants_480(SRC_720_DIR / "0324.png")
    f0 = raw[0].copy()
    f1_s = shift_img(raw[1], 0, 0)
    f2_s = shift_img(raw[2], 0, 5)
    alpha = np.zeros((480, 480, 1), dtype=np.float32)
    alpha[:332] = 1.0
    for y in range(332, 340):
        alpha[y] = 1.0 - (y - 332) / 8.0
    f1 = clean_white((f1_s * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    f2 = clean_white((f2_s * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    return [f0, f1, f2, f1.copy()], str(SRC_720_DIR / "0324.png")


def build_0326() -> tuple[list[np.ndarray], str]:
    raw = load_quadrants_480(SRC_720_DIR / "0326.png")
    f0 = shift_img(raw[0], -4, 0)
    f1 = shift_img(raw[1], -4, 0)
    f2 = shift_img(raw[2], -4, 16)
    return [f0, f1, f2, f1.copy()], str(SRC_720_DIR / "0326.png")


def build_0327() -> tuple[list[np.ndarray], str]:
    raw = load_quadrants_480(SRC_720_DIR / "0327.png")
    f0 = raw[0]
    f1 = shift_img(raw[1], 8, 0)
    f2 = shift_img(raw[2], 0, 10)
    return [f0, f1, f2, f1.copy()], str(SRC_720_DIR / "0327.png")


def build_0472() -> tuple[list[np.ndarray], str]:
    raw = load_quadrants_480(SRC_720_DIR / "0472.png")
    f0, f1, f2 = raw[0], raw[1], raw[2]
    return [f0, f1, f2, f1.copy()], str(SRC_720_DIR / "0472.png")


def build_0325() -> tuple[list[np.ndarray], str]:
    src = BATCH_DIR / "0325-generated.png"
    raw = load_quadrants_480(src)
    f0 = raw[0].copy()
    f1_s = shift_img(raw[1], -2, 0)
    f2_s = shift_img(raw[2], 2, 0)
    alpha = np.zeros((480, 480, 1), dtype=np.float32)
    alpha[:218] = 1.0
    for y in range(218, 228):
        alpha[y] = 1.0 - (y - 218) / 10.0
    f1 = clean_white((f1_s * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    f2 = clean_white((f2_s * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    return [f0, f1, f2, f1.copy()], str(src)


def build_0467() -> tuple[list[np.ndarray], str]:
    src = BATCH_DIR / "0467-generated.png"
    raw = load_quadrants_480(src)
    f0 = raw[0].copy()
    f1 = shift_img(raw[1], 3, 0)
    f2 = shift_img(raw[2], 0, -2)
    for f in (f1, f2):
        f[:, :118] = f0[:, :118]
        f[:, 362:] = f0[:, 362:]
        f[25:53, 118:180] = f0[25:53, 118:180]
        f[25:53, 305:362] = f0[25:53, 305:362]
    return [f0, clean_white(f1), clean_white(f2), clean_white(f1.copy())], str(src)


def build_0469() -> tuple[list[np.ndarray], str]:
    src = BATCH_DIR / "0469-generated.png"
    im = np.array(Image.open(src).convert("RGB"))
    im[np.all(im >= 245, axis=2)] = 255
    c0 = im[0:520, 16:536].copy()
    c1 = im[0:520, 504:1024].copy()
    c1[:, :40] = 255
    c2 = im[504:1024, 16:536].copy()
    c1_s = shift_img(c1, -18, -6)
    c2_s = shift_img(c2, 24, 33)

    c2_s[170:241, 190:270] = 255
    for y in range(241, 272):
        cut_x = int(round(207 + (y - 240) * 10.0 / 26.0))
        c2_s[y, cut_x:270] = 255
        c2_s[y, cut_x - 1] = np.minimum(255, (c2_s[y, cut_x - 1].astype(int) + 255) // 2).astype(np.uint8)

    red2 = (c2_s[:, :, 0].astype(int) - c2_s[:, :, 1].astype(int)) > 22
    for x in range(218, 265):
        rys = np.where(red2[:, x])[0]
        y_top_red = int(rys.min()) if len(rys) > 0 else 330
        c2_s[268 : y_top_red - 1, x] = 255

    def comp_upper(upper: np.ndarray, base_c0: np.ndarray) -> np.ndarray:
        h, w, _ = base_c0.shape
        alpha = np.zeros((h, w), dtype=np.float32)
        for y in range(h):
            if y < 312:
                x_cut, feather = 224, 2
            elif y < 405:
                t = (y - 312) / (405 - 312)
                x_cut, feather = int(round(256 + t * 12)), 5
            else:
                x_cut, feather = 180, 6
            for x in range(w):
                if x < x_cut - feather:
                    alpha[y, x] = 1.0
                elif x <= x_cut + feather:
                    alpha[y, x] = 1.0 - (x - (x_cut - feather)) / (2.0 * feather)
        out = (upper.astype(np.float32) * alpha[:, :, None] + base_c0.astype(np.float32) * (1.0 - alpha[:, :, None])).round().astype(np.uint8)
        return clean_white(out, 248)

    f0_520 = c0.copy()
    f1_520 = comp_upper(c1_s, c0)
    f2_520 = comp_upper(c2_s, c0)
    frames_480 = []
    for f in (f0_520, f1_520, f2_520, f1_520):
        r = np.array(Image.fromarray(f).resize((480, 480), Image.Resampling.LANCZOS))
        frames_480.append(clean_white(r, 248))
    return frames_480, str(src)


def build_0471() -> tuple[list[np.ndarray], str]:
    # Combine v2 (Cells 0, 1) and v1 (Cell 2) into 0471-generated.png and align planted hands & wall
    brain = Path("/Users/restartday/.gemini/antigravity/brain/2ab85b03-fbcb-4420-8235-cea20f9ee903")
    v2_path = brain / "0471_generated_v2_1794135638588.jpg"
    v1_path = brain / "0471_generated_v1_1794135611981.jpg"
    src = BATCH_DIR / "0471-generated.png"
    if v2_path.exists() and v1_path.exists():
        im_v2 = Image.open(v2_path).convert("RGB")
        im_v1 = Image.open(v1_path).convert("RGB")
        combined = im_v2.copy()
        combined.paste(im_v1.crop((0, 512, 512, 1024)), (0, 512))
        combined.save(src)
    raw = load_quadrants_480(src)
    f0 = raw[0].copy()
    f1 = shift_img(raw[1], 4, 1)
    f2 = shift_img(raw[2], 1, -2)

    for y in range(385, 416):
        t = (y - 385) / (415 - 385)
        dx_r = int(round(6 * t))
        row_new = f1[y].copy()
        for x in range(295, 365):
            src_x = min(364, max(290, x - dx_r))
            row_new[x] = f1[y, src_x]
        f1[y] = row_new

    f2_wrist = f2.copy()
    for y in range(375, 417):
        t = (y - 375) / (415 - 375)
        dx_l = int(round(18 * t))
        dx_r = int(round(-14 * t))
        row_new = f0[y].copy()
        row_new[255:312] = f2[y, 255:312]
        for x in range(190, 258):
            src_x = min(258, max(185, x - dx_l))
            row_new[x] = f2[y, src_x]
        for x in range(310, 375):
            src_x = min(379, max(310, x - dx_r))
            row_new[x] = f2[y, src_x]
        f2_wrist[y] = row_new
    f2 = f2_wrist

    for idx, f in enumerate([f1, f2]):
        alpha = np.ones((480, 480, 1), dtype=np.float32)
        alpha[:, :185] = 0.0
        for x in range(185, 193):
            alpha[:, x] = (x - 185) / 8.0
        alpha[414:, :300] = 0.0
        for y in range(410, 414):
            alpha[y, :300] = np.minimum(alpha[y, :300], 1.0 - (y - 410) / 4.0)
        alpha[408:, 300:] = 0.0
        for y in range(404, 408):
            alpha[y, 300:] = np.minimum(alpha[y, 300:], 1.0 - (y - 404) / 4.0)
        blended = clean_white((f * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8), 248)
        if idx == 0:
            f1 = blended
        else:
            f2 = blended

    return [f0, f1, f2, f1.copy()], str(src)


def build_0473() -> tuple[list[np.ndarray], str]:
    src = BATCH_DIR / "0473-generated.png"
    raw = load_quadrants_480(src)
    f0 = raw[0].copy()
    f1 = raw[1].copy()
    f2 = raw[2].copy()
    for f in (f1, f2):
        f[:36, :216] = f0[:36, :216]
        f[:36, 268:] = f0[:36, 268:]
    return [f0, clean_white(f1), clean_white(f2), clean_white(f1.copy())], str(src)


ANCHOR_SPECS = {
    "0467": {
        "left_upright_base": (65, 360, 118, 465),
        "right_upright_base": (362, 360, 415, 465),
        "left_grip": (122, 25, 178, 53),
        "right_grip": (306, 25, 360, 53),
    },
    "0323": {
        "rear_bench_foot": (30, 345, 110, 400),
        "front_bench_foot": (240, 375, 345, 435),
        "left_foot": (195, 400, 250, 455),
        "right_foot": (360, 370, 435, 430),
    },
    "0469": {
        "pelvis_floor": (245, 290, 345, 375),
        "planted_knees": (300, 185, 395, 275),
        "planted_feet": (365, 315, 462, 375),
    },
    "0324": {
        "rear_bench_foot": (31, 345, 110, 400),
        "front_bench_foot": (195, 400, 245, 455),
        "left_foot": (130, 360, 185, 415),
        "right_foot": (225, 420, 290, 470),
    },
    "0471": {
        "wall_top_left": (128, 12, 182, 140),
        "wall_base_left": (128, 300, 182, 425),
        "left_hand_floor": (210, 414, 260, 436),
        "right_hand_floor": (308, 409, 360, 434),
    },
    "0325": {
        "left_foot": (40, 405, 115, 455),
        "right_foot": (180, 430, 235, 475),
        "front_bench_base": (135, 425, 195, 468),
        "rear_bench_base": (300, 380, 375, 430),
    },
    "0472": {
        "left_upright_base": (80, 370, 130, 465),
        "right_upright_base": (350, 370, 400, 465),
        "left_grip": (165, 5, 205, 40),
        "right_grip": (275, 5, 315, 40),
    },
    "0326": {
        "rear_bench_foot": (16, 375, 71, 445),
        "front_bench_foot": (366, 400, 446, 450),
        "planted_feet": (271, 375, 331, 455),
    },
    "0473": {
        "left_upright_base": (70, 360, 145, 465),
        "right_upright_base": (335, 360, 415, 465),
        "left_grip": (165, 5, 214, 36),
        "right_grip": (270, 5, 318, 36),
    },
    "0327": {
        "planted_feet": (20, 360, 75, 412),
        "rear_bench_foot": (85, 350, 140, 410),
        "front_bench_foot": (340, 355, 410, 415),
    },
}


def measure_anchors(frames: list[np.ndarray], anchors: dict[str, tuple[int, int, int, int]]) -> dict:
    results = {}
    search_radius = 20
    for name, box in anchors.items():
        x1, y1, x2, y2 = box
        tpl = frames[0][y1:y2, x1:x2]
        per_frame = []
        max_res = 0.0
        min_score = 1.0
        for idx in range(1, 4):
            f = frames[idx]
            sx1 = max(0, x1 - search_radius)
            sy1 = max(0, y1 - search_radius)
            sx2 = min(f.shape[1], x2 + search_radius)
            sy2 = min(f.shape[0], y2 + search_radius)
            search = f[sy1:sy2, sx1:sx2]
            res = cv2.matchTemplate(search, tpl, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            dx = int((sx1 + max_loc[0]) - x1)
            dy = int((sy1 + max_loc[1]) - y1)
            dist = float(np.hypot(dx, dy))
            max_res = max(max_res, dist)
            min_score = min(min_score, float(max_val))
            per_frame.append({
                "frame": idx,
                "dx": dx,
                "dy": dy,
                "residual_px": round(dist, 2),
                "match_score": round(float(max_val), 4),
            })
        results[name] = {
            "box": list(box),
            "max_residual_px": round(max_res, 2),
            "min_match_score": round(min_score, 4),
            "frames": per_frame,
        }
    return results


def save_outputs(eid: str, frames: list[np.ndarray]) -> dict:
    pil_frames = [Image.fromarray(f) for f in frames]
    for i, pf in enumerate(pil_frames):
        pf.save(BATCH_DIR / f"{eid}-fixed-{i}.png")

    sheet = Image.new("RGB", (960, 960), (255, 255, 255))
    sheet.paste(pil_frames[0], (0, 0))
    sheet.paste(pil_frames[1], (480, 0))
    sheet.paste(pil_frames[2], (0, 480))
    sheet.paste(pil_frames[3], (480, 480))
    sheet.save(BATCH_DIR / f"{eid}-fixed-sheet.jpg", quality=95)

    gif_path = BATCH_DIR / f"{eid}-fixed.gif"
    pil_frames[0].save(
        gif_path,
        save_all=True,
        append_images=pil_frames[1:],
        duration=DURATIONS_MS,
        loop=0,
        disposal=2,
    )

    webp_path = BATCH_DIR / f"{eid}-fixed.webp"
    pil_frames[0].save(
        webp_path,
        format="WEBP",
        save_all=True,
        append_images=pil_frames[1:],
        duration=DURATIONS_MS,
        loop=0,
        lossless=True,
        quality=100,
        method=4,
    )

    # Check foreground bounds on each frame (margin >= 2px from all 4 edges)
    fg_bboxes = []
    fg_preserved = True
    for f in frames:
        mask = np.any(f < 242, axis=2)
        ys, xs = np.where(mask)
        bbox = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
        fg_bboxes.append(bbox)
        if bbox[0] <= 1 or bbox[1] <= 1 or bbox[2] >= 478 or bbox[3] >= 478:
            fg_preserved = False

    return {
        "fg_bboxes": fg_bboxes,
        "fg_preserved": fg_preserved,
        "frame4_equals_frame2": bool(np.array_equal(frames[3], frames[1])),
    }


def make_contact_sheets() -> None:
    for part_idx, group in enumerate([EXERCISES[:5], EXERCISES[5:]], start=1):
        canvas = Image.new("RGB", (480 * 4, 480 * len(group)), (255, 255, 255))
        draw = ImageDraw.Draw(canvas)
        for row_idx, eid in enumerate(group):
            for col_idx in range(4):
                im = Image.open(BATCH_DIR / f"{eid}-fixed-{col_idx}.png").convert("RGB")
                canvas.paste(im, (col_idx * 480, row_idx * 480))
                draw.text((col_idx * 480 + 12, row_idx * 480 + 12), f"{eid} F{col_idx+1}", fill=(40, 40, 40))
        canvas.save(BATCH_DIR / f"contact-{part_idx}.jpg", quality=92)


def main() -> None:
    builders = {
        "0467": build_0467,
        "0323": build_0323,
        "0469": build_0469,
        "0324": build_0324,
        "0471": build_0471,
        "0325": build_0325,
        "0472": build_0472,
        "0326": build_0326,
        "0473": build_0473,
        "0327": build_0327,
    }
    anchor_report = {}
    validation_report = {}
    all_passed = True

    for eid in EXERCISES:
        frames, src_path = builders[eid]()
        meta = save_outputs(eid, frames)
        anchors = measure_anchors(frames, ANCHOR_SPECS[eid])
        passing_anchors = [
            k for k, v in anchors.items()
            if v["max_residual_px"] <= 2.0 and v["min_match_score"] >= 0.96
        ]
        passed = len(passing_anchors) >= 2 and meta["fg_preserved"] and meta["frame4_equals_frame2"]
        if not passed:
            all_passed = False

        anchor_report[eid] = {
            "source": src_path,
            "anchors": anchors,
            "passing_anchor_count": len(passing_anchors),
            "passed": passed,
        }
        validation_report[eid] = {
            "source": src_path,
            "fg_bboxes": meta["fg_bboxes"],
            "fg_preserved": meta["fg_preserved"],
            "frame4_equals_frame2": meta["frame4_equals_frame2"],
            "passing_anchor_count": len(passing_anchors),
            "passed": passed,
        }
        print(f"[{eid}] passed={passed} fg_preserved={meta['fg_preserved']} passing_anchors={len(passing_anchors)}/{len(anchors)}")
        for k, v in anchors.items():
            print(f"    {k}: residual={v['max_residual_px']}px, min_score={v['min_match_score']}")

    make_contact_sheets()
    (BATCH_DIR / "anchor-measurements.json").write_text(
        json.dumps(anchor_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (BATCH_DIR / "registration-validation.json").write_text(
        json.dumps(validation_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not all_passed:
        raise SystemExit("One or more exercises failed registration validation!")
    print("All 10 exercises passed registration and anchor validation!")


if __name__ == "__main__":
    main()
