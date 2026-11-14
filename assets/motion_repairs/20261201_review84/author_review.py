#!/usr/bin/env python3
"""Author Batch 84 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261201_review84"
VERSION = "1.2.89"
VERSION_CODE = 2026120101

inspected = ["0248", "0271", "0272", "0445", "0446", "0447", "0448", "0449", "0450", "0451"]
review_candidates = []
registered_media = []

definition_updates = {
    "0248": {
        "name_zh": "平凳俯卧曲轴杠铃划船",
        "category": "back",
        "equipment": "barbell",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms", "shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "俯卧趴在平板训练凳上，胸部与腹部紧贴凳面支撑，双手采用正握握距抓握曲轴杠铃，双臂自然下垂垂直地面。",
            "保持颈椎中立目视凳面，沉肩锁紧肩胛骨，双脚前脚掌触地保持下半身支撑稳定。",
            "呼气由上背肌群与背阔肌发力沉肩引肘，向上将杠铃平稳提拉向胸腹交界处。",
            "在动作顶点充分夹紧双侧肩胛骨停顿 1 秒，吸气控制杠铃缓慢匀速下放至双臂完全伸展，按计划重复。",
        ],
    },
    "0271": {
        "name_zh": "瑜伽球仰卧卷腹",
        "category": "waist",
        "equipment": "stability ball",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors"],
        "required_equipment_zh": ["瑜伽球"],
        "instructions_zh": [
            "仰卧在瑜伽球上，下背与腰部贴实球体弧面，双脚与肩同宽平踏地面，膝关节呈 90 度角保持骨盆稳定。",
            "双手轻触双耳后侧或交叉抱于胸前，吸气微幅后仰拉伸腹直肌，保持颈椎自然中立不拽颈。",
            "呼气由腹直肌强力主导收缩，向上卷动肋骨朝骨盆靠拢，将上背部抬离球体表面。",
            "在卷腹顶点强烈挤压腹肌停顿 1 秒，吸气匀速受控缓慢放回上身至贴合球弧起始位，按计划重复。",
        ],
    },
    "0272": {
        "name_zh": "瑜伽球直臂仰卧卷腹",
        "category": "waist",
        "equipment": "stability ball",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors"],
        "required_equipment_zh": ["瑜伽球"],
        "instructions_zh": [
            "仰卧在瑜伽球上，下背贴实球体获得良好承托，双脚平踩地面稳定下肢，双臂向斜后上方伸直锁死肘关节。",
            "收紧核心肌群，颈椎与躯干保持同一轴线，吸气微幅延展腹部感受腹直肌拉伸。",
            "呼气由腹直肌发力带动双肩离开球体向上卷屈，双臂保持笔直指向斜前上方引导发力轨迹。",
            "在动作最高点顶峰收缩腹直肌停顿 1 秒，吸气匀速受控放回上身至起始拉伸位置，按规定次数重复。",
        ],
    },
    "0445": {
        "name_zh": "站姿曲杆反重力肩推",
        "category": "shoulders",
        "equipment": "ez barbell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "chest"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽稳固站立，双手采用窄于或等于肩宽的正握握距握持曲杆杠铃于锁骨前方。",
            "挺胸立腰收紧臀腹核心，肘关节微屈置于杠铃下方垂直承托重量。",
            "呼气由三角肌前束与中束强力发力，垂直将曲杆推举过头顶直至双臂完全伸展但肘不超伸。",
            "在推举顶点停顿 1 秒充分感受肩部受压，吸气匀速受控缓慢下放曲杆回到锁骨起始位，按计划重复。",
        ],
    },
    "0446": {
        "name_zh": "站姿曲杆窄握弯举",
        "category": "upper arms",
        "equipment": "ez barbell",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽自然站立，挺胸收腹，双手采用窄握反握握距（握在曲杆内侧内倾斜面）握持杠铃自然下垂。",
            "大臂垂直贴紧躯干两侧并保持静止，吸气沉肩稳定肩胛骨。",
            "呼气由肱二头肌外侧长头全力收缩发力，弯屈手肘将曲杆向上提拉弧形卷动至胸前高度。",
            "在动作顶点充分挤压肱二头肌顶峰停顿 1 秒，吸气匀速受控下放曲杆至双臂完全伸展，按计划重复。",
        ],
    },
    "0447": {
        "name_zh": "站姿曲杆标准弯举",
        "category": "upper arms",
        "equipment": "ez barbell",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站立，挺胸收腹下沉双肩，双手采用与肩同宽反握握距（握在曲杆外侧斜面）握紧杠铃。",
            "大臂紧贴身体两侧垂直固定，吸气做好核心支撑准备。",
            "呼气由肱二头肌主导收缩，保持手腕中立驱动小臂向上沿弧线提拉曲杆至肩前高位。",
            "在弯举顶点强烈挤压肱二头肌顶峰停顿 1 秒，吸气控制杠铃缓慢匀速下放至起始伸展位，按计划重复。",
        ],
    },
    "0448": {
        "name_zh": "下斜训练凳仰卧曲杆窄握臂屈伸",
        "category": "upper arms",
        "equipment": "ez barbell",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": ["带勾脚的下斜训练凳"],
        "instructions_zh": [
            "双脚牢固卡紧下斜训练凳的脚勾，仰卧在凳面上，双手采用窄握反向握距握紧曲杆垂直举于胸前上方。",
            "大臂保持微向头侧倾斜并锁紧角度静止，核心收紧紧贴凳面。",
            "吸气以肘关节为轴缓慢屈肘，平稳下放曲杆至前额或头顶斜上方，充分拉伸肱三头肌。",
            "呼气由肱三头肌强力发力推动曲杆沿原轨迹伸展还原至顶点并停顿 1 秒，吸气匀速回放，按计划重复。",
        ],
    },
    "0449": {
        "name_zh": "上斜训练凳坐姿曲杆过头臂屈伸",
        "category": "upper arms",
        "equipment": "ez barbell",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["上斜训练凳"],
        "instructions_zh": [
            "调整训练凳至约 45 度上斜角度，背靠椅背坐稳，双脚平踩地面，双手采用窄握正握握紧曲杆推举至头顶上方。",
            "大臂垂直或微后倾贴近双耳侧并保持固定，挺胸收腹锁紧核心。",
            "吸气控制手肘弯曲，缓慢将曲杆放向脑后枕骨方向，深度拉伸肱三头肌长头。",
            "呼气由肱三头肌主导发力伸展前臂向上推起曲杆至起始完全伸展位并停顿 1 秒，按计划重复。",
        ],
    },
    "0450": {
        "name_zh": "平凳仰卧曲杆杰姆卧推",
        "category": "upper arms",
        "equipment": "ez barbell",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "仰卧在平板训练凳上，双脚踏实地面，双手采用与肩同宽略窄正握握持曲杆置于上胸正上方伸直双臂。",
            "沉肩收腹使上背与臀部紧贴凳面，保持手腕中立与小臂稳定。",
            "吸气保持手肘微向身体内收夹紧，屈肘同时让杠铃沿垂直轨迹平稳下沉至锁骨与颈部之间上方约一拳高度。",
            "呼气由肱三头肌强力发力快速向上推展还原至双臂伸直，顶点顶峰收缩停顿 1 秒，按计划重复。",
        ],
    },
    "0451": {
        "name_zh": "站姿曲杆正握反向弯举",
        "category": "upper arms",
        "equipment": "ez barbell",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽稳固站立，双手采用与肩同宽正握握距（掌心朝下向后）握在曲杆斜把面上自然下垂。",
            "挺胸沉肩收腹，大臂贴紧躯干两侧保持稳定锁定，手腕保持中立挺直。",
            "呼气由肱桡肌与前臂伸肌协同肱二头肌发力，向上弯曲手肘将杠铃提拉至胸前高度。",
            "在动作最高点顶点挤压前臂肌群停顿 1 秒，吸气匀速受控缓慢放回曲杆至双臂下垂起始位，按计划重复。",
        ],
    },
}

pending = {
    "0248": "待修图 · 消除英文字符并补全平凳支持器械规范为平凳俯卧曲轴杠铃划船；原动图仅有 2 帧 (nf=2) 缺失杠铃提拉与下放过程帧，待重制为 4 帧循环图。",
    "0271": "待修图 · 规范球上卷腹译名并补全瑜伽球支持器械规范为瑜伽球仰卧卷腹；原动图存在严重锚点漂移 (delta=90)，待重制为 4 帧循环图。",
    "0272": "待修图 · 规范直臂卷腹译名并补全瑜伽球器械规范为瑜伽球直臂仰卧卷腹；原动图边框存在接触像素 (border pixels=12)，待重制为 4 帧循环图。",
    "0445": "待修图 · 规范曲杆肩推译名消除歧义为站姿曲杆反重力肩推；原动图仅有 2 帧 (nf=2) 缺失推举过头顶与还原过程帧，待重制为 4 帧循环图。",
    "0446": "待修图 · 规范曲杆窄握弯举规范为站姿曲杆窄握弯举；原动图为 10 帧 (nf=10) 超标且提拉过程缺乏顶峰停顿，待重制为 4 帧循环图。",
    "0447": "待修图 · 规范曲杆标准弯举译名为站姿曲杆标准弯举；原动图仅有 2 帧 (nf=2) 缺失小臂提拉与下放过程帧，待重制为 4 帧循环图。",
    "0448": "待修图 · 消除英文字符并补全下斜凳支持器械规范为下斜训练凳仰卧曲杆窄握臂屈伸；原动图仅有 2 帧 (nf=2) 缺失屈肘下放与推起过程帧，待重制为 4 帧循环图。",
    "0449": "待修图 · 规范过头臂屈伸译名并补全上斜凳支持器械规范为上斜训练凳坐姿曲杆过头臂屈伸；原动图仅有 2 帧 (nf=2) 缺失下沉至脑后与伸臂过程帧，待重制为 4 帧循环图。",
    "0450": "待修图 · 消除英文字符JM并补全平凳器械规范为平凳仰卧曲杆杰姆卧推；原动图为 10 帧 (nf=10) 超标且动作轨迹不平稳，待重制为 4 帧循环图。",
    "0451": "待修图 · 消除反握误译规范为站姿曲杆正握反向弯举；原动图为 10 帧 (nf=10) 超标且上臂轻微晃动，待重制为 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review84-20261201",
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
        "0248": ["平板训练凳"],
        "0271": ["瑜伽球"],
        "0272": ["瑜伽球"],
        "0448": ["带勾脚的下斜训练凳"],
        "0449": ["上斜训练凳"],
        "0450": ["平板训练凳"],
    },
    "expected_per_side_ids": [],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
