# Batch 120 Review Evidence (`20270106_review120`)

## Selection & Sources
- Inspected 10 unreviewed records: `1634`, `1635`, `1636`, `1637`, `1638`, `1639`, `1640`, `1641`, `1642`, `1643`.
- Upstream dataset: `exercises_1324` entries (`1634..1643`), visually verified against `contact-1.jpg`, `contact-2.jpg`, and native-resolution decoded crops (`1638`, `1641`, `1643`).

## Decisions (0 Approved, 10 Deferred)
- `1634` (`平凳仰卧龙门架绳索弯举`): 10-frame non-compliant WebP (`L:14, R:14`) -> deferred. Added `required_equipment_zh: ["平板训练凳"]`, clarified head-toward-pulley supine setup.
- `1635` (`牧师凳龙门架绳索单臂反握弯举`): 10-frame non-compliant WebP (`L:13`) -> deferred. Fixed critical `"反平板"` mistranslation (`isHold=true` false positive -> `false`), set `required_equipment_zh: ["牧师凳"]`, retained `"单臂"` (`perSide=true`).
- `1636` (`站姿龙门架高位绳索过头弯举`): 10-frame WebP with distorted Frame 3 head jump -> deferred. Replaced contradictory "elbows at sides" step with overhead upper-arm stability cue.
- `1637` (`坐瑜伽球龙门架绳索过头弯举`): 10-frame non-compliant WebP (`L:14, R:14`) -> deferred. Removed parentheses, added `required_equipment_zh: ["瑜伽球"]`.
- `1638` (`站姿龙门架高位直杆下拉弯举`): 2-frame WebP with impossible downward/foot-clipping cable bounce in Frame 2 -> deferred.
- `1639` (`牧师凳龙门架绳索锤式弯举`): 10-frame non-compliant WebP (`L:14, R:14`) -> deferred. Added `required_equipment_zh: ["牧师凳"]` and renamed from vague `"凳上"`.
- `1640` (`牧师凳龙门架绳索单臂锤式弯举`): 10-frame non-compliant WebP (`L:14, R:14`) -> deferred. Fixed `"手掌朝上"` step to neutral hammer grip (`掌心向内`), added `["牧师凳"]`, retained `"单臂"`.
- `1641` (`直立凳坐姿龙门架绳索弯举`): 10-frame non-compliant WebP (`L:14, R:13`) -> deferred. Added `required_equipment_zh: ["直立靠背训练凳"]` matching upright-back bench shown.
- `1642` (`平凳正坐龙门架绳索单臂集中弯举`): 10-frame non-compliant WebP (`R:12`) -> deferred. Added `required_equipment_zh: ["平板训练凳"]`, retained `"单臂"`, distinct from angled `1631`.
- `1643` (`直立凳坐姿龙门架高位绳索过头弯举`): 10-frame WebP with severe Frame 4 double-head ghosting artifact -> deferred. Replaced copy-pasted side-curl step with high-pulley seated overhead curl steps and `["直立靠背训练凳"]`.
