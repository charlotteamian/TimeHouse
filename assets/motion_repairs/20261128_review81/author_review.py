#!/usr/bin/env python3
"""Author Batch 81 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261128_review81"
VERSION = "1.2.86"
VERSION_CODE = 2026112801

inspected = ["0218", "0219", "0220", "0221", "0222", "0223", "0224", "0225", "0226", "0227"]
review_candidates = []
registered_media = []

definition_updates = {
    "0218": {
        "name_zh": "平凳坐姿龙门架绳索宽握划船",
        "category": "back",
        "equipment": "cable",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "坐在平凳上，双脚踏实地面，双手正手采用宽握握距握紧长杆横梁，躯干保持正直微前倾。",
            "双臂向前充分伸展指向低位滑轮，收紧核心肌群，沉肩锁住肩胛骨。",
            "呼气由上背部肌肉与背阔肌协同发力，驱动手肘向后向外拉引长杆至下胸部高度。",
            "在动作顶点完全收缩夹紧肩胛骨停顿 1 秒，吸气匀速受控放回长杆至双臂完全伸展，按计划重复。",
        ],
    },
    "0219": {
        "name_zh": "站姿龙门架绳索双臂肩推",
        "category": "shoulders",
        "equipment": "cable",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "upper back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "背对龙门架立柱站立，双脚前后弓步站稳，双手各持中位滑轮单把手柄置于肩部前方。",
            "手腕保持中立挺胸收腹，手肘微向下收拢约 45 度，形成坚实的推举起始姿态。",
            "呼气由三角肌前束与中束主导发力，推动手柄沿自然微内收弧线上推至头顶上方伸直手臂。",
            "在顶部顶点避免耸肩停顿 1 秒，吸气匀速受控下放手柄回到肩部高度起始位，按规定次数重复。",
        ],
    },
    "0220": {
        "name_zh": "站姿龙门架绳索耸肩",
        "category": "back",
        "equipment": "cable",
        "target": "traps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "面朝低位滑轮站立，双脚与肩同宽微屈膝，双手采用正握握牢短杠横杆，双臂自然下垂。",
            "挺胸收腹保持脊柱中立平直，双臂保持伸直且手肘微屈锁死，避免手臂屈伸借力。",
            "呼气由上斜方肌强力发力带动双肩垂直向上耸向耳朵方向，抬至最高位置。",
            "在顶峰强烈挤压斜方肌停顿 1 秒，吸气缓慢匀速受控放平肩膀回到起始位置，按计划重复。",
        ],
    },
    "0221": {
        "name_zh": "半圆平衡球站姿龙门架绳索单侧侧弯",
        "category": "waist",
        "equipment": "cable",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques"],
        "required_equipment_zh": ["半圆平衡球"],
        "instructions_zh": [
            "双脚站立于半圆平衡球圆顶上方保持身体平衡，单手持握低位滑轮单把手柄垂于体侧，另一手插腰。",
            "挺胸收腹保持骨盆端正，呼气由对侧腹斜肌主动发力，控制躯干向无阻力一侧做侧向屈曲弯伸。",
            "在侧屈顶点充分收紧侧腹核心肌肉停顿 1 秒，吸气控制平稳回到直立起始姿态。",
            "单侧完成规定次数后换边站立并持握手柄重复练习，全程保持球上重心平稳。",
        ],
    },
    "0222": {
        "name_zh": "站姿龙门架绳索单侧侧弯",
        "category": "waist",
        "equipment": "cable",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "侧对或背向低位滑轮稳固站立，双脚与肩同宽踩实地面，单手持握把手自然下垂，对侧手臂插腰。",
            "挺胸沉肩保持脊柱中立，呼气由对侧腹斜肌发力带动躯干朝对侧平稳侧屈拉伸与收缩。",
            "在动作顶点感受侧腰肌群深层挤压停顿 1 秒，吸气匀速受控缓慢放回身体至直立位置。",
            "单侧完成后换另一侧手臂握住手柄重复练习，避免利用前后晃动代偿借力。",
        ],
    },
    "0223": {
        "name_zh": "站姿龙门架绳索单侧侧卷腹",
        "category": "waist",
        "equipment": "cable",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "侧身站在低位或中位滑轮旁边，单手握住手柄曲肘置于耳旁或胸前，双脚平踩地面微屈膝。",
            "挺胸收腹，呼气集中同侧腹斜肌群主动发力，将肩肘朝同侧髋骨方向侧向卷屈缩紧。",
            "在侧卷腹极限位置强烈挤压腹部侧缘停顿 1 秒，吸气匀速受控伸展躯干回到起始姿态。",
            "完成规定次数后换另一侧重复相同练习，双侧保持等量负荷训练。",
        ],
    },
    "0224": {
        "name_zh": "站姿身后龙门架绳索腕弯举",
        "category": "lower arms",
        "equipment": "cable",
        "target": "forearms",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "brachialis"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "背对低位滑轮器械稳固站立，双脚与肩同宽，双手在臀部后方正握短杠横杆（手心朝后）。",
            "挺胸沉肩保持双臂自然下垂伸直，吸气放松手腕让短杠轻微下沉拉伸前臂屈肌。",
            "呼气由前臂屈肌群全力发力向上屈曲手腕，将短杠向上卷屈至最高幅度。",
            "在顶峰停顿 1 秒充分收缩前臂内侧肌肉，吸气平稳匀速放平手腕还原至起始位，按计划重复。",
        ],
    },
    "0225": {
        "name_zh": "站姿龙门架绳索交叉高位反向飞鸟",
        "category": "shoulders",
        "equipment": "cable",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["traps", "rhomboids", "rear deltoids"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "站在龙门架正中央，双手交叉持握高位滑轮两端手柄（左手拿右绳、右手拿左绳）。",
            "双脚前后站立微屈膝微前倾，双臂伸直微屈肘在胸前上方交叉相汇作为动作起点。",
            "呼气由三角肌后束与上背菱形肌主导发力，向后向外水平拉开双臂呈弧形展开飞鸟轨迹。",
            "在最远端顶峰收缩挤压后背与肩胛骨停顿 1 秒，吸气匀速受控让双臂向前交叉还原，按计划重复。",
        ],
    },
    "0226": {
        "name_zh": "站姿背向龙门架绳索卷腹",
        "category": "waist",
        "equipment": "cable",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "背对高位滑轮站立，双脚与肩同宽微屈膝，双手各持麻绳或把手紧贴固定于颈后肩头两侧。",
            "微前倾躯干并沉肩，呼气主动发力收紧腹直肌，带动上身肋骨向前下方朝骨盆方向卷屈。",
            "在卷腹最深处强烈挤压腹直肌停顿 1 秒，骨盆保持稳定不前后后晃。",
            "吸气匀速受控让腹肌伸展缓慢回放躯干至起始站姿，按规定次数重复完成训练。",
        ],
    },
    "0227": {
        "name_zh": "站姿龙门架绳索胸前飞鸟",
        "category": "chest",
        "equipment": "cable",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["delts", "triceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "背向龙门架两端中位滑轮站立，双脚前后弓步踏稳地面，双手各持手柄微屈肘在身侧展开。",
            "挺胸沉肩微前倾，核心收紧，呼气由胸大肌强力发力沿宽阔弧线向前向内合拢双臂。",
            "在胸前双手相聚顶点强烈收紧挤压胸大肌停顿 1 秒，肘部保持固定微屈角度。",
            "吸气匀速受控沿原弧线向后向外展开手臂充分拉伸胸肌，按规定次数平稳重复。",
        ],
    },
}

pending = {
    "0218": "待修图 · 补全平凳支持器械规范为平凳坐姿龙门架绳索宽握划船；原动图仅有 2 帧 (nf=2) 缺失宽握后拉至下胸与还原过程帧，待重制为 4 帧循环图。",
    "0219": "待修图 · 规范双臂推举规范为站姿龙门架绳索双臂肩推；原动图仅有 2 帧 (nf=2) 缺失推举过头顶与下放至肩部过程帧，待重制为 4 帧循环图。",
    "0220": "待修图 · 规范译名为站姿龙门架绳索耸肩；原动图仅有 2 帧 (nf=2) 缺失提肩挤压斜方肌与下放过程帧，待重制为 4 帧循环图。",
    "0221": "待修图 · 补全半圆平衡球器械规范为半圆平衡球站姿龙门架绳索单侧侧弯（激活单侧交替计次）；原动图仅有 2 帧 (nf=2) 缺失球上侧屈与回正过程帧，待重制为 4 帧循环图。",
    "0222": "待修图 · 规范单侧侧弯译名规范为站姿龙门架绳索单侧侧弯（激活单侧交替计次）；原动图为 10 帧 (nf=10) 超标且侧向屈曲幅度过快，待重制为 4 帧循环图。",
    "0223": "待修图 · 规范单侧侧卷腹规范为站姿龙门架绳索单侧侧卷腹（激活单侧交替计次）；原动图为 10 帧 (nf=10) 超标且身体轻微摇晃，待重制为 4 帧循环图。",
    "0224": "待修图 · 消除英文字符规范为站姿身后龙门架绳索腕弯举；原动图为 10 帧 (nf=10) 超标且身后卷屈轨迹欠均匀，待重制为 4 帧循环图。",
    "0225": "待修图 · 规范高位反向飞鸟规范为站姿龙门架绳索交叉高位反向飞鸟；原动图仅有 2 帧 (nf=2) 缺失交叉后展与前合过程帧，待重制为 4 帧循环图。",
    "0226": "待修图 · 规范站姿背向卷腹译名为站姿背向龙门架绳索卷腹；原动图仅有 2 帧 (nf=2) 缺失前卷与回升过程帧，待重制为 4 帧循环图。",
    "0227": "待修图 · 规范胸前飞鸟规范为站姿龙门架绳索胸前飞鸟；原动图仅有 2 帧 (nf=2) 缺失双臂前拢与后展拉伸过程帧，待重制为 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review81-20261128",
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
    "candidate_required_equipment": {
        "0218": ["平板训练凳"],
        "0221": ["半圆平衡球"],
    },
    "expected_per_side_ids": ["0221", "0222", "0223"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
