# Batch 124 Review Evidence (`20270110_review124`)

## Selection & Sources
- Inspected 10 unreviewed records: `1749`, `1750`, `1751`, `1752`, `1754`, `1755`, `1756`, `1758`, `1767`, `2135`.
- Inspected `selected.json`, `contact-1.jpg`, `contact-2.jpg`, frame counts, and margins across all 10 WebPs (5 with 10 frames, 5 with 2 frames; every single one also fails `>= 15px` borders).

## Approved Candidates (`0`)
- None approved in Batch 124: zero 4-frame WebPs exist in this batch, and multiple frames show severe visual defects (`1749` bar disappears in F1-F3, `1750` sliced extra ball under bench, `1754` floating halo, `1758` severed floating arm/chest torso in F3, `2135` floating bottom-left bar smudge).

## Deferred Decisions (10 Deferred -> `待修图`)
- `1749` (`站姿曲杆杠铃颈后臂屈伸`): 10 frames (`T:8, B:13`); empty fists in F1-F3 until barbell suddenly teleports clipped in F4.
- `1750` (`平凳仰卧药球胸前上抛`): 10 frames (`L:12, R:14`) with chopped stray ball under flat bench; added `required_equipment_zh: ["平板训练凳"]`, fixed `"健身球"` -> `"药球"`.
- `1751` (`站姿深蹲架安全销杠铃推举`): 10 frames (`T:12, B:12`), F4 clips top; fixed steps to reflect standing power-rack overhead pin press.
- `1752` (`史密斯机上斜训练凳仰卧臂屈伸`): 2 frames (`T:14, B:14`) with bottom-left marks; added `required_equipment_zh: ["上斜训练凳"]`.
- `1754` (`平凳负重置片双臂反屈伸`): 10 frames (`L:13, R:14`), halo over head in F3; fixed severe mistranslation `"三凳俯卧撑"`, added `required_equipment_zh: ["平板训练凳"]`.
- `1755` (`平凳负重宽腿坐缘反屈伸`): 2 frames (`L:14, R:14`); fixed mistranslation `"三头肌下压"`, added `required_equipment_zh: ["平板训练凳"]`.
- `1756` (`杠铃单腿硬拉`): 2 frames (`L:14, R:14`); cleared hold trigger words from steps while preserving `"单腿"` (`perSide=true`).
- `1758` (`稳固踏台辅助仰卧起坐`): 10 frames (`L:14, R:14`) with severe F3 chopped chest/arm glitch; added `required_equipment_zh: ["稳固踏台"]`.
- `1767` (`高双杠负重臂屈伸`): 2 frames (`T:14, B:14`); fixed mistranslation `"三头肌下压（高双杠）"`, added `required_equipment_zh: ["双杠"]`, removed parentheses.
- `2135` (`负重平板支撑`): 2 frames (`L:14, R:14`) with floating bottom-left smudge; verified legitimate `isHold=true` plank.
