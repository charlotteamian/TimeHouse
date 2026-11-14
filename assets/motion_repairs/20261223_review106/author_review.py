#!/usr/bin/env python3
"""Author Batch 106 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261223_review106"
VERSION = "1.2.111"
VERSION_CODE = 2026122301

inspected = ["1015", "1016", "1017", "1018", "1022", "1023", "1253", "1254", "1255", "1256"]
review_candidates = []
registered_media = []

definition_updates = {
    "1015": {
        "name_zh": "站姿弹力带垂直帕洛夫推举",
        "category": "waist",
        "equipment": "band",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["obliques", "glutes", "delts"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将弹力带固定在胸部高度的坚固锚点上，侧身垂直于锚点站立，双脚与肩同宽微屈膝站立。",
            "双手对合紧握弹力带把手收于胸口中央，拉紧弹力带使之产生横向拉力，挺胸收腹沉肩。",
            "呼气核心肌群强力等长抗旋转发力，双手顺畅向上垂直推举过头顶伸直，对抗弹力带向侧面旋转拉扯的力矩。",
            "在动作最高点顶峰收缩停顿 1 秒感受腹肌与核心的强抗扭张力，吸气受控屈肘将双手降回至胸口起始位，按计划重复。",
        ],
    },
    "1016": {
        "name_zh": "坐姿弹力带腕弯举",
        "category": "lower arms",
        "equipment": "band",
        "target": "forearms",
        "muscle_group": "",
        "secondary_muscles": ["biceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "端坐在训练凳或椅子上，双脚平踩地面踩住弹力带底端，双手反握（掌心朝上）握持弹力带把手。",
            "前臂平贴在同侧大腿面上，手腕悬出膝盖前端边缘，手腕放松顺势向下伸展。",
            "呼气前臂屈肌群集中发力，向上收缩卷曲手腕，将弹力带拉至最高点。",
            "在顶点顶峰收缩挤压前臂内侧肌群停顿 1 秒，吸气匀速受控放慢下落回至起始位，按计划重复。",
        ],
    },
    "1017": {
        "name_zh": "站姿弹力带斜上举",
        "category": "shoulders",
        "equipment": "band",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["traps", "rhomboids"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽踩在弹力带中段上，双手各握弹力带两端手柄垂于大腿前侧，掌心相对或朝内。",
            "挺胸收腹，双臂微屈肘锁定，肩胛骨微下沉稳定躯干。",
            "呼气三角肌前束与斜方肌协同发力，双臂沿斜上方 45 度角平稳上举，身体与双臂呈现斜上展身姿。",
            "在动作顶点挤压肩胛与肩部肌群停顿 1 秒，吸气匀速受控放慢双臂回落至大腿前起始位，按计划重复。",
        ],
    },
    "1018": {
        "name_zh": "站姿弹力带耸肩",
        "category": "back",
        "equipment": "band",
        "target": "traps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽踩在弹力带中段上，双手各握弹力带两端手柄自然垂于身体两侧或大腿前侧。",
            "挺胸沉肩锁紧核心，双臂完全伸直放松，颈部自然中立。",
            "呼气斜方肌上束集中主动发力，垂直向上耸起双肩至最高点，尽可能贴近耳垂。",
            "在顶点顶峰收缩停顿 1 秒充分挤压斜方肌，吸气匀速受控放慢双肩平稳下沉恢复至起始位，按计划重复。",
        ],
    },
    "1022": {
        "name_zh": "站姿俯身弹力带三角肌后束划船",
        "category": "shoulders",
        "equipment": "band",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["upper back", "traps", "biceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽踩在弹力带中段上，双手正握弹力带两端手柄。",
            "微屈双膝，屈髋向前俯身约 45 度至 60 度，背部挺直，双臂自然下垂，肘尖指向身体斜后外侧。",
            "呼气三角肌后束集中发力，大臂向两侧展开并将手柄向胸腹之间拉起，肘部向外上方引拉。",
            "在动作最高点顶峰收缩挤压三角肌后束停顿 1 秒，吸气匀速受控放慢双臂平稳下沉恢复至起始位，按计划重复。",
        ],
    },
    "1023": {
        "name_zh": "站姿弹力带直背直膝硬拉",
        "category": "upper legs",
        "equipment": "band",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽踩在弹力带中段上，双手各握弹力带两端手柄，双膝保持微屈并锁定膝关节角度。",
            "挺胸沉肩锁死背部肌群，保持脊柱中立且背部完全平直，收紧腹部核心。",
            "吸气屈髋将臀部向后推送，躯干前倾顺势将双手沿大腿前侧下放至膝下小腿中段，感受腘绳肌与臀肌充分拉伸。",
            "呼气臀大肌与腘绳肌强力收缩伸髋，拉直身体恢复至站立起始位，在顶点顶峰收紧臀肌停顿 1 秒，按计划重复。",
        ],
    },
    "1253": {
        "name_zh": "器械俯身驴式提踵",
        "category": "lower legs",
        "equipment": "leverage machine",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "glutes"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "俯身于驴式提踵机上，将垫板或负重臂稳固靠在后腰下背（骶骨上方），双手握住机器前方扶手以稳定身体。",
            "前脚掌稳踩在踏板边缘，脚后跟悬空并完全伸展下放至最低点，保持双膝微屈固定不锁死。",
            "呼气小腿三头肌（腓肠肌与比目鱼肌）强力收缩发力，全力抬高脚后跟并踮起脚尖至最高点。",
            "在最高收缩点顶峰收缩停顿 1 秒充分挤压小腿肌群，吸气匀速受控放慢下放脚后跟恢复至拉伸起始位，按计划重复。",
        ],
    },
    "1254": {
        "name_zh": "平凳仰卧弹力带推胸",
        "category": "chest",
        "equipment": "band",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "delts"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "将弹力带横压在平板训练凳下方或背部下方，仰卧于平凳上，双脚踏实地面，沉肩收腹挺胸。",
            "双手各握弹力带两端手柄置于胸部两侧外缘，手腕中立，小臂垂直于地面。",
            "呼气胸大肌发力将弹力带向上向前推起，双臂在胸部正上方伸直并顶峰挤压胸肌，肘关节微屈不锁死。",
            "在顶点停顿 1 秒挤压胸肌，吸气受控放慢下放双手至胸前起始位，按计划重复。",
        ],
    },
    "1255": {
        "name_zh": "下斜凳仰卧杠铃过头拉背",
        "category": "back",
        "equipment": "barbell",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "chest", "shoulders"],
        "required_equipment_zh": ["带勾脚的下斜训练凳"],
        "instructions_zh": [
            "仰卧在带勾脚的下斜训练凳上，双脚牢固卡紧固定海绵筒，头部处于低位，核心收紧。",
            "双手正握杠铃置于胸部上方，握距与肩同宽，双臂伸直微屈肘锁定肘关节。",
            "吸气背阔肌受控对抗拉伸，沿弧线轨迹将杠铃缓慢放落至头后方深处，感受背阔肌与胸廓充分延展。",
            "呼气背阔肌强力收缩发力，沿原弧线轨迹将杠铃拉回至胸部正上方起始位，按计划重复。",
        ],
    },
    "1256": {
        "name_zh": "下斜凳仰卧杠铃反握卧推",
        "category": "chest",
        "equipment": "barbell",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "delts"],
        "required_equipment_zh": ["带勾脚的下斜训练凳"],
        "instructions_zh": [
            "仰卧在带勾脚的下斜训练凳上，双脚牢固卡紧固定海绵筒，收紧核心臀部贴紧凳面。",
            "双手反握（掌心朝向面部）杠铃，握距略宽于肩宽，双肘适度内收贴近身体两侧。",
            "呼气胸大肌（尤其下胸与胸肌内侧）与肱三头肌发力，将杠铃平稳向上推起至双臂伸直微屈肘位置。",
            "吸气受控放慢将杠铃缓慢下落至下胸部上方，轻触下胸后再次向上推起，按计划重复。",
        ],
    },
}

pending = {
    "1015": "待修图 · 规范垂直帕洛夫推举动作命名为站姿弹力带垂直帕洛夫推举；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1016": "待修图 · 规范腕屈动作姿态为坐姿弹力带腕弯举；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1017": "待修图 · 消除字母直译规范为站姿弹力带斜上举；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1018": "待修图 · 规范耸肩姿态为站姿弹力带耸肩；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1022": "待修图 · 消除后三角直译规范为站姿俯身弹力带三角肌后束划船；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1023": "待修图 · 规范直背直膝硬拉命名为站姿弹力带直背直膝硬拉；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1253": "待修图 · 消除背卧小腿抬高错译规范为器械俯身驴式提踵；原动图 10 帧且帧率不合规，待重制为标准 4 帧循环图。",
    "1254": "待修图 · 规范平凳卧推动作为平凳仰卧弹力带推胸并补全平板训练凳支持器械；原动图帧时长不合规且背景杂色，待重制为标准 4 帧循环图。",
    "1255": "待修图 · 消除下拉错译规范为下斜凳仰卧杠铃过头拉背并校准背阔肌目标及带勾脚下斜训练凳支持器械；原动图仅 2 帧且帧率不合规，待重制为标准 4 帧循环图。",
    "1256": "待修图 · 消除反手直译规范为下斜凳仰卧杠铃反握卧推并补全带勾脚下斜训练凳支持器械；原动图 10 帧且帧率不合规，待重制为标准 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review106-20261223",
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
        "1254": ["平板训练凳"],
        "1255": ["带勾脚的下斜训练凳"],
        "1256": ["带勾脚的下斜训练凳"],
    },
    "expected_per_side_ids": [],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
