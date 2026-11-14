#!/usr/bin/env python3
"""Author Batch 116 review updates, pending notes, code baseline, and QA spec (0 candidates; 10 deferred)."""
from pathlib import Path
import json
import hashlib

B = Path(__file__).resolve().parent
R = B.parents[2]
BATCH_ID = "20270102_review116"
VERSION = "1.2.121"
VERSION_CODE = 2027010201

inspected = ["1420", "1425", "1426", "1431", "1432", "1433", "1434", "1435", "1436", "1438"]
review_candidates = []
registered_media = []

definition_updates = {
    "1420": {
        "name_zh": "跪姿杠铃爆发跳蹲",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "在保护垫或防滑地面上采用双膝跪姿（膝宽约与髋同宽），将轻至中等重量杠铃扛稳于上背部斜方肌处、双手抓牢横杆。",
            "臀坐脚跟轻微下沉蓄力，维持核心收紧与躯干挺拔。",
            "呼气调动臀肌与髋部强力爆发前顶发力，跃起离地的同时快速收腿转为双脚踩地的半蹲落地姿态。",
            "屈膝缓冲吸收冲击站稳还位，重置安全跪姿后再衔接下一次练习。",
        ],
    },
    "1425": {
        "name_zh": "四十五度斜卧雪橇单腿倒蹬",
        "category": "upper legs",
        "equipment": "sled machine",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "坐在 45 度斜卧倒蹬机上，腰背部与骨盆紧贴靠背固定不抬臀，双手握稳座椅两侧手把。",
            "将非工作侧脚掌平踩地面维持平衡，工作侧单脚平踩在踏板中下区、打开安全锁定杆。",
            "吸气控制弯曲工作侧膝髋，缓缓下放踏板至大腿靠近胸腹极限且下背不卷离靠垫。",
            "呼气用全脚掌发力蹬推踏板伸腿至接近伸直（膝关节保留微屈不锁死），单腿完成计划次数后锁好安全杆再换腿。",
        ],
    },
    "1426": {
        "name_zh": "平凳坐姿史密斯机反握腕弯举",
        "category": "lower arms",
        "equipment": "smith machine",
        "target": "forearms",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "brachialis"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "在史密斯机横杆前放置平板训练凳并坐稳，双脚平踩地面、转解锁扣。",
            "采用掌心朝上反握（与肩同宽）握住横杆，将双前臂平稳贴靠在双侧大腿前侧，令手腕自然悬出膝盖前缘。",
            "保持双前臂贴稳大腿固定不抬肘，控制手腕向下微放开握力至低位拉伸。",
            "呼气依靠前臂屈肌发力向上卷抬手腕与横杆至顶峰收缩停顿片刻，吸气缓慢下放还原，按计划重复。",
        ],
    },
    "1431": {
        "name_zh": "器械辅助站姿反握引体向上",
        "category": "back",
        "equipment": "leverage machine",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "根据训练目标设定辅助配重，踏上助力踏板稳稳站立，双手掌心朝内（反握或中立对握）抓稳上方握把。",
            "沉肩启动核心并保持挺胸与躯干自然直立，下肢稳定踩实助力板。",
            "呼气背阔肌发力主导将身体垂直向上拉起，同时控制肘关节向下贴近躯干两侧至下巴过杆高。",
            "顶峰挤压背肌停顿片刻后吸气匀速受控下放回充分垂臂位，按计划重复。",
        ],
    },
    "1432": {
        "name_zh": "器械辅助站姿正握引体向上",
        "category": "back",
        "equipment": "leverage machine",
        "target": "lats",
        "muscle_group": "",
        "secondary_muscles": ["biceps", "forearms"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "调好所需助力配重并站上辅助引体架助力踏板，双手略宽于肩采用掌心朝外正握牢牢握住上方把手。",
            "先做沉肩固定肩胛带，挺胸收腹保持全身一条直立中线。",
            "呼气调动背阔肌发力向上拉升身体至上胸靠近横把高度、双肘顺体侧下压。",
            "顶峰停顿挤压后背 1 秒后吸气缓慢受控下放到充分伸臂悬挂位，按计划重复。",
        ],
    },
    "1433": {
        "name_zh": "史密斯机前架式前蹲",
        "category": "upper legs",
        "equipment": "smith machine",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将史密斯横杆置于锁骨下方高度，面向立柱上前用双侧三角肌前束与锁骨承托横杆，采用翻举式高肘正握稳住杠杆并解锁。",
            "双脚约与肩同宽踩实地面、脚尖微外展，全程保持双肘高抬且核心紧绷挺胸。",
            "吸气屈髋屈膝受控垂直下蹲，直到大腿与地面平行或略低于水平。",
            "呼气全脚掌及脚跟稳定发力向上蹬起还原直立位，按计划完成后锁回安全卡槽。",
        ],
    },
    "1434": {
        "name_zh": "史密斯机低杠深蹲",
        "category": "upper legs",
        "equipment": "smith machine",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将史密斯机横杆调至略低于肩部高度，钻入杠下将横杆卡稳于肩胛冈下方与三角肌后束之间的低杠位，双手紧握横杆解锁。",
            "双脚与肩同宽略前移半步站稳、核心饱满收紧维持脊柱中立。",
            "吸气优先后推臀部再屈膝稳定下蹲（上躯干配合低杠重心适当微前倾但绝不弓腰），蹲至大腿约平行地面。",
            "呼气臀腿共同发力通过全脚掌垂直向上蹬起站直，按计划重复并挂回安全钩。",
        ],
    },
    "1435": {
        "name_zh": "站姿杠铃低杠深蹲",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "在深蹲架上将杠铃压稳在三角肌后束与肩胛冈下缘低杠位，紧握横杆收紧上背、出杠后退一步双脚略宽于肩站稳。",
            "深吸气憋紧核心与腰腹张力，维持脊椎全段刚性中立。",
            "优先向后推髋并弯曲双膝沿着脚尖方向受控下蹲至髋折痕与膝齐平或略低。",
            "呼气靠臀大肌与股四头肌同步强力驱动向上蹬地站直回起势位，按计划重复。",
        ],
    },
    "1436": {
        "name_zh": "站姿杠铃高杠深蹲",
        "category": "upper legs",
        "equipment": "barbell",
        "target": "glutes",
        "muscle_group": "",
        "secondary_muscles": ["quadriceps", "hamstrings", "calves", "core"],
        "required_equipment_zh": [],
        "instructions_zh": [
            "将杠铃稳扛于上背部斜方肌高杠位，双手略宽于肩正握抓牢，出杠站稳并保持双脚与肩同宽、脚尖微外展。",
            "吸气收紧核心挺胸竖脊，尽量保持躯干角度较垂直。",
            "顺控屈髋屈膝垂直向下蹲至大腿与地面平行或安全深度，避免膝盖大幅内扣。",
            "呼气脚掌踩稳发力向上站直回到起始站姿，按计划重复。",
        ],
    },
    "1438": {
        "name_zh": "平凳坐姿双壶铃推举",
        "category": "shoulders",
        "equipment": "kettlebell",
        "target": "delts",
        "muscle_group": "",
        "secondary_muscles": ["triceps", "upper back"],
        "required_equipment_zh": ["平板训练凳"],
        "instructions_zh": [
            "端坐于平板训练凳上，双脚分开踩实地面维持核心绷紧与腰椎中立。",
            "双手翻腕将一对壶铃提置双肩前架位，壶铃球体自然贴靠前臂外侧、掌心相对或略斜向前、双肘略朝前下压。",
            "呼气三角肌主导发力将双侧壶铃沿着头顶正上方推举至双臂自然伸直（不耸肩、不仰腰代偿）。",
            "在顶端微停后吸气匀速受控下放回肩前架位，按计划重复。",
        ],
    },
}

