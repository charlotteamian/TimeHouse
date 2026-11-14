#!/usr/bin/env python3
"""Author Batch 66 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261113_review66"
VERSION = "1.2.71"
VERSION_CODE = 2026111301

inspected = ["0040", "0041", "0042", "0043", "0044", "0045", "0046", "0047", "0048", "0049"]
review_candidates = []
registered_media = []

definition_updates = {
    "0040": {
        "name_zh": "平凳仰卧杠铃前举过头拉胸",
        "category": "chest",
        "equipment": "barbell",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["deltoids", "triceps", "lats"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "仰卧平躺于平凳上，双脚踩实地面，双手正握杠铃置于胸部上方，双肘微屈锁死。",
            "吸气由胸肌与前锯肌控制将杠铃向头顶后方缓慢弧线放落，感受胸大肌上部与胸廓充分延展。",
            "在最远端稍作停顿，呼气由胸大肌发力将杠铃沿大弧线拉回至胸部上方。",
            "紧接着微屈手臂将杠铃垂直向前向上平稳推起，完成复合循环后重复规定次数。",
        ],
    },
    "0041": {
        "name_zh": "站姿杠铃前平举",
        "category": "shoulders",
        "equipment": "barbell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "triceps", "upper chest"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩同宽站稳，双手正握杠铃垂于大腿前侧，握距与肩同宽，背部挺直微屈双膝。",
            "保持肘部微屈并固定角度，呼气由三角肌前束主动发力向前上方平稳举起杠铃。",
            "举至杠铃与肩同高或略低于视线高度，在顶点顶峰收缩 1 秒，身体不后仰借力。",
            "吸气缓慢匀速受控沿原轨迹下放杠铃至大腿前侧起始位，重复规定次数。",
        ],
    },
    "0042": {
        "name_zh": "站姿杠铃标准颈前深蹲",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "quadriceps",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩同宽站立，脚尖微向外展，将杠铃稳固架在三角肌前束与锁骨上，双肘向前高抬平行地面。",
            "收紧腹横肌维持躯干竖直中立，吸气屈髋屈膝垂直下蹲，臀部坐入双腿之间至大腿低于水平线。",
            "在最低点维持核心刚性停顿片刻，膝盖追踪脚尖方向不内扣。",
            "呼气由大腿前侧股四头肌与臀肌强力蹬地推起身体直立还原，双肘全程保持高抬，重复规定次数。",
        ],
    },
    "0043": {
        "name_zh": "站姿杠铃颈后全幅度深蹲",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "quadriceps",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将杠铃牢固扛在斜方肌上背部，双手握稳杠铃，双脚与肩同宽站立，脚尖略向外展。",
            "挺胸收腹核心紧绷，吸气屈髋屈膝同步向后向下坐，平稳下沉身体直到髋关节略低于膝盖水平面（全深蹲幅度）。",
            "在底部消除惯性稍作停顿，保持足底三点踩实地面，不弓腰塌背。",
            "呼气由臀大肌与股四头肌爆发发力蹬地推起身体直立站回起始位，重复规定次数。",
        ],
    },
    "0044": {
        "name_zh": "站姿杠铃颈后早安折髋式",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "hamstrings",
        "muscle_group": "lower back",
        "secondary_muscles": ["lower back", "glutes"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩同宽直立，将轻中重量杠铃扛于上背斜方肌上，双手握稳，微屈双膝并固定膝关节角度。",
            "收紧核心维持脊柱中立平直，吸气主动将臀部向后推移、髋关节向后折叠，躯干俯身前倾。",
            "俯身至上半身接近与地面平行，大腿后侧腘绳肌感受到强烈拉伸感时停顿 1 秒。",
            "呼气由臀部与腘绳肌协同收缩向前顶髋，将躯干拉回直立站姿，重复规定次数。",
        ],
    },
    "0045": {
        "name_zh": "平凳仰卧杠铃断头台卧推",
        "category": "chest",
        "equipment": "barbell",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "triceps"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "仰卧平躺于平凳上，双脚踏稳地面，双手采用略宽于肩的握距正握杠铃，杠铃出架支撑于颈部上方。",
            "肘部向身体两侧大角度外展（约 80-90 度），吸气缓慢将杠铃沿直线受控下放至锁骨与喉部下方（断头台轨迹）。",
            "在杠铃距离锁骨仅 2-3 厘米处稍作停顿，感受胸大肌上部深度拉伸。",
            "呼气由胸大肌主导发力将杠铃推回起始手臂直立位，动作全程保持绝对专注与适中负重，重复规定次数。",
        ],
    },
    "0046": {
        "name_zh": "站姿身后杠铃哈克深蹲",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "quadriceps",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "杠铃放置于身后地面，双脚与肩同宽站于杠铃前方，屈髋下蹲双手正握身后杠铃杆，握距与肩同宽。",
            "挺胸立腰收紧背部，双腿蹬地发力将杠铃沿小腿与大腿后侧贴身拉起直立，骨盆前推锁死。",
            "吸气屈髋屈膝受控下蹲，杠铃沿大腿后侧缓慢下降至靠近地面或大腿平行位置。",
            "在底部短暂停留维持肌肉张力，呼气由股四头肌强力蹬地再次推起直立，按规定次数完成练习。",
        ],
    },
    "0047": {
        "name_zh": "上斜训练凳仰卧杠铃卧推",
        "category": "chest",
        "equipment": "barbell",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "triceps"],
        "required_equipment_zh": ["上斜训练凳"],
        "instructions_zh": [
            "仰卧在上斜约 30-45 度的训练凳上，双脚踩实地面，臀部和背部贴实垫面，双手正握杠铃略宽于肩。",
            "将杠铃出架推起支撑在上胸正上方，吸气屈肘缓慢受控下放杠铃至锁骨下方的上胸部。",
            "触胸轻停感受上胸肌纤维充分拉伸，手腕与小臂垂直地面。",
            "呼气由胸大肌上束主动收缩将杠铃推回上胸起始锁定位，重复规定次数。",
        ],
    },
    "0048": {
        "name_zh": "上斜训练凳仰卧反握杠铃卧推",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": ["上斜训练凳"],
        "instructions_zh": [
            "调节训练凳至上斜 30-45 度，仰卧在凳上双脚踩实地面，双手反握（掌心朝向面部）握住杠铃，握距与肩同宽。",
            "出架将杠铃支撑于胸部上方，保持肘部自然向内贴近躯干，吸气屈肘将杠铃缓慢下落至胸下沿与上腹交界处。",
            "在底部短暂停顿，呼气由肱三头肌内侧与胸大肌上部协同发力将杠铃推回起始手臂直伸位。",
            "推起全程保持手腕中立不向后过度翻折，重复规定次数。",
        ],
    },
    "0049": {
        "name_zh": "上斜训练凳俯卧杠铃划船",
        "category": "back",
        "equipment": "barbell",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms", "lats"],
        "required_equipment_zh": ["上斜训练凳"],
        "instructions_zh": [
            "将训练凳调至 30-45 度角，身体趴在上斜凳上，胸部贴紧靠垫表面，双脚脚尖踩地维持稳定。",
            "双臂垂直自然下垂双手正握杠铃，肩胛骨下沉，呼气由上背部肌群与背阔肌发力拉引双肘向后上方屈臂拉起。",
            "杠铃拉至凳面边缘贴近胸部下沿，用力夹紧肩胛骨顶峰收缩 1 秒。",
            "吸气有控制地沿原轨迹缓慢下放杠铃至手臂完全伸展，重复规定次数。",
        ],
    },
}

pending = {
    "0040": "待修图 · 规范译名为平凳仰卧杠铃前举过头拉胸（补全平板训练凳必需器械、去除加号等符号、规避平板触发静力保持）；原动图仅有 2 帧 (nf=2) 缺失过渡帧，待重制为 4 帧循环图。",
    "0041": "待修图 · 规范译名为站姿杠铃前平举；原动图为 10 帧 (nf=10) 超标且手臂升降速率不均，待重制为 4 帧循环图。",
    "0042": "待修图 · 规范译名为站姿杠铃标准颈前深蹲；原动图仅有 2 帧 (nf=2) 缺失深蹲离心下潜过程，待重制为 4 帧循环图。",
    "0043": "待修图 · 规范译名为站姿杠铃颈后全幅度深蹲；原动图仅有 2 帧 (nf=2) 缺失蹲起折返过程，待重制为 4 帧循环图。",
    "0044": "待修图 · 纠正错译好晨式为站姿杠铃颈后早安折髋式；原动图仅有 2 帧 (nf=2) 缺失折髋后移过渡，待重制为 4 帧循环图。",
    "0045": "待修图 · 纠正错译颈前卧推为平凳仰卧杠铃断头台卧推（补全平板训练凳必需器械、规避平板触发静力保持）；原动图仅有 2 帧 (nf=2) 缺失锁骨推举折返帧，待重制为 4 帧循环图。",
    "0046": "待修图 · 纠正错译哑铃深蹲为站姿身后杠铃哈克深蹲；原动图仅有 2 帧 (nf=2) 缺失身后拉起与下蹲过程，待重制为 4 帧循环图。",
    "0047": "待修图 · 规范译名为上斜训练凳仰卧杠铃卧推（补全上斜训练凳必需器械）；原动图仅有 2 帧 (nf=2) 缺失推举过程帧，待重制为 4 帧循环图。",
    "0048": "待修图 · 消除反手推歧义规范为上斜训练凳仰卧反握杠铃卧推（补全上斜训练凳必需器械）；原动图为 10 帧 (nf=10) 超标且反握推举落点抖动，待重制为 4 帧循环图。",
    "0049": "待修图 · 规范译名为上斜训练凳俯卧杠铃划船（补全上斜训练凳必需器械）；原动图为 10 帧 (nf=10) 超标且俯卧拉起幅度不稳，待重制为 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review66-20261113",
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
