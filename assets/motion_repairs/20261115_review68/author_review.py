#!/usr/bin/env python3
"""Author Batch 68 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20261115_review68"
VERSION = "1.2.73"
VERSION_CODE = 2026111501

inspected = ["0060", "0061", "0063", "0064", "0065", "0066", "0067", "0068", "0069", "0070"]
review_candidates = []
registered_media = []

definition_updates = {
    "0060": {
        "name_zh": "平凳仰卧杠铃碎颅臂屈伸",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "平躺在平凳上，双脚踏地，双手窄距正握杠铃置于胸部上方，大臂微向后倾斜固定角度。",
            "固定大臂静止不动，吸气仅活动前臂屈肘将杠铃缓慢放落至额头上方发际线处。",
            "在最深拉伸点稍作停顿，呼气由肱三头肌发力将手臂伸直推回起始锁定位。",
            "动作全程保持肘关节稳定不向外晃动，重复规定次数。",
        ],
    },
    "0061": {
        "name_zh": "平凳仰卧杠铃仰卧臂屈伸",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "仰卧平躺于平凳上，头部靠近凳端，双手与肩同宽握住杠铃，双臂垂直于地面。",
            "上臂始终保持垂直固定，吸气屈肘将杠铃缓慢平稳放落至前额上方。",
            "在动作底部短暂停顿感受三头肌离心拉伸，呼气由肱三头肌发力将杠铃推回起始手臂直立位。",
            "动作全程保持节奏均匀平稳，按规定次数完成练习。",
        ],
    },
    "0063": {
        "name_zh": "站姿杠铃窄距深蹲",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "quadriceps",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚并拢或间距窄于髋部站立，将杠铃稳固扛于上背斜方肌上，双手握紧。",
            "核心紧绷挺胸，吸气由髋部和膝盖同步弯曲下蹲，重心平稳垂直下落直到大腿与地面平行。",
            "在深蹲最低点维持张力稍作停顿，强调股四头肌外侧头受力。",
            "呼气由大腿前侧爆发蹬地发力推直双腿站起回正，重复规定次数。",
        ],
    },
    "0064": {
        "name_zh": "站姿俯身杠铃单臂划船",
        "category": "back",
        "equipment": "barbell",
        "target": "upper back",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms", "lats"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚前后分立站稳，微屈双膝由髋部前倾俯身约 45 度，背部挺直锁定，单手握住杠铃杆正中或一端。",
            "手臂自然下垂悬垂杠铃，呼气由背阔肌与背部肌群主导发力，屈肘将杠铃拉向腰际侧腹。",
            "在最高点肩胛骨收紧停顿 1 秒，吸气缓慢匀速将杠铃下放回手臂伸展位。",
            "完成规定次数后换另一侧手臂进行相同练习。",
        ],
    },
    "0065": {
        "name_zh": "仰卧地面杠铃单臂推举",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "triceps",
        "muscle_group": "",
        "secondary_muscles": ["chest", "shoulders"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "屈膝仰卧平躺于地面垫上，双脚踩实地面，单手正握适重杠铃杆或短杠中央，垂直向上推直支撑。",
            "收紧核心维持身体骨盆不发生单侧侧倾，吸气屈肘缓慢将大臂垂直下沉靠近体侧地面。",
            "在大臂后侧轻触地面消除惯性稍作停顿，呼气由胸肌与肱三头肌强力发力将杠铃推回正上方起始位。",
            "单臂完成规定次数后换对侧手臂交替练习。",
        ],
    },
    "0066": {
        "name_zh": "站姿体侧杠铃单臂手提箱硬拉",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "quadriceps", "lower back", "obliques"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与髋同宽站立，杠铃置于身体一侧地面，屈髋屈膝俯身单手正握杠铃杆正中如手提箱般提起。",
            "挺胸立腰收紧对侧腹斜肌对抗侧向旋转屈曲，双腿蹬地伸髋将杠铃拉起至身体完全直立中立位。",
            "顶峰夹紧臀部短暂停留，吸气有控制地屈髋下沉将杠铃沿体侧缓慢放回地面。",
            "单侧完成规定次数后换另一侧进行练习。",
        ],
    },
    "0067": {
        "name_zh": "站姿杠铃单臂爆发抓举",
        "category": "shoulders",
        "equipment": "barbell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["traps", "forearms", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开与肩同宽站稳，杠铃置于身前地面，屈髋屈膝俯身单手正握杠铃中央，背部平直。",
            "双腿爆发蹬地伸展髋膝踝三关节，将杠铃直线爆发向上提拉过膝，顺势耸肩高肘翻腕。",
            "迅速屈膝下潜将杠铃顺势锁死在单臂头顶上方正上方直臂位。",
            "双腿蹬直站起锁定，吸气受控下落杠铃至地面或大腿起始位，完成单侧次数后换边练习。",
        ],
    },
    "0068": {
        "name_zh": "站姿杠铃颈后单腿深蹲",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "quads",
        "muscle_group": "",
        "secondary_muscles": ["glutes", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将轻适重量杠铃扛于上背斜方肌上，双手握稳，单脚站立支撑，另一腿向前自然悬空伸出。",
            "收紧核心维持上身直立中立，吸气支撑腿屈髋屈膝平稳下蹲，重心垂直下落至大腿接近平行地面。",
            "在单腿深蹲最低点维持平衡稍作停顿，呼气由支撑腿股四头肌强力蹬地推回站直起始位。",
            "完成规定次数后换另一腿交替练习。",
        ],
    },
    "0069": {
        "name_zh": "站姿杠铃宽握过头深蹲",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "quads",
        "muscle_group": "",
        "secondary_muscles": ["glutes", "hamstrings", "calves", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "双脚分开略宽于肩站立，采用宽握距将杠铃稳固推举在头顶上方正中央，双臂伸直锁定肩关节。",
            "收缩腹横肌与上背肌群维持杠铃在头顶轨迹不变，吸气屈髋屈膝垂直向下深蹲入腿。",
            "下蹲至髋关节低于膝盖水平面，保持胸部挺拔杠铃不向前倾倒漂移。",
            "在底部消除停顿，呼气双腿强力发力蹬地推起身体直立站回起始位，重复规定次数。",
        ],
    },
    "0070": {
        "name_zh": "坐姿牧师凳杠铃弯举",
        "category": "upper arms",
        "equipment": "barbell",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": ["牧师凳"],
        "instructions_zh": [
            "坐在牧师椅上双脚踏实地面，胸部靠紧斜托垫上缘，双臂大臂完全平贴在斜托板上，双手反握杠铃与肩同宽。",
            "呼气由肱二头肌主导发力屈肘向上弯举杠铃，至前臂垂直于地面达到顶峰收缩位。",
            "在顶点挤压肱二头肌停顿 1 秒，吸气沿斜板缓慢匀速下放杠铃至手臂完全伸直伸展。",
            "全程大臂不离开托板表面消除借力，按规定次数重复练习。",
        ],
    },
}

pending = {
    "0060": "待修图 · 消除顶压式歧义规范为平凳仰卧杠铃碎颅臂屈伸（补全平板训练凳必需器械、规避平板触发静力保持）；原动图为 10 帧 (nf=10) 超标且前额折返点漂移，待重制为 4 帧循环图。",
    "0061": "待修图 · 规范译名为平凳仰卧杠铃仰卧臂屈伸（补全平板训练凳必需器械、规避平板触发静力保持）；原动图仅有 2 帧 (nf=2) 缺失动作折返过程帧，待重制为 4 帧循环图。",
    "0063": "待修图 · 规范译名为站姿杠铃窄距深蹲；原动图仅有 2 帧 (nf=2) 缺失下蹲离心与蹬起过程，待重制为 4 帧循环图。",
    "0064": "待修图 · 规范译名为站姿俯身杠铃单臂划船（激活单侧计次）；原动图仅有 2 帧 (nf=2) 缺失单臂提拉折返帧，待重制为 4 帧循环图。",
    "0065": "待修图 · 规范译名为仰卧地面杠铃单臂推举（激活单侧计次）；原动图为 10 帧 (nf=10) 超标且手臂推起不同步，待重制为 4 帧循环图。",
    "0066": "待修图 · 消除侧硬拉歧义规范为站姿体侧杠铃单臂手提箱硬拉（激活单侧计次）；原动图仅有 2 帧 (nf=2) 缺失下沉离心过程，待重制为 4 帧循环图。",
    "0067": "待修图 · 规范译名为站姿杠铃单臂爆发抓举（激活单侧计次）；原动图仅有 2 帧 (nf=2) 缺失爆发接杠与伸展两段关键过渡帧，待重制为 4 帧循环图。",
    "0068": "待修图 · 规范译名为站姿杠铃颈后单腿深蹲（激活单侧计次）；原动图仅有 2 帧 (nf=2) 缺失单腿下蹲缓冲与蹬直过程，待重制为 4 帧循环图。",
    "0069": "待修图 · 规范译名为站姿杠铃宽握过头深蹲；原动图仅有 2 帧 (nf=2) 缺失过头支撑与深蹲过程帧，待重制为 4 帧循环图。",
    "0070": "待修图 · 规范译名为坐姿牧师凳杠铃弯举（补全牧师凳必需器械）；原动图仅有 2 帧 (nf=2) 缺失动作折返过程帧，待重制为 4 帧循环图。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review68-20261115",
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
    "expected_per_side_ids": ["0064", "0065", "0066", "0067", "0068"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
