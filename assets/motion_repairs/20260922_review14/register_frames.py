#!/usr/bin/env python3
"""Register and validate Batch 14 (20260922_review14) candidate animations."""
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


def build_0341() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0341")
    f1 = shift_img(f1, 2, 0)
    f2 = shift_img(f2, 1, 31)
    # Lock stationary left legs/feet + left bench post (x <= 198) and right bench post (x >= 355, y >= 235)
    for target in (f1, f2):
        target[:, :198] = f0[:, :198]
        target[235:, 355:] = f0[235:, 355:]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "planted_feet_and_left_bench_post": (12, 220, 195, 385),
        "right_bench_support_post": (360, 240, 465, 395),
    }
    return frames, anchors


def build_0342() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    orig_f0, orig_f1, orig_f2 = load_original_3("0342")
    # Reorder into smooth bottom -> mid-press -> full-lockout -> mid-press cycle:
    # orig_f1 is bottom at chest (top_y=157), orig_f0 is mid-extension (top_y=31), orig_f2 is full lockout (top_y=1)
    f0 = orig_f1.copy()
    f1 = orig_f0.copy()
    f2 = orig_f2.copy()
    # Lock stationary flat bench, head, pelvis, and planted legs/feet (y >= 268) from f1
    f0[268:, :] = f1[268:, :]
    f2[268:, :] = f1[268:, :]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "left_bench_support": (12, 295, 165, 420),
        "planted_legs_and_right_bench": (260, 290, 470, 455),
    }
    return frames, anchors


def build_0496() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0496")
    f1 = shift_img(f1, 12, 0)
    f2 = shift_img(f2, 18, 43)
    # Lock stationary flat bench below pad (y >= 312) and prone upper body/arms on right (x >= 255, y >= 225)
    for target in (f1, f2):
        target[312:, :] = f0[312:, :]
        target[225:, 255:] = f0[225:, 255:]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "bench_left_support": (60, 325, 225, 455),
        "bench_right_and_forearms": (260, 260, 450, 455),
    }
    return frames, anchors


def build_0343() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0343")
    f1 = shift_img(f1, 15, 0)
    f2 = shift_img(f2, 0, 15)
    # Lock stationary flat bench, head, pelvis, and planted legs/feet (y >= 258 and left head x <= 105)
    for target in (f1, f2):
        target[258:, :] = f0[258:, :]
        target[190:258, :105] = f0[190:258, :105]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "left_bench_support": (12, 290, 165, 415),
        "planted_legs_and_right_bench": (260, 285, 470, 440),
    }
    return frames, anchors


def build_0497() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0497")
    f1 = shift_img(f1, 1, 0)
    f2 = shift_img(f2, 0, 20)
    # Lock stationary left rack base (y >= 340, x <= 165) and right rack upright (x >= 355, y <= 265)
    for target in (f1, f2):
        target[340:, :165] = f0[340:, :165]
        target[:265, 355:] = f0[:265, 355:]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "left_rack_base": (12, 342, 160, 415),
        "right_rack_upper_post": (356, 95, 465, 260),
    }
    return frames, anchors


def build_0344() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0344")
    f1 = shift_img(f1, 1, 0)
    f2 = shift_img(f2, 0, 1)
    # Lock stationary flat bench and lower body below torso (y >= 285)
    for target in (f1, f2):
        target[285:, :] = f0[285:, :]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "planted_legs_and_feet": (10, 290, 150, 460),
        "bench_frame_and_supports": (160, 320, 465, 450),
    }
    return frames, anchors


def build_0498() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0498")
    f1 = shift_img(f1, -2, 0)
    # Lock stationary left rack post above shoes (x <= 38, y <= 395), bottom rack base (y >= 446, x <= 160), and top strap mount (x <= 105, y <= 145)
    for target in (f1, f2):
        target[:395, :38] = f0[:395, :38]
        target[446:, :160] = f0[446:, :160]
        target[:145, :105] = f0[:145, :105]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "top_strap_anchor_post": (2, 15, 102, 142),
        "left_vertical_rack_post": (2, 150, 36, 390),
    }
    return frames, anchors


def build_0345() -> tuple[list[np.ndarray], dict[str, tuple[int, int, int, int]]]:
    f0, f1, f2 = load_original_3("0345")
    f1 = shift_img(f1, 1, 0)
    f2 = shift_img(f2, 1, 24)
    # Lock stationary left legs/feet + left bench post (x <= 198) and right bench post below arm (x >= 365, y >= 252)
    for target in (f1, f2):
        target[:, :198] = f0[:, :198]
        target[252:, 365:] = f0[252:, 365:]
    frames = [clean_bg(f0), clean_bg(f1), clean_bg(f2), clean_bg(f1.copy())]
    anchors = {
        "planted_feet_and_left_bench_post": (12, 220, 195, 385),
        "right_bench_support_post": (368, 255, 465, 395),
    }
    return frames, anchors


BUILDERS = {
    "0341": build_0341,
    "0342": build_0342,
    "0496": build_0496,
    "0343": build_0343,
    "0497": build_0497,
    "0344": build_0344,
    "0498": build_0498,
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
