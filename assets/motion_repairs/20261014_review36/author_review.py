#!/usr/bin/env python3
"""Author Batch 36 (20261014_review36) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["1429", "1287", "1430", "1288", "1460", "1289", "1466", "1290", "1467", "1291"]
    review_candidates = []

    definition_updates = {
        "1429": {
            "name_zh": "宽握正手引体向上",
            "category": "back",
            "equipment": "body weight",
            "target": "lats",
            "muscle_group": "",
            "secondary_muscles": ["biceps", "forearms", "upper back"],
            "movement_patterns_zh": ["拉", "垂直拉"],
            "required_equipment_zh": ["单杠"],
            "instructions_zh": [
                "站在单杠下，双手采用宽于肩距的正手抓法（掌心朝前）握稳单杠横杆。",
                "双臂充分伸直离地，主动下沉肩胛骨并收紧核心与双腿避免晃动。",
                "呼气由背阔肌主导发力将双肘向下内收拉动身体向上，直至下巴清晰越过单杠横杆平面。",
                "在顶端短暂停顿收紧背部肌群后，吸气控制肌肉张力缓缓下放回伸直起始位；每次完整拉放计一次。",
            ],
        },
        "1287": {
            "name_zh": "带勾脚下斜哑铃单臂胸推",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "shoulders"],
            "movement_patterns_zh": ["推", "核心稳定"],
            "required_equipment_zh": ["带勾脚的下斜训练凳"],
            "instructions_zh": [
                "双脚稳稳勾住带勾脚的下斜训练凳滚轴护垫，仰卧贴实凳面，非工作臂自然放松或轻搭腹侧平衡，工作手正握单只哑铃置于胸侧上方（掌心朝向脚端）。",
                "收紧核心与臀腿抗旋转稳住身体在凳面上不侧滑偏移。",
                "呼气由胸大肌下部与肱三头肌、三角肌前束协同发力垂直向上推起哑铃至臂接近伸直。",
                "在顶点短暂停顿后，吸气有控制地沿原直线轨道缓慢放落哑铃回胸外侧；单臂完成规定次数后换手。",
            ],
        },
        "1430": {
            "name_zh": "双杠前倾臂屈伸",
            "category": "chest",
            "equipment": "body weight",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "shoulders"],
            "movement_patterns_zh": ["推", "垂直推"],
            "required_equipment_zh": ["双杠"],
            "instructions_zh": [
                "站在双杠架中央，双手稳握两侧双杠抓把撑直双臂并将重心提起离地，躯干略微前倾约15至25度、双膝微屈双脚后交维持平衡。",
                "下沉双肩远离双耳，收紧腹臀核心控制下肢不大幅前后摆动。",
                "吸气主动控制肘关节向斜后外侧屈曲缓缓降低身体，至上臂与双杠平行或略低、胸肩前束充分牵伸为止。",
                "呼气由胸大肌下束与肱三头肌共同发力向上推直双臂回到顶端起点；每次降起计一次。",
            ],
        },
        "1288": {
            "name_zh": "健身球仰卧哑铃单臂飞鸟",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["shoulders", "triceps"],
            "movement_patterns_zh": ["水平推", "核心稳定"],
            "required_equipment_zh": ["瑜伽球"],
            "instructions_zh": [
                "坐在瑜伽球上单手持哑铃，双脚前移滚躺至上背与肩胛贴稳球面呈水平桥状、双脚稳踩地面、另一手搭放骨盆处抗旋转。",
                "工作手将哑铃举于胸口正上方（掌心朝内，肘角始终保持微屈缓冲）。",
                "吸气保持微屈肘角向单侧缓慢划弧展开哑铃至大臂接近水平、胸部充分伸展。",
                "呼气由工作侧胸大肌主导收缩拉回哑铃至胸上方起点；单臂完成规定次数后换手。",
            ],
        },
        "1460": {
            "name_zh": "单腿交替行进弓步蹲",
            "category": "upper legs",
            "equipment": "body weight",
            "target": "glutes",
            "muscle_group": "",
            "secondary_muscles": ["quadriceps", "hamstrings", "calves"],
            "movement_patterns_zh": ["下肢", "单侧稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚并拢自然直立，双手叉腰或自然垂于体侧维持上身直立，核心收紧。",
                "一侧腿向前迈出一大步并顺势垂直下蹲，使前后膝均弯曲至约90度（前膝对齐脚尖、后膝轻近地面不猛磕）。",
                "呼气以前侧脚掌与臀股肌肉主动发力蹬地向前迈进并拔直站起，顺畅切换另一侧腿继续向前迈步成弓步下蹲。",
                "保持目视前方与骨盆平稳沿直线行进；按每侧交替迈出步数计次。",
            ],
        },
        "1289": {
            "name_zh": "上斜哑铃单臂胸推",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["shoulders", "triceps"],
            "movement_patterns_zh": ["推", "核心稳定"],
            "required_equipment_zh": ["上斜训练凳"],
            "instructions_zh": [
                "将上斜训练凳调整至约45度角并稳靠坐卧于凳面，双脚平踩地面、非工作手轻扶腹侧或大腿面协助抗旋转，工作手正握单只哑铃置于胸肩外侧上方、掌心朝前方。",
                "贴实肩背与臀部于凳面，收紧核心不扭转脊柱。",
                "呼气由上胸肌、三角肌前束与肱三头肌协同发力垂直向上略微内收推举哑铃至臂接近伸直。",
                "在顶端短暂停顿后，吸气控制下落速度回到胸肩侧起推位；单臂完成规定次数后换手。",
            ],
        },
        "1466": {
            "name_zh": "单侧仰卧臀桥髋旋",
            "category": "upper legs",
            "equipment": "body weight",
            "target": "glutes",
            "muscle_group": "",
            "secondary_muscles": ["obliques", "hamstrings"],
            "movement_patterns_zh": ["髋铰链", "核心旋转"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "仰卧于地面或训练垫，双腿屈膝约与髋同宽、全脚掌踩实垫面，双手平放体侧地面协助平衡。",
                "收紧臀大肌与核心向上挺髋进入标准臀桥位（肩、髋、膝在同一直线上），并保持双肩全程贴实垫面。",
                "呼气保持骨盆抬高高度基本稳定，有控制地将并拢的双膝一并向一侧温和旋落感受腹斜肌与对侧臀髋转动稳定控制，再回中立顶桥位并交替旋向另一侧。",
                "两侧完成规定交替次数后缓缓放回地面；按每侧旋动计一次。",
            ],
        },
        "1290": {
            "name_zh": "坐瑜伽球哑铃单臂推举",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["shoulders", "triceps", "core"],
            "movement_patterns_zh": ["推", "垂直推", "核心稳定"],
            "required_equipment_zh": ["瑜伽球"],
            "instructions_zh": [
                "挺直腰背稳坐在瑜伽球正中，双脚分开略宽于肩平踩稳地面、膝屈约90度，非工作手轻搭大腿辅助抗倾倒，工作手单持哑铃举于肩侧高度（掌心朝前）。",
                "收紧腹部核心与臀部稳住球体居中不晃，避免下腰向后代偿反弓。",
                "呼气由三角肌与上胸、肱三头肌协同发力向上推举哑铃过顶至臂接近伸直。",
                "在顶点短暂停顿后，吸气有控制地缓缓下放回到肩侧起推位；单臂完成规定次数后换手。",
            ],
        },
        "1467": {
            "name_zh": "俯卧前臂支肘臂屈伸",
            "category": "upper arms",
            "equipment": "body weight",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["chest", "shoulders", "core"],
            "movement_patterns_zh": ["推", "水平推"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "俯身以双手手掌与前臂平行贴地作双臂屈伸预备姿（两手肘压在肩前下方地面、双腿向后并直脚尖点地撑稳身体成直线）。",
                "收紧腹臀核心防止腰部塌陷或臀部翘高。",
                "呼气集中由肱三头肌收缩发力将双肘用力向地面撑推向上伸直（前臂随势离开地面至手掌撑直或近直臂高位）。",
                "在顶部控制停顿片刻后，吸气缓缓曲肘落回双前臂贴稳地面起始位；每次撑起放落计一次。",
            ],
        },
        "1291": {
            "name_zh": "坐瑜伽球仰靠哑铃单臂直臂上拉",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "lats", "upper back"],
            "movement_patterns_zh": ["肩伸展", "过顶伸展", "核心稳定"],
            "required_equipment_zh": ["瑜伽球"],
            "instructions_zh": [
                "背靠稳固瑜伽球略作仰靠并坐稳（双脚宽距平踩地面维持平衡，非工作手轻搭同侧大腿辅助稳控），工作手单握一只哑铃垂直举于胸前上方、肘关节保持微屈缓冲。",
                "收紧核心与下背防止球体滑移或肋骨过度上翻。",
                "吸气以肩为轴控制哑铃沿头后下方画出弧线缓慢下降至大臂接近水平、胸阔与背阔充分伸展。",
                "呼气由胸肌与背阔肌主导发力沿原弧线将哑铃拉回胸口正上方；单臂完成规定次数后换手。",
            ],
        },
    }

    sources = {}
    review_notes = {}

    pending = {
        "1429": "待修图 · 已纠正上游要点误写“杠铃”为单杠横杆并补充 `单杠` 支持；原图第 1 帧经 `(+2,0)` 对齐后左侧门柱虽达 `0.9801–0.9847`，但右侧门柱偏移达 `-1 px`（`rack_br sc=0.9437, rack_tr sc=0.9298`），存在 `1 px` 门架宽窄畸变未能多锚点同步达 `>= 0.96`，暂存待重制。",
        "1287": "待修图 · 已按实图带勾脚滚轴垫特征补充 `带勾脚的下斜训练凳` 并保持单臂计次；原图在 `(+18,0)/(0,+18)` 下 `bench_br` 仍偏移错位（`sc=0.884`）且头部角度差异较大（`head sc=0.73–0.74`），暂存待重制。",
        "1430": "待修图 · 已纠正原上游错译“胸推（在双杠架上）”与错词“倾斜杆／杠铃”，规范为双杠前倾臂屈伸并补齐 `双杠`；原图第 2 帧龙门顶角与底座角呈现 `2 px` 垂向及横向压缩畸变（`cage_tl sc=0.9568, cage_br res=2.24 px`），暂存待重制。",
        "1288": "待修图 · 已补充 `瑜伽球` 必需支持并保持单臂计次；原图 F0 至 F2 球面随肩外展整体左滚上移、脚位与身体姿态大幅偏移，暂存待重制。",
        "1460": "待修图 · 已规范为单腿交替行进弓步蹲（触发单腿逐侧计次）；原图行进前跨步从立姿跨入深弓步全身平移及幅度变化较大，暂存待重制。",
        "1289": "待修图 · 已补充 `上斜训练凳` 支持并保留单臂计次；原图第 2 帧头部与斜凳支脚位置发生 `9–27 px` 错位拉伸（`bench_br best_sc=0.9076`），暂存待重制。",
        "1466": "待修图 · 已纠正错译“扭髋抬腿”为单侧仰卧臀桥髋旋并触发单侧计次；原图第 1、2 帧头部（`dx=+10/-1, dy=+1/+35`）与肩臂及地面双足不同步漂移（`sc=0.82–0.93`），暂存待重制。",
        "1290": "待修图 · 已补充 `瑜伽球` 与过顶垂直推肩负荷筛查（保留单臂计次）；原图第 0 帧底缘 `y=479` 裁底、第 2 帧举铃触及顶缘 `y=0` 裁顶且头部偏斜，暂存待重制。",
        "1467": "待修图 · 已清理重复句及易触发“平板支撑”静态误判用语，改名为俯卧前臂支肘臂屈伸；原图第 1、2 帧前臂支撑与足尖之间存在 `~35 px` 水平滑动错位（`toes/forearms sc=0.78–0.87`），暂存待重制。",
        "1291": "待修图 · 已纠正严重错译“拉下推”为坐瑜伽球仰靠哑铃单臂直臂上拉（补 `瑜伽球` 与过顶肩负）；原图第 2 帧顶边 `y=0` 残留多余断手杂块且第 0、1 帧触底 `y=479`，暂存待重制。",
    }

    result = {
        "batch": "20261014_review36",
        "version": "1.2.41",
        "version_code": 2026101401,
        "apk_name": "时光屋-1.2.41-第三十六批动作复核.apk",
        "output": "build/review36-20261014",
        "report": "docs/releases/2026-10-14-review-batch36.md",
        "inspected": inspected,
        "definition_updates": definition_updates,
        "sources": sources,
        "review_candidates": review_candidates,
        "pending": pending,
        "registered_media": review_candidates,
        "original_pose_repairs": review_candidates,
        "generated_images_imported": 0,
        "image_generation_calls": 0,
        "quota_exhausted_reset_at": "2026-11-12T05:37:04Z",
        "review_notes": review_notes,
    }
    (B / "review-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

    code_files = sorted(R.glob("app/src/main/java/**/*.java"))
    baseline = {str(p.relative_to(R)): sha(p) for p in code_files}
    (B / "code-baseline.json").write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n")

    qa_spec = {
        "batch": "20261014_review36",
        "expected_checks": 16,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20261014_review36")


if __name__ == "__main__":
    main()
