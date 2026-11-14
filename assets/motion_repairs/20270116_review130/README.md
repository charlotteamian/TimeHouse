# Batch 130 Review Evidence (`20270116_review130`)

## Selection & Sources
- Inspected 10 unreviewed records: `3006`, `3007`, `3010`, `3017`, `3116`, `3117`, `3122`, `3123`, `3124`, `3142`.
- Inspected `selected.json`, `contact-1.jpg`, `contact-2.jpg`, and all seven 4-frame strips (`frames_3006.png`, `frames_3007.png`, `frames_3116.png`, `frames_3117.png`, `frames_3122.png`, `frames_3123.png`, `frames_3124.png`), frame counts, RIFF `ANMF` durations, borders, and IoU metrics.

## Approved Candidates (`0`)
- None approved in Batch 130: although 7 assets have 4 frames (`[800, 380, 800, 380]`), every single one fails margins (`< 15px`) and 6 fail both pure-white `bg0` and `y>=370` anchor registration (`iou370=0.3999–0.7333` with shrunken/shifted figures, chairs, benches, and anchor poles), while the remaining 3 (`3010`, `3017`, `3142`) have only 2 frames and `< 15px` borders.

## Deferred Decisions (10 Deferred -> `待修图`)
- `3006` (`阻力带坐姿髋外展`): 4 frames fail off-white `bg0=[254,255,254]`, margins `T:14, B:12`, and F3 jump (`iou370=0.4573`); removed `"支撑"`.
- `3007` (`稳固立柱阻力带站姿单腿直腿前伸`): 4 frames fail `T:14` and severe pole/figure shift (`iou370=0.3999`); set `required_equipment_zh: ["稳固立柱"]`, added `"单腿"` (`perSide=True`), aligned steps to standing straight-leg hip flexion shown.
- `3010` (`平凳仰卧曲杆弯臂过顶拉举`): 2 frames (`L:14, R:14`); fixed `"下拉"` mistranslation to pullover, set `required_equipment_zh: ["平板训练凳"]`, removed `"EZ/保持"`.
- `3017` (`杠铃潘德利划船`): 2 frames (`T:14, B:14`); clarified floor-reset reps and removed `"保持"`.
- `3116` (`高位锚定弹力带站姿反握下拉`): 4 frames fail off-white `bg0=[253,253,253]` and ceiling anchor top margin `T:9`; replaced `"固定背"` and removed `"保持"`.
- `3117` (`平凳坐姿高位锚定弹力带窄握下拉`): 4 frames fail off-white `bg0=[253,253,254]`, margins `T:4, B:11`, and F1/F3 bench drift (`iou370=0.7333`); fixed `"面向乐队"` mistranslation, set `required_equipment_zh: ["平板训练凳"]`.
- `3122` (`平凳坐姿阻力带推肩`): 4 frames fail off-white `bg0=[252,253,253]`, top margin `T:5`, and F3 shrunk/shifted bench (`iou370=0.4977`); set `required_equipment_zh: ["平板训练凳"]`.
- `3123` (`平凳坐姿阻力带弯举`): 4 frames fail off-white `bg0=[253,253,255]`, `T:14, B:2`, missing handles in F1, and F3 shift (`iou370=0.5585`); set `required_equipment_zh: ["平板训练凳"]`.
- `3124` (`直立靠背凳坐姿阻力带胸推`): 4 frames fail `bg0=[254,254,253]`, `L:9, R:13, T:12`, and F3 bench shift (`iou370=0.53`); set `required_equipment_zh: ["直立靠背训练凳"]`.
- `3142` (`史密斯机相扑宽距深蹲`): 2 frames (`T:14, B:14`); standardized sumo squat cueing and removed `"保持"`.
