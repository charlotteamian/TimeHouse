# Batch 128 Review Evidence (`20270114_review128`)

## Selection & Sources
- Inspected 10 unreviewed records: `2371`, `2399`, `2404`, `2405`, `2406`, `2407`, `2414`, `2432`, `2459`, `2464`.
- Inspected `selected.json`, `contact-1.jpg`, `contact-2.jpg`, frame counts, RIFF `ANMF` durations, borders, and IoU metrics across all 10 WebPs (8 with 10 frames, 2 with 2 frames, 0 compliant 4-frame WebPs).

## Approved Candidates (`0`)
- None approved in Batch 128: all 10 WebPs fail frame-count (`10` or `2` frames) and border (`< 15px`) gates, with `2406` & `2414` failing lower-edge static registration (`iou370=0.7949` / `0.889`), `2407` showing top-edge stray debris and a cambered bar instead of straight barbell, `2414` showing a bottom-cropped barbell fragment in Frames 1–3, and `2459` using an outdoor 2-frame photograph instead of anatomical 4-frame vector art.

## Deferred Decisions (10 Deferred -> `待修图`)
- `2371` (`着地屈膝负重球俄罗斯转体`): 10 frames (`L:12, R:14`); removed `"（第二式）"` and `"重物"`, disambiguated from `0845`/`0846`.
- `2399` (`坐姿龙门架绳索单侧转体`): 10 frames (`L:14, R:13`); fixed `"缆绳机/电缆"`, added `"单侧"` for unilateral `perSide`, removed `"保持"`.
- `2404` (`站姿护肘托板曲杆弯举`): 10 frames (`T:12, B:14`); fixed `"ez/手臂冲击波"`, unified `"护肘托板"`, removed `"保持"`.
- `2405` (`护肘托板绳索三角把下压`): 2 frames (`T:12, B:14`); removed Latin `"V"`, fixed `"电缆机/保持"`, unified `"护肘托板"`.
- `2406` (`护肘托板绳索反握曲杆下压`): 10 frames (`L:12, R:14`, `iou370=0.7949`); fixed misstated `"直杆"` to `"曲杆"` and unified `"护肘托板"`.
- `2407` (`站姿护肘托板杠铃弯举`): 10 frames (`T:12, B:12`), stray top debris & EZ-bar mismatch; fixed `"弯举哑铃"` and `"臂膀器/手臂冲击波"`.
- `2414` (`站姿单臂杠铃集中弯举`): 10 frames (`T:12, B:12`, `iou370=0.889`), bottom chopped barbell fragment & dumbbell-like grip; added `"单臂"` for `perSide`.
- `2432` (`平凳仰卧曲杆杠铃窄握卧推`): 10 frames (`L:12, R:13`); set `required_equipment_zh: ["平板训练凳"]`, removed `"保持"`.
- `2459` (`翻轮胎`): 2-frame outdoor photo (`bg0=[248,249,242]`, `0px` margins); standardized steps and removed `"保持"`.
- `2464` (`坐姿龙门架蒂博多单臂划船`): 10 frames (`L:14, R:14`); clarified floor-seated single D-handle unilateral row and added `"单臂"` for `perSide`.
