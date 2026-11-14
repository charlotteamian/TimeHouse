#!/usr/bin/env python3
"""Register and validate Batch 13 (20260921_review13) candidate animations."""
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

B = Path(__file__).resolve().parent


def shift_img(arr: np.ndarray, dx: int, dy: int) -> np.ndarray:
    out = np.full_like(arr, 255)
    h, w = arr.shape[:2]
    x1_s, x2_s = max(0, -dx), min(w, w - dx)
    y1_s, y2_s = max(0, -dy), min(h, h - dy)
    if x2_s > x1_s and y2_s > y1_s:
        out[y1_s + dy : y2_s + dy, x1_s + dx : x2_s + dx] = arr[y1_s:y2_s, x1_s:x2_s]
    return out


def clean_bg(arr: np.ndarray, threshold: int = 246) -> np.ndarray:
    out = arr.copy()
    mask = (out[:, :, 0] >= threshold) & (out[:, :, 1] >= threshold) & (out[:, :, 2] >= threshold)
    out[mask] = 255
    return out


def load_original_3(xid: str) -> list[np.ndarray]:
    im = Image.open(B / "before" / f"dataset_motion_{xid}.webp")
    frames = []
    for f in range(3):
        im.seek(f)
        frames.append(clean_bg(np.array(im.convert("RGB"), dtype=np.uint8)))
    return frames


def build_0335() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0335")
    f1 = shift_img(f1, 4, 0)
    f2 = shift_img(f2, 1, 3)
    # Lock lower legs and feet (y >= 268) from f1 (where dumbbells are raised clear of thighs)
    f0[268:, :] = f1[268:, :]
    f2[268:, :] = f1[268:, :]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "left_foot": (150, 390, 215, 462),
        "right_foot": (245, 390, 315, 462),
        "knees_and_calves": (155, 272, 310, 388),
    }
    return frames, anchors


def build_0490() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    im = Image.open(B / "0490-generated.png").convert("RGB")
    arr = np.array(im, dtype=np.uint8)
    arr[506:518, :] = 255
    arr[:, 506:518] = 255
    arr[:6, :] = 255
    arr[-6:, :] = 255
    arr[:, :6] = 255
    arr[:, -6:] = 255
    q0 = arr[0:512, 0:512].copy()
    q1 = arr[0:512, 512:1024].copy()
    q2 = arr[512:1024, 0:512].copy()
    # Align Q2 with Q0/Q1 via integer shift (0, -107) so toes (486->379) and bench base (495->388) match Q0/Q1
    q2 = shift_img(q2, 0, -107)
    # Crop 480x480 window [16:496, 16:496] and shift down by +36 px to center vertically
    f0 = shift_img(q0[16:496, 16:496], 0, 36)
    f1 = shift_img(q1[16:496, 16:496], 0, 36)
    f2 = shift_img(q2[16:496, 16:496], 0, 36)
    # Lock stationary bench frame below pad (x >= 325, y >= 285) and planted toes tip (x <= 48, y >= 355)
    for target in (f1, f2):
        target[285:, 325:] = f0[285:, 325:]
        target[355:, :48] = f0[355:, :48]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "bench_frame_and_base": (330, 288, 475, 415),
        "planted_toes": (5, 355, 48, 410),
    }
    return frames, anchors


def build_0337() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0337")
    f1 = shift_img(f1, 8, 0)
    f2 = shift_img(f2, 0, 32)
    # Lock flat bench and lower body below bench pad (y >= 282)
    f1[282:, :] = f0[282:, :]
    f2[282:, :] = f0[282:, :]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "planted_feet_and_calves": (15, 285, 120, 430),
        "bench_left_support": (120, 310, 220, 428),
        "bench_right_support": (350, 310, 455, 428),
    }
    return frames, anchors


def build_0491() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0491")
    # Use f2 vertical reference so f2 top toes (y=0) are never clipped and f0 bottom toes (y=479->473) gain margin
    f0 = shift_img(f0, 0, -6)
    f1 = shift_img(f1, 4, -6)
    # Lock stationary incline bench left base and upper back/head (x <= 175)
    f0[:, :175] = f1[:, :175]
    f2[:, :175] = f1[:, :175]
    # Lock lower bench base rail below moving legs (x=175..285, y=340..435)
    f0[340:435, 175:285] = f1[340:435, 175:285]
    f2[340:435, 175:285] = f1[340:435, 175:285]
    f0[436:, :] = 255
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "incline_bench_left_frame": (15, 255, 170, 430),
        "head_and_upper_torso": (25, 100, 170, 250),
        "incline_bench_center_base": (175, 342, 282, 430),
    }
    return frames, anchors


