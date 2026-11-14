# Batch 131 Review Evidence (`20270117_review131`)

## Selection & Sources
- Inspected 10 unreviewed records: `3144`, `3194`, `3195`, `3200`, `3235`, `3236`, `3237`, `3281`, `3286`, `3290`.
- Inspected `selected.json`, `contact-1.jpg`, `contact-2.jpg`, 4-frame strips `frames_3144.png` & `frames_3236.png`, RIFF `ANMF` durations, borders, pixel drift, and anchor stability metrics across all 10 WebPs.
- Candidate reference & local provenance for `3144`:
  - `https://spotebi.com/exercise-guide/` (floor-seated resistance band row form & neutral-spine pulling mechanics)
  - `assets/motion_repairs/20260910/prompts.json#3144` & `assets/motion_repairs/20260910/manifest.json#3144`

## Approved Candidate (`1`)
- `3144` (`阻力带坐姿直背划船`, `resistance band seated straight back row`): 480×480 native 4-frame anatomical loop (`[800, 380, 800, 380] ms`, `2.36s`, `F2 == F4` `max_diff=0`), pure white background (`[255, 255, 255]` on all 4 corners), generous margins across every frame (`L>=36, R>=43, T>=67, B=89`), floor contact anchored within `<= 1px` (`y>=390 IoU=1.0000`, heels/glutes static), clean coral-red lats & mid-back highlights, and removed `"保持"` static word from instructions.

## Deferred Decisions (9 Deferred -> `待修图`)
- `3194` (`弗兰肯斯坦杠铃前平举深蹲`): 2-frame red-wall gym photo (`bg0=[248,249,242]`, `0px` margins); clarified shoulder-shelf hold without `"保持"`.
- `3195` (`固定器械俯卧双上单下腿弯举`): 10 frames (`L:14, R:13`); fixed machine steps wrongly stating `"坐在靠背上"` to prone leg curl setup, removed `"（杠杆）/支撑/保持"`.
- `3200` (`固定器械三角把俯身划船`): 2 frames (`L:14, R:12`); fixed non-existent `"调整座椅高度"` step to standing bent-over stance and replaced `"V 形杆"` with `"三角握把"`.
- `3235` (`平凳俯卧龙门架绳索反助腿弯举`): 10 frames (`L:14, R:12`) with chopped bottom equipment fragments on every frame; set `required_equipment_zh: ["平板训练凳"]`, fixed `"缆绳机/腿筋/长凳"`.
- `3236` (`跪姿阻力带臀前推`): 4 frames fail off-white `bg0=[253,253,253]`, margins `T:12, B:13`, F3 kneeling shins levitating in mid-air (`iou370=0.4748`), and `(female)` mismatch against male art.
- `3237` (`地雷管单臂站姿侧平举`): 2 frames (`L:14, R:12`); fixed `"地雷"` mistranslation, added `"单臂"` (`perSide=True`).
- `3281` (`史密斯机全蹲`): 2 frames (`L:14, R:14`); standardized full-squat steps and removed `"保持"`.
- `3286` (`单杠负重双力臂`): 2 frames (`T:14, B:14`); fixed `"负重肌上"` mistranslation and bogus palm-reversal transition cue, set `required_equipment_zh: ["单杠"]`.
- `3290` (`单杠负重单臂引体向上`): 2 frames (`T:12, B:14`); added `"单臂"` (`perSide=True`), clarified non-working arm position, set `required_equipment_zh: ["单杠"]`.
