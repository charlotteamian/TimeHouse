#!/usr/bin/env python3
"""Author Batch 112 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261229_review112"
VERSION = "1.2.117"
VERSION_CODE = 2026122901

inspected = ["1343", "1344", "1345", "1347", "1348", "1349", "1350", "1351", "1353", "1354"]
review_candidates = []
registered_media = []

definition_updates = {
    "1343": {
        "name_zh": "瑜伽球俯卧挺髋抬腿",
        "category": "back",
        "equipment": "stability ball",
        "target": "spine",
        "muscle_group": "",
        "secondary_muscles": ["abdominals", "glutes"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "俯身用双手与肩同宽稳固撑地，将髋前侧与大腿前侧平放压靠在瑜伽球上方，双腿向后并拢伸直。",
            "肩胛下沉锁紧核心，身体保持从头到脚踝平直稳定的预备姿势。",
            "呼气臀肌与下背竖脊肌发力向上抬起并拢双腿，使大腿逐渐抬离球面、躯干不塌腰。",
            "顶端收缩停顿片刻，吸气受控下放双腿轻回球面起始位，按计划重复。",
        ],
    },
    "1344": {
        "name_zh": "曲杆杠铃俯身反握划船",
        "category": "back",
        "equipment": "ez barbell",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站立，微屈膝并以反握（掌心朝上）与肩同宽握住曲杆杠铃。",
            "保持脊柱中立挺胸收腹，屈髋向前俯身至躯干接近与地面平行。",
            "呼气上背菱形肌与中下斜方肌主导发力，贴近大腿前侧将曲杆拉向下胸部并挤压肩胛骨。",
            "顶端收缩停顿片刻，吸气缓慢受控下放伸直手臂，按计划重复。",
        ],
    },
    "1345": {
        "name_zh": "俯身双壶铃划船",
        "category": "back",
        "equipment": "kettlebell",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽踩实地面，双手各持一只壶铃垂于体前、掌心相对或朝后。",
            "保持脊柱中立，屈膝屈髋将躯干向前倾约 45 至 60 度并收紧核心。",
            "呼气上背肌群主导发力，屈肘贴近体侧将双壶铃向上拉至肋缘并挤压肩胛骨。",
            "在顶峰停顿片刻，吸气匀速受控下放壶铃回自然垂臂位，按计划重复。",
        ],
    },
    "1347": {
        "name_zh": "器械坐姿单臂宽握下拉",
        "category": "back",
        "equipment": "leverage machine",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "rhomboids", "rear deltoids"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调整坐垫高度面对机器胸垫坐稳，双脚踩实地面、非工作侧手轻扶机架稳住躯干。",
            "工作侧单手宽握上方拉杆把手，手臂向斜上方充分伸展预拉背阔肌。",
            "呼气沉肩发力将把手顺弧线向体侧下方拉低至肩腰部，避免借力猛晃侧倾。",
            "底端挤压停顿片刻，吸气缓慢伸臂复位，单侧完成计划次数后换边重复。",
        ],
    },
    "1348": {
        "name_zh": "器械坐姿胸托反握划船",
        "category": "back",
        "equipment": "leverage machine",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调整坐垫与脚踏位置后坐上器械，前胸紧靠前方胸托垫、双脚踩实前踏板。",
            "采用反握（掌心朝上）握住双侧划船把手，伸展双臂使肩胛骨充分前展。",
            "呼气上背斜方肌与菱形肌主导发力，贴体后拉把手向胸肋下缘并夹紧两侧肩胛骨。",
            "顶端停顿片刻后吸气受控伸臂放回起始位，按计划重复。",
        ],
    },
    "1349": {
        "name_zh": "器械俯靠正握丁字杠划船",
        "category": "back",
        "equipment": "leverage machine",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调整丁字杠器械的踏板与坐胸垫高度，前胸贴稳斜向靠垫、双脚稳踩底踏板。",
            "正握（掌心朝下）宽握外侧横柄，双臂自然前伸建立上背拉伸。",
            "呼气上背与后束协同发力，屈肘向胸廓两侧拉起杠杆并充分挤压肩胛骨。",
            "在收缩末端停顿片刻，吸气缓慢受控下放还原至前伸起始位，按计划重复。",
        ],
    },
    "1350": {
        "name_zh": "器械坐姿胸托划船",
        "category": "back",
        "equipment": "leverage machine",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调整器械座椅高度使胸部中段贴合胸托靠垫，双脚平踩前方踏板保持稳定。",
            "正握或对握与肩同宽的固定把手，保持挺胸直背并收紧核心。",
            "呼气沉肩屈肘将双侧把手稳步拉向躯干两侧，充分挤压肩胛骨中下束。",
            "顶峰略停后吸气缓慢受控释放手臂复位，按计划重复。",
        ],
    },
    "1351": {
        "name_zh": "器械俯靠反握丁字杠划船",
        "category": "back",
        "equipment": "leverage machine",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调整丁字杠器械座椅并踩实双脚踏板，使胸腹部稳固俯靠在斜向胸垫上。",
            "采用反握（掌心朝上或内对）握住内侧划船把手，双臂伸直前引牵拉上背。",
            "呼气上背肌群主导发力贴体向后拉起把手至下胸位置，收紧肩胛骨。",
            "末端停顿片刻后吸气受控伸臂还原，按计划重复。",
        ],
    },
    "1353": {
        "name_zh": "深蹲爆发力药球前上抛接",
        "category": "back",
        "equipment": "medicine ball",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "面对墙面或开阔接球区双脚与肩同宽站立，双手将药球抱于胸前下方准备。",
            "顺势屈髋屈膝下蹲蓄力，同时保持脊柱中立、核心紧绷。",
            "呼气由下肢蹬伸衔接上肢与背阔肌爆发推进，将药球向斜前上方强力抛出。",
            "待球回弹或下落时屈膝缓冲接稳收回胸前，顺畅衔接下一次下蹲抛接。",
        ],
    },
    "1354": {
        "name_zh": "站姿过顶药球爆发砸地",
        "category": "back",
        "equipment": "medicine ball",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽踩实地面，双手持药球直臂高举过头顶并轻微展胸伸髋蓄力。",
            "收紧核心准备发力，目视身前安全落球地面。",
            "呼气调动背阔肌、上背与核心快速向下收压，微屈膝伴随躯干屈伸将药球重砸向身前地面。",
            "稳住核心顺势接回弹起的药球高举回起始位，按计划重复。",
        ],
    },
}

pending = {
    "1343": "待修图 · 规范并纠正步骤中垫上仰卧错译为瑜伽球俯卧挺髋抬腿（实为双手撑地大腿靠球）；原图 4 帧第 3 帧球体整体上漂 22 像素，待重制。",
    "1344": "待修图 · 消除中文说明与步骤中的英文缩写并规范为曲杆杠铃俯身反握划船；原动图仅 2 帧，待重制为标准 4 帧循环图。",
    "1345": "待修图 · 规范名称为俯身双壶铃划船；原图 4 帧第 2/4 帧双脚水平左移 20 像素且第 3 帧上跳 5 像素，待重制。",
    "1347": "待修图 · 去括号规范为器械坐姿单臂宽握下拉并激活单侧计次；原动图仅 2 帧，待重制为标准 4 帧循环图。",
    "1348": "待修图 · 去括号规范为器械坐姿胸托反握划船；原动图仅 2 帧，待重制为标准 4 帧循环图。",
    "1349": "待修图 · 去括号规范为器械俯靠正握丁字杠划船；原动图仅 2 帧，待重制为标准 4 帧循环图。",
    "1350": "待修图 · 去括号规范为器械坐姿胸托划船；原动图 10 帧且帧率不合规，待重制为标准 4 帧循环图。",
    "1351": "待修图 · 去括号并纠正步骤中误写的正手握法为器械俯靠反握丁字杠划船；原动图仅 2 帧，待重制为标准 4 帧循环图。",
    "1353": "待修图 · 消除接抛头顶歧义规范为深蹲爆发力药球前上抛接并对应斜前上抛画面；原动图仅 2 帧且右缘药球被裁切、带背景参照线，待重制。",
    "1354": "待修图 · 规范药球头顶砸地为站姿过顶药球爆发砸地；原动图仅 2 帧且缺少砸地与上举过程帧，待重制。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review112-20261229",
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
    "expected_per_side_ids": ["1347"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
