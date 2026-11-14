# Batch 132 Review Evidence (`20270118_review132`)

## Selection & Sources
- Inspected 10 unreviewed records: `3305`, `3312`, `3313`, `3562`, `3563`, `3641`, `3642`, `3643`, `3644`, `3666`.
- Inspected `selected.json`, `contact-1.jpg`, `contact-2.jpg`, frame counts, RIFF `ANMF` durations, borders, and IoU metrics across all 10 WebPs (7 with 2 frames, 3 with 10 frames, 0 compliant 4-frame WebPs).

## Approved Candidates (`0`)
- None approved in Batch 132: all 10 WebPs fail frame count (`2` or `10` frames) and margins (`< 15px`), with `3641` containing a pair of severed bare feet chopped at the top border, `3642` containing a large jagged white cutout inside the front knee/quadriceps in Frame 3, and `3563` showing cable stack shift (`iou370=0.7606`) and a faint shoulder blur in Frame 4.

## Deferred Decisions (10 Deferred -> `待修图`)
- `3305` (`站姿杠铃深蹲推举`): 2 frames (`T:14, B:14`); disambiguated thruster from standard barbell shoulder press.
- `3312` (`高单杠负重标准双力臂`): 2 frames (`T:14, B:14`); fixed `"负重肌上（杠上）"` mistranslation, set `required_equipment_zh: ["单杠"]`.
- `3313` (`双杠负重前倾偏胸臂屈伸`): 2 frames (`T:13, B:14`); fixed `"负重直杠下压"` mistranslation, aligned parallel-bar depiction with `required_equipment_zh: ["双杠"]`.
- `3562` (`平凳上背仰靠双腿杠铃臀桥`): 10 frames (`L:14, R:14`); fixed `"双腿放凳"` mistranslation, removed `"（男）"`, set `required_equipment_zh: ["平板训练凳"]`.
- `3563` (`站姿龙门架绳索单臂下拉`): 10 frames (`L:14, R:14`, `iou370=0.7606`) + F4 shoulder smudge; kept `"单臂"` (`perSide=True`).
- `3641` (`跪姿双臂负重直臂上摆`): 2 frames (`T:12, B:14`) with severed upside-down feet artifact at top edge; corrected static-kneeling swing steps.
- `3642` (`负重弓步伸展`): 10 frames (`T:12, B:14`, `iou370=0.6551`) + severe F3 white cutout missing chunk on front knee/quad.
- `3643` (`高脚杯式负重哥萨克侧蹲`): 2 frames (`T:13, B:14`); removed `"（男）"` and `"保持"`.
- `3644` (`负重箭步蹲前摆`): 2 frames (`T:14, B:12`); clarified simultaneous lunge + front swing, removed `"保持"`.
- `3666` (`斜坡跑步机步行`): 2 frames (`L:14, R:14`); set `required_equipment_zh: ["跑步机"]` and fixed `"使其冷却"`/`"保持"`.
