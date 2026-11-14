#!/usr/bin/env python3
"""Author Batch 65 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261112_review65"
VERSION = "1.2.70"
VERSION_CODE = 2026111201

inspected = ["0030", "0031", "0032", "0033", "0034", "0035", "0036", "0037", "0038", "0039"]
review_candidates = []
registered_media = []

definition_updates = {
    "0030": {
        "name_zh": "平凳仰卧杠铃窄握卧推",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "仰卧平躺于平凳上，双脚踏实地面，双手正握杠铃，握距与肩同宽或略窄于肩宽。",
            "将杠铃出架支撑于胸部正上方，双肘自然朝前内夹，大臂贴紧身体两侧。",
            "吸气缓慢屈肘将杠铃受控下落至下胸或剑突位置，肘关节向后下方折叠。",
            "触胸稍作停顿，呼气由肱三头肌主导发力推直双臂将杠铃推回起始位，重复规定次数。",
        ],
    },
    "0031": {
        "name_zh": "站姿杠铃标准弯举",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩同宽直立站稳，双手反握杠铃，握距与肩同宽，杠铃垂于大腿前方。",
            "上臂紧贴躯干两侧固定，呼气由肱二头肌收缩带动前臂屈肘向上弧形弯举杠铃至胸肩前侧。",
            "在动作最高点充分挤压肱二头肌停顿 1 秒，保持身体不借力后仰。",
            "吸气缓慢有控制地沿原弧线轨迹下放杠铃至手臂完全伸直，重复规定次数。",
        ],
    },
    "0032": {
        "name_zh": "站姿传统杠铃硬拉",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "lower back", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与髋同宽站立，杠铃杆贴近胫骨正中，俯身屈髋屈膝双手正握或正反握杠铃，握距略宽于双腿外侧。",
            "下沉肩胛骨锁紧后背，挺胸立腰收紧核心，双腿蹬地发力带动杠铃沿胫骨直线贴身拉起。",
            "过膝后强力伸髋顶臀，身体直立锁死，在最高点夹紧臀大肌短暂停顿。",
            "吸气由髋关节向后折叠，控制杠铃沿大腿与小腿贴身缓慢下放回地面，重复规定次数。",
        ],
    },
    "0033": {
        "name_zh": "下斜凳仰卧杠铃卧推",
        "category": "chest",
        "equipment": "barbell",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": ["带勾脚的下斜训练凳"],
        "instructions_zh": [
            "躺在下斜训练凳上，双脚牢固勾在脚垫滚轴下方固定下半身，双手正握杠铃，握距略宽于肩。",
            "出架将杠铃移至下胸正上方伸直双臂，吸气屈肘受控下沉杠铃至下胸肋骨边缘。",
            "在底部触胸稍作停顿感受下胸肌充分拉伸，保持手腕与前臂垂直地面。",
            "呼气由胸大肌下部主导发力将杠铃垂直推回起始位，动作顶点不锁死手肘，重复规定次数。",
        ],
    },
    "0034": {
        "name_zh": "下斜凳仰卧杠铃屈臂拉背",
        "category": "back",
        "equipment": "barbell",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "chest"],
        "required_equipment_zh": ["带勾脚的下斜训练凳"],
        "instructions_zh": [
            "平躺在下斜凳上，双脚勾紧固定轴，双手窄握杠铃置于胸部上方，微屈手肘并锁定肘角度。",
            "吸气由背阔肌控制，将杠铃沿大弧线平稳向头顶斜后下方下放，直到感受到背阔肌深层拉伸。",
            "在充分延展位停顿片刻，呼气由背阔肌与大圆肌强力发力将杠铃沿原弧线拉回至胸部上方。",
            "全程保持肘关节微屈且角度固定不变，重复规定次数。",
        ],
    },
    "0035": {
        "name_zh": "下斜凳仰卧杠铃窄握臂屈伸",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": ["带勾脚的下斜训练凳"],
        "instructions_zh": [
            "双脚勾住下斜凳滚轴平躺，双手窄握杠铃置于面部上方，大臂垂直于地面并固定位置。",
            "吸气仅活动前臂屈肘将杠铃缓慢受控下落至额头上方或头顶斜后侧，感受肱三头肌充分延展。",
            "在最低点稍作停顿，呼气由肱三头肌强力收缩伸展肘关节，将杠铃推回起始手臂直立位。",
            "全程大臂始终保持相对静止不动，重复规定次数。",
        ],
    },
    "0036": {
        "name_zh": "下斜凳仰卧杠铃宽握卧推",
        "category": "chest",
        "equipment": "barbell",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": ["带勾脚的下斜训练凳"],
        "instructions_zh": [
            "躺在下斜训练凳上双腿勾牢固定，双手采用宽于肩部约 1.5 倍的宽握距握紧杠铃。",
            "出架将杠铃稳固悬于胸口，吸气屈肘将杠铃垂直下落至胸部两侧，感受胸肌外侧深度拉伸。",
            "触胸轻停，呼气由胸大肌爆发性发力向正上方推起杠铃至手臂接近伸直。",
            "在最高点主动内收夹紧胸肌，吸气离心缓慢下放，重复规定次数。",
        ],
    },
    "0037": {
        "name_zh": "下斜凳仰卧杠铃宽握拉背",
        "category": "back",
        "equipment": "barbell",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "chest"],
        "required_equipment_zh": ["带勾脚的下斜训练凳"],
        "instructions_zh": [
            "平躺在下斜凳上固定双脚，双手采用宽握距反握或正握杠铃悬于胸前。",
            "双肘微屈锁死角度，吸气由背阔肌控制将杠铃向头后斜下方弧线放落，获得更大拉背幅度。",
            "在最远端短暂停顿强化背阔肌离心受力，呼气背阔肌收紧将杠铃拉回胸上方起始位。",
            "动作平顺稳定不借力，按规定次数完成练习。",
        ],
    },
    "0038": {
        "name_zh": "站姿杠铃贴身拖曳弯举",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽直立，挺胸收腹，双手反握杠铃贴在大腿前侧。",
            "呼气弯举时，肘部主动向身体后方移动并屈肘，使杠铃始终紧贴躯干正面垂直向上拖曳提升。",
            "杠铃拖至胸下部顶峰位，用力挤压肱二头肌外侧长头停顿 1 秒。",
            "吸气沿躯干正面缓慢下放还原至大腿前侧，重复规定次数。",
        ],
    },
    "0039": {
        "name_zh": "站姿杠铃胸前贴靠深蹲",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "quadriceps",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩同宽站立，将杠铃双手抱持或托在胸前紧贴胸骨，双肘向下收拢。",
            "核心紧绷保持脊柱中立挺直，吸气屈髋屈膝垂直下蹲，臀部向后下方坐至大腿平行地面。",
            "在深蹲最低点维持核心张力短暂停顿，膝盖始终指向脚尖方向。",
            "呼气由臀部和大腿前侧强力蹬地推直身体站起还原，重复规定次数。",
        ],
    },
}

pending = {
    "0030": "待修图 · 规范译名为平凳仰卧杠铃窄握卧推（补全平板训练凳必需器械、规避平板触发静力保持）；原动图为 10 帧 (nf=10) 超标且杠铃落点晃动，待重制为 4 帧循环图。",
    "0031": "待修图 · 规范译名为站姿杠铃标准弯举；原动图仅有 2 帧 (nf=2) 缺失动作折返过程帧，待重制为 4 帧循环图。",
    "0032": "待修图 · 规范译名为站姿传统杠铃硬拉；原动图仅有 2 帧 (nf=2) 缺失下放离心与拉起向心过程，待重制为 4 帧循环图。",
    "0033": "待修图 · 规范译名为下斜凳仰卧杠铃卧推（补全带勾脚的下斜训练凳必需器械）；原动图为 10 帧 (nf=10) 超标且推举速率不匀，待重制为 4 帧循环图。",
    "0034": "待修图 · 规范译名为下斜凳仰卧杠铃屈臂拉背（补全带勾脚的下斜训练凳必需器械）；原动图仅有 2 帧 (nf=2) 缺失下落拉伸与拉回过渡帧，待重制为 4 帧循环图。",
    "0035": "待修图 · 规范译名为下斜凳仰卧杠铃窄握臂屈伸（补全带勾脚的下斜训练凳必需器械、消除头顶推歧义）；原动图为 10 帧 (nf=10) 超标且肘关节定位偏移，待重制为 4 帧循环图。",
    "0036": "待修图 · 规范译名为下斜凳仰卧杠铃宽握卧推（补全带勾脚的下斜训练凳必需器械）；原动图为 10 帧 (nf=10) 超标且胸肌推起停顿不合规范，待重制为 4 帧循环图。",
    "0037": "待修图 · 规范译名为下斜凳仰卧杠铃宽握拉背（补全带勾脚的下斜训练凳必需器械）；原动图为 10 帧 (nf=10) 超标且过头拉背轨迹抖动，待重制为 4 帧循环图。",
    "0038": "待修图 · 规范译名为站姿杠铃贴身拖曳弯举；原动图为 10 帧 (nf=10) 超标且贴身拉起过程形变严重，待重制为 4 帧循环图。",
    "0039": "待修图 · 规范译名为站姿杠铃胸前贴靠深蹲；原动图仅有 2 帧 (nf=2) 缺失深蹲下沉离心过程，待重制为 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review65-20261112",
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
