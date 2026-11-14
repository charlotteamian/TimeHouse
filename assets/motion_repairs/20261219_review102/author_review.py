#!/usr/bin/env python3
"""Author Batch 102 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261219_review102"
VERSION = "1.2.107"
VERSION_CODE = 2026121901

inspected = ["0971", "0972", "0974", "0975", "0976", "0977", "0978", "0979", "0980", "0981"]
review_candidates = []
registered_media = []

definition_updates = {
    "0971": {
        "name_zh": "弹力带辅助跪姿健腹轮前滚",
        "category": "waist",
        "equipment": "band",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["lower back", "lats", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双膝跪在训练垫上，将弹力带一端系在身后固定锚点，另一端套在腰间或健腹轮轴心提供回拉辅助。",
            "双手握稳健腹轮两侧把手，垂直置于肩关节正下方，微收下巴，腹肌与骨盆保持紧绷锁紧。",
            "吸气主要由腹直肌离心发力受控，缓慢推动健腹轮向前平稳滚动，躯干向前舒展延伸直至接近地面。",
            "在最远受控伸展点顶峰停顿 1 秒，呼气由腹直肌强力收缩，借助弹力带辅助拉力将健腹轮平稳拉回至跪姿起始位，按计划重复。",
        ],
    },
    "0972": {
        "name_zh": "弹力带仰卧空中自行车卷腹",
        "category": "waist",
        "equipment": "band",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors", "obliques"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧在训练垫上，将迷你环状弹力带套在双脚前脚掌上，双手轻触耳后或头侧，下背部紧贴地面。",
            "双腿微屈抬离地面，深吸气蓄力准备。",
            "呼气主要由腹斜肌收缩发力，带动躯干受控向右旋转，左侧肘关节向右膝靠近，同时右膝弯曲向胸口提拉对抗弹力带阻力，左腿伸直向前蹬出。",
            "在顶峰对侧接触点停顿 1 秒挤压腹肌，吸气顺畅换边，右肘向左膝靠近，两腿如踩单车般左右交替按计划重复。",
        ],
    },
    "0974": {
        "name_zh": "弹力带窄握高位下拉",
        "category": "back",
        "equipment": "band",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "upper back", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将弹力带固定在头顶高位锚点上，双脚与肩同宽站立或跪立，面对锚点双手窄距对握或正握弹力带两端。",
            "双臂向上伸直带动背部充分舒展拉伸，挺胸沉肩，核心微紧。",
            "呼气由背阔肌集中收缩发力，屈肘将弹力带向下平稳拉向胸部上沿，主动后缩并下沉双侧肩胛骨。",
            "在下拉最低点顶峰收紧背阔肌停顿 1 秒，吸气匀速受控放慢双臂回弹至高位起始拉伸位，按计划重复。",
        ],
    },
    "0975": {
        "name_zh": "弹力带窄距俯卧撑",
        "category": "upper arms",
        "equipment": "band",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将弹力带横跨后背穿过腋下，双手各压住弹力带两端手柄或带端撑在地面上，双手间距与肩同宽或略窄于肩宽。",
            "双脚并拢支撑，躯干从头到脚跟保持平直斜线，双肘紧贴体侧收紧。",
            "吸气主要由肱三头肌受控离心屈肘下沉身体，大臂紧贴身体两侧，直至胸部接近地面。",
            "呼气由肱三头肌强力向心收缩发力，推蹬掌心将身体撑回起始伸臂位，在最高点顶峰收紧三头肌，按计划重复。",
        ],
    },
    "0976": {
        "name_zh": "坐姿弹力带单臂集中弯举",
        "category": "upper arms",
        "equipment": "band",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "坐在训练凳或椅子边缘，双腿向两侧自然分开，双脚平踩地面，同侧前脚掌踩住弹力带底端。",
            "同侧手臂反手抓握弹力带上方把手，上身微前倾，将肘关节靠在大腿内侧接近膝关节处作为稳定支点。",
            "大臂保持垂直静止，呼气主要由肱二头肌集中收缩发力，屈肘将把手向上弯举至肩膀胸前高度。",
            "在弯举顶点顶峰收缩挤压二头肌停顿 1 秒，吸气匀速受控放低手臂回至起始伸展位，按计划完成单侧后换边重复。",
        ],
    },
    "0977": {
        "name_zh": "站姿弹力带斜前平举",
        "category": "shoulders",
        "equipment": "band",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["traps", "upper back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽踩在弹力带中段上，双手各握弹力带两端把手垂于身体前侧，手背朝向斜上方。",
            "挺胸沉肩锁死肩胛，收紧核心维持躯干稳定，双臂微屈肘锁定固定关节。",
            "呼气主要由三角肌前束与前侧发力，沿身体前方斜 45 度角平稳将双臂向上平举至与肩齐平高度。",
            "在平举最高顶点顶峰收缩停顿 1 秒充分收紧肩部肌群，吸气匀速受控放回双臂至体前起始位，按计划重复。",
        ],
    },
    "0978": {
        "name_zh": "站姿弹力带前平举",
        "category": "shoulders",
        "equipment": "band",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["traps", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站立踩住弹力带中段，双手正握弹力带两端垂于大腿前侧，掌心朝向身体。",
            "挺胸收腹，双膝微屈弹性站立，肩胛骨保持稳定下沉不耸肩。",
            "呼气主要由三角肌前束集中收缩发力，手臂保持微屈伸展，向前上方平稳将弹力带拉起至与肩齐平水平高度。",
            "在顶点顶峰收缩停顿 1 秒挤压三角肌前束，吸气匀速受控沿原轨迹缓慢下放回至大腿前侧起始位，按计划重复。",
        ],
    },
    "0979": {
        "name_zh": "站姿弹力带水平帕洛夫推胸",
        "category": "waist",
        "equipment": "band",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques", "glutes"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将弹力带固定在胸部高度的坚固锚点上，侧身垂直于锚点站立，双脚与肩同宽微屈膝站立。",
            "双手对合紧握弹力带把手收于胸口中央，拉紧弹力带使之产生横向拉力，挺胸收腹沉肩。",
            "呼气核心肌群强力等长抗旋转发力，双手顺畅向前水平推送伸直，对抗弹力带向侧面旋转拉扯的力矩。",
            "在双臂完全伸直点顶峰收缩停顿 1 秒感受腹肌与核心的强抗扭张力，吸气受控屈肘将双手收回至胸口起始位，按计划重复。",
        ],
    },
    "0980": {
        "name_zh": "站姿弹力带俯身后抬腿",
        "category": "upper legs",
        "equipment": "band",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将环状弹力带套在双脚脚踝或小腿下沿，双脚与髋同宽站立，双手扶稳前方固定把手或墙面。",
            "屈髋微俯身保持脊柱中立平直，支撑腿膝关节微屈锁紧维持稳定。",
            "呼气主要由臀大肌强力收缩发力，驱动发力侧腿保持膝盖微屈向后上方平稳蹬伸后抬至髋关节完全伸展。",
            "在最高点顶峰收缩充分挤压臀部肌群停顿 1 秒，吸气匀速受控放回下肢至起始位，左右交替或换边按计划重复。",
        ],
    },
    "0981": {
        "name_zh": "弹力带仰卧折刀起坐",
        "category": "waist",
        "equipment": "band",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors", "obliques"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧在训练垫上，双手全握弹力带两端过头向后平展伸直，双腿并拢伸直微悬空离地。",
            "深吸气蓄力准备，下背部紧贴地面。",
            "呼气主要由腹直肌爆发向心收缩发力，同时折起上半身与双腿呈折刀形态，双手带动弹力带向脚踝前侧平稳拉拢靠齐。",
            "在折刀最高折叠点顶峰收缩强力挤压腹肌停顿 1 秒，吸气匀速受控放缓下放上半身与双腿回至起始拉伸位，按计划重复。",
        ],
    },
}

pending = {
    "0971": "待修图 · 消除滚轮直译规范为弹力带辅助跪姿健腹轮前滚；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "0972": "待修图 · 规范空中自行车动作命名为弹力带仰卧空中自行车卷腹；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "0974": "待修图 · 规范高位下拉姿态为弹力带窄握高位下拉；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "0975": "待修图 · 规范窄距俯卧撑姿态为弹力带窄距俯卧撑；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "0976": "待修图 · 规范单臂动作命名为坐姿弹力带单臂集中弯举；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "0977": "待修图 · 规范斜平举命名为站姿弹力带斜前平举；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "0978": "待修图 · 规范前平举标准动作命名为站姿弹力带前平举；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "0979": "待修图 · 消除帕洛夫推直译规范为站姿弹力带水平帕洛夫推胸；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "0980": "待修图 · 纠正臀推错译规范为站姿弹力带俯身后抬腿；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "0981": "待修图 · 纠正跪姿错译规范为弹力带仰卧折刀起坐；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review102-20261219",
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
    "expected_checks": 16,
    "expected_reviewed_after_approve": reviewed_count,
    "candidate_ids": [],
    "candidate_required_equipment": {},
    "expected_per_side_ids": ["0976"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
