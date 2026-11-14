#!/usr/bin/env python3
"""Author Batch 104 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261221_review104"
VERSION = "1.2.109"
VERSION_CODE = 2026122101

inspected = ["0993", "0994", "0996", "0997", "0998", "0999", "1000", "1001", "1002", "1003"]
review_candidates = []
registered_media = []

definition_updates = {
    "0993": {
        "name_zh": "站姿弹力带反向飞鸟",
        "category": "shoulders",
        "equipment": "band",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["upper back", "traps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将弹力带固定在胸部高度锚点，或双手向前伸直拉紧弹力带中段两端，双脚与肩同宽站立。",
            "挺胸沉肩锁死肩胛，收紧腹部核心，双臂在身前微屈肘固定关节夹角。",
            "呼气主要由三角肌后束与上背肌群集中收缩发力，双臂水平向身体两侧向后展开拉开弹力带，主动夹紧肩胛骨。",
            "在最外侧展开顶点顶峰收缩挤压三角肌后束停顿 1 秒，吸气匀速受控放慢双臂回拢至体前起始位，按计划重复。",
        ],
    },
    "0994": {
        "name_zh": "坐姿弹力带反握腕弯举",
        "category": "lower arms",
        "equipment": "band",
        "target": "forearms",
        "muscle_group": "",
        "secondary_muscles": ["biceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "端坐在训练凳或椅子上，双脚平踩地面踩住弹力带底端，双手正握（掌心朝下）上方把手或带端。",
            "前臂平贴在同侧大腿面上，手腕悬出膝盖边缘，手腕保持水平放松伸展。",
            "呼气主要由前臂伸肌群强力收缩发力，手腕向上反向屈曲抬起把手至最大屈曲幅度。",
            "在顶点顶峰收缩充分挤压前臂外侧肌群停顿 1 秒，吸气匀速受控放慢手腕缓慢下沉回至起始位，按计划重复。",
        ],
    },
    "0996": {
        "name_zh": "弹力带坐姿髋内旋",
        "category": "upper legs",
        "equipment": "band",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "quadriceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "端坐在椅子或平凳边缘，背部平直挺拔，双脚平踩地面与髋同宽。",
            "将环状弹力带套在双侧大腿下部膝关节上方，双手扶稳凳面维持骨盆水平稳定。",
            "呼气主要由臀部肌群发力克服弹力带阻力，双膝向两侧平稳展开外展外旋，双脚内侧平稳接触地面。",
            "在展开最宽顶点顶峰收缩挤压臀大肌与臀中肌停顿 1 秒，吸气匀速受控让双膝缓慢并拢回至起始平行位，按计划重复。",
        ],
    },
    "0997": {
        "name_zh": "站姿弹力带推肩",
        "category": "shoulders",
        "equipment": "band",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "upper back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站立踩住弹力带中段，双手正握把手提至肩膀水平高度，掌心朝前上方，双肘微张于体侧前斜方。",
            "挺胸沉肩锁紧核心，下背部保持自然生理弯曲，双膝微屈弹性站立。",
            "呼气主要由三角肌前束与中束发力，协同肱三头肌向上平稳推举把手过头顶，直至手臂接近伸直但不锁死肘关节。",
            "在推举最高点顶峰收紧肩部肌群停顿 1 秒，吸气匀速受控缓慢放低把手回至耳朵肩膀高度起始位，按计划重复。",
        ],
    },
    "0998": {
        "name_zh": "站姿弹力带侧向臂屈伸",
        "category": "upper arms",
        "equipment": "band",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站立，双手各握弹力带两端把手，双臂向身体两侧水平展开微屈肘，掌心朝下。",
            "挺胸沉肩，双侧大臂保持在水平高度固定作为稳定转动轴心。",
            "呼气主要由肱三头肌强力向心收缩发力，向身体两侧水平伸展前臂，直至整条手臂完全侧向锁直伸展。",
            "在最远完全伸直点顶峰收缩挤压肱三头肌停顿 1 秒，吸气匀速受控屈肘将手拉向肩膀内侧起始位，大臂保持水平不坠落，按计划重复。",
        ],
    },
    "0999": {
        "name_zh": "站姿弹力带单腿提踵",
        "category": "lower legs",
        "equipment": "band",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["ankles"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "单脚前脚掌平踩在踏板或平地边缘踩住弹力带底端，单手或双手提拉把手上端提供垂直向下的阻力，另一手扶稳固定物维持平衡。",
            "对侧非支撑腿屈膝悬空，支撑腿膝关节保持微屈锁直，脚后跟悬空自然下沉充分拉伸腓肠肌。",
            "呼气主要由小腿肌群全力爆发推蹬前脚掌，驱动脚跟垂直向上提拉至踝关节最高屈曲点。",
            "在提踵最高顶点顶峰收缩挤压小腿停顿 1 秒，吸气匀速受控放缓下沉脚跟回至深度拉伸位，按计划完成单腿后换边重复。",
        ],
    },
    "1000": {
        "name_zh": "站姿弹力带单腿反向提踵",
        "category": "lower legs",
        "equipment": "band",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "glutes"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "单脚脚跟着地支撑，将弹力带套在同侧前脚掌脚背上方提供向下的拉力阻力，双手拉紧把手维持带子张力。",
            "挺胸沉肩核心微紧，对侧腿微屈悬空，另一手可轻扶墙面辅助平衡。",
            "呼气主要由胫骨前肌强力向心收缩发力，向上主动背屈踝关节勾起脚尖至最高极限。",
            "在勾脚尖最高点顶峰收缩挤压小腿前侧肌群停顿 1 秒，吸气匀速受控放慢下放脚掌回至起始触地位，按计划完成单侧后换边重复。",
        ],
    },
    "1001": {
        "name_zh": "弹力带单腿分腿蹲",
        "category": "upper legs",
        "equipment": "band",
        "target": "quads",
        "muscle_group": "",
        "secondary_muscles": ["glutes", "hamstrings"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "前后大跨步分腿站立，前腿脚掌踩住弹力带中段，双手各持把手提在胸前或垂于体侧维持张力。",
            "挺胸收腹，躯干保持正直中立，后腿脚尖抓地点地支撑。",
            "吸气屈膝下蹲，身体重心垂直平稳下降，前腿膝盖轨迹与脚尖方向一致，下蹲至大腿与地面接近平行。",
            "呼气主要由前腿股四头肌强力蹬地发力，垂直推起身体回至直立起始分腿位，在顶点顶峰收紧大腿肌群，按计划完成单侧后换边重复。",
        ],
    },
    "1002": {
        "name_zh": "弹力带仰卧直腿举腿",
        "category": "waist",
        "equipment": "band",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "平躺在训练垫上，将弹力带中段套在双脚足弓处，双手全握带端紧贴身体两侧地面固定拉紧。",
            "下背部紧贴地面锁死核心，双腿伸直脚尖微绷悬空离地。",
            "呼气主要由腹直肌强力收缩发力，带动双腿保持伸直平稳向上抬升至与地面垂直 90 度，骨盆可微抬卷腹。",
            "在最高顶点顶峰收紧腹肌停顿 1 秒，吸气匀速受控放缓下放双腿回至接近地面悬空位，下背部全程贴实地面，按计划重复。",
        ],
    },
    "1003": {
        "name_zh": "站姿弹力带深蹲划船",
        "category": "upper legs",
        "equipment": "band",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "quadriceps", "upper back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将弹力带固定在胸腰高度锚点，面对锚点站立，双脚与肩同宽踩地，双手对握把手向前伸直手臂拉紧带子。",
            "吸气屈髋屈膝下蹲，臀部向后下方坐下至大腿平行地面，背部保持平直中立，双臂向前顺应拉力延伸拉伸背肌。",
            "呼气由臀大肌与股四头肌强力推蹬全脚掌起立，同时双臂屈肘将把手平稳拉向胸肋两侧，后缩并挤压双侧肩胛骨。",
            "在深蹲起立划船结合顶点顶峰强力收缩臀大肌与背肌停顿 1 秒，吸气匀速受控下蹲并送出双臂回至起始深蹲位，按计划重复。",
        ],
    },
}

pending = {
    "0993": "待修图 · 规范飞鸟动作姿态为站姿弹力带反向飞鸟；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "0994": "待修图 · 消除反向腕弯举直译规范为坐姿弹力带反握腕弯举；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "0996": "待修图 · 规范坐姿髋内展动作为弹力带坐姿髋内旋；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "0997": "待修图 · 规范推肩动作命名为站姿弹力带推肩；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "0998": "待修图 · 消除侧三头肌伸展直译规范为站姿弹力带侧向臂屈伸；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "0999": "待修图 · 规范单腿提踵姿态为站姿弹力带单腿提踵；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1000": "待修图 · 规范单腿反向提踵命名为站姿弹力带单腿反向提踵；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1001": "待修图 · 规范单腿分腿蹲动作为弹力带单腿分腿蹲；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1002": "待修图 · 规范直腿抬高命名为弹力带仰卧直腿举腿；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1003": "待修图 · 规范复合动作姿态为站姿弹力带深蹲划船；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review104-20261221",
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
    "expected_per_side_ids": ["0999", "1000", "1001"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
