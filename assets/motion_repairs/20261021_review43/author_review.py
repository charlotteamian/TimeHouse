#!/usr/bin/env python3
"""Author Batch 43 review updates, pending notes, sources, code baseline, and QA spec (all 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261021_review43"
VERSION = "1.2.48"
VERSION_CODE = 2026102101

inspected = ["1773", "1651", "1774", "1652", "1775", "1653", "2271", "1654", "2298", "1655"]
review_candidates = []
registered_media = []

definition_updates = {
    "1773": {
        "name_zh": "单臂立柱绕毛巾划船",
        "category": "back",
        "equipment": "body weight",
        "target": "upper back",
        "muscle_group": "upper back",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": ["毛巾", "稳固立柱"],
        "instructions_zh": [
            "将长毛巾中段绕在稳固立柱约腰胸高度，双脚与肩同宽微曲膝稳站立于立柱后侧，工作手单臂正握毛巾两端、非工作臂自然下垂。",
            "保持背部挺直与核心收紧，屈髋微前倾使手臂先向前伸展拉直毛巾。",
            "呼气启动肩胛后缩与上背肌群，沿腰腹方向顺势单臂将毛巾拉向胸肋旁。",
            "在顶点略作停顿后吸气缓慢伸臂放回起始伸展位，完成一侧次数后换另一只手臂。",
        ],
    },
    "1651": {
        "name_zh": "交替转体弓步哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩同宽自然站立，双手掌心朝前各握一只哑铃垂放体侧。",
            "一侧脚向前跨出下蹲成前后分腿弓步位，同时顺势将双臂哑铃向上弯举至肩前并轻微向同侧转体收紧核心。",
            "下放哑铃并蹬地收回前脚回到直立位，随即跨另一条腿向相反方向交替重复。",
        ],
    },
    "1774": {
        "name_zh": "单侧侧卧抬髋外展举腿",
        "category": "upper legs",
        "equipment": "body weight",
        "target": "abductors",
        "muscle_group": "glutes",
        "secondary_muscles": ["glutes", "obliques"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "侧卧于地面，双腿并拢伸直叠放，下侧前臂贴地屈肘置于肩关节正下方，上侧手轻扶叉腰。",
            "收紧侧腹与臀中肌发力将髋部抬离地面，使头肩髋踝呈斜直线。",
            "骨盆保持正对前方不后仰，向上方尽可能抬高上侧直腿，短暂停顿后受控下放并在完成后换边。",
        ],
    },
    "1652": {
        "name_zh": "单腿抬起瑜伽球坐姿哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms", "shoulders"],
        "required_equipment_zh": ["瑜伽球"],
        "instructions_zh": [
            "端坐在瑜伽球顶部中央，一侧脚稳踩地面、另一条腿伸直抬离地面维持水平稳定，双手掌心朝前持哑铃自然下垂。",
            "保持上臂贴靠身体两侧不动，呼气同时向上弯举哑铃至接近肩前。",
            "顶点停顿感受肱二头肌收紧后吸气缓慢放回伸展位，完成规定次数后换另一条腿抬起重复。",
        ],
    },
    "1775": {
        "name_zh": "单侧侧卧抬髋内收举腿",
        "category": "upper legs",
        "equipment": "body weight",
        "target": "adductors",
        "muscle_group": "adductors",
        "secondary_muscles": ["obliques", "glutes"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "侧卧于地面，双腿并拢伸直，下侧小臂横贴地面、手肘位于肩正下方，上侧手扶腰稳定身体。",
            "启动核心发力将髋部略微抬起呈稳定侧桥位，随后保持下侧腿蹬稳，上侧直腿顺势向上方抬起延展。",
            "在最高点短暂停顿后缓慢放回贴近下方腿位，完成目标次数后换边进行。",
        ],
    },
    "1653": {
        "name_zh": "单侧鹤立单脚点地哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "直立站稳并保持单侧支撑脚实踩地面，另一条腿微向后撤以脚尖轻点地面维持平衡，双手掌心朝前各握哑铃垂放体侧。",
            "维持大臂靠近躯干两侧稳定不动，呼气双臂发力将哑铃弯举至肩前高位。",
            "在顶点略作停顿后吸气缓慢受控下放还原，完成组次后换支撑腿重复。",
        ],
    },
    "2271": {
        "name_zh": "拳击站姿单侧左平勾拳",
        "category": "shoulders",
        "equipment": "body weight",
        "target": "delts",
        "muscle_group": "delts",
        "secondary_muscles": ["biceps", "triceps", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "前后分腿呈拳击格斗站姿站稳，膝盖微屈，双手握拳贴护于下颌与面颊两侧。",
            "前脚脚掌微旋发力配合髋肩拧转，顺势抬起左侧屈肘向正前方水平挥出左平勾拳。",
            "击出至最高发力点后迅速沿原路径收拳护颌回到备战起始位，完成目标次数后换侧练习。",
        ],
    },
    "1654": {
        "name_zh": "站姿反握哑铃弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与髋同宽自然站直，双手掌心朝后反握一对哑铃自然垂放于大腿前外侧。",
            "维持上臂固定贴近躯干两侧，呼气发力同时向上弯举哑铃至接近肩前水平。",
            "顶峰略作停顿感受小臂前外侧与肱二头肌发力后吸气缓慢下放回垂臂起姿。",
        ],
    },
    "2298": {
        "name_zh": "平凳仰卧正手自重反向划船",
        "category": "back",
        "equipment": "body weight",
        "target": "upper back",
        "muscle_group": "upper back",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "在平板训练凳下方仰卧伸直双腿以脚跟着地，头部靠近凳垫下方并向上伸出双臂以略宽于肩正手握稳凳面边缘。",
            "先保持双臂伸直使背部轻贴近地面准备，核心收紧保持肩髋踝呈直线。",
            "呼气发力收缩上背与肩胛骨，屈肘顺势将胸口向上拉向平板训练凳下缘，顶点停顿后吸气缓慢放回低位。",
        ],
    },
    "1655": {
        "name_zh": "哑铃弯举复合深蹲",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "biceps",
        "secondary_muscles": ["forearms", "quadriceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩同宽站立，双手掌心朝前各握一只哑铃垂放体侧。",
            "吸气向后推髋屈膝下蹲至大腿接近水平，同时顺势屈肘向上弯举一对哑铃至胸肩前高度。",
            "在深蹲与弯举顶点短暂停顿后发力蹬地站直，并同步有控制地放回哑铃回到起始站姿。",
        ],
    },
}

pending = {
    "1773": "待修图 · 立柱底座与站在地面双脚跨帧水平间距缩放 9-18 px（bottom F0 -18 / F2 -9 vs head 0），无法刚性平移对齐，已补充毛巾与稳固立柱及上背目标，待重制。",
    "1651": "待修图 · 前跨弓步与直立起始态双脚位置大幅重定位（bottom sc0=0.0661/0.1756），已清除原名括号注释并完善交替动作细节，待重制。",
    "1774": "待修图 · 侧桥外展过程 F2 髋部与双腿大幅抬高离开地面（bottom sc0=-0.0058），已避静态触发词并核正髋外展肌群与单侧计次，待重制。",
    "1652": "待修图 · 经 F1 (+17,0)、F2 (0,+3) 对齐球底与踩地脚后 F2 头顶仍产生 +4 px 垂向偏移（head_crown sc0=0.6042 < 0.96，max_res=4.12 px），已补充瑜伽球与单腿计数，待重制。",
    "1775": "待修图 · F1 触及左边缘 1 px 且 F2 抬髋及举腿大幅偏移（bottom sc0=0.0892），已修正“侧平板”静态触发名并核正内收肌群与单侧计次，待重制。",
    "1653": "待修图 · 前脚与后脚点地间距及垂向高度跨帧偏移（head_crown sc0=0.7385 < 0.96，max_res=2.24 px），已修正鹤立单侧计数，待重制。",
    "2271": "待修图 · 出拳转身旋髋带动脚底位移 9-11 px（bottom +14/-3 vs head +3/0），已规范命名并核正三角肌目标与单侧计次，待重制。",
    "1654": "待修图 · 经 F1 (+10,0) 对齐左脚及头顶后，右脚仍在 F1 较 F0/F2 横扩 2 px（foot_right sc0=0.7478/0.7612 < 0.96），站距形变无法整体配准，待重制。",
    "2298": "待修图 · 反向划船 F2 身体与脚跟大跨度上升拉向凳底（bottom F2 sc0=0.0563），已补充平板训练凳与上背肌群并去除悬挂静态触发词，待重制。",
    "1655": "待修图 · F0/F1 双脚裁底 35/37 px、F2 顶部见哑铃残影 33 px（y=0），同时补充原上游缺失的下蹲要领与股四头肌协同标注，待重制。",
}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"])

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review43-20261021",
    "inspected": inspected,
    "review_candidates": review_candidates,
    "registered_media": registered_media,
    "definition_updates": definition_updates,
    "pending": pending,
    "sources": {},
    "review_notes": {},
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
    "expected_checks": 16,
    "expected_reviewed_after_approve": reviewed_count,
    "expected_per_side_ids": ["1773", "1774", "1652", "1775", "1653", "2271"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
