# Batch 129 Review Evidence (`20270115_review129`)

## Selection & Sources
- Inspected 10 unreviewed records: `2611`, `2612`, `2616`, `2736`, `2741`, `2798`, `2799`, `2800`, `2810`, `2987`.
- Inspected `selected.json`, `contact-1.jpg`, `contact-2.jpg`, frame counts, RIFF `ANMF` durations, borders, and IoU metrics across all 10 WebPs (7 with 10 frames, 3 with 2 frames, 0 compliant 4-frame WebPs).

## Approved Candidates (`0`)
- None approved in Batch 129: all 10 fail frame count (`10` or `2`) and borders (`< 15px`), with `2612` showing a chopped oval at the top edge of every frame, `2736` switching grip and showing a floating black oval overhead in Frame 4, `2741` showing a shoulder whiteout distortion and trailing glute smudge, and `2798` leaving a chopped black floor dome under the shin in Frame 2.

## Deferred Decisions (10 Deferred -> `待修图`)
- `2611` (`器械水平单腿倒蹬`): 10 frames (`L:12, R:14`, `iou370=0.9118`); fixed both-feet setup steps, kept `"单腿"` `perSide=True`.
- `2612` (`跳绳`): 10 frames (`T:14, B:12`, `iou370=0.9411`), chopped top-edge oval fragment across all frames.
- `2616` (`龙门架坐姿三角把高位下拉`): 10 frames (`T:12, B:14`); removed space and `"V/v/保持/电缆/护膝"`.
- `2736` (`固定器械反握高位下拉`): 10 frames (`T:14, B:14`), F1–F3/F4 grip inconsistency + behind-neck shift & overhead floating oval artifact.
- `2741` (`站姿曲杆宽握弯举`): 10 frames (`T:14, B:12`), F3 deltoid pinch & F4 rear black strap smudge.
- `2798` (`杠铃深蹲跳接后撤箭步蹲`): 2 frames (`T:14, B:14`), missing jump apex + bottom chopped dome cap under F2 shin.
- `2799` (`平凳坐姿杠铃负重交替抬腿`): 10 frames (`L:12, R:14`); set `required_equipment_zh: ["平板训练凳"]`, removed `"保持"`.
- `2800` (`平凳坐姿女性杠铃交替抬腿`): 2 frames (`L:14, R:14`); set `required_equipment_zh: ["平板训练凳"]`, removed `"（女）"` and `"支撑/保持"`.
- `2810` (`站姿杠铃单腿前后分腿下蹲`): 2 frames (`T:14, B:14`); added `"单腿"` (`perSide=True`), removed `"（第二式）"` and `"保持"`.
- `2987` (`单杠负重窄握反手引体向上`): 10 frames (`T:14, B:13`, `iou370=0.9535`); fixed `"（吊环架）/站在俯卧撑前面"` mistranslation and set `required_equipment_zh: ["单杠"]`.
