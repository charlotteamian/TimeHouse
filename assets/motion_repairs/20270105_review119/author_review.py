#!/usr/bin/env python3
"""Author Batch 119 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20270105_review119"
VERSION = "1.2.124"
VERSION_CODE = 2027010501

inspected = ["1616", "1625", "1626", "1627", "1628", "1629", "1630", "1631", "1632", "1633"]
review_candidates = []
registered_media = []

definition_updates = {
    "1616": {
        "name_zh": "器械坐姿反握牧师凳弯举",
        "category": "upper arms",
        "equipment": "leverage machine",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调好牧师凳弯举器械座椅高度，使大臂后侧平贴斜托垫面、胸口贴靠靠垫并双脚踩稳地面。",
            "以正握（掌心朝下）反手方式握住器械双侧手柄，肘部伸至微屈预拉位。",
            "保持上臂与手腕稳固不动，呼气由肱肌、肱桡肌与肱二头肌协同发力向上弯起握把。",
            "顶峰收缩停顿片刻后吸气缓慢受控下放还原，按计划重复。",
        ],
    },
    "1625": {
        "name_zh": "史密斯机上斜窄握卧推",
        "category": "upper arms",
        "equipment": "smith machine",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": ["上斜训练凳"],
        "instructions_zh": [
            "在史密斯机内摆好上斜训练凳（约 35 至 45 度），仰靠坐稳并双脚平踩地面、上胸对准横杆下方。",
            "正握略窄于肩抓牢史密斯机横杆并解锁挂钩，保持肩胛下沉收紧与肘部贴近体侧。",
            "吸气受控屈肘将横杆缓慢下放至中上胸前上方接近轻触位置，随后呼气由肱三头肌主导发力沿导轨向上推起双臂至接近伸直（保持肘微屈）。",
            "顶端停顿片刻后按均匀节奏反复推降，结束后稳固重新挂回安全挂钩。",
        ],
    },
    "1626": {
        "name_zh": "史密斯机下斜反握窄距卧推",
        "category": "chest",
        "equipment": "smith machine",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": ["带勾脚的下斜训练凳"],
        "instructions_zh": [
            "在史密斯机内摆好带勾脚的下斜训练凳，仰卧将双脚踝稳固勾住脚垫滚筒、上背与头部贴稳斜垫。",
            "比肩略窄抓握史密斯横杆并旋转解锁，保持肩胛下沉、上臂夹近躯干且前臂垂直导轨。",
            "吸气控制屈肘下放横杆至胸下缘附近轻停，呼气由胸大肌下束与肱三头肌共同发力向上推回至肘微屈锁定前。",
            "按计划完成次数后先稳固挂回挂钩，再缓慢松握起身。",
        ],
    },
    "1627": {
        "name_zh": "曲杆杠铃牧师凳窄握弯举",
        "category": "upper arms",
        "equipment": "ez barbell",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": ["牧师凳"],
        "instructions_zh": [
            "坐在牧师凳上并调整好高度，双手反握（掌心朝上）曲杆杠铃内侧窄握区，将大臂后侧稳固贴实斜托垫。",
            "沉肩收腹，双臂顺斜垫向下伸展至接近完全伸直但保留肘微屈缓冲。",
            "呼气保持大臂与肘关节压实垫面不动，由肱二头肌主导发力将曲杆向上弯起至肩膀前上方。",
            "顶峰挤压停留 1 秒后吸气缓慢受控下放还原，按计划重复。",
        ],
    },
    "1628": {
        "name_zh": "曲杆杠铃牧师凳蜘蛛弯举",
        "category": "upper arms",
        "equipment": "ez barbell",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": ["牧师凳"],
        "instructions_zh": [
            "反向站在牧师凳竖直背靠侧，双腿向后开立踩实支撑躯干，上胸贴实斜垫顶缘使双臂垂直悬垂在垫前。",
            "以掌心朝前的反握方式握住曲杆杠铃，让手肘自然垂直向下伸展。",
            "呼气保持上臂垂直位置尽量不前后摆动，由肱二头肌纯孤立发力向上弯举曲杆至顶峰高度。",
            "顶峰收紧停顿片刻后吸气受控匀速下放回垂臂起始位，按计划重复。",
        ],
    },
    "1629": {
        "name_zh": "站姿杠铃宽握弯举",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚约与肩同宽自然站稳，双手比肩更宽以掌心朝前（反握）方式稳握直杠铃，双臂自然垂于大腿前。",
            "挺胸收紧核心与臀部，将上臂轻贴体侧保持稳定不借力晃动躯干。",
            "呼气保持肘部位置稳固，由肱二头肌短头主导向上弯起杠铃至胸肩前高点。",
            "顶端挤压收紧后吸气受控缓慢下放至肘微屈起始位，按计划重复。",
        ],
    },
    "1630": {
        "name_zh": "站姿龙门架绳索窄握弯举",
        "category": "upper arms",
        "equipment": "cable",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将直杆附件挂接于龙门架低位滑轮，面向滑轮比肩略窄站立、双膝微屈收紧核心。",
            "双手以掌心朝上略窄于肩握距稳握直杆，肘部贴近身体两侧并保持上臂稳固。",
            "呼气带动小臂向上弯举拉起直杆至胸前高点，感受肱二头肌全程持续张力。",
            "顶端停顿收紧片刻后吸气缓慢受控下放还原（肘部保留微屈不断张力），按计划重复。",
        ],
    },
    "1631": {
        "name_zh": "平凳坐姿龙门架绳索单臂集中弯举",
        "category": "upper arms",
        "equipment": "cable",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "在低滑轮一侧垂直放置一张平板训练凳，双脚开立跨坐凳面，工作侧手以掌心朝上单手握稳拉索单柄。",
            "上体适度前倾，将工作侧上臂肘部后方稳固抵靠同侧大腿内侧，非工作手自然撑放膝头稳住躯干。",
            "呼气保持抵腿上臂不动，由肱二头肌集中发力将单柄向同侧肩前弯起至顶峰收缩。",
            "顶端停留 1 秒后吸气缓慢受控回放至手臂接近伸直，完成单侧次数后再换另一侧手臂重复。",
        ],
    },
    "1632": {
        "name_zh": "站姿龙门架绳索拖拽弯举",
        "category": "upper arms",
        "equipment": "cable",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将直杆挂接于龙门架低滑轮，面向滑轮双脚开立站稳，双手掌心朝上约与肩同宽握住直杆。",
            "吸气挺胸收紧核心，准备将直杆沿腹前路径向上提拉。",
            "呼气控制双肘向身体后侧方顺畅后引，让直杆贴近腹部并紧擦躯干前侧垂直向上拖拽至下胸高度。",
            "顶峰充分挤压肱二头肌停顿片刻后，吸气顺原路缓慢沿躯干前侧回放双臂还原，按计划重复。",
        ],
    },
    "1633": {
        "name_zh": "牧师凳龙门架绳索单臂弯举",
        "category": "upper arms",
        "equipment": "cable",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": ["牧师凳"],
        "instructions_zh": [
            "将牧师凳摆在龙门架中低滑轮前方，工作侧单手以掌心朝上反握单柄，站在牧师凳后方俯身将同侧大臂后侧压实斜托垫面。",
            "保持背部平直核心收紧，非工作手自然扶稳牧师凳边缘保持对称稳定。",
            "呼气保持肘关节与上臂压实垫面不动，由单侧肱二头肌发力将手柄拉向同侧肩部前上方。",
            "顶峰收缩停顿片刻后吸气受控回放至肘微屈拉伸位，完成单侧全部次数后换另一侧重复。",
        ],
    },
}

pending = {
    "1616": "待修图 · 纠正原中文步骤将反手正握（手掌朝下）误写成手掌朝上为器械坐姿反握牧师凳弯举；原动图仅 2 帧，待重制为标准 4 帧循环图。",
    "1625": "待修图 · 根据原图明显上斜仰靠凳体与双脚踩地姿势纠正原英文与步骤中错标的下斜描述为史密斯机上斜窄握卧推并补全上斜训练凳支持器械；原动图仅 2 帧，待重制为标准 4 帧循环图。",
    "1626": "待修图 · 消除生硬直译“反下斜”并补全带勾脚的下斜训练凳规范为史密斯机下斜反握窄距卧推；原动图仅 2 帧，待重制为标准 4 帧循环图。",
    "1627": "待修图 · 规范为曲杆杠铃牧师凳窄握弯举并补全牧师凳支持器械、去除步骤中英文 ez；原动图 10 帧且帧率与循环节奏不合规，待重制为标准 4 帧循环图。",
    "1628": "待修图 · 纠正原直译“曲杆蜘蛛卷”为曲杆杠铃牧师凳蜘蛛弯举并按图示补全牧师凳支持器械；原动图 10 帧且右缘 R:13<15，待重制为标准 4 帧循环图。",
    "1629": "待修图 · 规范为站姿杠铃宽握弯举；原动图 10 帧且下缘 B:12<15，待重制为标准 4 帧循环图。",
    "1630": "待修图 · 规范为站姿龙门架绳索窄握弯举；原动图 10 帧且上缘 T:12<15，待重制为标准 4 帧循环图。",
    "1631": "待修图 · 补充单臂与平凳坐姿定位为平凳坐姿龙门架绳索单臂集中弯举，启用单侧计次并补全平板训练凳支持器械；原动图 10 帧不合规，待重制为标准 4 帧循环图。",
    "1632": "待修图 · 修正步骤中沿用普通弯举“上臂完全不动”而未体现拖拽贴身轨迹的问题并规范为站姿龙门架绳索拖拽弯举；原动图仅 2 帧，待重制为标准 4 帧循环图。",
    "1633": "待修图 · 纠正原中文误将牧师凳翻成平板而触发等长保持门控的问题，改名为牧师凳龙门架绳索单臂弯举并补全牧师凳支持器械与单侧计次；原动图 10 帧不合规，待重制为标准 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review119-20270105",
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
    "expected_per_side_ids": ["1631", "1633"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
