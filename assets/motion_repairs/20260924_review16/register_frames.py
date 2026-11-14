#!/usr/bin/env python3
"""Register and validate Batch 16 (20260924_review16) candidate animations."""
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


def build_0351() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0351")
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "planted_legs_and_feet": (10, 290, 155, 455),
        "bench_frame_and_supports": (155, 315, 465, 455),
    }
    return frames, anchors


def build_0352() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    im = Image.open(B / "0352-generated.jpg").convert("RGB")
    w, h = im.size
    hw, hh = w // 2, h // 2
    q0 = clean_bg(np.array(im.crop((0, 0, hw, hh)).resize((480, 480), Image.Resampling.LANCZOS), dtype=np.uint8))
    q1 = clean_bg(np.array(im.crop((hw, 0, w, hh)).resize((480, 480), Image.Resampling.LANCZOS), dtype=np.uint8))
    q2 = clean_bg(np.array(im.crop((0, hh, hw, h)).resize((480, 480), Image.Resampling.LANCZOS), dtype=np.uint8))
    q2 = shift_img(q2, 0, -19)
    frames = [clean_bg(q0), clean_bg(q1), clean_bg(q2), clean_bg(q1.copy())]
    anchors = {
        "planted_feet_and_legs": (10, 290, 145, 455),
        "flat_bench_base": (220, 315, 465, 435),
        "bench_head_support": (310, 250, 455, 325),
    }
    return frames, anchors


def build_0353() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0353")
    f1 = shift_img(f1, 2, 0)
    f2 = shift_img(f2, 0, 2)
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "left_planted_foot_and_shin": (30, 260, 145, 445),
        "right_planted_foot_and_shin": (295, 260, 420, 445),
        "stability_ball_base": (140, 345, 300, 425),
    }
    return frames, anchors


def build_0354() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0354")
    f1 = shift_img(f1, 2, 0)
    f2 = shift_img(f2, 0, -1)
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "planted_feet_on_floor": (105, 380, 260, 465),
        "thighs_and_calves": (130, 220, 275, 380),
        "torso_head_and_bracing_hand": (285, 115, 415, 295),
    }
    return frames, anchors


def build_0570() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0570")
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "left_bench_leg": (20, 325, 110, 445),
        "right_bench_leg": (210, 325, 310, 445),
    }
    return frames, anchors


def build_0355() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0355")
    f1 = shift_img(f1, -13, 0)
    f2 = shift_img(f2, -18, -1)
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "left_planted_foot": (155, 415, 210, 472),
        "right_planted_foot": (220, 415, 270, 472),
        "lower_legs_stance": (160, 320, 270, 415),
    }
    return frames, anchors


BUILDERS = {
    "0351": build_0351,
    "0352": build_0352,
    "0353": build_0353,
    "0354": build_0354,
    "0570": build_0570,
    "0355": build_0355,
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
    for page, subset in enumerate([keys[:3], keys[3:]], 1):
        contact = Image.new("RGB", (1200, 1000), "#ffffff")
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
