#!/usr/bin/env python3
"""Author Batch 59 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261106_review59"
VERSION = "1.2.64"
VERSION_CODE = 2026110601

inspected = ["3419", "3546", "3420", "3547", "3433", "3548", "3470", "3560", "3523", "3635"]
review_candidates = []
registered_media = []

definition_updates = {
    "3419": {
        "name_zh": "地面直角撑体",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "hip flexors",
        "secondary_muscles": [],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双腿向前伸直并拢坐在地面上，双手平按于臀部两侧地面、手指朝前，双臂伸直锁死。",
            "沉肩下压双手、腹直肌与屈髋肌群极度紧绷发力。",
            "将臀部与完全伸直的双腿一体向上推离地面悬空，双腿与躯干大致保持 90 度直角。",
            "稳定控制重心悬空维持规定秒数，结束后受控落回地面坐姿。",
        ],
    },
    "3546": {
        "name_zh": "平凳坐姿单臂交替哑铃推肩",
        "category": "shoulders",
        "equipment": "dumbbell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "upper back"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "端坐在平凳上，双脚踩实地面、腰背挺直，双手各持一只哑铃举于肩上、掌心朝内或微前。",
            "核心收紧保持身体直立，呼气时由一侧三角肌发力将该侧哑铃垂直向上推过头顶至手臂接近伸直。",
            "顶峰稍作停顿后吸气匀速下放回肩部高度，同时另一侧手臂开始向上推起哑铃。",
            "保持双臂交替推举节奏，按规定次数完成左右两侧练习。",
        ],
    },
    "3420": {
        "name_zh": "地面屈体V字平衡撑体",
        "category": "waist",
        "equipment": "body weight",
        "target": "abs",
        "muscle_group": "hip flexors",
        "secondary_muscles": [],
        "required_equipment_zh": [],
        "instructions_zh": [
            "坐在地面上，双腿并拢伸展，双手置于身体两侧准备。",
            "核心收缩启动，上体后倾约 45 度同时将并拢伸直的双腿向上斜抬起约 45 度，身体呈锐角“V”字形。",
            "双臂可向前平伸平行于地面以平衡支撑，腹部与髂腰肌强力发力锁住姿势。",
            "静力定型维持规定秒数不掉腿塌背，随后有控制地缓慢放下双腿与上身。",
        ],
    },
    "3547": {
        "name_zh": "直立靠背训练凳坐姿哑铃弯举推肩",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "shoulders",
        "secondary_muscles": [],
        "required_equipment_zh": ["直立靠背训练凳"],
        "instructions_zh": [
            "坐稳于直立靠背训练凳上，背部与肩胛贴紧靠垫，双手各握一只哑铃垂于体侧、掌心朝前。",
            "呼气时肱二头肌发力将哑铃屈臂弯举至肩膀前方高点。",
            "随后顺势外旋前臂使掌心朝前，由三角肌与肱三头肌协同向上垂直推举哑铃至头顶双臂伸直位。",
            "吸气反向受控先下放哑铃至肩前，再旋腕下放伸直前臂回到起始垂臂位，重复规定次数。",
        ],
    },
    "3433": {
        "name_zh": "俯卧双腿单侧交替拍水踢腿",
        "category": "upper legs",
        "equipment": "body weight",
        "target": "glutes",
        "muscle_group": "hamstrings",
        "secondary_muscles": ["quadriceps", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "俯卧平趴在训练垫上，双臂伸直置于头部前方或体侧，双腿向后自然并直伸展。",
            "核心与臀背微收紧，将胸部与膝盖微抬离开垫面。",
            "以髋关节为转轴，双腿后侧臀肌与腘绳肌发力上下小幅交替快速拍动打水踢腿，脚面绷直。",
            "全程保持呼吸均匀与躯干稳定不左右剧烈摆动，完成规定次数或时长。",
        ],
    },
    "3548": {
        "name_zh": "单臂过头负重哑铃行走",
        "category": "shoulders",
        "equipment": "dumbbell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["traps", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽站立，单手持一只哑铃直臂向上推起至头顶正上方锁紧，大臂紧贴耳侧。",
            "腹部与核心强力绷紧抵抗单侧重心倾斜，目视正前方。",
            "维持躯干完全直立不侧弯，迈出匀速而稳健的步幅平稳向前行走。",
            "完成规定步数或距离后，受控放下哑铃并换另一侧手进行练习。",
        ],
    },
    "3470": {
        "name_zh": "自重单腿交替向前弓步蹲",
        "category": "upper legs",
        "equipment": "body weight",
        "target": "glutes",
        "muscle_group": "quadriceps",
        "secondary_muscles": ["hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚并拢站立，挺胸收腹，双手叉腰或自然放于胸前。",
            "一侧单腿向前迈出约一步半距离，后脚顺势抬起脚跟、脚尖点地。",
            "垂直下沉躯干屈双膝成弓步，前大腿接近平行于地面，前膝不严重内扣或过度超脚尖。",
            "前脚跟发力蹬地后推身体站直收回起始站姿，随后换对侧腿交替迈出，重复规定次数。",
        ],
    },
    "3560": {
        "name_zh": "站姿单臂交替哑铃锤式弯举推举",
        "category": "upper arms",
        "equipment": "dumbbell",
        "target": "biceps",
        "muscle_group": "forearms",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚与肩同宽直立站稳，双手对握持哑铃垂于大腿两侧，核心收紧、躯干挺直。",
            "呼气时一侧手臂发力做锤式弯举将哑铃提至肩胸高度，上臂保持紧夹体侧。",
            "随后顺势发力将该侧哑铃竖直向上推举过头顶至手臂接近完全伸展。",
            "吸气缓慢按原轨迹受控下放哑铃回至体侧垂臂位，紧接着换对侧手臂交替完成弯举推举，重复规定次数。",
        ],
    },
    "3523": {
        "name_zh": "平凳上背仰靠双腿臀桥",
        "category": "upper legs",
        "equipment": "body weight",
        "target": "glutes",
        "muscle_group": "hamstrings",
        "secondary_muscles": ["core"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "背向平板训练凳坐于地面，将肩胛下沿与上背部仰靠贴稳于平凳边缘，双脚屈膝与髋同宽平踩地面。",
            "收紧腹部核心不骨盆前倾，呼气时臀大肌强力发力向上推举髋部。",
            "推至大腿与躯干呈一条直线、小腿垂直于地面的顶峰收缩位，短暂停顿挤压臀肌。",
            "吸气有控制地下放臀部缓慢回落贴近地面，重复规定次数。",
        ],
    },
    "3635": {
        "name_zh": "单臂哑铃异侧向前弓步蹲",
        "category": "upper legs",
        "equipment": "dumbbell",
        "target": "glutes",
        "muscle_group": "quadriceps",
        "secondary_muscles": ["hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚并拢站立，单手持一只哑铃垂于体侧，对侧手自然叉腰维持平衡，核心收紧。",
            "向前迈出与持哑铃侧异侧的单腿成弓步并屈膝下沉躯干，使持哑铃侧哑铃自然靠近迈出脚内侧。",
            "前腿屈膝约 90 度并保持重心稳定，感受前腿股四头肌与臀部充分受力承重。",
            "前脚跟用力蹬地将身体推回双脚并拢位，按规定次数交替或单侧完成训练。",
        ],
    },
}

pending = {
    "3419": "待修图 · 已规范为地面直角撑体（定型等长保持、去重字段）；原图 F2 支撑双手与头部纵移 +12..+13 px，待重制。",
    "3546": "待修图 · 纠正错译为平凳坐姿单臂交替哑铃推肩（消除平板保持误触发、补全平板训练凳、激活单侧计次、移除误归主训的肱三头肌）；原图 F0 触底 y=479 (bottom=36) 且 F2 触顶 y=0 (top=43) 双端截断，待重制。",
    "3420": "待修图 · 规范为地面屈体V字平衡撑体（定型等长保持、去重字段）；原图支撑手与脚 F1(-24,17)/F2(10,-23) 发生剧烈错位飘移 (bs=0.8036 < 0.96)，待重制。",
    "3547": "待修图 · 纠正错译为直立靠背训练凳坐姿哑铃弯举推肩（补全直立靠背训练凳、去重字段）；原图 F0 触底 y=479 (bottom=13) 与相邻残影且 F2 触顶 y=0 (top=17) 截断，待重制。",
    "3433": "待修图 · 去括号去“（男）”规范为俯卧双腿单侧交替拍水踢腿（激活单侧计次、去重字段）；原图拍水踢腿全程下肢躯干浮动无法静态配准，待重制。",
    "3548": "待修图 · 纠正错译为单臂过头负重哑铃行走（激活单侧计次、移除误归主训的斜方肌）；原图 F0(top=8) 与 F1(top=10) 举高哑铃顶缘发生截断，待重制。",
    "3470": "待修图 · 去“（男）”规范为自重单腿交替向前弓步蹲（激活单侧计次）；原图弓步大跨步移动无法锁定刚体背景锚点，待重制。",
    "3560": "待修图 · 纠正错译为站姿单臂交替哑铃锤式弯举推举（激活单侧计次、去重字段）；原图 F0 触底 y=479 (bottom=28) 且 F2 触顶 y=0 (top=35) 双端截断，待重制。",
    "3523": "待修图 · 去“（男）”并纠正错译为平凳上背仰靠双腿臀桥（图像实为上背仰靠平凳脚踩地臀推、补全平板训练凳）；原图平凳左支脚 F2 纵移 +24 px (bs=0.8327) 与右支脚 (-24,+24) 发生 24 px 结构错位变形，待重制。",
    "3635": "待修图 · 已规范为单臂哑铃异侧向前弓步蹲（激活单侧计次）；原图 F0 触底 y=479 (bottom=93) 且 F2 触顶 y=0 (top=82) 发生全画面极其严重的双向大幅截断溢出，待重制。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review59-20261106",
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
    "expected_per_side_ids": ["3546", "3433", "3548", "3470", "3560", "3635"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
