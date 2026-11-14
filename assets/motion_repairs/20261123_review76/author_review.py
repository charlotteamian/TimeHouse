#!/usr/bin/env python3
"""Author Batch 76 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261123_review76"
VERSION = "1.2.81"
VERSION_CODE = 2026112301

inspected = ["0162", "0164", "0165", "0167", "0168", "0169", "0170", "0171", "0172", "0173"]
review_candidates = []
registered_media = []

definition_updates = {
    "0162": {
        "name_zh": "站姿龙门架绳索前平举",
        "category": "shoulders",
        "equipment": "cable",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "背对龙门架低位滑轮稳立，双脚与肩同宽微屈膝，双手正手握住低位绳索手柄垂于大腿前侧。",
            "挺胸收腹核心紧锁，双臂微屈肘保持角度固定，呼气由三角肌前束主导发力向前上方平稳举起手臂。",
            "举高手臂至与地面平行视线高度，在最高点稍作停顿充分收缩三角肌前束。",
            "吸气缓慢受控匀速将手柄放回大腿前侧起始位，全程避免身体后仰代偿，重复规定次数。",
        ],
    },
    "0164": {
        "name_zh": "站姿龙门架绳索前平举第二式",
        "category": "shoulders",
        "equipment": "cable",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["trapezius", "biceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽稳立于龙门架滑轮前方，双手握住低位把手，挺胸收腹保持脊柱绝对中立。",
            "双臂伸直自然下垂，呼气以肩部为轴心带动双手向前平稳抬高至肩部水平。",
            "手肘微屈锁死，在最高点充分挤压肩部前束并停顿 1 秒。",
            "吸气匀速受控将绳索放低回大腿前方，按规定次数平稳重复练习。",
        ],
    },
    "0165": {
        "name_zh": "站姿龙门架绳索把手锤式弯举",
        "category": "upper arms",
        "equipment": "cable",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "面对龙门架低位滑轮站立，双脚自然分开与肩同宽，双手采用对握握距（掌心相对）抓握绳索把手两端。",
            "上臂自然夹紧体侧并保持绝对静止，呼气由肱肌、肱二头肌外侧长头与肱桡肌主导屈肘向上弯举把手。",
            "弯举至锁骨肩部水平最高点，顶峰全力挤压手臂肌群并停顿 1 秒。",
            "吸气缓慢匀速下放把手至双臂自然伸展起始姿态，按规定次数平稳完成练习。",
        ],
    },
    "0167": {
        "name_zh": "跪姿地面龙门架绳索高位划船",
        "category": "back",
        "equipment": "cable",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双膝跪于龙门架前方的平整地面上，脚背贴地臀部微后坐，双手正手握住中高位直杆把手。",
            "挺胸直背微前倾，吸气向前伸展双臂充分拉伸背部肌群与背阔肌。",
            "呼气由上背肌群与肩胛骨主导发力后缩，顺势屈肘将横杠拉向前胸上腹部。",
            "在动作顶点极力挤压肩胛骨停顿 1 秒，吸气匀速缓慢放回把手至起始位，重复规定次数。",
        ],
    },
    "0168": {
        "name_zh": "站姿龙门架绳索单腿髋内收",
        "category": "upper legs",
        "equipment": "cable",
        "target": "adductors",
        "muscle_group": "",
        "secondary_muscles": ["glutes", "quadriceps"],
        "perSide": True,
        "required_equipment_zh": [],
        "instructions_zh": [
            "侧对龙门架低位滑轮站立，靠近机器的一侧脚踝系紧绑带，手扶立柱保持身体平衡直立。",
            "支撑腿微屈膝稳固踩地，呼气由绑带腿的大腿内收肌群强力发力将腿向内侧拉越过身体中线。",
            "在内收最深点停顿 1 秒充分感受大腿内侧肌群顶峰收缩。",
            "吸气缓慢受控将腿放回外侧起始位，换另一侧腿交替完成规定次数练习。",
        ],
    },
    "0169": {
        "name_zh": "上斜训练凳坐姿龙门架绳索卧推",
        "category": "chest",
        "equipment": "cable",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["deltoids", "triceps"],
        "required_equipment_zh": ["上斜训练凳"],
        "instructions_zh": [
            "将上斜训练凳调至约 45 度角置于龙门架中央，背部紧贴椅背坐稳，双脚平踩地面，双手握稳低位手柄。",
            "挺胸收紧肩胛骨，呼气由上胸部胸大肌主导发力，沿斜上方推举把手至双臂完全伸直。",
            "在推举顶点双手微向内聚拢并短暂停顿挤压上胸肌群。",
            "吸气屈肘受控缓慢下放把手至胸部两侧充分拉伸，按规定次数重复练习。",
        ],
    },
    "0170": {
        "name_zh": "瑜伽球上斜靠姿龙门架绳索飞鸟",
        "category": "chest",
        "equipment": "cable",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["deltoids", "triceps"],
        "required_equipment_zh": ["瑜伽球"],
        "instructions_zh": [
            "将稳固瑜伽球置于龙门架中央，背部斜靠在瑜伽球上呈上斜姿势，双脚平踏地面稳定核心。",
            "双手各握一侧低位绳索手柄，双臂向两侧展开微屈肘，吸气充分打开胸廓拉伸上胸大肌。",
            "呼气由胸大肌向上向内环抱发力将把手沿弧线向胸前正上方聚拢合拢。",
            "在合拢顶点极力挤压胸肌停顿 1 秒，吸气平稳匀速展开双臂回到起始位，重复规定次数。",
        ],
    },
    "0171": {
        "name_zh": "上斜训练凳坐姿龙门架绳索飞鸟",
        "category": "chest",
        "equipment": "cable",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["deltoids", "triceps"],
        "required_equipment_zh": ["上斜训练凳"],
        "instructions_zh": [
            "坐在调至 30-45 度的上斜训练凳上，背部紧贴靠背，双脚平踏地面，双手握住低位滑轮把手。",
            "双臂向身体两侧展开微屈肘，吸气充分扩展胸腔拉伸胸大肌锁骨部。",
            "呼气由胸大肌发力将手臂沿宽弧线向上向内合拢至胸部正上方。",
            "在最高顶点充分挤压胸肌上缝停顿 1 秒，吸气缓慢匀速放回双臂至起始位，重复规定次数。",
        ],
    },
    "0172": {
        "name_zh": "站姿前倾龙门架绳索直臂下压",
        "category": "back",
        "equipment": "cable",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "面对龙门架高位滑轮站立，双手正握直杆横杠，双手略宽于肩，躯干前倾约 30 度直背收腹。",
            "手肘微屈锁死角度，吸气双臂抬起至头部前上方，充分感受背阔肌外侧延展拉伸。",
            "呼气由背阔肌主导全力向下向大腿前侧划弧压下横杠，直至贴近大腿根部。",
            "在动作底部极力挤压背阔肌停顿 1 秒，吸气受控匀速将横杠送回高位起始点，重复规定次数。",
        ],
    },
    "0173": {
        "name_zh": "站姿前倾龙门架绳索过头臂屈伸",
        "category": "upper arms",
        "equipment": "cable",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "背对龙门架低位或中位滑轮站立，前后分腿站稳，躯干向前倾斜约 45 度，双手握住绳索把手举过头顶。",
            "大臂贴近耳侧保持角度静止锁定，吸气屈肘将把手向脑后下放，充分拉长肱三头肌长头。",
            "呼气由肱三头肌发力强力向前上方伸直小臂，直至双臂完全展开锁定。",
            "在充分伸展顶点停顿 1 秒挤压三头肌，吸气受控放回脑后起始位，重复规定次数练习。",
        ],
    },
}

pending = {
    "0162": "待修图 · 规范译名为站姿龙门架绳索前平举；原动图仅有 2 帧 (nf=2) 缺失平举至肩平与匀速下放过渡帧，待重制为 4 帧循环图。",
    "0164": "待修图 · 消除前肩推举歧义规范为站姿龙门架绳索前平举第二式；原动图仅有 2 帧 (nf=2) 缺失平举升降过渡帧，待重制为 4 帧循环图。",
    "0165": "待修图 · 消除绳索重名歧义规范为站姿龙门架绳索把手锤式弯举；原动图为 10 帧 (nf=10) 超标且手臂弯举顶峰缺乏停顿，待重制为 4 帧循环图。",
    "0167": "待修图 · 规范跪姿环境规范为跪姿地面龙门架绳索高位划船；原动图为 10 帧 (nf=10) 超标且身体轻微摇晃，待重制为 4 帧循环图。",
    "0168": "待修图 · 消除内收俗称规范为站姿龙门架绳索单腿髋内收（激活单侧交替计次）；原动图仅有 2 帧 (nf=2) 缺失内收与外展缓冲帧，待重制为 4 帧循环图。",
    "0169": "待修图 · 补全上斜训练凳器械规范为上斜训练凳坐姿龙门架绳索卧推；原动图为 10 帧 (nf=10) 超标且推举轨迹欠平稳，待重制为 4 帧循环图。",
    "0170": "待修图 · 消除健身球错译并补全器械规范为瑜伽球上斜靠姿龙门架绳索飞鸟（补全瑜伽球必需器械）；原动图为 10 帧 (nf=10) 超标且动作幅度晃动，待重制为 4 帧循环图。",
    "0171": "待修图 · 补全上斜训练凳器械规范为上斜训练凳坐姿龙门架绳索飞鸟；原动图为 10 帧 (nf=10) 超标且合拢顶点缺乏停顿，待重制为 4 帧循环图。",
    "0172": "待修图 · 消除上斜下压错译规范为站姿前倾龙门架绳索直臂下压；原动图仅有 2 帧 (nf=2) 缺失下压划弧与高位放回过渡帧，待重制为 4 帧循环图。",
    "0173": "待修图 · 消除三头肌伸展俗称规范为站姿前倾龙门架绳索过头臂屈伸；原动图仅有 2 帧 (nf=2) 缺失屈肘下放与向前推展过程帧，待重制为 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review76-20261123",
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
        "0169": ["上斜训练凳"],
        "0170": ["瑜伽球"],
        "0171": ["上斜训练凳"],
    },
    "expected_per_side_ids": ["0168"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
