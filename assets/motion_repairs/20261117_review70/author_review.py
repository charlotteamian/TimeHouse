#!/usr/bin/env python3
"""Author Batch 70 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261117_review70"
VERSION = "1.2.75"
VERSION_CODE = 2026111701

inspected = ["0081", "0082", "0083", "0084", "0085", "0086", "0087", "0088", "0089", "0090"]
review_candidates = []
registered_media = []

definition_updates = {
    "0081": {
        "name_zh": "坐姿牧师凳杠铃反握弯举",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms", "brachialis"],
        "required_equipment_zh": ["牧师凳"],
        "instructions_zh": [
            "坐在牧师椅上双脚踏实地面，胸部靠紧斜托垫上缘，双臂大臂完全平贴在斜托板上，双手正握杠铃（手心朝下反向握持）与肩同宽。",
            "大臂始终保持贴紧托板静止，呼气由肱二头肌与肱肌发力屈肘向上弯举杠铃至前臂接近垂直。",
            "在顶点充分挤压肱二头肌与前臂肌群停顿 1 秒，吸气沿斜板缓慢匀速下放杠铃至手臂完全伸展。",
            "全程大臂不离开托板表面消除借力，按规定次数重复练习。",
        ],
    },
    "0082": {
        "name_zh": "平凳坐姿杠铃反手腕弯举",
        "category": "lower arms",
        "equipment": "barbell",
        "target": "forearms",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "brachialis"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "坐在平凳上双脚踏实地面，双手正握杠铃与肩同宽，手心朝下反向握杠。",
            "将前臂平放在大腿上，手腕自然伸出膝盖边缘悬空。",
            "保持前臂静止贴紧大腿，呼气仅由手腕发力尽力向上背伸弯举杠铃。",
            "在最高屈腕点充分挤压前臂伸肌停顿 1 秒，吸气缓慢受控向下伸展手腕回起始位，重复规定次数。",
        ],
    },
    "0083": {
        "name_zh": "平凳跪姿杠铃推腹滚轮",
        "category": "waist",
        "equipment": "barbell",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "triceps", "lats"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "跪在平凳前方的垫子上，双手与肩同宽正握平凳表面的杠铃杆两端。",
            "收紧腹部核心与背部肌群，缓慢向前推动杠铃沿平凳面延伸滑动，身体逐渐伸展拉长。",
            "推至躯干与手臂接近完全延展的张力极限点短暂停顿，感受腹直肌强烈的离心牵拉抗阻。",
            "呼气收缩腹直肌强力后拉杠铃沿平凳滑动滚回膝前起始位，全程腰椎避免过度塌陷借力。",
        ],
    },
    "0084": {
        "name_zh": "跪姿地面杠铃推腹滚轮",
        "category": "waist",
        "equipment": "barbell",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "lower back", "lats"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双膝跪在训练垫上，双手正握杠铃与肩同宽置于膝前地面，核心紧绷骨盆微后倾锁定。",
            "平稳向前滚动杠铃，手臂向前延伸、身体向地面平展下沉直至躯干接近水平地面。",
            "在最远延展点维持腹部核心高度张力稍作停顿，避免骨盆前倾塌腰。",
            "呼气由腹直肌收缩发力将杠铃向膝盖方向拉回起始位，保持受控匀速完成规定次数。",
        ],
    },
    "0085": {
        "name_zh": "站姿杠铃罗马尼亚硬拉",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与髋同宽站立，正手握住杠铃垂于大腿前侧，挺胸收腹肩胛后缩锁定。",
            "膝盖保持微屈固定角度，吸气由髋部主动向后折叠后推，杠铃沿大腿与小腿贴身缓慢垂直下落。",
            "下落至小腿中段感受腘绳肌与臀大肌充分受拉伸展开时短暂停顿。",
            "呼气由臀部向前强力伸髋推回站直起始位，并在顶部收紧臀大肌锁定，重复规定次数。",
        ],
    },
    "0086": {
        "name_zh": "平凳坐姿杠铃颈后推举",
        "category": "shoulders",
        "equipment": "barbell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "upper back", "traps"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "端坐在平凳上双脚踏实地面，双手正握杠铃略宽于肩，将杠铃置于颈后斜方肌上方。",
            "挺胸收紧核心保持躯干竖直中立，呼气由三角肌发力将杠铃沿垂直轨迹推举过头顶上方至双臂完全伸直。",
            "在最高点稍作停顿锁定，吸气控制杠铃平稳缓慢下落回颈后起始高度。",
            "推举全程保持手肘向两侧自然展开，按规定次数平稳完成练习。",
        ],
    },
    "0087": {
        "name_zh": "平凳坐姿杠铃布拉德福德前后推举",
        "category": "shoulders",
        "equipment": "barbell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "upper back", "traps"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "端坐在平凳上双脚踏实地面，双手略宽于肩正握杠铃置于胸前锁骨高度。",
            "呼气由三角肌发力将杠铃刚好推过头顶高度，顺势掠过发顶下落至颈后肩膀高度。",
            "紧接着由颈后再次微幅推起刚过头顶，顺势前移下落回胸前起始锁骨高度，完成一次前后循环。",
            "动作全程保持三角肌持续张力不锁定肘关节，以平稳节奏重复完成练习。",
        ],
    },
    "0088": {
        "name_zh": "平凳坐姿踏台杠铃双腿提踵",
        "category": "lower legs",
        "equipment": "barbell",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "quadriceps"],
        "required_equipment_zh": ["平板训练凳", "稳固踏台"],
        "instructions_zh": [
            "坐在平凳上，将前脚掌踩在稳固踏台或脚垫边缘，杠铃平稳置于大腿下端近膝盖处并用双手握持固定。",
            "吸气缓慢将脚后跟尽力向下沉放，直至小腿三头肌与跟腱获得充分拉伸。",
            "在最深拉伸点停顿片刻，呼气由小腿肌群爆发发力提踵将脚跟抬至最高点。",
            "在最高顶峰收缩点停顿 1 秒充分挤压小腿肌，缓慢受控下放脚跟回起始拉伸位，重复规定次数。",
        ],
    },
    "0089": {
        "name_zh": "平凳坐姿杠铃窄握集中弯举",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "双脚平踩地面端坐在平凳上，双膝自然向两侧打开，双手窄距反握杠铃，双臂手肘内侧平稳抵在两腿大腿内侧上方。",
            "上臂始终紧靠大腿消除晃动借力，呼气由肱二头肌孤立发力屈肘向上弯举杠铃至前臂接近垂直。",
            "在最高收缩顶点用力挤压肱二头肌停顿 1 秒，吸气匀速受控将杠铃缓慢下放至手臂近乎完全伸直。",
            "全程保持身体躯干平稳不耸肩，按规定次数重复练习。",
        ],
    },
    "0090": {
        "name_zh": "平凳坐姿杠铃早安折髋式",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "lower back"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "端坐在平凳边缘双脚与肩同宽踏实地面，将适重杠铃平稳扛于上背斜方肌上，双手握紧固定。",
            "挺胸收紧腰腹核心保持脊柱中立平直，吸气主动由髋关节向前折叠俯身倾斜躯干向下。",
            "俯身至躯干接近大腿水平且背部平直未弯腰时稍作停顿，感受臀肌与后侧链张力。",
            "呼气由臀大肌发力强力向后伸髋推起躯干平稳回至端坐起始位，重复规定次数。",
        ],
    },
}

pending = {
    "0081": "待修图 · 规范译名为坐姿牧师凳杠铃反握弯举（补全牧师凳必需器械）；原动图为 10 帧 (nf=10) 超标且手臂弯举轨迹不匀速，待重制为 4 帧循环图。",
    "0082": "待修图 · 消除反腕俗称规范为平凳坐姿杠铃反手腕弯举（补全平板训练凳必需器械、规避平板触发静力保持）；原动图为 10 帧 (nf=10) 超标且手腕折返角度不稳，待重制为 4 帧循环图。",
    "0083": "待修图 · 规范译名为平凳跪姿杠铃推腹滚轮（补全平板训练凳必需器械、规避平板触发静力保持）；原动图仅有 2 帧 (nf=2) 缺失推腹前滑与回收过渡帧，待重制为 4 帧循环图。",
    "0084": "待修图 · 消除滚轮简写规范为跪姿地面杠铃推腹滚轮；原动图仅有 2 帧 (nf=2) 缺失身体延展与收腹回缩过程帧，待重制为 4 帧循环图。",
    "0085": "待修图 · 规范译名为站姿杠铃罗马尼亚硬拉；原动图仅有 2 帧 (nf=2) 缺失屈髋折叠下沉与伸髋锁死过程，待重制为 4 帧循环图。",
    "0086": "待修图 · 消除后脑推举俗称规范为平凳坐姿杠铃颈后推举（补全平板训练凳必需器械、规避平板触发静力保持）；原动图为 10 帧 (nf=10) 超标且颈后推举轨迹偏移，待重制为 4 帧循环图。",
    "0087": "待修图 · 规范译名为平凳坐姿杠铃布拉德福德前后推举（补全平板训练凳必需器械、规避平板触发静力保持）；原动图仅有 2 帧 (nf=2) 缺失前后翻转过渡过程，待重制为 4 帧循环图。",
    "0088": "待修图 · 补全踏台支持并规范为平凳坐姿踏台杠铃双腿提踵（补全平板训练凳与稳固踏台必需器械、规避平板触发静力保持）；原动图仅有 2 帧 (nf=2) 缺失踝关节拉伸与提踵顶峰过程，待重制为 4 帧循环图。",
    "0089": "待修图 · 规范译名为平凳坐姿杠铃窄握集中弯举（补全平板训练凳必需器械、规避平板触发静力保持）；原动图仅有 2 帧 (nf=2) 缺失大臂固定弯举与下放过程，待重制为 4 帧循环图。",
    "0090": "待修图 · 消除好晨式错译规范为平凳坐姿杠铃早安折髋式（补全平板训练凳必需器械、规避平板触发静力保持）；原动图为 10 帧 (nf=10) 超标且折髋俯身过程缺失张力停顿，待重制为 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review70-20261117",
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