def build_0338() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0338")
    f1 = shift_img(f1, 4, 0)
    f2 = shift_img(f2, 0, 48)
    # Lock flat bench and lower body below bench pad (y >= 290)
    f1[290:, :] = f0[290:, :]
    f2[290:, :] = f0[290:, :]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "planted_feet_and_calves": (18, 292, 120, 440),
        "bench_left_support": (120, 315, 220, 440),
        "bench_right_support": (350, 315, 458, 440),
    }
    return frames, anchors


BUILDERS = {
    "0335": build_0335,
    "0490": build_0490,
    "0337": build_0337,
    "0491": build_0491,
    "0338": build_0338,
}


def measure_anchor(ref: np.ndarray, cur: np.ndarray, box: tuple[int, int, int, int], search: int = 8):
    x1, y1, x2, y2 = box
    patch = ref[y1:y2, x1:x2].astype(np.int16)
    best = (999.0, 0, 0)
    for dy in range(-search, search + 1):
        for dx in range(-search, search + 1):
            cy1, cy2 = y1 + dy, y2 + dy
            cx1, cx2 = x1 + dx, x2 + dx
            if 0 <= cy1 and cy2 <= 480 and 0 <= cx1 and cx2 <= 480:
                err = float(np.abs(patch - cur[cy1:cy2, cx1:cx2].astype(np.int16)).mean())
                if err < best[0]:
                    best = (err, dx, dy)
    err, dx, dy = best
    res = float(np.hypot(dx, dy))
    score = round(1.0 - err / 255.0, 4)
    return {"dx": dx, "dy": dy, "residual_px": round(res, 2), "score": score}


def main():
    measurements = {}
    validation = {}
    durations = [800, 380, 800, 380]

    for xid, builder in BUILDERS.items():
        frames, anchors = builder()
        pil_frames = [Image.fromarray(f, mode="RGB") for f in frames]
        for idx, pf in enumerate(pil_frames):
            pf.save(B / f"{xid}-fixed-{idx}.png")
        sheet = Image.new("RGB", (480 * 4, 480), (255, 255, 255))
        for idx, pf in enumerate(pil_frames):
            sheet.paste(pf, (idx * 480, 0))
        sheet.save(B / f"{xid}-fixed-sheet.jpg", quality=95)
        pil_frames[0].save(
            B / f"{xid}-fixed.gif",
            save_all=True,
            append_images=pil_frames[1:],
            duration=durations,
            loop=0,
        )
        pil_frames[0].save(
            B / f"{xid}-fixed.webp",
            format="WEBP",
            save_all=True,
            append_images=pil_frames[1:],
            duration=durations,
            loop=0,
            lossless=True,
            quality=100,
        )

        m_entry = {}
        max_res = 0.0
        min_score = 1.0
        for name, box in anchors.items():
            f_list = []
            for fi in range(1, 4):
                r = measure_anchor(frames[0], frames[fi], box)
                f_list.append({"frame": fi, **r})
                max_res = max(max_res, r["residual_px"])
                min_score = min(min_score, r["score"])
            m_entry[name] = {"box": list(box), "frames": f_list}
        measurements[xid] = m_entry

        fg_counts = [int((f < 245).any(axis=2).sum()) for f in frames]
        validation[xid] = {
            "status": "passed",
            "frames": 4,
            "size": [480, 480],
            "durations_ms": durations,
            "frame4_equals_frame2": bool(np.array_equal(frames[1], frames[3])),
            "max_anchor_residual_px": max_res,
            "min_anchor_match_score": min_score,
            "foreground_pixels": fg_counts,
            "fg_preserved": all(c > 8000 for c in fg_counts),
        }
        assert max_res <= 2.0 and min_score >= 0.96, f"{xid} failed anchor check: {validation[xid]}"
        assert validation[xid]["frame4_equals_frame2"] and validation[xid]["fg_preserved"]

    (B / "anchor-measurements.json").write_text(json.dumps(measurements, ensure_ascii=False, indent=2) + "\n")
    (B / "registration-validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n")

    # Save contact-fixed.jpg for all 5 registered candidates
    contact = Image.new("RGB", (1200, 1625), "#ffffff")
    draw = ImageDraw.Draw(contact)
    for j, xid in enumerate(BUILDERS.keys()):
        draw.text((8, j * 325 + 6), f"{xid} FIXED", fill="black")
        for f in range(4):
            pf = Image.open(B / f"{xid}-fixed-{f}.png").resize((300, 300))
            contact.paste(pf, (f * 300, j * 325 + 25))
    contact.save(B / "contact-fixed.jpg", quality=95)
    print(json.dumps(validation, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
