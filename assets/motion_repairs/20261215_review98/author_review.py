#!/usr/bin/env python3
"""Author Batch 98 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261215_review98"
VERSION = "1.2.103"
VERSION_CODE = 2026121501

inspected = ["0774", "0775", "0776", "0786", "0788", "0796", "0798", "0811", "0818", "0830"]
review_candidates = []
registered_media = []

definition_updates = {
    "0774": {
        "name_zh": "史密斯站姿军式推举",
        "category": "shoulders",
        "equipment": "smith machine",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "upper back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚并拢或与肩同宽站立在史密斯机滑轨正下方，双膝微屈弹性站立，沉肩收紧腰腹与臀部核心。",
            "双手全正握抓握锁骨上方的杠铃杆，握距略宽于双肩，向上微推旋转杠铃解开安全挂钩。",
            "吸气控制杠铃缓慢平稳下落至上胸锁骨上沿位置，大臂下沉小臂垂直地面。",
            "在最低点停顿 1 秒，呼气由三角肌前束与中束爆发向上推起杠铃至双臂充分过头伸展位，肘部微屈不锁死，按计划重复。",
        ],
    },
    "0775": {
        "name_zh": "史密斯站姿直立划船",
        "category": "shoulders",
        "equipment": "smith machine",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["traps", "biceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站立在史密斯机滑轨前方，腰背挺直中立，挺胸收紧腹部核心。",
            "双手全正握抓握杠铃杆中央，握距与肩同宽，微推旋转解除杠铃安全卡扣，双臂自然下垂。",
            "呼气主要由三角肌中束与斜方肌主动发力，以手肘为主导向上将杠铃垂直沿滑轨向上提拉至胸部高度，手肘始终高于手腕。",
            "在最高提拉点停顿 1 秒充分挤压三角肌中束，吸气匀速受控放回杠铃至起始手臂充分垂悬伸展位，按计划重复。",
        ],
    },
    "0776": {
        "name_zh": "站姿杠铃抓举高拉",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "quads",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "glutes", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与髋同宽站立在杠铃后方，屈髋屈膝下蹲，双手采用宽握距抓握杠铃杆（宽于双肩），挺胸沉肩锁死背部。",
            "深吸气锁紧腹压，呼气由股四头肌蹬地伸膝第一拉将杠铃平稳提过膝盖上方。",
            "杠铃过膝后，爆发性全力蹬伸髋、膝、踝三关节并协同耸肩提肘，驱动杠铃沿身体竖直向上惯性拉升至胸下沿高度。",
            "在顶点停顿 1 秒感受全身后链与腿部爆发力释放，吸气控制受控回放杠铃至地面起始位，按计划重复。",
        ],
    },
    "0786": {
        "name_zh": "站姿杠铃下蹲挺",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "quads",
        "muscle_group": "",
        "secondary_muscles": ["glutes", "hamstrings", "calves", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站立，杠铃架在前肩锁骨三角肌前束丰厚处，双手扶稳杠铃，双肘抬高朝前。",
            "深吸气收紧躯干，双膝微屈向下快速缓冲浅蹲（预屈），随后双腿全力爆发向上蹬伸将杠铃向上推离肩部。",
            "当杠铃上升通过头部瞬间，双臂强力锁直手臂向上支撑杠铃，同时身体快速下沉钻入杠铃正下方接杠成全蹲姿势。",
            "在深蹲支撑底端稳固平衡停顿 1 秒，呼气由双腿协同发力蹬伸地面站立回到直立站姿起始位，受控下落杠铃，按计划重复。",
        ],
    },
    "0788": {
        "name_zh": "站姿杠铃颈后推举",
        "category": "shoulders",
        "equipment": "barbell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "upper back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站立，双膝微屈弹性站立，沉肩收腹核心锁紧维持脊柱生理中立。",
            "将杠铃平稳架在后颈上斜方肌上，双手正手全握杠铃杆，握距略宽于双肩，手肘自然下沉向两侧展开。",
            "深吸气稳定胸腔，呼气主要由三角肌中束与前束发力向上将杠铃垂直推过头顶，手臂完全伸直过顶。",
            "在推举最高点停顿 1 秒挤压肩部肌群，吸气缓慢受控将杠铃放回后颈部起始位，避免颈椎过度前探，按计划重复。",
        ],
    },
    "0796": {
        "name_zh": "站姿健腹轮前滚",
        "category": "waist",
        "equipment": "wheel roller",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["lower back", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站立在地面上，俯身前倾将健腹轮平置于双脚正前方的地面上，双手紧握两侧把手。",
            "收紧腹直肌与骨盆核心，保持背部微拱抗伸展，吸气受控驱动健腹轮缓慢向前滚出。",
            "身体逐渐向前向下舒展延伸至躯干接近与地面平行，核心极度紧绷抵抗腰椎反弓塌陷。",
            "在身体充分前伸极限点停顿 1 秒，呼气由腹肌与背阔肌强力收缩卷缩身体将健腹轮向后拉回至双脚前方起始位，按计划重复。",
        ],
    },
    "0798": {
        "name_zh": "器械健身车骑行",
        "category": "cardio",
        "equipment": "leverage machine",
        "target": "cardiovascular system",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调整健身车坐垫高度使膝盖在踏板踩至最低点时微屈约 25 至 30 度，双脚平稳踩入脚踏并拉紧锁带。",
            "双手握稳前侧车把，沉肩挺胸，保持脊柱生理中立微前倾，核心微收稳定骨盆。",
            "双腿交替顺畅驱动脚踏做 360 度圆周踩踏，控制踏频保持匀速稳定的骑行节奏。",
            "全程维持均匀深长呼吸，根据预设计划平稳维持设定阻力与时长，按计划重复。",
        ],
    },
    "0811": {
        "name_zh": "站姿六角杠硬拉",
        "category": "upper legs",
        "equipment": "trap bar",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "quadriceps", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与髋同宽站立在六角杠铃框内正中央，双脚脚尖微向外展，膝盖对准脚尖。",
            "屈髋屈膝俯身下沉重心，双手对握抓住两侧中立握把，沉肩收紧背阔肌，挺胸锁紧脊柱中立。",
            "深吸气收紧腹部核心，呼气由脚后跟用力蹬地，股四头肌与臀大肌协同发力垂直拉起六角杠铃至完全站直身姿。",
            "在站立顶峰收缩臀部停顿 1 秒，吸气控制屈髋推臀让六角杠铃沿垂直轨迹平稳放回地面起始位，按计划重复。",
        ],
    },
    "0818": {
        "name_zh": "绳索坐姿双柄对握高位下拉",
        "category": "back",
        "equipment": "cable",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "rhomboids", "rear deltoids"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "坐在高位下拉机坐垫上，调节压膝挡垫稳固卡紧大腿，双脚平踏地面保持身体平衡。",
            "双手向上伸展对握抓握挂在龙门架上的双把手把柄（掌心相对），沉肩挺胸，上身微向后仰约 10 至 15 度。",
            "呼气主要由背阔肌与大圆肌收缩发力，屈肘顺应身体侧面将双把手平稳向下拉向锁骨与上胸位置。",
            "在下拉最低点用力夹紧肩胛骨停顿 1 秒感受背部充分挤压，吸气匀速受控放回双臂至充分过头伸展位，按计划重复。",
        ],
    },
    "0830": {
        "name_zh": "平凳负重臂屈伸",
        "category": "upper arms",
        "equipment": "weighted",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双手撑在平凳前沿边缘，双手与肩同宽，掌根抵紧凳面手指朝前，双腿向前伸展脚跟着地。",
            "将杠铃片或重物平稳置于大腿前侧上方，臀部悬空滑出平凳边缘，挺胸沉肩收紧腰腹。",
            "吸气缓慢受控屈肘下沉身体，大臂紧贴躯干向后弯曲，下沉至大臂几乎与地面平行，手肘呈约 90 度角。",
            "在最低点停顿 1 秒充分拉伸肱三头肌，呼气由肱三头肌爆发推撑平凳推起身体回到起始双臂伸直位，肘部不锁死，按计划重复。",
        ],
    },
}

pending = {
    "0774": "待修图 · 消除军姿推直译规范为史密斯站姿军式推举；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0775": "待修图 · 规范划船姿态为史密斯站姿直立划船；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0776": "待修图 · 纠正抓举拉错译规范为站姿杠铃抓举高拉；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0786": "待修图 · 规范举重专业术语为站姿杠铃下蹲挺；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0788": "待修图 · 规范推举名称为站姿杠铃颈后推举；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0796": "待修图 · 消除滚轮直译规范为站姿健腹轮前滚；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0798": "待修图 · 纠正步行错译规范为器械健身车骑行；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0811": "待修图 · 规范六角杠硬拉为站姿六角杠硬拉；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0818": "待修图 · 消除平行握拉下直译规范为绳索坐姿双柄对握高位下拉；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0830": "待修图 · 纠正凳俯卧撑严重错译规范为平凳负重臂屈伸；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review98-20261215",
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
