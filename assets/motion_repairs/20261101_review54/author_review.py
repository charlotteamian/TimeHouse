#!/usr/bin/env python3
"""Author Batch 54 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261101_review54"
VERSION = "1.2.59"
VERSION_CODE = 2026110101

inspected = ["3239", "2189", "3287", "2292", "3288", "2293", "3289", "2294", "3291", "2317"]
review_candidates = []
registered_media = []

definition_updates = {
    "3239": {
        "name_zh": "高姿俯撑单手交替拍肩",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "obliques",
        "secondary_muscles": ["shoulders", "triceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "采用直臂高姿俯撑起始姿势，双手略窄于肩按实地面，双脚分开略宽于髋前脚掌点地稳住下肢，身体从头到脚跟呈斜直线。",
            "核心与腹斜肌全程绷紧抵抗骨盆左右扭转，重心略微稳向一侧撑地手臂。",
            "吸气时抬起另一侧手轻快拍触对侧肩头并在顶峰短暂稳定，随后放回地面按实。",
            "呼气换对侧手以相同控制力交替拍肩，全程避免塌腰或顶髋晃动，重复规定次数。",
        ],
    },
    "2189": {
        "name_zh": "靠背凳坐姿双哑铃颈后臂屈伸",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["直立靠背训练凳"],
        "instructions_zh": [
            "坐姿于直立靠背训练凳上，腰背轻贴靠垫、双脚分开踩实地面，双手正握或对握各持一只哑铃直臂高举至头顶正上方。",
            "保持双上臂夹近耳侧、肘尖朝向正上方或微前斜固定不动、核心收紧。",
            "吸气时缓慢受控屈肘将双哑铃一并下放至脑后深度，充分拉伸肱三头肌。",
            "呼气集中肱三头肌发力伸直双肘举回高举起始位，重复规定次数。",
        ],
    },
    "3287": {
        "name_zh": "平凳反向臂屈伸",
        "category": "upper arms",
        "equipment": "body weight",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "背对平板训练凳，双手分开约与肩同宽反抓凳面边缘，双腿向前伸直以脚跟着地、臀部前移悬空靠近凳缘。",
            "核心收紧、肩胛骨下沉避免耸肩，双肘略微夹向身后。",
            "吸气时受控屈肘向后垂直下沉躯干，直到上臂接近与地面平行。",
            "呼气由肱三头肌发力推直双臂将身体抬回直臂高位，重复规定次数。",
        ],
    },
    "2292": {
        "name_zh": "站姿俯身哑铃反向飞鸟",
        "category": "shoulders",
        "equipment": "dumbbell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["trapezius", "rhomboids"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩或髋同宽站稳，微屈膝盖、屈髋俯身使背部平直接近水平，双手对握各持哑铃自然垂于躯干下方。",
            "核心绷紧维持躯干角度固定，呼气时三角肌后束发力带动双臂沿大弧线向两侧平展拉起，肘部微屈固定角度。",
            "抬至双臂与地面大致平行、双肩后侧明显收紧时略停，避免借腰背甩动或猛耸斜方肌。",
            "吸气缓慢受控沿原弧线放回垂臂起始位，重复规定次数。",
        ],
    },
    "3288": {
        "name_zh": "双杠后置臂屈伸",
        "category": "chest",
        "equipment": "body weight",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": ["双杠"],
        "instructions_zh": [
            "背向站立于稳固双杠之间或一侧杠前，双手反握或正握身后的杠面直臂撑起身体，双腿向前下方伸直脚跟着地或微悬。",
            "沉肩挺胸、核心收紧并微后仰躯干使胸肌受力。",
            "吸气受控屈肘向后外侧展开下放身体，感受胸大肌与肩前束充分拉伸。",
            "呼气发力伸直双肘推起身体回到高位，重复规定次数。",
        ],
    },
    "2293": {
        "name_zh": "站姿牧师凳哑铃佐特曼弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "forearms",
        "secondary_muscles": [],
        "required_equipment_zh": ["牧师凳"],
        "instructions_zh": [
            "双脚分开站稳于牧师凳后侧，俯身将双上臂后侧贴靠在倾斜垫面上，双手反握（掌心朝前上方）各持一只哑铃垂臂起始。",
            "保持上臂稳贴斜垫不动，呼气时肱二头肌集中发力将哑铃向上弯举至肩前高位。",
            "在最高点短暂停顿并将前臂内旋转为正握（掌心朝向前下方），随即缓慢受控匀速下放哑铃至底端以强化前臂离心收缩。",
            "底端转回掌心朝前的反握起始位，重复规定次数。",
        ],
    },
    "3289": {
        "name_zh": "双杠前臂下放臂屈伸",
        "category": "upper arms",
        "equipment": "body weight",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": ["双杠"],
        "instructions_zh": [
            "双手正握或对握稳固双杠直臂撑起身体，双膝弯曲使双脚悬空于身体下方，核心与臀部紧收。",
            "身体控制性向后下方顺势移动同时屈肘下放，使双前臂逐步贴近或贴靠于双杠上表面以深层牵拉肱三头肌。",
            "感受肱三头肌与肘周承受极大张力后在底端略作控制。",
            "发力伸肘向前上方重新撑推起身体回到直臂悬空高位，重复规定次数。",
        ],
    },
    "2294": {
        "name_zh": "坐姿牧师凳哑铃佐特曼弯举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "forearms",
        "secondary_muscles": [],
        "required_equipment_zh": ["牧师凳"],
        "instructions_zh": [
            "端坐于牧师凳座垫上，双脚分开平踩地面，腋窝与双上臂后侧贴靠在斜垫表面，双手反握各持一只哑铃自然伸臂于垫前。",
            "稳住躯干与上臂贴垫不动，呼气时肱二头肌发力向上弯举哑铃至高位。",
            "顶峰短暂停顿后顺势旋腕改为掌心朝下正握，吸气匀速放回哑铃感受前臂肌群离心控制。",
            "回到臂展底端后旋转手腕恢复掌心朝上反握位，重复规定次数。",
        ],
    },
    "3291": {
        "name_zh": "分腿慢起手倒立",
        "category": "upper arms",
        "equipment": "body weight",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "采取地面分腿坐姿，双腿向左右尽量大幅外展伸直，双手分开约与肩同宽实按于胯前内侧地面，双臂伸直压肩收腹。",
            "核心极度收紧并前倾肩部重心，以肱三头肌、三角肌及髂腰核心力量发力下压地面将臀部与分直双腿缓慢悬空离地。",
            "维持紧身与夹肘控制继续向上缓慢推举起髋部与双腿，直至躯干垂直、双腿在空中呈大幅分腿稳定倒立。",
            "在最高点短暂停顿后反向下落受控返回地面分腿坐姿，重复规定次数。",
        ],
    },
    "2317": {
        "name_zh": "平凳坐姿屈臂哑铃侧平举",
        "category": "shoulders",
        "equipment": "dumbbell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["trapezius", "rhomboids"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "坐稳于平板训练凳一端，双脚分开平踩地面、腰背挺直、核心收紧。",
            "双手各握一只哑铃置于身体两侧，保持肘关节先屈曲约 90 度固定折角、掌心朝向身体内侧。",
            "呼气时三角肌中束发力带动双大臂向两侧外展平抬至与肩及地面平行，全程维持小臂屈肘角度与躯干稳定。",
            "高点略作停顿后吸气缓慢受控沿原弧线放回两侧起始位，重复规定次数。",
        ],
    },
}

pending = {
    "3239": "待修图 · 纠正图不对题的“跪姿平板拍肩（男）”为高姿俯撑单手交替拍肩（图像为直腿足尖高姿俯撑、去“平板”静态触发词、补全腹斜肌主训与单侧计次）；原图 F2 足尖独立滑偏 (+8,+10)/(+10,-2) 而撑手在 (-8,+10)，锚点匹配分 <= 0.9474，待重制。",
    "2189": "待修图 · 已规范为靠背凳坐姿双哑铃颈后臂屈伸（补全直立靠背训练凳、去除误归主训的肩部）；原图 F0/F1 底端 y=479 截断 (bottom=32/31) 且 F2 高举哑铃顶缘 y=0 严重截断 (top=27)，待重制。",
    "3287": "待修图 · 纠正错译“肘撑”为平凳反向臂屈伸（补全平板训练凳、移除误归主训的胸部）；原图 F1/F2 平凳 (+8,0)/(+2,+24) 与双脚 (-7,-21)/(-25,+18) 大幅错位漂移，待重制。",
    "2292": "待修图 · 已规范为站姿俯身哑铃反向飞鸟（去除误归主训的斜方肌）；原图 F2 头部后移 (-3,+17) 而双脚 (-3,+12) 存在 5 px 垂直差速且 head bs=0.9239 < 0.96，待重制。",
    "3288": "待修图 · 纠正错译“韩国俯卧撑”为双杠后置臂屈伸（补全双杠支撑、移除误归主训的肱三头肌）；原图全帧双杠发生位移形变 (F1(+14,-1)/F2(+8,+14), bs=0.8969 < 0.96)，待重制。",
    "2293": "待修图 · 已规范为站姿牧师凳哑铃佐特曼弯举（补全牧师凳，保留二头+前臂双主训红标）；原图牧师凳斜垫与左/右支脚跨帧横拉错位 (preacher_leg_left(-2,0) vs right(0,0), max_res > 12 px, min_sc < 0.80)，待重制。",
    "3289": "待修图 · 纠正错译“不可能俯卧撑”为双杠前臂下放臂屈伸（补全双杠支撑、移除误归主训的胸部）；原图双杠构图晃动失真 (bs=0.8654 < 0.96) 且随屈臂下探全身大幅滑移，待重制。",
    "2294": "待修图 · 已规范为坐姿牧师凳哑铃佐特曼弯举（补全牧师凳，保留二头+前臂双主训红标）；原图 F1 右脚与右凳腿 (+7,0) 相比左脚 (+3,0) 横向拉伸 4 px 且 F2 右脚 (-3,+3) bs=0.9580 < 0.96，待重制。",
    "3291": "待修图 · 纠正错译步骤为分腿慢起手倒立（移除误归主训的肩部为肱三头肌）；原图从分腿坐地慢起倒立全程支撑手变形漂移 (hands bs=0.6180) 且躯干大幅倒转腾空，待重制。",
    "2317": "待修图 · 已规范为平凳坐姿屈臂哑铃侧平举（补全平板训练凳、去除误归主训的斜方肌）；原图 F1 左脚独立偏移 (-6,-3) 而右脚与凳脚留于 (0,0)/(-1,0)（全局刚体平移残差 >= 5.0 px > 2.0 px），待重制。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review54-20261101",
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
    "expected_per_side_ids": ["3239"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
