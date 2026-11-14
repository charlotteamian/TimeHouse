#!/usr/bin/env python3
"""Author Batch 115 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20270101_review115"
VERSION = "1.2.120"
VERSION_CODE = 2027010101

inspected = ["1395", "1396", "1408", "1409", "1410", "1411", "1412", "1413", "1416", "1417"]
review_candidates = []
registered_media = []

definition_updates = {
    "1395": {
        "name_zh": "器械坐姿单腿踏板提踵",
        "category": "lower legs",
        "equipment": "smith machine",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "坐在座椅上并调整靠垫前后位置，背部稳贴靠背，双手扶握座侧固定把手。",
            "工作侧单脚前脚掌踩在斜踏板边缘使后脚跟悬空，另一侧非工作腿脚掌稳放于地面休息。",
            "保持工作腿膝角稳定并先控制下压拉伸小腿，随后呼气用前脚掌着力将脚跟尽量推踮高。",
            "顶峰收缩停顿片刻后吸气缓慢复位，单腿完成计划次数后换腿重复。",
        ],
    },
    "1396": {
        "name_zh": "史密斯机站姿踏台提踵",
        "category": "lower legs",
        "equipment": "smith machine",
        "target": "calves",
        "muscle_group": "",
        "secondary_muscles": ["ankles", "shins"],
        "required_equipment_zh": ["稳固踏台"],
        "instructions_zh": [
            "在史密斯机横杆正下方放置稳固踏台，进入立柱内将横杆稳固扛在上背部斜方肌上，双手正握横杆并解锁。",
            "双脚与肩同宽仅以前脚掌踩在踏台边缘，令脚跟自然悬空下沉拉长小腿后侧。",
            "收紧核心避免塌腰借力，呼气依靠小腿收缩用力向上踮起双侧脚后跟至顶峰位置。",
            "顶端停顿片刻后吸气受控下放脚跟低于踏台平面，按计划重复。",
        ],
    },
    "1408": {
        "name_zh": "弹力带仰卧臀桥",
        "category": "upper legs",
        "equipment": "band",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "quadriceps"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将环形弹力带套在双膝略上方，仰卧于防滑地面或训练垫上，双膝弯曲、双脚比髋略宽平踩地面。",
            "膝关节微向外顶开以保持弹力带适度张力，双手掌心朝下平放躯干两侧地面。",
            "呼气臀大肌发力通过脚跟下蹬将髋部向上顶起，直至膝、髋、肩呈一条平稳斜线，避免腰椎过度反弓。",
            "顶峰用力夹紧臀部停顿片刻，吸气缓慢受控下放臀部回贴地面，按计划重复。",
        ],
    },
    "1409": {
        "name_zh": "仰卧杠铃负重臀桥",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "lower back"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧屈膝于地面，双脚与肩同宽踩稳，将装好护垫的杠铃横置于髋折痕前方并双手扶稳杠铃防止滚动。",
            "收紧核心并让下背温和贴近地面，脚后跟稳固发力做准备。",
            "呼气臀肌主导发力将杠铃与髋部向上顶举至膝、髋、肩连成一直线。",
            "顶部挤压臀部停顿片刻后吸气缓慢受控下放回地面，按计划重复。",
        ],
    },
    "1410": {
        "name_zh": "站姿扛杆杠铃单腿交替侧弓步",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将杠铃稳固扛于上背部斜方肌上方并双手抓牢，核心收紧保持躯干挺直站立。",
            "工作侧向体侧迈出一大步，屈髋向后坐同时弯曲工作侧膝关节顺着脚尖方向下蹲至大腿约与地面平行，对侧腿保持伸直踩实。",
            "呼气靠工作侧臀腿蹬地发力推回起始直立位，全程保持脊柱中立不圆腰。",
            "按计划单侧完成或左右腿交替迈步侧蹲，完成后平稳还杠。",
        ],
    },
    "1411": {
        "name_zh": "平凳俯臂正握杠铃反手腕弯举",
        "category": "lower arms",
        "equipment": "barbell",
        "target": "forearms",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "brachialis"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "跪蹲或坐姿在平板训练凳旁侧，采用掌心朝下正握（与肩同宽）握住杠铃，将双前臂平稳贴靠在凳面上并使手腕自然探出凳沿。",
            "双前臂全程紧贴凳面固定不动，先控制手腕向下弯曲下放杠铃充分伸展前臂伸肌群。",
            "呼气仅依靠前臂背侧肌群收缩向上卷抬手腕与拳背至最高处。",
            "顶部停顿片刻后吸气缓慢受控下放还原，按计划重复。",
        ],
    },
    "1412": {
        "name_zh": "平凳俯臂仰掌杠铃腕弯举",
        "category": "lower arms",
        "equipment": "barbell",
        "target": "forearms",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "shoulders"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "坐在平板训练凳前端或伏于凳侧，采用掌心朝上反握（与肩同宽）握住杠铃，双前臂稳固平放凳面上并将手腕悬出凳沿。",
            "保持双前臂贴稳凳垫不借肘腕上抬，控制手腕下垂打开手掌至低位。",
            "呼气前臂屈肌发力将手腕及杠铃尽量向上卷曲收紧。",
            "顶端收缩停顿片刻后吸气受控下放还原，按计划重复。",
        ],
    },
    "1413": {
        "name_zh": "站姿龙门架单臂反握弯举",
        "category": "upper arms",
        "equipment": "cable",
        "target": "biceps",
        "muscle_group": "",
        "secondary_muscles": ["forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将单手拉柄挂接至龙门架最低滑轮，面对或略微前站半步于滑轮前方直立站稳，工作侧手掌心朝下正握把手并建立微张力。",
            "大臂贴近体侧保持固定不晃肩借力，躯干收腹站直。",
            "呼气工作侧弯举拉起把手向上靠近前肩，强化前臂桡侧与肱肌协同发力。",
            "顶端略停后吸气受控伸臂还原，单侧完成计划次数后换边重复。",
        ],
    },
    "1416": {
        "name_zh": "瑜伽球俯卧单腿髋外旋",
        "category": "upper legs",
        "equipment": "stability ball",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "quadriceps", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "俯身用双手稳固撑地，将下腹与骨盆位置稳压在瑜伽球中央，双腿并拢向后伸展使下身接近水平。",
            "收紧核心维持上身与支撑侧平稳，非工作侧腿顺势轻搭稳地或略浮保持平衡，将工作侧单腿平稳抬升至与地面平行。",
            "呼气工作侧臀中肌与臀大肌主导发力，保持伸直将工作腿缓缓向外侧平展旋转画弧，保持骨盆尽量稳固不大幅翻转。",
            "在终点微停后吸气控制收回中立下放，单侧完成后换腿重复。",
        ],
    },
    "1417": {
        "name_zh": "瑜伽球仰卧单腿斜踢腘绳肌勾腿",
        "category": "upper legs",
        "equipment": "stability ball",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "仰卧于地面或防滑垫上，将非工作侧单脚后跟踩稳在瑜伽球顶部、工作侧直腿向上悬空准备，双臂平置体侧撑稳地面。",
            "核心与臀肌收紧向上抬髋起桥至肩、髋、球支撑脚成一条稳定直线，工作侧保持屈膝收向胸前预备或伸直。",
            "呼气将工作腿沿斜上方蹬踢充分伸直，同时下方踩球腿保持稳定并感受腘绳肌与臀肌强力收缩。",
            "顶端控制停顿片刻，吸气缓慢屈回膝盖并保持髋位不塌陷，单腿完成计划次数后换腿重复。",
        ],
    },
}

pending = {
    "1395": "待修图 · 规范为器械坐姿单腿踏板提踵并激活单侧计次；原动图 10 帧且帧率不合规，待重制为标准 4 帧循环图。",
    "1396": "待修图 · 规范名称为史密斯机站姿踏台提踵并补全稳固踏台支持器械；原动图仅 2 帧，待重制为标准 4 帧循环图。",
    "1408": "待修图 · 规范名称为弹力带仰卧臀桥；原图虽为 4 帧但第 3 帧足底与头背整体上漂 44 像素（bottom 105->149），待重制锁死落地锚点。",
    "1409": "待修图 · 规范名称为仰卧杠铃负重臀桥；原素材为仅 2 帧的满屏实景照片，待重制为标准 4 帧解剖循环图。",
    "1410": "待修图 · 规范为站姿扛杆杠铃单腿交替侧弓步并激活单侧计次；原动图仅 2 帧，待重制为标准 4 帧循环图。",
    "1411": "待修图 · 纠正步骤前臂放大腿错写为平凳俯臂正握杠铃反手腕弯举并补全平板训练凳支持器械；原动图仅 2 帧，待重制为标准 4 帧循环图。",
    "1412": "待修图 · 去括号规范为平凳俯臂仰掌杠铃腕弯举并补全平板训练凳支持器械；原动图 10 帧且帧率不合规，待重制为标准 4 帧循环图。",
    "1413": "待修图 · 规范为站姿龙门架单臂反握弯举并激活单侧计次；原动图 10 帧且帧率不合规，待重制为标准 4 帧循环图。",
    "1416": "待修图 · 消除直译规范为瑜伽球俯卧单腿髋外旋并保留单侧计次；原图 4 帧第 3 帧球体与双手离开地面上漂 40 像素，待重制。",
    "1417": "待修图 · 消除直译规范为瑜伽球仰卧单腿斜踢腘绳肌勾腿并保留单侧计次；原图 4 帧第 3 帧球与肩背整体上漂 19 像素，待重制。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review115-20270101",
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
        "1396": ["稳固踏台"],
        "1411": ["平板训练凳"],
        "1412": ["平板训练凳"],
    },
    "expected_per_side_ids": ["1395", "1410", "1413", "1416", "1417"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