pending = {
    "1420": "待修图 · 规范为跪姿杠铃爆发跳蹲；原素材为仅 2 帧的满屏实景照片，待重制为标准 4 帧解剖循环图。",
    "1425": "待修图 · 规范为四十五度斜卧雪橇单腿倒蹬并激活单侧计次；原动图 10 帧且帧率与循环节奏不合规，待重制为标准 4 帧循环图。",
    "1426": "待修图 · 规范为平凳坐姿史密斯机反握腕弯举并补全平板训练凳支持器械；原动图 10 帧且底边含散落黑色条点杂影，待重制。",
    "1431": "待修图 · 规范为器械辅助站姿反握引体向上并纠正步骤中的正手错写；原动图 10 帧且帧率不合规，待重制为标准 4 帧循环图。",
    "1432": "待修图 · 规范为器械辅助站姿正握引体向上；原动图 10 帧且帧率不合规，待重制为标准 4 帧循环图。",
    "1433": "待修图 · 消除括号与生硬直译干净握规范为史密斯机前架式前蹲；原动图仅 2 帧且左右杠铃片贴边裁切，待重制。",
    "1434": "待修图 · 纠正严重将低杠译成高杠错译为史密斯机低杠深蹲并修正低杠杠位说明；原动图仅 2 帧且底缘含杂点条影，待重制。",
    "1435": "待修图 · 规范为站姿杠铃低杠深蹲；原动图仅 2 帧，待重制为标准 4 帧循环图。",
    "1436": "待修图 · 规范为站姿杠铃高杠深蹲；原动图仅 2 帧且第 1 帧左上角存在灰色横条杂影，待重制。",
    "1438": "待修图 · 规范名称为平凳坐姿双壶铃推举并补全平板训练凳支持器械；原图虽为 4 帧但第 3 帧平凳与双脚上漂 8 像素且壶铃近顶边（top=2），待重制。",
}

sources = {}
review_notes = {}

before_reviews = json.loads((B / "before/exercise_reviews.json").read_text())
reviewed_count = len(before_reviews["reviewed"]) + len(review_candidates)

review_result = {
    "batch": BATCH_ID,
    "version": VERSION,
    "version_code": VERSION_CODE,
    "output": "build/review116-20270102",
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
        "1426": ["平板训练凳"],
        "1438": ["平板训练凳"],
    },
    "expected_per_side_ids": ["1425"],
}
(B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
print(f"Authored review-result.json, code-baseline.json, and qa-spec.json for {BATCH_ID}")
