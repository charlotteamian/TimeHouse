# Batch 123 Review Evidence (`20270109_review123`)

## Selection & Sources
- Inspected 10 unreviewed records: `1723`, `1724`, `1725`, `1726`, `1727`, `1728`, `1744`, `1745`, `1747`, `1748`.
- Inspected `selected.json`, `contact-1.jpg`, `contact-2.jpg`, frame counts, borders, and bottom IoU metrics across all 10 WebPs (6 with 10 frames, 2 with 2 frames, and 2 non-compliant 4-frame WebPs).

## Approved Candidates (`0`)
- None approved in Batch 123: eight fail frame count (`10` or `2` frames), and the two 4-frame WebPs (`1744`, `1745`) fail border margins (`R:12, T:12` on `1744`; `T:4, B:0` on `1745`), base/ball stability (`iou370=0.8437` and `0.6924 < 0.96`), and pose sequencing/label fidelity.

## Deferred Decisions (10 Deferred -> `待修图`)
- `1723` (`站姿龙门架绳索单臂下压`): 10 frames (`T:14, B:14`); fixed upstream steps falsely referencing straight bar / barbell instead of single D-handle; added `"单臂"` (`perSide=true`).
- `1724` (`背站龙门架高位长绳过头臂屈伸`): 10 frames (`T:14, B:14`); standardized neutral rope grip and stance.
- `1725` (`上斜训练凳龙门架长绳过头臂屈伸`): 2 frames (`L:14, R:14`); fixed steps from standing to incline bench and added `required_equipment_zh: ["上斜训练凳"]`.
- `1726` (`仰卧垫面龙门架低位长绳臂屈伸`): 10 frames (`L:14, R:12`); clarified supine floor setup facing low pulley.
- `1727` (`站姿龙门架反握单臂过头臂屈伸`): 10 frames (`T:14, B:14`) with severed dangling cable debris floating mid-air in Frame 3; added `"单臂"` (`perSide=true`).
- `1728` (`俯身龙门架双臂臂后屈伸`): 10 frames (`L:14, R:13`) with stray horizontal sliver floating at `y=67..71` above head; added missing hip-hinge bent-over torso cue.
- `1744` (`瑜伽球双臂反屈伸`): 4 frames failing borders (`R:12, T:12`), foot/ball stability (`iou370=0.8437`), and broken alternating pose loop (`F1==F3` return).
- `1745` (`坐瑜伽球单臂哑铃三头肌负重拉伸`): 4 frames failing borders (`T:4, B:0`), ball shift (`iou370=0.6924`), and equipment/pose fidelity — re-classified `equipment: "dumbbell"` with `required_equipment_zh: ["瑜伽球"]` and `"单臂"` (`perSide=true`).
- `1747` (`瑜伽球坐姿曲杆杠铃颈后臂屈伸`): 10 frames (`T:13, B:14`); added `required_equipment_zh: ["瑜伽球"]` and removed Latin `EZ`.
- `1748` (`平凳仰卧曲杆杠铃窄握颈后臂屈伸`): 2 frames (`T:14, B:14`) with severe Frame 2 anatomical deformity (bar placed over groin with missing left arm instead of behind head); added `required_equipment_zh: ["平板训练凳"]`, stripped parens/`ez`.
