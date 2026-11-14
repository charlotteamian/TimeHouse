# Batch 122 Review Evidence (`20270108_review122`)

## Selection & Sources
- Inspected 10 unreviewed records: `1712`, `1713`, `1714`, `1716`, `1717`, `1718`, `1719`, `1720`, `1721`, `1722`.
- Inspected source entries (`selected.json`), frame contact sheets (`contact-1.jpg`, `contact-2.jpg`), and frame count / border metrics for all 10 WebPs (7 with 10 frames, 3 with 2 frames).

## Approved Candidates (`0`)
- None approved in Batch 122: every WebP fails the mandatory 4-frame animation contract (`10` frames or `2` frames), and multiple entries exhibit severe border clipping or visual artifacts (`1714` horizontal 180-degree flip, `1716` black crescent debris above the forward stability ball, `1721` chopped stray feet/calves along `y=0..16`).

## Deferred Decisions (10 Deferred -> `待修图`)
- `1712` (`侧卧垫台单腿内收肌拉伸`): 10-frame non-compliant WebP (`L:14, R:12..14`); added `required_equipment_zh: ["稳固踏台"]` and `"单腿"` (`perSide=true`).
- `1713` (`俯卧手拉单腿股四头肌拉伸`): 2-frame non-compliant WebP (`R:14`); added `"单腿"` (`perSide=true`).
- `1714` (`俯卧单腿股直肌拉伸`): 2-frame WebP (`L:14`) with F1->F2 whole-body horizontal 180-degree flip; fixed upstream `category: "waist" -> "upper legs"`, `target: "abs" -> "quads"`, cleared `muscle_group`, added `"单腿"` (`perSide=true`).
- `1716` (`坐姿双瑜伽球胸大肌拉伸`): 10-frame WebP with floating black crescent debris above held ball in F3; added `required_equipment_zh: ["瑜伽球"]` and rewrote steps to match sitting on one ball while pressing hands on a second forward ball.
- `1717` (`蹲姿龙门架长绳划船`): 2-frame non-compliant WebP (`L:14, R:14`); stripped parenthetical `（带绳索附件）`.
- `1718` (`平凳坐姿杠铃窄握颈后臂屈伸`): 10-frame non-compliant WebP (`T:14, B:14`); added `required_equipment_zh: ["平板训练凳"]`, avoided hold trigger in name/steps.
- `1719` (`上斜训练凳杠铃窄握卧推`): 10-frame non-compliant WebP (`T:13, B:14`); added `required_equipment_zh: ["上斜训练凳"]`.
- `1720` (`平凳仰卧杠铃过头颅后臂屈伸`): 10-frame non-compliant WebP (`L:14, R:10..14`); added `required_equipment_zh: ["平板训练凳"]`.
- `1721` (`平凳仰卧杠铃反握臂屈伸`): 10-frame WebP (`L:14, R:14`) with chopped stray feet/calves at the top margin (`y=0..16`) of every frame; fixed mistranslated `"弯举"` -> `"臂屈伸"` to match `target: "triceps"`, added `required_equipment_zh: ["平板训练凳"]`.
- `1722` (`站姿龙门架高位绳索过头臂屈伸`): 10-frame non-compliant WebP (`R:12..14`); clarified facing-away overhead triceps extension steps.
