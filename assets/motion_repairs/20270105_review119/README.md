# Batch 119 Review Evidence (`20270105_review119`)

## Selection & Sources
- Inspected 10 unreviewed records: `1616`, `1625`, `1626`, `1627`, `1628`, `1629`, `1630`, `1631`, `1632`, `1633`.
- Upstream dataset: `exercises_1324` entries (`1616, 1625..1633`), visually verified against `contact-1.jpg`, `contact-2.jpg`, and per-frame decoded PNGs.

## Decisions (0 Approved, 10 Deferred)
- `1616` (`器械坐姿反握牧师凳弯举`, biceps): original 2-frame WebP (`[1180, 1180]` ms) -> deferred (`待修图`). Fixed contradicting upstream step ("手掌朝上") to match overhand/pronated palms-down grip shown in illustration; cleared `muscle_group`.
- `1625` (`史密斯机上斜窄握卧推`, triceps): original 2-frame WebP -> deferred (`待修图`). Illustration clearly depicts a 35–45° incline bench with feet flat on the floor rather than a decline bench; corrected `name_zh`, set `required_equipment_zh: ["上斜训练凳"]`, and rewrote steps accurately.
- `1626` (`史密斯机下斜反握窄距卧推`, pectorals): original 2-frame WebP -> deferred (`待修图`). Replaced awkward `"反下斜"` literal translation, set `required_equipment_zh: ["带勾脚的下斜训练凳"]`, cleared `muscle_group`.
- `1627` (`曲杆杠铃牧师凳窄握弯举`, biceps): non-compliant 10-frame `[900, 70*4, 900, 70*4]` WebP -> deferred (`待修图`). Added `required_equipment_zh: ["牧师凳"]`, removed English `"ez "` in steps, clarified resting triceps side of upper arms on pad.
- `1628` (`曲杆杠铃牧师凳蜘蛛弯举`, biceps): non-compliant 10-frame WebP with tight right margin (`R:13 < 15`) -> deferred (`待修图`). Replaced `"曲杆蜘蛛卷"` mistranslation (`卷` -> `弯举`), added `required_equipment_zh: ["牧师凳"]` matching the vertical side of the preacher bench shown (removing hallucinated stability ball option).
- `1629` (`站姿杠铃宽握弯举`, biceps): non-compliant 10-frame WebP (`B:12 < 15`) -> deferred (`待修图`). Standardized Chinese name and clear palms-forward wide-grip steps.
- `1630` (`站姿龙门架绳索窄握弯举`, biceps): non-compliant 10-frame WebP (`T:12 < 15`) -> deferred (`待修图`). Standardized Chinese name and clear steps.
- `1631` (`平凳坐姿龙门架绳索单臂集中弯举`, biceps): non-compliant 10-frame WebP -> deferred (`待修图`). Added `"单臂"` to trigger `perSide=true`, added `required_equipment_zh: ["平板训练凳"]` matching seated bench in illustration.
- `1632` (`站姿龙门架绳索拖拽弯举`, biceps): original 2-frame WebP -> deferred (`待修图`). Fixed generic curl step to describe dragging bar straight up torso with elbows gliding back.
- `1633` (`牧师凳龙门架绳索单臂弯举`, biceps): non-compliant 10-frame WebP -> deferred (`待修图`). Fixed critical mistranslation where `"平板"` (for `"preacher"`) falsely triggered `ExerciseTempo` isometric `isHold=true`! Renamed to `"牧师凳龙门架绳索单臂弯举"` (`isHold=false`, `perSide=true`) and set `required_equipment_zh: ["牧师凳"]`.
