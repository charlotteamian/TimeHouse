# Batch 121 Review Evidence (`20270107_review121`)

## Selection & Sources
- Inspected 10 unreviewed records: `1644`, `1645`, `1682`, `1683`, `1701`, `1705`, `1707`, `1708`, `1709`, `1710`.
- Upstream & clinical reference: `exercises_1324` (`1644..1710`), visually inspected via `contact-1.jpg`, `contact-2.jpg`, and native 4-frame strip `frames_1705.png`; `1705` aligned with WorkoutLabs Bosu Ball Squats (`https://workoutlabs.com/exercise-guide/bosu-ball-squats/`) and ACE/NASM dome-up squat cues.

## Approved Candidate (`1705` -> `已完成`)
- `1705` (`半圆平衡球深蹲`, `squat on bosu ball`): native 480×480 4-frame WebP (`durations=[800, 380, 800, 380]`, `F4 == F2 mae=0.00`), pure white background, clean borders (`L:170, R>=86, T>=33, B>=42`), dome-up Bosu ball & grounded feet locked (`y>=370 IoU(F1,F2)=0.9956`, `IoU(F1,F3)=0.9891`), zero artifacts, red muscle highlight matches `quads` (`target: "quads"`) + `glutes`/`hamstrings`/`calves`. Standardized `博苏球` -> `半圆平衡球`, added counterbalance arms-forward cue, cleared `muscle_group`.

## Deferred Decisions (9 Deferred -> `待修图`)
- `1644` (`蹲姿龙门架绳索弯举`): 10-frame non-compliant WebP (`L:14, R:14`).
- `1645` (`上斜凳坐姿龙门架绳索双臂弯举`): 10-frame non-compliant WebP (`L:14, R:12`); added `required_equipment_zh: ["上斜训练凳"]`.
- `1682` (`平凳坐姿曲杆杠铃窄握集中弯举`): 2-frame WebP with cropped stray EZ bar artifact along bottom edge; added `required_equipment_zh: ["平板训练凳"]`, removed English `EZ`.
- `1683` (`史密斯机站姿弯举`): 2-frame non-compliant WebP (`T:14, B:14`).
- `1701` (`药球窄距俯卧撑`): 2-frame non-compliant WebP; removed `"高平板支撑"`/`"健身球"` wording errors in steps.
- `1707` (`瑜伽球俯卧转体挺身`): 4-frame WebP fails border (`R:1` in F1, **`R:0` hand clipped** in F3) and ball anchor stability (`y>=370 IoU(F1,F3)=0.2063 < 0.96`).
- `1708` (`仰卧绳带单腿小腿拉伸`): 2-frame WebP with bottom black shadow smudge artifact; added `"单腿"` (`perSide=true`).
- `1709` (`仰卧穿针抱膝单侧臀肌拉伸`): 2-frame WebP with whole-body horizontal flip between F1 & F2; added `"单侧"` (`perSide=true`).
- `1710` (`仰卧单膝抱胸单侧臀中肌与梨状肌拉伸`): 2-frame WebP (`L:14, R:14`); fixed completely mismatched figure-4 upstream copy-paste instructions to match straight opposite leg + single knee hugged to chest, added `"单侧"` (`perSide=true`).
