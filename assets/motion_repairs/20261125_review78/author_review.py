#!/usr/bin/env python3
"""Author Batch 78 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261125_review78"
VERSION = "1.2.83"
VERSION_CODE = 2026112501

inspected = ["0186", "0188", "0189", "0190", "0191", "0192", "0193", "0194", "0195", "0196"]
review_candidates = []
registered_media = []

definition_updates = {
    "0186": {
        "name_zh": "平凳仰卧龙门架绳索臂屈伸第二式",
        "category": "upper arms",
        "equipment": "cable",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "将平凳垂直置于龙门架低位滑轮前方，头部靠近机器方向仰卧于凳面上，双脚平踩地面稳定躯干。",
            "双手对握绳索把手举至胸前正上方，大臂与地面垂直并保持固定锁死角度。",
            "吸气缓慢屈肘将把手放低至额头上方，充分拉伸肱三头肌长头与外侧头。",
            "呼气由肱三头肌强力发力推直小臂回到起始锁定位置，停顿 1 秒挤压肌肉，重复规定次数。",
        ],
    },
    "0188": {
        "name_zh": "站姿龙门架绳索中位飞鸟",
        "category": "chest",
        "equipment": "cable",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["deltoids", "triceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将龙门架双侧滑轮调至胸部齐平高度，双手各握一侧手柄向前迈出一步呈稳固站姿，挺胸直背微前倾。",
            "手肘微屈锁死，双臂向两侧展开与胸同高，吸气充分拉伸胸大肌中部。",
            "呼气由胸大肌主导发力向身体正前方合拢双手，在胸口正前方聚拢轻触。",
            "在合拢顶点极力挤压胸肌中缝停顿 1 秒，吸气匀速受控放回双臂至起始位，重复规定次数。",
        ],
    },
    "0189": {
        "name_zh": "站姿俯身龙门架绳索单臂划船",
        "category": "back",
        "equipment": "cable",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms"],
        "perSide": True,
        "required_equipment_zh": [],
        "instructions_zh": [
            "面对龙门架低位滑轮站立，双脚与肩同宽微屈膝，由髋部前倾俯身约 45 度，背部保持平直核心收紧。",
            "单手握住绳索手柄垂于体前，手臂完全伸直充分拉伸背阔肌。",
            "呼气由上背肌群与背阔肌主导屈肘将手柄拉向体侧腰际，手肘紧贴躯干并强力后缩肩胛骨。",
            "在动作顶点挤压背肌停顿 1 秒，吸气受控送回手臂，换另一侧交替完成规定次数。",
        ],
    },
    "0190": {
        "name_zh": "站姿龙门架绳索单臂反握弯举",
        "category": "upper arms",
        "equipment": "cable",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "perSide": True,
        "required_equipment_zh": [],
        "instructions_zh": [
            "面对龙门架低位滑轮稳固站立，单手采用掌心朝上的反手握距握紧单把手，上臂贴紧体侧保持静止。",
            "挺胸收腹核心紧绷，呼气由肱二头肌强力发力屈肘向上弯举手柄至胸前肩峰前方。",
            "在最高顶点充分收缩挤压二头肌峰值停顿 1 秒，吸气缓慢匀速下放手柄至手臂完全自然伸直。",
            "动作全程保持身体不晃动借力，换另一侧手臂交替完成规定次数练习。",
        ],
    },
    "0191": {
        "name_zh": "站姿俯身龙门架绳索单臂飞鸟",
        "category": "chest",
        "equipment": "cable",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["deltoids", "trapezius"],
        "perSide": True,
        "required_equipment_zh": [],
        "instructions_zh": [
            "侧身或微俯身面向龙门架低位滑轮站立，单手反手或对握单手柄垂于体前，微屈膝直背收腹。",
            "手臂微屈肘保持角度固定，吸气将手柄自然下垂至体前充分延展胸肌外缘。",
            "呼气由胸大肌发力将手臂沿宽弧线向身体斜上方及对侧环抱拉起至胸前水平。",
            "在收缩顶点极力挤压单侧胸大肌停顿 1 秒，吸气缓慢受控放回起始位，换另一侧交替重复规定次数。",
        ],
    },
    "0192": {
        "name_zh": "站姿龙门架绳索单臂侧平举",
        "category": "shoulders",
        "equipment": "cable",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["traps", "triceps"],
        "perSide": True,
        "required_equipment_zh": [],
        "instructions_zh": [
            "侧对龙门架低位滑轮站立，远端手握住从身体后侧或前侧穿出的单手柄，挺胸沉肩核心锁死。",
            "手肘微屈锁死角度，呼气由三角肌中束主导发力向身体外侧上方平稳抬起手臂。",
            "抬高手柄至与肩同高水平位置，在最高点停顿 1 秒强调外侧峰值张力。",
            "吸气缓慢匀速受控放回把手至起始位，换另一侧交替完成规定次数练习。",
        ],
    },
    "0193": {
        "name_zh": "跪姿地面龙门架绳索单臂高位划船",
        "category": "back",
        "equipment": "cable",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "shoulders"],
        "perSide": True,
        "required_equipment_zh": [],
        "instructions_zh": [
            "单膝或双膝跪在龙门架前方的平整地面上，单手握紧中高位滑轮手柄，躯干保持直立挺胸核心紧绷。",
            "手臂向前上方伸展充分拉伸背部肌群，呼气由中背与背阔肌主导屈肘将手柄向后拉向胸部侧面。",
            "在动作顶点手肘后拉并强力内收肩胛骨停顿 1 秒。",
            "吸气匀速受控放回手臂至高位舒展起始点，换另一侧手臂交替完成规定次数。",
        ],
    },
    "0194": {
        "name_zh": "站姿龙门架绳索麻绳过头臂屈伸",
        "category": "upper arms",
        "equipment": "cable",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "背对龙门架高位滑轮站立，前后分腿站稳呈稳固弓步，双手对握麻绳把手末端举过头顶。",
            "上臂贴近耳朵保持角度固定前倾，吸气屈肘将麻绳缓慢放低至脑后充分拉伸肱三头肌。",
            "呼气由肱三头肌强力发力向前上方伸直小臂，并在动作末端顺势向两侧拉开绳索末端。",
            "在充分伸展顶点停顿 1 秒挤压肱三头肌，吸气受控放回脑后，按规定次数重复练习。",
        ],
    },
    "0195": {
        "name_zh": "坐姿牧师凳龙门架绳索反握弯举",
        "category": "upper arms",
        "equipment": "cable",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": ["牧师凳"],
        "instructions_zh": [
            "将牧师凳置于龙门架低位滑轮前方，端坐在坐垫上，胸口贴紧斜托垫，上臂平整贴实斜垫斜面。",
            "双手采用反手握距（掌心朝上）握住横杠把手，双臂顺着斜面完全伸展。",
            "呼气由肱二头肌孤立强力发力向上弯举把手至最高点，手腕保持中立不借力。",
            "在最高顶点充分挤压二头肌峰值停顿 1 秒，吸气受控沿斜垫缓慢下放至双臂充分伸展起始姿态，重复规定次数。",
        ],
    },
    "0196": {
        "name_zh": "站姿龙门架绳索过裆伸髋挺身",
        "category": "upper legs",
        "equipment": "cable",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "背对龙门架低位滑轮跨立，双手从两腿胯下穿过握紧麻绳把手，向前迈出一至两步让绳索产生初张力。",
            "保持脊柱平直核心收紧，吸气由髋部主动向后推出折叠，屈髋俯身让躯干下放至与地面接近平行。",
            "在折髋最深点稍作停顿充分感受臀大肌与腘绳肌的离心拉伸感。",
            "呼气由臀大肌强力发力向前推髋伸直身体站立锁定，在顶端用力夹紧臀肌停顿 1 秒，重复规定次数。",
        ],
    },
}

pending = {
    "0186": "待修图 · 消除英文字符并补全平凳器械规范为平凳仰卧龙门架绳索臂屈伸第二式；原动图为 10 帧 (nf=10) 超标且前额屈伸缺乏停顿，待重制为 4 帧循环图。",
    "0188": "待修图 · 消除中飞鸟俗称规范为站姿龙门架绳索中位飞鸟；原动图仅有 2 帧 (nf=2) 缺失中位聚拢合拢与后展过渡帧，待重制为 4 帧循环图。",
    "0189": "待修图 · 规范译名为站姿俯身龙门架绳索单臂划船（激活单侧交替计次）；原动图为 10 帧 (nf=10) 超标且躯干轻微扭转，待重制为 4 帧循环图。",
    "0190": "待修图 · 消除单臂弯举歧义规范为站姿龙门架绳索单臂反握弯举（激活单侧交替计次）；原动图仅有 2 帧 (nf=2) 缺失单臂弯举上升与下落过渡帧，待重制为 4 帧循环图。",
    "0191": "待修图 · 消除侧平举错译规范为站姿俯身龙门架绳索单臂飞鸟（激活单侧交替计次）；原动图为 10 帧 (nf=10) 超标且动作幅度晃动，待重制为 4 帧循环图。",
    "0192": "待修图 · 规范译名为站姿龙门架绳索单臂侧平举（激活单侧交替计次）；原动图为 10 帧 (nf=10) 超标且外侧抬起缺乏平稳停顿，待重制为 4 帧循环图。",
    "0193": "待修图 · 规范跪姿地面环境规范为跪姿地面龙门架绳索单臂高位划船（激活单侧交替计次）；原动图为 10 帧 (nf=10) 超标且单侧提拉摇晃，待重制为 4 帧循环图。",
    "0194": "待修图 · 规范麻绳附件规范为站姿龙门架绳索麻绳过头臂屈伸；原动图为 10 帧 (nf=10) 超标且推直锁定速度欠均匀，待重制为 4 帧循环图。",
    "0195": "待修图 · 消除平板弯举错译并补全牧师凳规范为坐姿牧师凳龙门架绳索反握弯举（补全牧师凳必需器械、规避平板触发静力保持）；原动图仅有 2 帧 (nf=2) 缺失斜托弯举过程帧，待重制为 4 帧循环图。",
    "0196": "待修图 · 消除拉伸错译规范为站姿龙门架绳索过裆伸髋挺身；原动图为 10 帧 (nf=10) 超标且伸髋顶点缺乏稳定停顿，待重制为 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review78-20261125",
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
        "0186": ["平板训练凳"],
        "0195": ["牧师凳"],
    },
    "expected_per_side_ids": ["0189", "0190", "0191", "0192", "0193"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
