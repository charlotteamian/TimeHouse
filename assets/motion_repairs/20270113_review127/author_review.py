#!/usr/bin/env python3
"""Author Batch 127 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20270113_review127"
VERSION = "1.2.132"
VERSION_CODE = 2027011301

inspected = ["2297", "2311", "2315", "2318", "2328", "2330", "2331", "2334", "2335", "2364"]
review_candidates = []
registered_media = []

definition_updates = {
    "2297": {
        "name_zh": "瑜伽球双手扶头大跨度卷腹",
        "category": "waist",
        "equipment": "stability ball",
        "target": "abs",
        "muscle_group": "",
        "secondary_muscles": ["hip flexors"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将中下背顺势仰靠在大瑜伽球球面上，双脚分开约与肩同宽稳踩防滑地面、大小腿呈九十度直角。",
            "双手轻扶耳侧或头后侧（不抱头拉扯颈椎），双肘自然向两侧打开、胸背先贴合球弧微向后仰展拉开腹直肌。",
            "呼气集中腹直肌收缩发力，沿大幅圆弧顺势向前上方卷起上背与双肩靠近骨盆方向。",
            "顶峰收腹控制停顿 1 秒后吸气缓慢匀速沿球弧后仰展开回起始拉伸位，按计划重复。",
        ],
    },
    "2311": {
        "name_zh": "楼梯台阶机攀登踩踏",
        "category": "cardio",
        "equipment": "stepmill machine",
        "target": "cardiovascular system",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "glutes", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "先扶稳楼梯机两侧扶手踩上阶梯底座，设定适宜的入门步频速率后再启动台阶运转。",
            "躯干自然微前倾直立、视线望向前方（不趴扶压靠扶手），双手仅轻握扶手辅助平衡并收紧核心。",
            "全脚掌稳落上层移动踏阶，由臀肌与股四头肌轮流主动发力踏实抬升，双腿流畅交替持续登阶。",
            "完成目标时长或步数后先调低速度，待踏阶停稳后再下机舒展下肢。",
        ],
    },
    "2315": {
        "name_zh": "器械坐姿膝垫负重提踵",
        "category": "lower legs",
        "equipment": "leverage machine",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["soleus", "ankle stabilizers"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "端坐在坐姿膝压式旋转小腿机座椅上，将带厚垫的大腿滚筒压稳于双膝上方大腿前缘，双脚前脚掌踩实踏板前沿、脚跟悬空外露。",
            "双手扶握座椅两侧下方稳固把手并挺直脊柱，先吸气缓慢控制脚跟下沉使小腿后侧充分拉伸。",
            "呼气集中腓肠肌与比目鱼肌发力前脚掌向下踩压踏板，顺势顶起膝垫直至足跟抬到最高收缩点。",
            "顶端挤压小腿停顿 1 秒后吸气匀速缓慢回降脚跟，按均匀节律重复。",
        ],
    },
    "2318": {
        "name_zh": "器械坐姿双柄推肩",
        "category": "shoulders",
        "equipment": "leverage machine",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "chest"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调节推肩器械座椅高度使双侧手柄起始位置约与双耳或肩峰齐平，背紧贴靠背坐稳且双脚稳踩地面。",
            "双手正握或对握双侧握柄，手腕保持直立中立位、收紧核心避免腰背离开靠垫反弓。",
            "呼气沉肩由三角肌主导发力将双柄向上顺弧线稳步推举至双臂接近伸直（手肘微屈不锁死）。",
            "顶端稍作控制后吸气缓慢沿原轨迹下放至耳侧起始高度（不撞击配重片），按计划重复。",
        ],
    },
    "2328": {
        "name_zh": "瑜伽球窄距俯卧撑",
        "category": "upper arms",
        "equipment": "stability ball",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将瑜伽球安稳置于防滑地面上，双手以略窄于肩宽的间距紧扶球面两侧上方，双腿向后并拢伸直以前脚掌踩实地面使头肩髋踝成直线。",
            "核心与臀部收紧避免塌腰晃球，吸气控制双肘夹近体侧斜后方缓慢屈肘，将胸口压向瑜伽球上方。",
            "下放至胸部接近触球且肩肘可控稳固的最低点稍作控制。",
            "呼气集中肱三头肌与胸肌协同发力向下按压球面推回高撑起始位，按受控节奏重复。",
        ],
    },
    "2330": {
        "name_zh": "龙门架坐姿全程宽握高位下拉",
        "category": "back",
        "equipment": "cable",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "rhomboids", "rear deltoids"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调节高位下拉器腿部滚垫压稳大腿根部上方，正握宽距高拉直杆两侧（握距宽于肩宽）并坐直使双臂充分上伸展开肩胛。",
            "微收核心并略向后倾胸背十余度、腰椎自然中立，避免大幅仰身甩腰借力。",
            "呼气先沉肩带动肩胛下压，由背阔肌充分发力沿全程弧线将横杆下拉至贴近上胸锁骨前方。",
            "顶端挤压背部停顿 1 秒后，吸气受控匀速顺势上放直至双臂上伸、肩胛充分向上拉开完成全行程拉伸，按计划重复。",
        ],
    },
    "2331": {
        "name_zh": "立式固定器械健身车骑行",
        "category": "cardio",
        "equipment": "leverage machine",
        "target": "cardiovascular system",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "glutes"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调节健身车座椅高度使单腿踩到底端时膝微屈约二三十度，跨坐稳妥并将前脚掌置入脚蹬固定带中、双手轻扶前方车把。",
            "微倾躯干并适度收紧核心、双肩放松不耸肩，根据训练需求设定目标阻力级别。",
            "双腿顺畅连续交替踩动脚踏画圆骑行，均匀体会股四头肌与臀腿后链交替发力。",
            "按预定时间完成骑行后调低阻力放慢节奏，待飞轮平稳后再下车伸展放松。",
        ],
    },
    "2334": {
        "name_zh": "倒蹬机斜卧直腿提踵",
        "category": "lower legs",
        "equipment": "sled machine",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "glutes"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰躺于四十五度雪橇式倒蹬机斜垫上，肩背臀贴紧靠垫并双手握稳座椅两侧安全锁把手。",
            "双腿推起配重解锁后将膝关节微屈稳定住（不完全锁死超伸），把双脚前脚掌踩在踏板最下缘、脚跟悬空向下伸出。",
            "吸气控制脚踝充分背屈使双脚跟朝身体方向缓降拉伸小腿后侧，随后呼气集中腓肠肌发力通过前脚掌向上全力蹬推踏板直至足背充分跖屈。",
            "顶端挤压小腿停顿控制片刻后吸气匀速回降，完成预定次数后拉回安全锁挂好配重。",
        ],
    },
    "2335": {
        "name_zh": "固定器械坐姿膝垫提踵",
        "category": "lower legs",
        "equipment": "leverage machine",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["soleus", "hamstrings"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "坐稳在坐姿杠杆提踵机座椅上，将上方大腿滚垫高度调整至稳妥压贴双膝上方大腿前端（而非扛压肩部），双手握牢座椅两侧扶手。",
            "双脚前脚掌踩实前方踏板前缘使双脚跟自然悬空向下伸展，挺直上身并收稳核心。",
            "吸气顺势下沉双脚跟直至比目鱼肌与小腿后侧充分拉伸，随后呼气由前脚掌发力向上推顶脚跟直至小腿最大幅度跖屈顶起杠杆垫。",
            "最高点挤压小腿停顿 1 秒后吸气缓慢受控降跟回落，按计划重复。",
        ],
    },
    "2364": {
        "name_zh": "辅助跪姿宽握双杠偏胸臂屈伸",
        "category": "chest",
        "equipment": "leverage machine",
        "target": "pectorals",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调好辅助重力配重后走入双杠辅助架，双手以比肩略宽握紧双侧宽握横柄并将双膝安稳跪放在辅助升降软垫上、伸直手臂悬正。",
            "沉肩微收下颌，将胸背顺势向前微倾约二十至三十度使重力重心更集中于下胸大肌前外侧，避免含胸耸肩。",
            "吸气缓慢屈肘控制下沉身体直至上臂接近与地面平行、胸肌外缘感到明显拉伸。",
            "呼气集中胸大肌发力夹胸带动双臂向上稳步推直还原（肘微屈不锁死），按受控节奏完成次数。",
        ],
    },
}

pending = {
    "2297": "待修图 · 去除命名括号并将健身球统一为瑜伽球（瑜伽球双手扶头大跨度卷腹）；原 4 帧动图右缘 R:2<15、底色偏灰白（bg0=[254,253,253]）且第 3 帧人体与球体整体向上明显跳移（y>=370 IoU=0.5215<0.96），待重制。",
    "2311": "待修图 · 清除原中文步骤中的“支撑/保持”触发词并规范为楼梯台阶机攀登踩踏；原动图 10 帧且上下边距 T:14, B:14<15，待重制为标准 4 帧循环图。",
    "2315": "待修图 · 去除命名“（杠杆）”并消除步骤“保持”字样，规范为器械坐姿膝垫负重提踵；原动图 10 帧且左右边距 L:14, R:13<15，待重制为标准 4 帧循环图。",
    "2318": "待修图 · 去除“（第三式）（杠杆）”括号并规范为器械坐姿双柄推肩；原动图 10 帧（T:14, B:14<15）且第 3 帧出现极严重的“双头重叠”人物畸变伪影，待重制。",
    "2328": "待修图 · 清除“保持”字样并规范为瑜伽球窄距俯卧撑；原 4 帧图右缘 R:13<15、底色偏灰（bg0=[253,254,253]）且第 3 帧球体明显上浮跳移（y>=370 IoU=0.5321<0.96），待重制。",
    "2330": "待修图 · 清除“保持”并规范为龙门架坐姿全程宽握高位下拉；原动图仅 2 帧且左右边距 L:14, R:14<15，待重制为标准 4 帧循环图。",
    "2331": "待修图 · 避开与 2138 重名并规范为立式固定器械健身车骑行（清“保持”）；原动图 10 帧（T:14, B:13<15）且每帧最底缘正下方均残留截断黑圆影伪影，待重制。",
    "2334": "待修图 · 消除“保持”并规范为倒蹬机斜卧直腿提踵；原动图 10 帧且左右边距 L:14, R:14<15，待重制为标准 4 帧循环图。",
    "2335": "待修图 · 纠正原中文步骤把“肩膀对齐肩垫”误抄到膝压坐姿提踵机的问题（清“（杠杆）/保持”改为固定器械坐姿膝垫提踵）；原动图 10 帧且 L:14, R:14<15，待重制。",
    "2364": "待修图 · 纠正原中文命名误译“胸下压（跪姿）”并去括号与“保持”（实为配重辅助跪垫宽握胸肌双杠臂屈伸，规范为辅助跪姿宽握双杠偏胸臂屈伸）；原动图 10 帧且 L:14, R:14<15，待重制。",
}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review127-20270113",
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
