#!/usr/bin/env python3
"""Author Batch 83 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261130_review83"
VERSION = "1.2.88"
VERSION_CODE = 2026113001

inspected = ["0238", "0239", "0240", "0241", "0242", "0243", "0244", "0245", "0246", "0247"]
review_candidates = []
registered_media = []

definition_updates = {
    "0238": {
        "name_zh": "站姿龙门架绳索直杆直臂下压",
        "category": "back",
        "equipment": "cable",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "biceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "面朝高位滑轮站立，双脚与肩同宽微屈膝微前倾，双手采用正握握距与肩同宽握住直杆横杠。",
            "双臂充分向前上方伸展，肘关节微屈锁死，挺胸收紧核心，沉肩锁紧肩胛骨。",
            "呼气由背阔肌强力发力驱动双臂弧形向下按压横杠，直至贴近大腿前侧。",
            "在动作底部顶峰收缩挤压背阔肌停顿 1 秒，吸气匀速受控让横杠顺应阻力升回高位完全拉伸，按计划重复。",
        ],
    },
    "0239": {
        "name_zh": "平凳坐姿龙门架绳索直背划船",
        "category": "back",
        "equipment": "cable",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms", "shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "端坐于平凳上，双脚平踩地面保持骨盆中立稳定，双手正握划船手柄两端伸直双臂。",
            "挺胸立腰保持脊柱正直微前倾，双臂指向中低位滑轮，收紧核心肌群。",
            "呼气由背阔肌与中背肌群发力沉肩引肘，将手柄平稳拉向下腹位置。",
            "在动作顶点充分夹紧肩胛骨停顿 1 秒，吸气匀速受控放回手柄至双臂完全伸展，按计划重复。",
        ],
    },
    "0240": {
        "name_zh": "平凳俯卧龙门架绳索反向飞鸟",
        "category": "shoulders",
        "equipment": "cable",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["traps", "rhomboids"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "俯卧在平凳上方，胸部紧贴凳面，双手各持低位滑轮交叉单把手柄自然垂直下垂。",
            "沉肩收腹保持颈椎自然中立，手肘微屈锁死，呼气由三角肌后束发力向两侧水平展开双臂做飞鸟轨迹。",
            "抬至大臂与地面接近平行高度，顶点强烈收紧挤压后肩与菱形肌停顿 1 秒。",
            "吸气缓慢匀速下放双臂回到起始垂放位置，避免利用躯干反弹借力，按规定次数重复。",
        ],
    },
    "0241": {
        "name_zh": "站姿龙门架绳索三角把下压",
        "category": "upper arms",
        "equipment": "cable",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "面向高位滑轮立柱站立，双脚与肩同宽微屈膝，微前倾躯干，双手正握 V 形三角把手两端。",
            "大臂垂直贴实躯干两侧保持稳定，前臂抬起呈 90 度，呼气由肱三头肌发力推动把手向下伸展双臂。",
            "在动作底部双臂完全伸直锁定，强烈挤压肱三头肌外侧与长头停顿 1 秒。",
            "吸气匀速受控缓慢屈肘放回把手至前臂接近水平起始位，大臂全程保持静止，按计划重复。",
        ],
    },
    "0242": {
        "name_zh": "地面仰卧龙门架绳索反向卷腹",
        "category": "waist",
        "equipment": "cable",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧在地面训练垫上，头朝低位滑轮方向，双手拉紧缆绳把手或脚踝佩戴绑带连接低位滑轮。",
            "屈膝抬起双腿大腿垂直地面，呼气由腹直肌下部主导收缩，驱动骨盆离开地面向胸腔方向反向卷屈。",
            "在卷屈顶点臀部离地充分挤压下腹部肌群停顿 1 秒，保持下背平稳。",
            "吸气匀速受控缓慢放下臀部与双腿回放至起始悬空位置，避免双腿触地借力，按计划重复。",
        ],
    },
    "0243": {
        "name_zh": "站姿龙门架绳索核心转体",
        "category": "waist",
        "equipment": "cable",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "侧对中位滑轮站立，双脚比肩略宽微屈膝微前倾，双手合握单把手柄置于胸前正前方。",
            "双臂伸直微屈肘锁定，挺胸收紧核心，呼气由腹斜肌群与核心旋转链强力发力向身体外侧旋转躯干。",
            "旋转约 90 度至对侧最远端顶峰停顿 1 秒，目视双手轨迹保持骨盆相对稳定。",
            "吸气匀速受控平稳回转躯干至起始正中位，单侧完成后换边站立重复练习。",
        ],
    },
    "0244": {
        "name_zh": "站姿龙门架绳索单臂转体划船",
        "category": "back",
        "equipment": "cable",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "biceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "面向低位或中位滑轮弓步站立，单手持握滑轮手柄，手臂向前伸直，对侧手置于腰髋稳定身体。",
            "挺胸收腹，呼气由同侧背阔肌主导向后拉肘，同时顺势带动上身躯干微幅向同侧转体划动。",
            "在划船动作顶点手肘贴紧肋侧并充分夹紧背阔肌停顿 1 秒，感受背肌强烈收缩。",
            "吸气匀速受控缓慢放直手臂回转躯干至起始伸展位，单侧完成后换另一侧手臂重复。",
        ],
    },
    "0245": {
        "name_zh": "坐姿龙门架绳索反握高位下拉",
        "category": "back",
        "equipment": "cable",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "端坐在高位下拉器械坐垫上，挡板牢牢卡住大腿前侧，双脚平踏地面保持身体平衡稳定。",
            "双手采用与肩同宽的反握握距（掌心朝向自己）握住横杠两端，双臂充分向上伸直伸展背部。",
            "挺胸微后仰约 15 度，呼气由背阔肌下部发力带动双肘垂直向下拉引横杠至锁骨下方上胸处。",
            "在动作底部充分挤压背阔肌与肱二头肌停顿 1 秒，吸气控制横杠缓慢匀速放回高位完全拉伸，按计划重复。",
        ],
    },
    "0246": {
        "name_zh": "站姿龙门架绳索直立划船",
        "category": "shoulders",
        "equipment": "cable",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["traps", "biceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "面朝低位滑轮稳固站立，双脚与肩同宽，双手采用窄于或等于肩宽的正握握距握紧短杠横梁。",
            "挺胸沉肩收腹，呼气由三角肌外侧中束与上斜方肌协同发力，驱动手肘向上向外垂直提拉短杠至锁骨高度。",
            "在动作顶点手肘始终保持略高于手腕，顶峰停顿 1 秒充分收缩肩部，吸气匀速受控下放短杠至完全下垂起始位。",
            "全程避免利用身体前后晃动甩动代偿借力，按规定次数平稳完成。",
        ],
    },
    "0247": {
        "name_zh": "平凳坐姿龙门架绳索反握腕弯举",
        "category": "lower arms",
        "equipment": "cable",
        "target": "forearms",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "brachialis"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "坐在平凳前沿，前臂平放支撑在大腿上，手腕探出膝关节边缘悬空面向低位滑轮。",
            "双手采用反握握距（掌心朝上）握紧短杠横杆，吸气放松手腕让短杠轻微下沉拉伸前臂屈肌。",
            "呼气由前臂屈肌群全力发力向上屈曲手腕，将短杠向上卷动至最高幅度。",
            "在最高点顶峰收缩停顿 1 秒充分挤压前臂肌肉，吸气匀速受控放平手腕还原至起始位，按计划重复。",
        ],
    },
}

pending = {
    "0238": "待修图 · 消除英文字符规范为站姿龙门架绳索直杆直臂下压；原动图仅有 2 帧 (nf=2) 缺失直臂下压至大腿与还原过程帧，待重制为 4 帧循环图。",
    "0239": "待修图 · 补全平凳支持器械规范为平凳坐姿龙门架绳索直背划船；原动图为 10 帧 (nf=10) 超标且躯干轻微晃动，待重制为 4 帧循环图。",
    "0240": "待修图 · 消除仰卧错译并补全平凳器械规范为平凳俯卧龙门架绳索反向飞鸟；原动图为 10 帧 (nf=10) 超标且双臂抬起顶峰缺乏停顿，待重制为 4 帧循环图。",
    "0241": "待修图 · 消除英文字符规范为站姿龙门架绳索三角把下压；原动图为 10 帧 (nf=10) 超标且伸臂速度偏快，待重制为 4 帧循环图。",
    "0242": "待修图 · 规范反向卷腹规范为地面仰卧龙门架绳索反向卷腹；原动图为 10 帧 (nf=10) 超标且屈腿轨迹不均匀，待重制为 4 帧循环图。",
    "0243": "待修图 · 规范核心转体译名为站姿龙门架绳索核心转体；原动图仅有 2 帧 (nf=2) 缺失转体两端过渡帧，待重制为 4 帧循环图。",
    "0244": "待修图 · 规范单臂转体划船规范为站姿龙门架绳索单臂转体划船（激活单侧交替计次）；原动图为 10 帧 (nf=10) 超标且单侧拉动节奏偏快，待重制为 4 帧循环图。",
    "0245": "待修图 · 规范反握高位下拉译名为坐姿龙门架绳索反握高位下拉；原动图仅有 2 帧 (nf=2) 缺失反握下拉至上胸与还原过程帧，待重制为 4 帧循环图。",
    "0246": "待修图 · 规范直立划船译名消除歧义为站姿龙门架绳索直立划船；原动图仅有 2 帧 (nf=2) 缺失提肘至锁骨与下放过程帧，待重制为 4 帧循环图。",
    "0247": "待修图 · 补全平凳支持器械规范为平凳坐姿龙门架绳索反握腕弯举；原动图仅有 2 帧 (nf=2) 缺失屈腕与卷起过程帧，待重制为 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review83-20261130",
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
        "0239": ["平板训练凳"],
        "0240": ["平板训练凳"],
        "0247": ["平板训练凳"],
    },
    "expected_per_side_ids": ["0244"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
