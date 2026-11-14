#!/usr/bin/env python3
"""Register and validate Batch 15 (20260923_review15) candidate animations."""
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


def build_0499() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0499")
    f1 = shift_img(f1, -12, -1)
    f2 = shift_img(f2, -3, -1)
    # Lock stationary left rack uprights above legs (y <= 215, x <= 185) and right rack base strictly below body (y >= 290, x >= 305)
    for target in (f1, f2):
        target[:215, :185] = f0[:215, :185]
        target[290:, 305:] = f0[290:, 305:]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "left_rack_uprights": (15, 10, 175, 210),
        "right_rack_base": (308, 292, 465, 455),
    }
    return frames, anchors


def build_0346() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0346")
    f1 = shift_img(f1, 2, 0)
    f2 = shift_img(f2, 0, 28)
    # Lock stationary flat bench and lower body below torso (y >= 285)
    for target in (f1, f2):
        target[285:, :] = f0[285:, :]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "planted_legs_and_feet": (10, 290, 150, 460),
        "bench_frame_and_supports": (155, 320, 465, 455),
    }
    return frames, anchors


def build_0347() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0347")
    f1 = shift_img(f1, -18, 0)
    f2 = shift_img(f2, 0, 1)
    # Lock stationary left feet and left bench support strictly above/left of dumbbells (y <= 410, x <= 190)
    for target in (f1, f2):
        target[:410, :190] = f0[:410, :190]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "planted_feet_left": (5, 250, 88, 385),
        "left_bench_support": (88, 275, 188, 405),
    }
    return frames, anchors


def build_0348() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0348")
    f1 = shift_img(f1, 1, 0)
    # Lock stationary central bench base (x=150..330, y >= 332) and central silver post strictly between dumbbells (x=228..252, y=185..332)
    for target in (f1, f2):
        target[332:, 150:330] = f0[332:, 150:330]
        target[185:332, 228:252] = f0[185:332, 228:252]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "central_bench_column": (228, 188, 252, 330),
        "bench_floor_base": (152, 335, 328, 455),
    }
    return frames, anchors


def build_0349() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0349")
    f2 = shift_img(f2, 0, 20)
    # Lock stationary left bench support & head (x <= 112) and right planted legs & bench support (x >= 312)
    for target in (f1, f2):
        target[:, :112] = f0[:, :112]
        target[:, 312:] = f0[:, 312:]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "left_bench_and_head": (5, 210, 110, 455),
        "right_planted_legs_and_bench": (314, 220, 475, 435),
    }
    return frames, anchors


def build_0508() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0508")
    f1[:, :10] = 255  # Clean original left-border 3px smudge before shifting
    f1 = shift_img(f1, 21, 0)
    f2 = shift_img(f2, 16, 6)
    # Lock stationary pelvis, thighs, calves, and planted feet (x >= 252)
    for target in (f1, f2):
        target[:, 252:] = f0[:, 252:]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "pelvis_and_thighs": (254, 215, 355, 385),
        "calves_and_planted_feet": (356, 225, 470, 385),
    }
    return frames, anchors


def build_0350() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0350")
    f2 = shift_img(f2, 0, 20)
    # Lock stationary left head/bench (x <= 88, y <= 315) and right lower body + bench (x >= 245, y >= 255)
    for target in (f1, f2):
        target[:315, :88] = f0[:315, :88]
        target[255:, 245:] = f0[255:, 245:]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "left_head_and_bench_edge": (5, 195, 86, 312),
        "right_planted_legs_and_bench": (250, 275, 475, 465),
    }
    return frames, anchors


BUILDERS = {
    "0499": build_0499,
    "0346": build_0346,
    "0347": build_0347,
    "0348": build_0348,
    "0349": build_0349,
    "0508": build_0508,
    "0350": build_0350,
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

    keys = list(BUILDERS.keys())
    for page, subset in enumerate([keys[:4], keys[4:]], 1):
        contact = Image.new("RGB", (1200, 1300), "#ffffff")
        draw = ImageDraw.Draw(contact)
        for j, xid in enumerate(subset):
            draw.text((8, j * 325 + 6), f"{xid} FIXED", fill="black")
            for f in range(4):
                pf = Image.open(B / f"{xid}-fixed-{f}.png").resize((300, 300))
                contact.paste(pf, (f * 300, j * 325 + 25))
        contact.save(B / f"contact-fixed-{page}.jpg", quality=95)
    print(json.dumps(validation, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
