#!/usr/bin/env python3
"""Author Batch 69 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261116_review69"
VERSION = "1.2.74"
VERSION_CODE = 2026111601

inspected = ["0071", "0072", "0073", "0074", "0075", "0076", "0077", "0078", "0079", "0080"]
review_candidates = []
registered_media = []

definition_updates = {
    "0071": {
        "name_zh": "仰卧杠铃推举起坐",
        "category": "waist",
        "equipment": "barbell",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "chest"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "平躺在训练垫上，屈膝双脚平踩地面，双手正握杠铃置于胸前。",
            "腹部核心持续收紧发力，卷腹将上半身平稳抬起至躯干约 45 度角，同时顺势将杠铃垂直推举过头顶上方。",
            "在最高顶点稍作停顿感受腹直肌峰值收缩，缓慢控制上半身下落并将杠铃匀速收回胸前起始位。",
            "全程保持动作连贯受控，按规定次数重复练习。",
        ],
    },
    "0072": {
        "name_zh": "上斜训练凳俯卧杠铃弯举",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": ["上斜训练凳"],
        "instructions_zh": [
            "俯卧趴在倾斜约 45 度的上斜训练凳上，胸腹部贴紧凳面，双臂垂直自然下垂，双手反握杠铃与肩同宽。",
            "大臂始终保持垂直固定静止，呼气由肱二头肌发力屈肘向上弯举杠铃至最大幅度。",
            "在最高点充分挤压肱二头肌停顿 1 秒，吸气沿弧线缓慢平稳下放杠铃至手臂完全自然伸直。",
            "全程上身与大臂不借力晃动，重复规定次数。",
        ],
    },
    "0073": {
        "name_zh": "平凳仰卧杠铃过头拉背",
        "category": "back",
        "equipment": "barbell",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["chest", "triceps", "shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "仰卧平躺于平凳上，头部靠近平凳边缘，双脚踏地保持身体稳定，双手正握杠铃伸直推起在胸部上方。",
            "肘关节保持微屈并锁定角度，吸气由背阔肌控制将杠铃缓慢呈弧线向头部后方下落，直至感受背阔肌与胸廓充分拉伸。",
            "在最深伸展点短暂停顿，呼气由背阔肌发力将杠铃沿弧线拉回至胸部上方起始位。",
            "全程腰部避免过度反弓借力，按规定次数完成练习。",
        ],
    },
    "0074": {
        "name_zh": "站姿杠铃架上拉",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与髋同宽站立于深蹲架杠铃前方，脚尖微向外展，杠铃高度设定在膝盖高度位置。",
            "屈髋微屈膝俯身，双手正握杠铃略宽于肩，背部平直挺紧锁定，肩胛收缩锁定。",
            "呼气脚跟蹬地、臀部前推伸髋挺直身体，拉起杠铃至身体完全直立，并在顶部用力收紧臀大肌。",
            "吸气顺畅屈髋控制杠铃缓慢平稳下落放回架上支架起始位，重复规定次数。",
        ],
    },
    "0075": {
        "name_zh": "站姿俯身杠铃后束平举",
        "category": "shoulders",
        "equipment": "barbell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["traps", "rhomboids"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩同宽站立，双手正握轻杠铃，手心朝向身体。",
            "屈膝并从髋部向前俯身至躯干接近与地面平行，背部保持挺直中立。",
            "双臂微屈肘锁定，呼气由三角肌后束发力将杠铃两端向上平举提起至大臂与肩齐平高度。",
            "在最高点挤压肩后束停顿 1 秒，吸气匀速受控将杠铃下放回悬垂起始位，重复规定次数。",
        ],
    },
    "0076": {
        "name_zh": "站姿俯身杠铃后束划船",
        "category": "shoulders",
        "equipment": "barbell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["traps", "rhomboids", "biceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站立，双膝微屈，向前俯身约 60 度，背部挺直核心收紧。",
            "采用宽握距双手正握杠铃，双臂自然下垂。",
            "手肘向身体两侧展开成约 90 度角，呼气由三角肌后束主导屈肘将杠铃向胸部上方提拉。",
            "在顶部肩胛后缩感受三角肌后束强烈收缩停顿 1 秒，吸气缓慢下放杠铃回起始位，重复规定次数。",
        ],
    },
    "0077": {
        "name_zh": "站姿杠铃单腿交替向后弓步第二式",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "perSide": True,
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚并拢站立，将杠铃平稳扛于上背斜方肌上，双手握紧杠铃保持躯干挺直。",
            "单脚平稳向后撤出大步，前脚掌着地，吸气双膝同时弯曲下蹲至前侧大腿接近与地面平行。",
            "在前侧臀部与腿部张力最低点稍作停顿，呼气前侧腿蹬地发力收回后撤腿站立回正。",
            "换另一侧腿向后撤步重复动作，双侧交替进行完成规定次数。",
        ],
    },
    "0078": {
        "name_zh": "站姿杠铃单腿交替向后弓步",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "perSide": True,
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与髋同宽站立，杠铃扛在斜方肌上，挺胸收腹核心紧绷。",
            "一侧腿向后跨出一大步脚尖点地，吸气垂直平稳下蹲直至前侧大腿平行于地面、后膝接近地面。",
            "在动作底部保持身体重心平衡短暂停顿，呼气以前脚跟强力蹬地推回身体恢复直立起始位。",
            "双腿交替向后跨步完成，重复规定总次数。",
        ],
    },
    "0079": {
        "name_zh": "平凳坐姿杠铃反手腕弯举第二式",
        "category": "lower arms",
        "equipment": "barbell",
        "target": "forearms",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "brachialis"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "坐在平凳上双脚踏实地面，双手正握杠铃与肩同宽，手心朝下。",
            "将前臂平放在大腿上，手腕自然伸出膝盖边缘悬空。",
            "保持前臂静止贴紧大腿，呼气仅由手腕发力尽力向上背伸弯举杠铃。",
            "在最高屈腕点充分挤压前臂伸肌停顿 1 秒，吸气缓慢受控向下伸展手腕回起始位，重复规定次数。",
        ],
    },
    "0080": {
        "name_zh": "站姿杠铃正握反向弯举",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩同宽站立，双手正握杠铃（手心朝下反向握持），握距与肩同宽垂直垂于体前。",
            "大臂紧贴身体两侧保持静止，呼气由肱二头肌与肱肌发力屈肘向上弯举杠铃至前臂接近垂直。",
            "在最高点挤压二头肌与小臂前侧停顿 1 秒，吸气沿平稳弧线匀速下落杠铃至双臂完全伸展起始位。",
            "动作全程避免借力耸肩晃动身体，重复规定次数。",
        ],
    },
}

pending = {
    "0071": "待修图 · 规范译名为仰卧杠铃推举起坐；原动图仅有 2 帧 (nf=2) 缺失推举与卷起过程帧，待重制为 4 帧循环图。",
    "0072": "待修图 · 消除斜板歧义规范为上斜训练凳俯卧杠铃弯举（补全上斜训练凳必需器械）；原动图为 10 帧 (nf=10) 超标且手臂弯举轨迹不匀速，待重制为 4 帧循环图。",
    "0073": "待修图 · 纠正错译下拉规范为平凳仰卧杠铃过头拉背（补全平板训练凳必需器械、规避平板触发静力保持）；原动图为 10 帧 (nf=10) 超标且头部后方拉伸折返点不稳，待重制为 4 帧循环图。",
    "0074": "待修图 · 规范译名为站姿杠铃架上拉；原动图仅有 2 帧 (nf=2) 缺失离心下放与伸髋锁定过程，待重制为 4 帧循环图。",
    "0075": "待修图 · 消除后三角俗称规范为站姿俯身杠铃后束平举；原动图仅有 2 帧 (nf=2) 缺失平举上升过渡帧，待重制为 4 帧循环图。",
    "0076": "待修图 · 消除后三角俗称规范为站姿俯身杠铃后束划船；原动图仅有 2 帧 (nf=2) 缺失拉至胸前与下放过渡，待重制为 4 帧循环图。",
    "0077": "待修图 · 规避英文字符规范为站姿杠铃单腿交替向后弓步第二式（激活单侧交替计次）；原动图仅有 2 帧 (nf=2) 缺失下蹲下沉与站起过渡，待重制为 4 帧循环图。",
    "0078": "待修图 · 规范译名为站姿杠铃单腿交替向后弓步（激活单侧交替计次）；原动图仅有 2 帧 (nf=2) 缺失下蹲与起身过程帧，待重制为 4 帧循环图。",
    "0079": "待修图 · 规避英文字符并规范为平凳坐姿杠铃反手腕弯举第二式（补全平板训练凳必需器械、规避平板触发静力保持）；原动图为 10 帧 (nf=10) 超标且手腕折返角度不稳，待重制为 4 帧循环图。",
    "0080": "待修图 · 消除反手歧义规范为站姿杠铃正握反向弯举；原动图为 10 帧 (nf=10) 超标且身体轻微借力晃动，待重制为 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review69-20261116",
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
    "expected_per_side_ids": ["0077", "0078"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
