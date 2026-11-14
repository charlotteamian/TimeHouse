#!/usr/bin/env python3
"""Author Batch 40 review updates, pending notes, sources, code baseline, and QA spec."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261018_review40"
VERSION = "1.2.45"
VERSION_CODE = 2026101801

inspected = ["1604", "1441", "1686", "1459", "1687", "1617", "1688", "1618", "1689", "1619"]
review_candidates = ["1441"]
registered_media = ["1441"]

definition_updates = {
    "1604": {
        "name_zh": "单侧世界最伟大拉伸",
        "category": "upper legs",
        "equipment": "body weight",
        "target": "hamstrings",
        "muscle_group": "hamstrings",
        "secondary_muscles": ["glutes", "quadriceps", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "从深弓步位开始，一脚向前迈出踩稳地面，另一腿向后伸直，双手撑于前脚内侧。",
            "下放后侧膝盖轻落地面并伸直前腿，感受前腿后侧腘绳肌充分拉伸。",
            "随后前腿屈膝踩稳，向同侧旋转躯干并将同侧手臂垂直举向天花板。",
            "在伸展顶点停顿片刻后慢慢收回手掌，再换另一侧腿向前重复拉伸。",
        ],
    },
    "1441": {
        "name_zh": "平凳坐姿哑铃单臂反握腕弯举",
        "category": "lower arms",
        "equipment": "dumbbell",
        "target": "forearms",
        "muscle_group": "forearms",
        "secondary_muscles": ["wrist extensors", "brachialis"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "稳坐在平板训练凳一侧，双脚分开平踩地面维持重心，非工作手轻搭在同侧大腿上。",
            "工作侧手掌朝下正握一只哑铃，将前臂平铺贴稳在平板训练凳上，手腕自然探出训练凳边缘。",
            "保持前臂紧贴凳面不动，呼气时向上背伸抬起手腕，将哑铃弯举至最高处。",
            "在顶点略作停顿后吸气缓慢下放哑铃回到起始伸展位，完成目标次数后换另一侧手臂。",
        ],
    },
    "1686": {
        "name_zh": "自重深蹲过头转体伸展",
        "category": "upper legs",
        "equipment": "body weight",
        "target": "quads",
        "muscle_group": "quadriceps",
        "secondary_muscles": ["glutes", "hamstrings", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "站立准备，双脚分开与肩同宽，脚尖略微外展。",
            "屈膝并向后推髋下蹲至大腿接近水平，同时双臂向前平举维持平衡。",
            "蹬地站起时将双臂顺势伸直举过头顶并舒展转体，下蹲回落后再换向交替伸展。",
        ],
    },
    "1459": {
        "name_zh": "哑铃罗马尼亚硬拉",
        "category": "upper legs",
        "equipment": "dumbbell",
        "target": "glutes",
        "muscle_group": "hamstrings",
        "secondary_muscles": ["hamstrings", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩同宽站稳，双手正握一对哑铃垂放于大腿前侧，背部挺直核心收紧。",
            "保持膝盖微屈并顺着屈髋轨迹向后推臀，令哑铃紧贴双腿前侧缓慢下放。",
            "当感受臀部与腘绳肌充分拉长后，双脚脚跟稳蹬地面并收紧臀腿推髋起身站直。",
        ],
    },
    "1687": {
        "name_zh": "交替后撤弓步过头伸展",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "abs",
        "secondary_muscles": ["glutes", "hamstrings", "quadriceps", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与髋同宽自然站立，双臂垂放于身体两侧。",
            "一脚向后撤步并以脚掌着地，顺势屈膝下沉至前后分腿弓步位。",
            "下蹲的同时保持核心稳定并将双臂直举过头顶拉长腹前侧，短暂停顿后发力收回前脚站立并换边交替。",
        ],
    },
    "1617": {
        "name_zh": "下斜训练凳单臂锤式哑铃推举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "triceps",
        "muscle_group": "triceps",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": ["带勾脚的下斜训练凳"],
        "instructions_zh": [
            "仰卧在带勾脚的下斜训练凳上，双脚稳妥固定在勾脚滚筒下方，非工作手轻放于体侧腹旁。",
            "工作手掌心朝内锤握哑铃于胸肩上方，吸气屈肘下放并让大臂贴近躯干。",
            "呼气集中肱三头肌与胸肩力量向上垂直推起至手臂伸直，按节奏下放并在完成后换臂。",
        ],
    },
    "1688": {
        "name_zh": "交替前跨弓步转体",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "abs",
        "secondary_muscles": ["quadriceps", "glutes", "hamstrings"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩同宽站立，双手轻合抱于胸前。",
            "一脚向前跨步并屈膝下沉成稳固弓步位，保持躯干直立。",
            "下蹲到底部时收紧腹斜肌向同侧旋转躯干，随后回正蹬地起身站立并换另一条腿交替。",
        ],
    },
    "1618": {
        "name_zh": "瑜伽球上斜仰卧锤式哑铃推举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "triceps",
        "muscle_group": "triceps",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": ["瑜伽球"],
        "instructions_zh": [
            "先坐在瑜伽球上双手锤握哑铃，双脚前移带动背部沿球面滚动，直到上背部与肩颈稳靠在瑜伽球上方成上斜仰姿。",
            "双脚与肩同宽稳踩地面稳定骨盆，双手掌心相对将哑铃置于胸肩两侧。",
            "呼气将双臂向上推起并微向内聚拢至伸直锁定，吸气有控制地屈肘放回起始位。",
        ],
    },
    "1689": {
        "name_zh": "自重低位推拉俯卧撑",
        "category": "chest",
        "equipment": "body weight",
        "target": "pectorals",
        "muscle_group": "pectorals",
        "secondary_muscles": ["triceps", "deltoids"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "以高位俯卧撑起姿准备，双手略宽于肩压稳地面，核心收紧使肩髋膝呈一条直线。",
            "屈肘将胸部贴近地面后保持低位贴地做小幅前后推拉游移，随后再发力撑掌向上推起回到起始高位。",
        ],
    },
    "1619": {
        "name_zh": "上斜训练凳单臂锤式哑铃推举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "triceps",
        "muscle_group": "triceps",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": ["上斜训练凳"],
        "instructions_zh": [
            "靠坐在上斜训练凳上，双脚分开踩实地面，非工作手轻搭同侧大腿保持躯干稳定。",
            "工作手掌心朝内锤握哑铃，先由垂臂起姿稳步提至肩前预备位，再垂直向上推起至手臂完全伸直。",
            "顶部停顿片刻后有控制地屈肘下放回落至肩侧起始位，完成次数后换边。",
        ],
    },
}

pending = {
    "1604": "待修图 · F0 触及下底边 21 px 且 F2 指尖裁顶 27 px 并见 y=0 残留鬼影，且后膝落地前腿伸展属动态迁移，已修订单侧最伟大拉伸资料，待重制。",
    "1686": "待修图 · F0 双脚触及底边 34 px、F2 双手裁顶 33 px 且下蹲与站姿足宽大幅跳变（bottom_band sc0=0.0053），已核正深蹲过头转体伸展资料，待重制。",
    "1459": "待修图 · F0/F1 双脚裁底 39 px、F2 见顶部 y=0 哑铃鬼影（top=38 px）且各帧脚踝站姿水平漂移，已核正哑铃罗马尼亚硬拉资料，待重制。",
    "1687": "待修图 · F0 足底触边 9 px、F2 指尖裁顶 11 px，且后撤弓步与站姿双脚位移显著（bottom_band sc0=-0.0962），已完善交替后撤弓步过头伸展资料，待重制。",
    "1617": "待修图 · 下斜板脚与滚筒经 F1 (+8,0)、F2 (0,+21) 配准后仍存在 F2 头部抬离偏移 2 px（head sc0=0.8644 < 0.96）及右支架滚筒匹配低于 0.96（0.9597），已补充带勾脚下斜训练凳与单臂资料，待重制。",
    "1688": "待修图 · 站立与前跨弓步双脚重心和膝距大幅变化（bottom_band sc0=0.0247/0.0899），已完善交替前跨弓步转体及核心目标资料，待重制。",
    "1618": "待修图 · F0 足底裁底 20 px、F2 哑铃裁顶 43 px，且瑜伽球与前脚水平位移分歧 3 px（+11 vs +14）、头部仰角偏移 4-5 px（sc0=0.6644），已补充瑜伽球必需器械，待重制。",
    "1689": "待修图 · F0 右趾触边 9 px、F1 左趾触边 6 px，且俯卧推拉过程手脚支点沿地面滑动无法整体配准，已修正机器直译并清晰化步骤，待重制。",
    "1619": "待修图 · F0/F1 触及底边、F2 同时触及顶边 21 px 与底边 43 px，且 F2 头部下移 +19 px 与上斜凳支脚 +10 px 产生 9 px 垂向背离，已核正上斜训练凳单臂推举资料，待重制。",
}

sources = {
    "1441": "https://raw.githubusercontent.com/exercemus/exercises/minified/exercises.json#dumbbell_over_bench_one_arm_reverse_wrist_curl"
}

review_notes = {
    "1441": "来源为 exercemus/exercises 公开动作库 1441（dumbbell over bench one arm reverse wrist curl）。纠偏原名并按动作图示补充平板训练凳必需器械、前臂/腕伸肌目标肌群及单臂分段计次；经 F2 (0, +1) 纯整数垂直平移配准并锁定 800/380/800/380 ms 四帧循环（F4=F2），纯白背景无边缘截断，平凳左右支脚、双脚与头部五大锚点对齐残差均 ≤ 1.0 px（匹配分 ≥ 0.9714）。"
}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
before_reviews["reviewed"]  # validate file exists
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review40-20261018",
    "inspected": inspected,
    "review_candidates": review_candidates,
    "registered_media": registered_media,
    "definition_updates": definition_updates,
    "pending": pending,
    "sources": sources,
    "review_notes": review_notes,
    "image_generation_calls": 0,
    "generated_images_imported": 0,
}
(B / "review-result.json").write_text(json.dumps(review_result, ensure_ascii=False, indent=2) + "\n")

code_paths = [
    "app/src/main/java",
    "scripts/validate_exercise_dataset.sh",
    "scripts/build_android_debug.sh",
]
baseline = {}
for rel in code_paths:
    p = R / rel
    if p.is_file():
        baseline[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    else:
        for f in sorted(p.rglob("*")):
            if f.is_file():
                baseline[str(f.relative_to(R))] = hashlib.sha256(f.read_bytes()).hexdigest()
(B / "code-baseline.json").write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n")

qa_spec = {
    "batch": BATCH_ID,
    "expected_checks": 10,
    "expected_reviewed_after_approve": reviewed_count,
    "candidate_id": "1441",
    "candidate_required_equipment": ["平板训练凳"],
    "expected_per_side_ids": ["1604", "1441", "1617", "1619"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
