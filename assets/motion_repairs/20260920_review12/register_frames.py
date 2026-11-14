#!/usr/bin/env python3
"""Register, stabilize, and validate all 10 exercises in batch 20260920_review12."""

import json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw

BATCH_DIR = Path("assets/motion_repairs/20260920_review12")
BEFORE_DIR = BATCH_DIR / "before"
DURATIONS_MS = [800, 380, 800, 380]

EXERCISES = [
    "0474", "0328", "0475", "0329", "0476",
    "0330", "0484", "0331", "0488", "0332",
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


def load_before_webp(eid: str) -> tuple[list[np.ndarray], str]:
    p = BEFORE_DIR / f"dataset_motion_{eid}.webp"
    im = Image.open(p)
    frames = []
    for i in range(im.n_frames):
        im.seek(i)
        frames.append(clean_white(np.array(im.convert("RGB")), 248))
    return frames, str(p)


def build_0474() -> tuple[list[np.ndarray], str]:
    src = BATCH_DIR / "0474-generated.png"
    cells = load_quadrants_480(src)
    base = shift_img(cells[1], -18, 0)
    c0 = shift_img(cells[0], 61 - 18, 0)
    c2 = shift_img(cells[2], 6 - 18, -18)

    rack_bg = base.copy()
    rack_bg[242:322, :335] = 255
    post_row = base[326, 295:325].copy()
    for y in range(242, 322):
        rack_bg[y, 295:325] = post_row

    m0 = np.zeros((480, 480, 1), dtype=np.float32)
    fg0 = np.any(c0 < 242, axis=2)
    for y in range(220, 468):
        xmin_w = 248 if y < 435 else 244
        xmax_w = 313 if y < 280 else (309 if y < 340 else 301)
        xs = np.where(fg0[y, xmin_w:xmax_w])[0]
        if len(xs) > 0:
            m0[y, xmin_w + xs.min() : xmin_w + xs.max() + 1, 0] = 1.0
    for y in range(220, 232):
        m0[y] *= (y - 220) / 12.0
    f0 = clean_white((c0 * m0 + rack_bg * (1.0 - m0)).round().astype(np.uint8))
    f1 = base.copy()

    m2 = np.zeros((480, 480, 1), dtype=np.float32)
    fg2 = np.any(c2 < 242, axis=2)
    for y in range(20, 290):
        xmax_l = 200 if y < 75 else (220 if y < 140 else 242)
        xs_l = np.where(fg2[y, 120:xmax_l])[0]
        if len(xs_l) > 0:
            m2[y, 120 + xs_l.min() : 120 + xs_l.max() + 1, 0] = 1.0
        if y >= 182:
            xmax_b = 335 if y <= 238 else int(round(335 - (y - 238) * 1.35))
            xmax_b = max(265, min(335, xmax_b))
            xs_b = np.where(fg2[y, 160:xmax_b])[0]
            if len(xs_b) > 0:
                m2[y, 160 + xs_b.min() : 160 + xs_b.max() + 1, 0] = 1.0
    for y in range(182, 194):
        m2[y, 236:] *= (y - 182) / 12.0
    rack_bg2 = rack_bg.copy()
    rack_bg2[172:232, 215:255] = 255
    f2 = clean_white((c2 * m2 + rack_bg2 * (1.0 - m2)).round().astype(np.uint8))
    return [f0, f1, f2, f1.copy()], str(src)


def build_0328() -> tuple[list[np.ndarray], str]:
    src = BATCH_DIR / "0328-generated.png"
    cells = load_quadrants_480(src)
    f0 = cells[1].copy()
    alpha = np.ones((480, 480, 1), dtype=np.float32)
    alpha[295:] = 0.0
    for y in range(285, 295):
        alpha[y] = 1.0 - (y - 285) / 10.0
    alpha[260:, :165] = 0.0
    for x in range(165, 175):
        alpha[260:295, x] = np.minimum(alpha[260:295, x], (x - 165) / 10.0)
    f1 = clean_white((cells[0] * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    c2_s = shift_img(cells[2], -6, 2)
    f2 = clean_white((c2_s * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    return [f0, f1, f2, f1.copy()], str(src)


def build_0475() -> tuple[list[np.ndarray], str]:
    raw, src = load_before_webp("0475")
    f0 = raw[0].copy()
    f1 = shift_img(raw[1], 5, 0)
    f2 = shift_img(raw[2], 1, 0)
    return [f0, f1, f2, f1.copy()], src


def build_0329() -> tuple[list[np.ndarray], str]:
    raw, src = load_before_webp("0329")
    f0 = raw[0].copy()
    f1_s = shift_img(raw[1], 7, 0)
    f2_s = raw[2].copy()
    alpha = np.ones((480, 480, 1), dtype=np.float32)
    alpha[378:] = 0.0
    for y in range(368, 378):
        alpha[y] = 1.0 - (y - 368) / 10.0
    f1 = clean_white((f1_s * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    f2 = clean_white((f2_s * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    return [f0, f1, f2, f1.copy()], src


def build_0476() -> tuple[list[np.ndarray], str]:
    raw, src = load_before_webp("0476")
    f0 = raw[0].copy()
    f1 = shift_img(raw[1], 1, 0)
    f2 = shift_img(raw[2], 1, 1)
    return [f0, f1, f2, f1.copy()], src


def build_0330() -> tuple[list[np.ndarray], str]:
    src = BATCH_DIR / "0330-generated.png"
    cells = load_quadrants_480(src)
    f0 = cells[0].copy()
    alpha = np.zeros((480, 480, 1), dtype=np.float32)
    for y in range(206):
        for x in range(225, 480):
            if y >= 152 and x >= 362:
                continue
            if y >= 166 and x >= 350:
                continue
            alpha[y, x] = 1.0
    alpha = cv2.GaussianBlur(alpha, (9, 9), 0)[:, :, None]
    c3_s = shift_img(cells[3], 13, 19)
    c1_s = shift_img(cells[1], 6, 0)
    f1 = clean_white((c3_s * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    f2 = clean_white((c1_s * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    return [f0, f1, f2, f1.copy()], str(src)


def build_0484() -> tuple[list[np.ndarray], str]:
    src = BATCH_DIR / "0484-generated.png"
    cells = load_quadrants_480(src)
    f0 = cells[0].copy()
    alpha = np.ones((480, 480, 1), dtype=np.float32)
    alpha[:, :92] = 0.0
    for x in range(92, 102):
        alpha[:, x] = (x - 92) / 10.0
    alpha[:, 386:] = 0.0
    for x in range(376, 386):
        alpha[:, x] = 1.0 - (x - 376) / 10.0
    alpha[413:, 92:386] = 0.0
    for y in range(407, 413):
        alpha[y, 92:386] = np.minimum(alpha[y, 92:386], 1.0 - (y - 407) / 6.0)
    f1 = clean_white((cells[1] * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    c2_s = shift_img(cells[2], 1, -4)
    f2 = clean_white((c2_s * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    return [f0, f1, f2, f1.copy()], str(src)


def build_0331() -> tuple[list[np.ndarray], str]:
    raw, src = load_before_webp("0331")
    f0 = raw[0].copy()
    f1_s = shift_img(raw[1], 4, 0)
    f2_s = shift_img(raw[2], 0, 28)
    alpha = np.ones((480, 480, 1), dtype=np.float32)
    alpha[350:] = 0.0
    for y in range(340, 350):
        alpha[y] = 1.0 - (y - 340) / 10.0
    f1 = clean_white((f1_s * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    f2 = clean_white((f2_s * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    return [f0, f1, f2, f1.copy()], src


def build_0488() -> tuple[list[np.ndarray], str]:
    src = BATCH_DIR / "0488-generated.png"
    cells = load_quadrants_480(src)
    f0 = cells[0].copy()
    alpha = np.zeros((480, 480, 1), dtype=np.float32)
    for y in range(480):
        for x in range(480):
            if x > 286 and y < 330:
                alpha[y, x] = 1.0
            elif y < 258 and x > 225 + max(0, (y - 175) * 0.45):
                alpha[y, x] = 1.0
    alpha = cv2.GaussianBlur(alpha, (9, 9), 0)[:, :, None]
    c1_s = shift_img(cells[1], 2, 0)
    c2_s = shift_img(cells[2], -18, 9)
    f1 = clean_white((c1_s * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    f2 = clean_white((c2_s * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    return [f0, f1, f2, f1.copy()], str(src)


def build_0332() -> tuple[list[np.ndarray], str]:
    raw, src = load_before_webp("0332")
    f0 = shift_img(raw[0], 0, 6)
    f1_s = shift_img(raw[1], -1, 6)
    f2_s = shift_img(raw[2], 1, 7)
    alpha = np.ones((480, 480, 1), dtype=np.float32)
    alpha[335:] = 0.0
    for y in range(325, 335):
        alpha[y] = 1.0 - (y - 325) / 10.0
    f1 = clean_white((f1_s * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    f2 = clean_white((f2_s * alpha + f0 * (1.0 - alpha)).round().astype(np.uint8))
    return [f0, f1, f2, f1.copy()], src


ANCHOR_SPECS = {
    "0474": {
        "top_pullup_bar": (210, 20, 415, 80),
        "right_upright_post": (365, 80, 415, 455),
        "lower_rack_base": (315, 340, 442, 460),
    },
    "0328": {
        "rear_bench_foot": (25, 360, 140, 455),
        "front_bench_leg": (280, 340, 365, 455),
        "planted_feet": (345, 380, 452, 472),
    },
    "0475": {
        "left_top_joint": (82, 11, 145, 85),
        "right_top_joint": (315, 18, 366, 110),
        "hands_bar": (140, 15, 290, 65),
    },
    "0329": {
        "rear_bench_foot": (35, 360, 150, 425),
        "front_bench_base": (220, 405, 335, 455),
        "planted_legs_feet": (305, 355, 442, 462),
    },
    "0476": {
        "left_top_joint": (82, 5, 145, 80),
        "right_top_joint": (340, 15, 396, 110),
        "hands_bar": (150, 15, 300, 70),
    },
    "0330": {
        "rear_bench_foot": (330, 370, 430, 440),
        "front_bench_base": (115, 370, 225, 460),
        "planted_feet": (50, 385, 195, 465),
    },
    "0484": {
        "head_floor": (22, 335, 92, 418),
        "resting_hand_floor": (180, 412, 340, 434),
        "planted_feet_floor": (386, 365, 456, 428),
    },
    "0331": {
        "rear_bench_strut": (81, 290, 215, 398),
        "front_bench_base": (225, 395, 345, 455),
        "left_foot": (245, 425, 315, 475),
        "right_leg_foot": (375, 345, 463, 470),
    },
    "0488": {
        "front_base_foot": (65, 405, 155, 465),
        "rear_base_foot": (360, 410, 435, 465),
        "ankle_rollers_legs": (52, 235, 220, 445),
    },
    "0332": {
        "left_leg_foot": (170, 335, 232, 472),
        "right_foot": (255, 415, 305, 472),
        "shins_knees": (175, 335, 305, 472),
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
        "0474": build_0474,
        "0328": build_0328,
        "0475": build_0475,
        "0329": build_0329,
        "0476": build_0476,
        "0330": build_0330,
        "0484": build_0484,
        "0331": build_0331,
        "0488": build_0488,
        "0332": build_0332,
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
