#!/usr/bin/env python3
"""Register Batch 44 candidate 1659 with integer shifts, 800/380/800/380 ms loop, and anchor verification."""
from pathlib import Path
import json
import struct
import numpy as np
from PIL import Image, ImageDraw, ImageSequence

B = Path(__file__).resolve().parent
R = B.parents[2]
W, H = 480, 480
DURATIONS = [800, 380, 800, 380]

CANDIDATES = {
    "1659": {
        "shifts": [(0, -2), (0, -2), (0, -2), (0, -2)],
        "anchors": {
            "ball_bottom": (145, 345, 260, 445),
            "foot_left": (195, 395, 275, 474),
            "foot_right": (300, 390, 395, 474),
            "head_crown": (195, 6, 255, 65),
        },
    },
}


def ncc_at(ref_gray, tgt_gray, box, dx, dy):
    x0, y0, x1, y1 = box
    h, w = ref_gray.shape
    xx0, yy0, xx1, yy1 = x0 + dx, y0 + dy, x1 + dx, y1 + dy
    if xx0 < 0 or yy0 < 0 or xx1 > w or yy1 > h:
        return -1.0
    a = ref_gray[y0:y1, x0:x1]
    b = tgt_gray[yy0:yy1, xx0:xx1]
    sa, sb = a.std(), b.std()
    if sa < 1e-3 or sb < 1e-3:
        return 0.0
    return float(((a - a.mean()) * (b - b.mean())).mean() / (sa * sb))


def best_shift(ref_gray, tgt_gray, box, radius=8):
    best_sc, bdx, bdy = -1.0, 0, 0
    sc0 = ncc_at(ref_gray, tgt_gray, box, 0, 0)
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            sc = ncc_at(ref_gray, tgt_gray, box, dx, dy)
            if sc > best_sc:
                best_sc, bdx, bdy = sc, dx, dy
    return bdx, bdy, best_sc, sc0


report = {}
strip = Image.new("RGB", (W * 4, H), (255, 255, 255))

for idx, (eid, cfg) in enumerate(CANDIDATES.items()):
    src = R / f"app/src/main/res/raw/dataset_motion_{eid}.webp"
    orig_frames = [f.convert("RGB") for f in ImageSequence.Iterator(Image.open(src))]
    assert len(orig_frames) == 4 and all(f.size == (W, H) for f in orig_frames)
    shifts = cfg["shifts"]
    out_frames = []
    for fi in range(4):
        src_i = 1 if fi == 3 else fi
        dx, dy = shifts[fi]
        canvas = Image.new("RGB", (W, H), (255, 255, 255))
        canvas.paste(orig_frames[src_i], (dx, dy))
        out_frames.append(canvas)

    arrs = [np.asarray(f, dtype=np.float32) for f in out_frames]
    grays = [a.mean(axis=2) for a in arrs]
    fg = [int((a.min(axis=2) < 245).sum()) for a in arrs]
    assert np.array_equal(arrs[1], arrs[3]), f"{eid}: Frame 4 must equal Frame 2"
    for fi, a in enumerate(arrs):
        m = a.min(axis=2) < 245
        assert not (m[0].any() or m[-1].any() or m[:, 0].any() or m[:, -1].any()), f"{eid} F{fi} touches border"

    max_res = 0.0
    min_sc0 = 1.0
    anchor_detail = {}
    for aname, box in cfg["anchors"].items():
        anchor_detail[aname] = {}
        for fi in (0, 2):
            bdx, bdy, bsc, sc0 = best_shift(grays[1], grays[fi], box)
            res = (bdx ** 2 + bdy ** 2) ** 0.5
            max_res = max(max_res, res)
            min_sc0 = min(min_sc0, sc0)
            anchor_detail[aname][f"F{fi}"] = {
                "best_dx": bdx,
                "best_dy": bdy,
                "best_score": round(bsc, 4),
                "score_at_0": round(sc0, 4),
                "residual_px": round(res, 2),
            }

    assert max_res <= 2.0, f"{eid} max_res={max_res}"
    assert min_sc0 >= 0.96, f"{eid} min_sc0={min_sc0}"

    out_webp = B / f"{eid}-fixed.webp"
    out_frames[0].save(
        out_webp,
        format="WEBP",
        save_all=True,
        append_images=out_frames[1:],
        duration=DURATIONS,
        loop=0,
        lossless=True,
    )

    raw_webp = out_webp.read_bytes()
    re_durs = []
    pos = 12
    while pos < len(raw_webp):
        tag = raw_webp[pos:pos + 4]
        sz = struct.unpack("<I", raw_webp[pos + 4:pos + 8])[0]
        if tag == b"ANMF":
            re_durs.append(int.from_bytes(raw_webp[pos + 20:pos + 23], "little"))
        pos += 8 + sz + (sz & 1)
    reopened = Image.open(out_webp)
    re_frames = [f.convert("RGB") for f in ImageSequence.Iterator(reopened)]
    assert len(re_frames) == 4 and re_durs == DURATIONS
    assert np.array_equal(np.asarray(re_frames[1]), np.asarray(re_frames[3]))

    for fi, f in enumerate(re_frames):
        strip.paste(f, (fi * W, idx * H))
    draw = ImageDraw.Draw(strip)
    draw.text((8, idx * H + 8), f"{eid} FIXED", fill=(0, 0, 0))

    report[eid] = {
        "status": "passed",
        "frames": 4,
        "size": [W, H],
        "durations_ms": DURATIONS,
        "frame4_equals_frame2": True,
        "max_anchor_residual_px": round(max_res, 2),
        "min_anchor_match_score": round(min_sc0, 4),
        "foreground_pixels": fg,
        "fg_preserved": True,
        "anchors": anchor_detail,
    }

strip.save(B / "contact-fixed-1.jpg", quality=92)
print(json.dumps(report, ensure_ascii=False, indent=2))
