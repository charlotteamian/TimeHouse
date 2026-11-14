#!/usr/bin/env python3
"""Author Batch 90 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261207_review90"
VERSION = "1.2.95"
VERSION_CODE = 2026120701

inspected = ["0577", "0578", "0579", "0580", "0581", "0582", "0583", "0584", "0585", "0586"]
review_candidates = []
registered_media = []

definition_updates = {
    "0577": {
        "name_zh": "器械坐姿水平推胸",
        "category": "chest",
        "equipment": "leverage machine",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调节推胸器械座椅高度，确保推胸握把位于胸部中中部水平线，背部与臀部紧贴靠背，双脚踩实地面。",
            "双手握紧推胸把手掌心朝下或微相对，沉肩挺胸，肩胛骨收紧贴紧后靠垫。",
            "呼气由胸大肌发力带动肱三头肌协同推进，向前平稳推起把手直至双臂充分伸展，注意手肘不超伸锁死。",
            "在推起最高点顶峰收缩胸大肌停顿 1 秒，吸气控制把手匀速缓慢后撤回放至胸大肌充分拉伸起始位，按计划重复。",
        ],
    },
    "0578": {
        "name_zh": "器械站姿硬拉",
        "category": "upper legs",
        "equipment": "leverage machine",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "quads"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与髋同宽稳固站在器械踏板上，下蹲并双手紧握硬拉杠杆把手，掌心相对或朝向自己。",
            "挺胸沉肩紧锁核心，脊柱维持自然平直生理曲度，屈髋屈膝建立后链肌群张力。",
            "呼气由臀大肌与股四头肌强力蹬伸踏板，驱动杠杆平稳拉起并完全直立伸展髋膝关节。",
            "在直立顶点臀部强力收紧停顿 1 秒，吸气控制杠杆受控匀速屈髋下沉回落至起始拉伸位，按计划重复。",
        ],
    },
    "0579": {
        "name_zh": "器械坐姿前高位下拉",
        "category": "back",
        "equipment": "leverage machine",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "rhomboids", "rear deltoids"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调节座椅高度与压膝垫位置，双脚踩实地面，面朝器械坐稳，膝盖牢固卡在挡垫下方。",
            "双手宽握抓持前下拉手柄掌心朝前，挺胸沉肩，上身微后仰保持下背部生理微拱。",
            "呼气由背阔肌主动收缩发力，屈肘沿身体侧向将手柄向下拉至锁骨与胸部上方。",
            "在拉至最低点收紧夹紧肩胛骨停顿 1 秒，吸气匀速受控将手柄放回至初始手臂充分上伸拉伸位，按计划重复。",
        ],
    },
    "0580": {
        "name_zh": "器械无握力耸肩",
        "category": "back",
        "equipment": "leverage machine",
        "target": "traps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调节器械高度，将前臂或双肘稳妥卡在器械软垫托架中，双脚与肩同宽稳固站立或坐姿固定。",
            "挺胸沉肩收紧腹部，脊柱保持中立平直，双臂自然下垂不受握力疲劳限制。",
            "呼气由斜方肌上束主动收缩向上垂直耸起双肩，使肩峰尽可能贴近耳垂。",
            "在最高耸肩点顶峰收缩停顿 1 秒充分刺激斜方肌，吸气匀速受控下放双肩回到初始充分拉伸位，按计划重复。",
        ],
    },
    "0581": {
        "name_zh": "器械坐姿高位划船",
        "category": "back",
        "equipment": "leverage machine",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "rear deltoids"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调节座椅高度与胸垫前后距离，坐在坐垫上胸部稳固贴靠前方支撑垫，双脚平踏地面踩实踏板。",
            "双手对握抓持高位把手，初始双臂斜上方伸展建立上背张力，挺胸沉肩保持脊柱中立。",
            "呼气由上背肌群与菱形肌协同发力，屈肘将把手向身体侧后下方拉动至胸肋两侧。",
            "在动作顶点肩胛骨用力向后夹紧收缩停顿 1 秒，吸气匀速受控前伸回放至起始拉伸位，按计划重复。",
        ],
    },
    "0582": {
        "name_zh": "器械跪姿单腿弯举",
        "category": "upper legs",
        "equipment": "leverage machine",
        "target": "hamstrings",
        "muscle_group": "",
        "secondary_muscles": ["glutes", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调整器械阻力滚筒位置，一侧膝盖跪在支撑软垫上，双肘前趴支撑在上垫面上维持躯干平稳。",
            "训练侧腿伸展将脚跟或阿基里斯腱部位紧密抵住阻力滚筒，腹部微收骨盆保持水平中立。",
            "呼气由训练侧腘绳肌发力向上屈膝后勾，将阻力滚筒平稳拉起卷向臀部方向。",
            "在弯举最高点紧绷收缩大腿后侧腘绳肌停顿 1 秒，吸气控制小腿缓慢匀速下放回起始接近伸直位，单侧完成后换另一侧腿。",
        ],
        "perSide": True,
    },
    "0583": {
        "name_zh": "器械跪姿核心转体",
        "category": "waist",
        "equipment": "leverage machine",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双膝跪在器械旋转垫板上，双手握紧固定把手，保持上身挺拔挺胸，骨盆与垫板紧密贴合。",
            "收紧核心腹肌与腹外斜肌，以躯干为轴主动发力克服阻力向一侧旋转扭转。",
            "在旋转顶点顶峰收缩侧腹肌群停顿 1 秒，吸气匀速受控回转至初始正向中立位置。",
            "随后向另一侧对称进行扭转，交替循环完成规定次数。",
        ],
    },
    "0584": {
        "name_zh": "器械坐姿侧平举",
        "category": "shoulders",
        "equipment": "leverage machine",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["traps", "upper back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调节座椅高度，坐在坐垫上胸背挺直贴靠背垫，双肘外侧贴合在器械侧平举阻力软垫上。",
            "双手轻握辅助把手掌心朝内，沉肩挺胸避免耸肩借力，肘关节保持微屈固定角度。",
            "呼气由三角肌中束主导发力，驱动双肘向身体两侧斜上方平稳抬升直至上臂接近平行地面。",
            "在抬至最高点顶峰收紧三角肌中束停顿 1 秒，吸气控制双臂缓慢匀速落回身体两侧起始位，按计划重复。",
        ],
    },
    "0585": {
        "name_zh": "器械坐姿腿屈伸",
        "category": "upper legs",
        "equipment": "leverage machine",
        "target": "quads",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调节座椅靠背与阻力滚筒位置，坐在坐垫上背部紧贴靠背，双脚脚背前方卡在阻力滚筒下缘。",
            "双手握紧座椅两侧固定把手保持臀部与大腿贴紧坐垫，膝关节对准器械旋转转轴。",
            "呼气由股四头肌强力发力伸直双膝，向上平稳抬起滚筒直至双腿完全伸展但膝关节不超伸锁死。",
            "在伸直顶点顶峰收缩股四头肌停顿 1 秒，吸气控制滚筒缓慢匀速下落回小腿垂直起始位，按计划重复。",
        ],
    },
    "0586": {
        "name_zh": "器械俯卧腿弯举",
        "category": "upper legs",
        "equipment": "leverage machine",
        "target": "hamstrings",
        "muscle_group": "",
        "secondary_muscles": ["calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "面朝下俯卧在腿弯举训练机上，膝盖微露出垫边，脚踝后侧紧贴阻力滚筒下方。",
            "双手握紧前方握把贴紧胸垫，收紧核心保持骨盆与大腿紧贴卧垫，避免臀部弓起借力。",
            "呼气由双侧腘绳肌发力驱动双膝向上屈曲，将滚筒平稳后卷至贴近臀部位置。",
            "在最高点充分挤压大腿后侧腘绳肌停顿 1 秒，吸气控制小腿匀速受控下放至双腿接近伸直起始位，按计划重复。",
        ],
    },
}

pending = {
    "0577": "待修图 · 消除杠杆直译规范为器械坐姿水平推胸；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0578": "待修图 · 消除杠杆直译规范为器械站姿硬拉；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0579": "待修图 · 消除杠杆直译规范为器械坐姿前高位下拉；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0580": "待修图 · 消除杠杆直译规范为器械无握力耸肩；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0581": "待修图 · 消除杠杆直译规范为器械坐姿高位划船；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0582": "待修图 · 消除杠杆直译并激活单侧独立计次规范为器械跪姿单腿弯举；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0583": "待修图 · 消除杠杆直译规范为器械跪姿核心转体；原动图仅 2 帧且边缘杂色，待重制为 4 帧循环图。",
    "0584": "待修图 · 消除杠杆直译规范为器械坐姿侧平举；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0585": "待修图 · 消除杠杆直译规范为器械坐姿腿屈伸；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
    "0586": "待修图 · 消除机器错译（仰卧纠正为俯卧）规范为器械俯卧腿弯举；原动图多达 10 帧且边缘杂色，待重制为 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review90-20261207",
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
    "expected_per_side_ids": ["0582"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
