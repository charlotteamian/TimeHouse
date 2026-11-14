#!/usr/bin/env python3
"""Author Batch 72 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261119_review72"
VERSION = "1.2.77"
VERSION_CODE = 2026111901

inspected = ["0102", "0103", "0104", "0105", "0106", "0107", "0108", "0109", "0110", "0111"]
review_candidates = []
registered_media = []

definition_updates = {
    "0102": {
        "name_zh": "跪姿地面杠铃折髋深蹲",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "quads",
        "muscle_group": "",
        "secondary_muscles": ["glutes", "hamstrings"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双膝跪在平整训练垫上与髋同宽，小腿贴地脚背朝下，将轻适杠铃平稳扛于上背斜方肌上，双手握紧固定。",
            "挺胸收紧核心，吸气主动屈髋向后下方折叠坐向脚跟方向，保持脊柱平直中立不弯腰。",
            "折髋下沉至臀部接近脚跟且股四头肌与臀肌张力充分展开时短暂停顿。",
            "呼气由臀大肌发力强力前推伸髋挺直身体回至垂直跪立起始位，并在顶部用力夹紧臀肌，重复规定次数。",
        ],
    },
    "0103": {
        "name_zh": "站姿地面杠铃推腹滚轮",
        "category": "waist",
        "equipment": "barbell",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "lower back", "lats"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚并拢或与肩同宽站立，俯身微屈膝，双手正握地面上的杠铃杆两端，核心深度收紧锁定。",
            "双脚站稳地面，平稳向前滚动杠铃，身体向前下方平展延伸直至躯干接近水平地面、双臂伸直于头前。",
            "在最远延展点维持腹部核心极限张力稍作停顿，避免腰椎反弓塌陷。",
            "呼气由腹直肌与后侧链协同爆发收缩拉回杠铃至脚前起始俯身位，保持控制完成规定次数。",
        ],
    },
    "0104": {
        "name_zh": "站姿体后杠铃腕弯举",
        "category": "lower arms",
        "equipment": "barbell",
        "target": "forearms",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "brachialis"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站立，双手正握杠铃（手心朝后远离身体）置于臀部后方，双臂自然伸直下垂。",
            "大臂与上身保持直立静止，仅依靠腕关节活动，呼气由前臂屈肌发力向上弯屈手腕将杠铃向上提拉。",
            "在最高屈腕收缩顶点停顿 1 秒挤压前臂肌肉，吸气缓慢平稳下放杠铃至手指轻微展开伸展位。",
            "全程避免利用身体前后摆动借力，按规定次数重复练习。",
        ],
    },
    "0105": {
        "name_zh": "站姿杠铃布拉德福德前后推举",
        "category": "shoulders",
        "equipment": "barbell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "upper back", "traps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站稳，双手略宽于肩正握杠铃置于胸前锁骨高度，核心收紧脊柱中立。",
            "呼气由三角肌发力将杠铃刚好推过头顶发际线高度，顺势掠过头顶下放至颈后肩部高度。",
            "紧接着由颈后再次微幅推起刚过头顶，顺势向前移动下放回胸前起始锁骨高度，完成一次前后循环。",
            "全程保持三角肌持续抗阻张力不锁死手肘，按规定节奏平稳完成练习。",
        ],
    },
    "0106": {
        "name_zh": "站姿杠铃窄握弯举",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "站立挺胸，双脚与肩同宽站稳，双手采用窄于肩宽的反手握距握住杠铃垂于体前，手心朝上。",
            "双肘紧贴躯干两侧固定静止，呼气由肱二头肌外侧长头主导发力屈肘向上弯举杠铃至前臂接近垂直。",
            "在动作顶点充分挤压二头肌峰值停顿 1 秒，吸气沿平稳弧线匀速下放杠铃至双臂完全自然伸直。",
            "动作全程保持上身平直不后仰借力，按规定次数重复练习。",
        ],
    },
    "0107": {
        "name_zh": "站姿杠铃前平举过头",
        "category": "shoulders",
        "equipment": "barbell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "upper back", "traps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站立，双手正握轻杠铃垂于大腿前侧，握距与肩同宽，手心朝向大腿。",
            "挺胸收腹核心收紧，手臂微屈肘锁定，呼气由三角肌前束与斜方肌主导将杠铃向前上方划弧平举直至完全举过头顶正上方。",
            "在头顶直立最高点稍作停顿感受肩部肌群收缩，吸气控制杠铃缓慢平稳沿前方大弧线匀速下落回起始大腿前侧。",
            "全程避免腰部反弓挺腹借力，按规定次数连贯完成练习。",
        ],
    },
    "0108": {
        "name_zh": "站姿杠铃双腿提踵",
        "category": "lower legs",
        "equipment": "barbell",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "glutes"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与髋同宽平稳站立于平地上，将杠铃平稳扛于上背斜方肌上，双手握紧挺胸直立。",
            "收紧腰腹核心，呼气由小腿三头肌强力收缩发力将脚后跟尽力抬离地面至前脚掌最高点。",
            "在提踵最高顶峰收缩点停顿 1 秒充分挤压小腿腓肠肌，吸气缓慢匀速下放脚跟恢复平踩地面起始位。",
            "动作全程保持身体垂直稳定不晃动，按规定次数重复练习。",
        ],
    },
    "0109": {
        "name_zh": "站姿杠铃颈后臂屈伸",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽平稳站立，挺胸收腹，双手窄握杠铃将其完全推举过头顶上方，大臂垂直贴近头部两侧。",
            "保持大臂完全固定竖直不动，吸气屈肘仅活动前臂将杠铃缓慢平稳下落至颈后头后方。",
            "在最深伸展位短暂停顿感受三头肌离心拉伸，呼气由肱三头肌发力将手臂推直回头顶起始位。",
            "全程手肘避免向外过度外撇晃动，按规定次数重复练习。",
        ],
    },
    "0110": {
        "name_zh": "站姿反握杠铃臂弯举",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩同宽站立，双手正握杠铃（手心朝下反向抓握），握距与肩同宽垂于大腿前方。",
            "保持上臂紧贴躯干两侧固定静止，呼气由肱二头肌与肱肌主导发力屈肘向上弯举杠铃至胸前高度。",
            "在最高顶点充分挤压手臂肌肉停顿 1 秒，吸气沿受控弧线缓慢匀速下放杠铃至双臂完全自然垂展。",
            "动作全程保持躯干稳定不后仰借力，按规定次数重复练习。",
        ],
    },
    "0111": {
        "name_zh": "站姿杠铃前后摇摆提踵",
        "category": "lower legs",
        "equipment": "barbell",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "quadriceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与髋同宽平稳站立，将杠铃平稳扛于上背斜方肌上，双手握紧固定保持脊柱中立。",
            "收紧核心维持重心平稳，首先呼气由小腿肌发力前脚掌蹬地将脚后跟尽力抬起至最高点提踵。",
            "随后吸气平稳落回脚跟，顺势将重心平稳后移至脚跟、前脚掌自然微抬勾脚，形成连贯前后摇摆节奏。",
            "保持脚踝与小腿在前后摇摆中完全受控平衡，按规定次数平稳完成练习。",
        ],
    },
}

pending = {
    "0102": "待修图 · 消除跪姿深蹲俗称规范为跪姿地面杠铃折髋深蹲；原动图仅有 2 帧 (nf=2) 缺失折髋后坐与伸髋起身过程帧，待重制为 4 帧循环图。",
    "0103": "待修图 · 消除腹轮滚出俗称规范为站姿地面杠铃推腹滚轮；原动图仅有 2 帧 (nf=2) 缺失站姿向前延展与回拉收缩过渡帧，待重制为 4 帧循环图。",
    "0104": "待修图 · 消除后腕弯举俗称规范为站姿体后杠铃腕弯举；原动图为 10 帧 (nf=10) 超标且体后腕屈伸轨迹偏移，待重制为 4 帧循环图。",
    "0105": "待修图 · 规范译名为站姿杠铃布拉德福德前后推举；原动图为 10 帧 (nf=10) 超标且头顶前后翻转过程缺少顶峰收缩，待重制为 4 帧循环图。",
    "0106": "待修图 · 规范译名为站姿杠铃窄握弯举；原动图为 10 帧 (nf=10) 超标且身体轻微借力后仰，待重制为 4 帧循环图。",
    "0107": "待修图 · 规范译名为站姿杠铃前平举过头；原动图仅有 2 帧 (nf=2) 缺失大弧线平举上升与回落过程帧，待重制为 4 帧循环图。",
    "0108": "待修图 · 规范译名为站姿杠铃双腿提踵；原动图为 10 帧 (nf=10) 超标且提踵顶峰缺乏张力停顿，待重制为 4 帧循环图。",
    "0109": "待修图 · 消除三头肌伸展俗称规范为站姿杠铃颈后臂屈伸；原动图仅有 2 帧 (nf=2) 缺失颈后屈肘离心与伸臂推直过程帧，待重制为 4 帧循环图。",
    "0110": "待修图 · 规范译名为站姿反握杠铃臂弯举；原动图仅有 2 帧 (nf=2) 缺失正握反向弯举过程过渡帧，待重制为 4 帧循环图。",
    "0111": "待修图 · 消除摆动腿提踵错译规范为站姿杠铃前后摇摆提踵；原动图为 10 帧 (nf=10) 超标且重心前后摇摆失衡，待重制为 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review72-20261119",
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
    "expected_per_side_ids": [],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
