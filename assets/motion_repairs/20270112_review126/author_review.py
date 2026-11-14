#!/usr/bin/env python3
"""Author Batch 126 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20270112_review126"
VERSION = "1.2.131"
VERSION_CODE = 2027011201

inspected = ["2205", "2206", "2207", "2208", "2209", "2285", "2286", "2287", "2288", "2289"]
review_candidates = []
registered_media = []

definition_updates = {
    "2205": {
        "name_zh": "跪姿滚轴压腿俯身伸展",
        "category": "upper legs",
        "equipment": "roller",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "quadriceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "跪在防滑瑜伽垫上，将泡沫轴横压在膝下小腿上段与大腿前侧交界处，双手先撑稳垫面、上身微抬。",
            "吸气收紧核心稳定腰背，将髋臀向后轻压同时随着泡沫轴前下滑动顺势将双手向前伸展滑远、胸口缓缓下沉靠近地面。",
            "至臀大肌、股后与肩背侧面出现清晰温和的牵拉感时停顿呼吸感受数秒。",
            "呼气收手撑地慢慢抬起胸背并将躯干回移至跪立位，按均匀节奏重复。",
        ],
    },
    "2206": {
        "name_zh": "仰卧夹轮反向卷腹",
        "category": "waist",
        "equipment": "roller",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧于平坦瑜伽垫上，双臂向上越过头顶自然伸展放稳地面，双腿伸直并拢并将健腹轮滚轮夹稳于双脚踝与前足之间。",
            "微收下腹使下背贴近垫面不明显拱腰。",
            "呼气集中下腹部发力屈膝屈髋将夹住滚轮的双腿向上向胸口方向卷收抬高，顺势带动尾骨微离地面。",
            "顶端收缩下腹停顿 1 秒后吸气缓慢控制双腿与滚轮伸直放回接近地面起始位（脚跟不重摔触地），按计划重复。",
        ],
    },
    "2207": {
        "name_zh": "站姿握轮前推背阔肌拉伸",
        "category": "back",
        "equipment": "roller",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["shoulders", "triceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽自然站立，双手正握住健腹轮手柄置于大腿前下方，膝关节微屈解锁。",
            "屈髋将躯干平稳前倾并让双臂带着滚轮沿地面斜前方缓缓向前推滚伸展，使背阔肌和肩背侧面充分拉长。",
            "到肩背与腋下后缘感到温和牵拉的最远延展位时停顿深呼吸数秒（不猛甩腰背）。",
            "吸气收紧核心控制顺势将滚轮向双脚方向缓慢回滚并起身还原至站姿，按计划重复。",
        ],
    },
    "2208": {
        "name_zh": "仰卧滚轴上背滚压伸展",
        "category": "back",
        "equipment": "roller",
        "target": "spine",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "glutes"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "坐于瑜伽垫上双膝屈曲脚掌稳踩地面，将泡沫轴横垫在中下背下方，双手轻扶头部两侧或抱胸以稳住颈椎。",
            "收腹抬臀使上背重量均匀落于泡沫轴上，避免腰椎过度塌陷反弓。",
            "吸气缓慢向后推动身体并适度向后伸展胸椎与双臂过头顶，让泡沫轴从中背循序滚向肩胛上背段。",
            "滚至上背舒适伸展高点稍停后，呼气控力稳步向前滚动回位，按均匀节律完成。",
        ],
    },
    "2209": {
        "name_zh": "长坐姿健腹轮直臂前平举",
        "category": "chest",
        "equipment": "roller",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["deltoids", "triceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "坐在平坦防滑垫面上，双腿向前自然伸直微开，挺直背部且肩胛微收下沉。",
            "双手正握健腹轮手柄置于大腿正上方，双臂垂直或微屈肘准备向上举起。",
            "呼气集中胸大肌前内束与肩前束协同发力，锁定手肘微屈将健腹轮向前上方平举抬高至约与肩同高。",
            "顶端收缩停顿控制片刻后吸气匀速放回大腿上方起始位，按受控节奏重复。",
        ],
    },
    "2285": {
        "name_zh": "器械坐姿直臂下压拉背",
        "category": "back",
        "equipment": "leverage machine",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "坐稳在固定式斜拉仰靠拉背机座椅上（滚轴压腿固定如配设），上背贴紧靠垫且双脚稳踩踏板。",
            "双手伸向头顶前上方正握紧高位横把或双侧杠杆拉柄，双肘微屈不超伸锁定。",
            "呼气沉肩由背阔肌主导发力，保持手臂近似直臂弧线顺畅向下前方划弧压拉直至横把接近大腿上前方。",
            "顶端挤压背部停顿 1 秒后吸气缓慢受控回放至前上方高位拉伸位置，按计划重复。",
        ],
    },
    "2286": {
        "name_zh": "器械坐姿斜蹬髋腿伸展",
        "category": "upper legs",
        "equipment": "leverage machine",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调节好斜蹬腿器械座椅背靠距离，坐稳后腰背与臀部紧贴背垫、双手紧握座椅两侧固定扶手，双脚与肩同宽踏实踏板中上段。",
            "吸气收紧核心控制踏板屈膝收向胸腹前下方直至大腿接近胸前（臀部不翘离座垫）。",
            "呼气集中臀大肌与股后大腿根部协同发力，通过全脚掌与足跟稳步向前下方蹬直踏板（膝微屈不锁死）。",
            "顶端微停顿收紧臀腿后吸气有控制地屈膝折髋回放，按规范节奏完成次数。",
        ],
    },
    "2287": {
        "name_zh": "器械坐姿交替蹬腿",
        "category": "upper legs",
        "equipment": "leverage machine",
        "target": "quads",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "glutes"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调好固定器械交替蹬腿机的座椅前后与重量配重，坐稳使腰背臀紧贴靠垫、双手握牢体侧扶手。",
            "双脚左右分开约与肩同宽稳踩各自对应踏板，膝关节与脚尖方向对齐不内扣。",
            "呼气一侧腿发力向前稳步蹬伸踏板至接近伸直位（膝微屈不锁死），同时对侧腿维持起始屈膝稳定位。",
            "吸气缓慢受控屈膝回放该侧踏板，紧接着换另一侧腿交替蹬伸并按预定次数连贯循环。",
        ],
    },
    "2288": {
        "name_zh": "器械坐姿握力夹握",
        "category": "lower arms",
        "equipment": "leverage machine",
        "target": "forearms",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "triceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调好前臂握力夹握器械座椅高度，稳坐垫上使双脚踩实地面、腰背挺直。",
            "双手分别伸向前方握紧活动握把与固定支撑柄外缘，使手腕顺直、前臂中立稳定。",
            "呼气由手指与前臂屈肌发力有力收紧双柄并拢挤压，感受小臂前侧全面收缩。",
            "顶端挤压停顿 1 秒后吸气缓慢可控松握放回张开起始位，按计划重复。",
        ],
    },
    "2289": {
        "name_zh": "器械坐姿前蹬小腿提踵",
        "category": "lower legs",
        "equipment": "leverage machine",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调节坐姿蹬腿小腿提踵机座椅位置，坐在座垫上双臂握紧两侧直立扶手稳定上身，双腿几乎伸直并使双脚前脚掌踩牢踏板下缘、脚跟悬空在踏板之外。",
            "吸气控制踝关节顺势放松背屈使脚跟尽量向体侧方向充分牵拉降下，感受小腿后侧肌群拉长。",
            "呼气集中腓肠肌与比目鱼肌发力前蹬脚掌使脚踝最大限度跖屈推起配重。",
            "顶端挤压小腿停顿 1 秒后吸气匀速回放降跟至充分拉伸位，按均匀节律重复。",
        ],
    },
}

pending = {
    "2205": "待修图 · 纠正原名称错把 lat 译成“斜方肌”且步骤错写“双手放在滚轮上”问题（实为泡沫轴压膝下、双手前移伸展），去“保持/支撑”改为跪姿滚轴压腿俯身伸展；原动图仅 2 帧且 L:14, R:14<15，待重制。",
    "2206": "待修图 · 规范为仰卧夹轮反向卷腹；原动图仅 2 帧（L:14, R:14<15）且躯干下方悬空出现一截截断的半圆形黑帽杂物伪影，待重制。",
    "2207": "待修图 · 纠正原名称把 lat 译为“斜方肌”并去除步骤“保持”字样为站姿握轮前推背阔肌拉伸；原动图仅 2 帧且 L:14, R:14<15（第 2 帧滚轮轴处手臂遮挡截断），待重制。",
    "2208": "待修图 · 规范为仰卧滚轴上背滚压伸展；原动图 10 帧（L:14, R:13<15）且每帧胸膝正上方悬空存在截断的灰色金属凳架条状残影伪影，待重制。",
    "2209": "待修图 · 对齐双腿长坐姿直臂前平举实景（英文名虽含 single leg 但画面双腿双臂对称前平举，保留双侧计次更名为长坐姿健腹轮直臂前平举，并去“保持”）；原动图仅 2 帧且 L:14, R:12<15，待重制。",
    "2285": "待修图 · 纠正原中文名称严重误译“杠杆下拉（俯卧）”（实为仰靠坐姿固定器械直臂下压拉背）并去“保持”；原动图 10 帧（L:14, R:14<15）且第 4 帧视角突变为背对背面角度，待重制。",
    "2286": "待修图 · 纠正原步骤错写“向后抬起双腿”与括号附注（实为斜坐向前蹬踏板伸髋腿，规范为器械坐姿斜蹬髋腿伸展）；原动图仅 2 帧且 L:12, R:14<15，待重制。",
    "2287": "待修图 · 纠正原直译“杠杆交替腿推”并明确双手握把稳定躯干步骤（规范为器械坐姿交替蹬腿）；原动图 10 帧且 L:14, R:14<15，待重制为标准 4 帧循环图。",
    "2288": "待修图 · 纠正直译“杠杆握力手”并去“保持”规范为器械坐姿握力夹握；原动图 10 帧（L:14, R:14<15）且每帧最顶缘头顶上方悬浮两只被截断的散落光脚脚趾伪影，待重制。",
    "2289": "待修图 · 纠正原中文步骤错把站姿扛肩垫提踵抄写到坐姿提踵机（画面明确为坐姿前蹬踏板）并规范为器械坐姿前蹬小腿提踵；原动图 10 帧且 T:14, B:14<15，待重制。",
}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review126-20270112",
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
    "candidate_ids": [],
    "candidate_required_equipment": {},
    "expected_per_side_ids": [],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
