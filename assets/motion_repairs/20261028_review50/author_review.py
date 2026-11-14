#!/usr/bin/env python3
"""Author Batch 50 review updates, pending notes, sources, code baseline, and QA spec (all 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261028_review50"
VERSION = "1.2.55"
VERSION_CODE = 2026102801

inspected = ["3168", "1732", "3193", "1733", "3201", "1734", "3202", "1735", "3203", "1736"]
review_candidates = []
registered_media = []

definition_updates = {
    "3168": {
        "name_zh": "悬挂带深蹲划船",
        "category": "back",
        "equipment": "body weight",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "shoulders", "quadriceps"],
        "required_equipment_zh": ["TRX 悬挂带"],
        "instructions_zh": [
            "双手对握或正握稳固悬挂带手柄，双脚分开与肩同宽站立，双臂前伸拉直悬挂带并将身体后倾微靠张力。",
            "吸气屈膝推髋向后下方蹲低至深蹲位，背部保持平直、双膝不明显内扣。",
            "在深蹲底位或蹬地站起同时，上背与肩胛发力屈肘将胸腹顺势拉近悬挂带手柄，夹紧肩胛骨。",
            "顶峰略作停顿后缓慢伸臂后退回到深蹲或直立伸展预备位，重复规定次数。",
        ],
    },
    "1732": {
        "name_zh": "单侧前弓步过顶哑铃臂屈伸",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "triceps",
        "muscle_group": "triceps",
        "secondary_muscles": ["shoulders", "core", "quadriceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开站立，双手协握同一只哑铃（或各持哑铃并拢）举过头顶至双臂接近伸直，核心收紧。",
            "一侧腿向前跨出屈膝下蹲呈稳定前弓步姿势（后腿膝部近地不碰地），躯干保持直立。",
            "维持大臂稳定朝上且肘部朝前内收，吸气屈肘将哑铃有控制地向脑后下方低放至肱三头肌充分拉伸。",
            "呼气集中肱三头肌发力向上伸肘推举哑铃回过顶伸直位，完成规定次数后换前侧弓步腿重复。",
        ],
    },
    "3193": {
        "name_zh": "罗马椅跪姿俯身臀腿抬起",
        "category": "upper legs",
        "equipment": "body weight",
        "target": "hamstrings",
        "muscle_group": "glutes",
        "secondary_muscles": ["lower back"],
        "required_equipment_zh": ["罗马椅"],
        "instructions_zh": [
            "调整器械脚踝护垫与腿垫间距以贴合小腿长度，双腿俯卧架设并将脚跟抵紧后侧挡垫、膝前抵实弧形护垫。",
            "双臂交叉贴于胸前，起始从竖直跪立高位收紧臀肌与核心出发。",
            "有控制地屈伸髋膝顺势向前下方缓慢俯倒躯干，直到身体接近水平位，全程靠腘绳肌与臀肌制动不塌腰。",
            "随后集中腘绳肌与臀大肌协同发力拉起躯干返回接近竖直跪立高位，重复规定次数。",
        ],
    },
    "1733": {
        "name_zh": "上斜凳仰卧双臂哑铃臂屈伸",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "triceps",
        "muscle_group": "triceps",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["上斜训练凳"],
        "instructions_zh": [
            "将训练凳调整至上斜角度，仰躺其上使肩背稳贴靠垫、双脚分开平踩地面。",
            "双手对握各持一只哑铃垂直举至肩胸上方，大臂保持稳固并略微后倾。",
            "大臂位置固定不动，吸气屈肘有控制地将两只哑铃下放至头顶两侧斜后方，感受肱三头肌拉伸。",
            "呼气集中肱三头肌发力伸肘将哑铃推回上方伸直起始位，重复规定次数。",
        ],
    },
    "3201": {
        "name_zh": "四分之一卷腹起身",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧于平坦地面或训练垫上，双膝弯曲约 90 度、双脚分开平踩地面，手指轻扶耳后双肘自然展开。",
            "收紧腹部核心，呼气顺势向上卷起肩胛与上背部离开地面约四分之一幅度，下背仍轻贴地面。",
            "在腹肌收缩顶点短暂控制后吸气缓慢有控制地平躺回起始位，避免双手抱头猛拽颈椎。",
        ],
    },
    "1734": {
        "name_zh": "瑜伽球坐姿双臂哑铃后屈伸",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "triceps",
        "muscle_group": "triceps",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["瑜伽球"],
        "instructions_zh": [
            "坐在稳固的瑜伽球上，双脚分开踩实地面维持球身稳定，双手对握各持一只哑铃。",
            "屈髋将躯干略微向前俯倾并保持背部挺直，抬起双侧大臂贴近躯干侧面使前臂约呈 90 度垂放。",
            "大臂贴体固定不动，呼气时肱三头肌发力向后伸直双前臂至顶峰挤压收紧。",
            "在最高点短暂停顿后吸气缓慢屈肘放回预备屈臂位，重复规定次数。",
        ],
    },
    "3202": {
        "name_zh": "仰卧半程起坐",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧于地面或瑜伽垫上，双膝屈曲、双脚平踩地面，双手轻置耳侧或头后侧。",
            "腹直肌集中收缩发力，呼气将肩背及躯干抬起至与地面约成 45 度半程高度，避免借惯性甩腰。",
            "在顶点略作停顿后吸气有控制地逐节放回肩背躺平，重复规定次数。",
        ],
    },
    "1735": {
        "name_zh": "平凳仰卧单臂哑铃臂屈伸",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "triceps",
        "muscle_group": "triceps",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "仰卧在稳固的平板训练凳上，双脚平踩地面、核心轻收以稳固骨盆与肩背。",
            "工作侧单手对握一只哑铃垂直举至肩胸正上方，非工作手自然放在体侧或腹部辅助平衡。",
            "保持上臂竖直固定不动，吸气屈肘有控制地将哑铃缓慢下放至前额或头顶旁侧。",
            "在底位短暂停顿感受肱三头肌拉伸后，呼气发力伸肘推回垂直高位，完成规定次数后换臂练习。",
        ],
    },
    "3203": {
        "name_zh": "抱头仰卧半程起坐",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧于平坦地面上，双膝弯曲、双脚分开踩实，双手轻抱头后两侧并使双肘向两侧充分打开。",
            "收紧核心与腹直肌，呼气将上半身卷曲抬起至与地面约成 45 度半起高度，手部仅轻扶不做前拽颈部。",
            "在顶点短暂控制后吸气缓慢放回仰卧起始位，重复规定次数。",
        ],
    },
    "1736": {
        "name_zh": "瑜伽球坐姿单臂过顶哑铃臂屈伸",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "triceps",
        "muscle_group": "triceps",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["瑜伽球"],
        "instructions_zh": [
            "端坐在稳固的瑜伽球上，双脚分开平踩地面，躯干直立收紧核心，非工作手轻扶同侧大腿或膝旁稳定平衡。",
            "工作侧单手正握/微内旋握住一只哑铃高举过头并保持大臂靠近耳侧竖直固定、先屈肘置于脑后高点。",
            "呼气发力集中肱三头肌伸直肘部将哑铃垂直向上推举过顶，顶峰略停顿但不耸肩。",
            "吸气有控制地沿原路屈肘下放回脑后起始角度，完成规定次数后换臂练习。",
        ],
    },
}

pending = {
    "3168": "待修图 · 已规范为悬挂带深蹲划船（补全 TRX 悬挂带与上背主训、股四头肌协同）；原图 F2 铁架顶端贴顶 y=0 截断，且下蹲起立全过程铁架立柱与人体存在 -12..-14 px 水平位移（F1 rack sc0=-0.2760..0.1351），待重制。",
    "1732": "待修图 · 已规范为单侧前弓步过顶哑铃臂屈伸（核正肱三头肌主训与单侧计次）；原图 F1(+22,0)后前脚与头面（sc0=0.9011）差 1 px（+23 时 foot_front 跌至 0.7878），F2 头躯(0,+9)而双脚(0,+10)呈 1 px 纵拉形变（sc0=0.8202 vs 0.9267），待重制。",
    "3193": "待修图 · 已去机译并规范为罗马椅跪姿俯身臀腿抬起（补全罗马椅与腘绳肌/臀肌双主训）；原图 F2 水平俯倒时头顶贴右缘 y/x 截断(x=479)，且器械底座跨帧横偏 11–26 px 并伴随高度错位，待重制。",
    "1733": "待修图 · 已核正上斜凳仰卧双臂哑铃臂屈伸（补全上斜训练凳与肱三头肌主训）；原图 F1(-12,0)后头部仍偏移(-2,-10)（sc0=0.1814），F2(-1,-6)后头部偏 9.22 px（sc0=0.4366），待重制。",
    "3201": "待修图 · 已更名为四分之一卷腹起身（核正腹肌主训并去重）；原图 F1 整体横移 +15..+23 px，F2 上肢起身 95 px 且双脚同步前移 +18..+29 px，待重制。",
    "1734": "待修图 · 已核正瑜伽球坐姿双臂哑铃后屈伸（补全瑜伽球、肱三头肌主训并去除未汉化 back 字段）；原图 F0 坐直而 F1/F2 前倾左移致头部横偏 -27..-31 px（sc0=-0.02..-0.28）而球底几乎静置，待重制。",
    "3202": "待修图 · 已去除性别后缀并更名为仰卧半程起坐（核正腹肌主训）；原图 F0 右缘(x=479)、F1/F3 左缘(x=0)双端贴边截断，且 F1 足踝与球鞋左缘差速漂移、F2 全身左移 80+ px，待重制。",
    "1735": "待修图 · 已规范为平凳仰卧单臂哑铃臂屈伸（补全平板训练凳、肱三头肌主训与单侧计次）；原图 F1(+4,0)虽稳，但 F2(0,+32)对齐平凳左右支腿后头部仍偏(+2,-1) px（sc0=0.8631）且近脚呈 -1 px 垂差（sc0=0.9142），待重制。",
    "3203": "待修图 · 已去粗译“囚徒”与性别后缀更名为抱头仰卧半程起坐（核正腹肌主训）；原图 F1 全身横移 +20..+29 px 且上下脚错位 9 px，F2 整体大幅左上偏移 +10..+29 px，待重制。",
    "1736": "待修图 · 已去括号并规范为瑜伽球坐姿单臂过顶哑铃臂屈伸（补全瑜伽球、肱三头肌主训与单侧计次）；原图 F0 触底 y=479 且底部漏出雪碧图下方哑铃端盖残影、F2 哑铃触顶 y=0 截断，且 F1 头球差速偏移，待重制。",
}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"])

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review50-20261028",
    "inspected": inspected,
    "review_candidates": review_candidates,
    "registered_media": registered_media,
    "definition_updates": definition_updates,
    "pending": pending,
    "sources": {},
    "review_notes": {},
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
    "expected_per_side_ids": ["1732", "1735", "1736"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
