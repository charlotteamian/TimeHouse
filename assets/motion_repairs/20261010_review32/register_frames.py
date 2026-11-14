#!/usr/bin/env python3
"""Register and validate Batch 32 (20261010_review32) candidate animation (1367)."""
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


def build_1367() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("1367")
    f0 = shift_img(f0, 0, 3)
    f1 = shift_img(f1, 16, 3)
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "rack_bottom_left": (55, 370, 120, 465),
        "rack_bottom_right": (355, 370, 425, 465),
        "rack_top_left": (55, 10, 120, 100),
        "rack_top_right": (360, 10, 425, 100),
    }
    return frames, anchors


BUILDERS = {
    "1367": build_1367,
}


def measure_anchor(ref: np.ndarray, cur: np.ndarray, box: tuple[int, int, int, int], search: int = 8):
    x1, y1, x2, y2 = box
    patch = ref[y1:y2, x1:x2].astype(np.int16)
    err0 = float(np.abs(patch - cur[y1:y2, x1:x2].astype(np.int16)).mean())
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
    score_at_0 = round(1.0 - err0 / 255.0, 4)
    return {"dx": dx, "dy": dy, "residual_px": round(res, 2), "score": score_at_0}


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

    contact = Image.new("RGB", (1200, 350), "#ffffff")
    draw = ImageDraw.Draw(contact)
    for j, xid in enumerate(BUILDERS.keys()):
        draw.text((8, j * 325 + 6), f"{xid} FIXED", fill="black")
        for f in range(4):
            pf = Image.open(B / f"{xid}-fixed-{f}.png").resize((300, 300))
            contact.paste(pf, (f * 300, j * 325 + 25))
    contact.save(B / "contact-fixed-1.jpg", quality=95)
    print(json.dumps(validation, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
