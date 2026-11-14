#!/usr/bin/env python3
"""Author Batch 30 (20261008_review30) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["1326", "0425", "1327", "0427", "1346", "0428", "1352", "0429", "1355", "0431"]
    review_candidates = ["1327"]

    definition_updates = {
        "1326": {
            "name_zh": "反手引体向上",
            "category": "back",
            "equipment": "body weight",
            "target": "lats",
            "muscle_group": "",
            "secondary_muscles": ["biceps", "forearms", "upper back"],
            "movement_patterns_zh": ["拉", "垂直拉"],
            "required_equipment_zh": ["单杠"],
            "instructions_zh": [
                "面对单杠站立，双手约与肩同宽反握（掌心朝向自己）抓稳上方单杠横杆，双臂伸直并主动下沉肩胛进入稳定起始位。",
                "双脚离地，收紧腹部核心与臀部避免下肢前后晃动。",
                "呼气由背阔肌与肱二头肌协同发力带动肘关节向体侧下后方拉动，将胸口拉向单杠直至下巴越过横杆平面。",
                "在最高点短暂停顿收紧背部与二头肌后，吸气有控制地缓缓伸直手臂下放回垂直位；每次拉起与下放计一次。",
            ],
        },
        "0425": {
            "name_zh": "哑铃站立单臂反握弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽直立站稳，一侧手采用正反旋前握法（手背朝前、掌心朝后贴近大腿）持一只哑铃自然垂于体侧，另一手臂自然垂放平衡。",
                "挺胸沉肩锁稳腹部核心，将工作侧上臂贴近肋侧全程保持垂直不前甩。",
                "呼气由前臂肱桡肌、肱肌与肱二头肌协同发力弯曲工作肘将哑铃向上弯举至肩前高度（掌心于顶端朝前方）。",
                "在顶峰停顿片刻后，吸气有控制地缓缓伸肘放回大腿侧垂悬起始位；单侧完成规定次数后换另一臂。",
            ],
        },
        "1327": {
            "name_zh": "窄握反手引体向上",
            "category": "back",
            "equipment": "body weight",
            "target": "lats",
            "muscle_group": "",
            "secondary_muscles": ["biceps", "forearms", "upper back"],
            "movement_patterns_zh": ["拉", "垂直拉"],
            "required_equipment_zh": ["单杠"],
            "instructions_zh": [
                "站在单杠下，双手采用窄于肩距的反握法（掌心朝向自己、两手间距约一拳至半肩宽）稳握单杠横杆。",
                "双臂充分伸直离地，下沉肩胛并收紧核心与臀腿交叉稳定躯干避免前后荡摆。",
                "呼气专注收紧背阔肌下部与肱二头肌将肘尖直向下后方拉动，把上胸和下颌顺势拉高过单杠横杆。",
                "在最高处停顿收紧背阔肌与二头肌后，吸气控制肌肉张力缓缓下放回到伸直起始位；每次完整拉起与下放计一次。",
            ],
        },
        "0427": {
            "name_zh": "哑铃站立对握过顶推举",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "traps", "core"],
            "movement_patterns_zh": ["垂直推", "过顶伸展", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽稳踩地面站直，双手采用掌心相对的平行对握法举起一对哑铃停于双肩前外侧、小臂保持垂直地面。",
                "收紧核心与臀部锁稳骨盆与肋骨，避免推起过程中下背过度反弓。",
                "呼气保持掌心全程相对对握，由三角肌与肱三头肌发力垂直向上推举过头顶至双臂接近伸直（肘留微屈缓冲）。",
                "在顶点短暂停顿控制后，吸气顺原直线缓慢放回肩外侧起始高度；每次推起与下放计一次。",
            ],
        },
        "1346": {
            "name_zh": "跪姿举臂侧倾背阔肌拉伸",
            "category": "back",
            "equipment": "body weight",
            "target": "lats",
            "muscle_group": "",
            "secondary_muscles": ["obliques", "shoulders"],
            "movement_patterns_zh": ["拉伸", "核心侧屈"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双膝分开约与髋同宽跪在软垫上，挺直脊柱并轻微收紧核心稳定骨盆不前后摇晃。",
                "双手高举过头顶并于上方轻轻交握掌心朝内，双臂尽量伸直远离双耳而不耸肩。",
                "呼气保持躯干不前弯或扭转，温和而缓慢地向身体一侧侧屈伸展，清晰感受对侧背阔肌及侧腰肋缘被温和拉长。",
                "到达舒适牵伸幅度后呼气自然缓回正中，左右侧或单侧交替顺畅完成预定次数。",
            ],
        },
        "0428": {
            "name_zh": "牧师凳站姿哑铃弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲"],
            "required_equipment_zh": ["牧师凳"],
            "instructions_zh": [
                "站立在稳固的牧师凳后侧双脚开立踩稳，俯身将双上臂后侧贴实斜放于牧师凳倾斜垫面，双手反握各持一只哑铃（掌心斜朝前上）。",
                "腋下轻贴斜垫上缘锁稳上臂不前移抬肘，肘尖朝前下方自然伸展并微留缓冲。",
                "呼气由肱二头肌与肱肌集中发力带动双手沿着斜垫前方弧线向上弯举哑铃直至前肩前方位置。",
                "在顶峰短暂停顿收紧后，吸气缓慢控制下放回几乎伸直但不磕垫撞击的底端；每次弯举与下放计一次。",
            ],
        },
        "1352": {
            "name_zh": "俯卧下背挺身",
            "category": "back",
            "equipment": "body weight",
            "target": "lower back",
            "muscle_group": "",
            "secondary_muscles": ["glutes", "hamstrings"],
            "movement_patterns_zh": ["髋伸展", "脊柱伸展"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "俯卧在地面或训练垫上，双腿伸直并拢脚背轻点垫面，双臂伸直掌心贴腿侧地面保持稳定。",
                "微收下颌目光看向垫前方维持颈椎自然延伸，先轻微收紧臀部与大腿后侧。",
                "呼气由竖脊肌发力有控制地缓慢向上抬起胸部与上肩离开垫面，髋部与双腿始终紧贴地面不借力猛甩。",
                "在舒适伸展顶峰停顿片刻后，吸气缓缓控制降回垫面恢复平躺位；每次挺身与下放计一次。",
            ],
        },
        "0429": {
            "name_zh": "哑铃站立反握弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽直立站稳，双手采用正反旋前握法（掌心朝向身体与后方、手背朝正前方）各握一只哑铃垂于体侧。",
                "挺胸沉肩收紧核心，保持双侧上臂贴近肋部全程固定不前后借力晃动。",
                "呼气由前臂肱桡肌、肱肌与肱二头肌协同收缩弯曲双肘，将哑铃同时向上弯举至胸肩前方高度。",
                "在顶峰短暂停顿后，吸气有控制地缓缓伸肘放回大腿前方垂悬起始位；每次弯举与下放计一次。",
            ],
        },
        "1355": {
            "name_zh": "扶墙单臂背阔肌伸展推撑",
            "category": "back",
            "equipment": "body weight",
            "target": "lats",
            "muscle_group": "",
            "secondary_muscles": ["shoulders", "triceps", "core"],
            "movement_patterns_zh": ["单臂", "站姿稳定"],
            "required_equipment_zh": ["墙面"],
            "instructions_zh": [
                "面向墙面站在离墙约一臂远的位置，双脚略宽于髋踩稳地面，单侧手臂直伸向前将掌根稳抵墙面肩高处，另一手臂自然垂于体侧。",
                "下沉肩胛并收紧核心维持躯干与脊柱中立。",
                "吸气保持工作臂伸直掌稳贴墙，缓慢屈髋并向后下方沉压胸椎拉长该侧背阔肌与侧腋。",
                "呼气由背阔肌与肩下压力量主动将手掌下按推墙使躯干回到直立高撑起始位；单侧完成规定次数后换另一臂。",
            ],
        },
        "0431": {
            "name_zh": "哑铃单腿登阶",
            "category": "upper legs",
            "equipment": "dumbbell",
            "target": "glutes",
            "muscle_group": "",
            "secondary_muscles": ["quads", "hamstrings", "calves"],
            "movement_patterns_zh": ["下肢推", "单腿"],
            "required_equipment_zh": ["稳固踏台"],
            "instructions_zh": [
                "站在稳固踏台或跳箱前约半步，双手各持一只哑铃自然垂于体侧、掌心朝向身体，将工作侧脚掌稳踩踏台中央，另一脚踏地准备。",
                "挺胸收腹保持躯干轻微前倾，工作膝盖对准脚尖方向不内扣。",
                "呼气以前脚掌与脚跟发力向下踩踏台，由工作腿臀肌与股四头肌主导带动身体顺直站上踏台、另一脚并拢落台。",
                "站稳顶峰后，吸气缓慢先用非工作脚后撤落回地面复位后再下踩或连续单腿交替完成规定次数后换腿。",
            ],
        },
    }

    sources = {
        "1327": "https://www.muscleandstrength.com/exercises/chin-up",
    }

    review_notes = {
        "1327": "规范“窄握反手引体向上”（窄于肩距反握、避开静态词并更正“杠铃杆”错译，补齐必需器械 `单杠` 与背阔肌/二头/上背肌群）；原图第 2 帧垂直微移 `(0, +1)` 后龙门架四角（上下左右框脚）全部精确对齐，残差 `≤ 1.0 px`（匹配分 `≥ 0.9803`），无顶底边缘截断。",
    }

    pending = {
        "1326": "待修图 · 已纠正错译“杠铃杆”为单杠横杆并补齐 `单杠` 支持；原图第 0 帧脚尖触底（y=479）、第 2 帧头顶触顶（y=0）且龙门架配重柱与横杆在各帧间明显位移，暂存待重制。",
        "0425": "待修图 · 已规范哑铃站立单臂反握弯举（单臂单侧计次）并补充前臂肱桡与肱肌协同标签；原图第 1 帧经 `(+7, 0)` 平移对齐后第 2 帧双脚（`dy=-1`）与头部（`dy=+2`, `head sc0=0.8835`）之间存在 `3 px` 逆向压缩错位，暂存待重制。",
        "0427": "待修图 · 已规范为哑铃站立对握过顶推举并清理错误 `chest` 次要肌群；原图第 2 帧推举过顶时双脚（`dy=-6`）、裤腰（`dy=-17`）与头部（`dy=-20`, `head sc=0.7865`）存在 `14–20 px` 纵向缩水错位，暂存待重制。",
        "1346": "待修图 · 已纠正原混淆名称“跪姿下拉拉伸”为跪姿举臂侧倾背阔肌拉伸并删除矛盾“20-30秒”要求；原图第 1 帧整幅左移 `30 px`，第 2 帧跪姿膝底比前两帧抬离地面参考线达 `23 px`（`474 -> 451`），暂存待重制。",
        "0428": "待修图 · 已规范牧师凳站姿哑铃弯举并补齐 `牧师凳` 必需支撑器械；原图第 2 帧牧师凳与双脚上移 `6 px` 而头部仅移 `1 px`（存在 `5 px` 纵向压缩错位，`head sc=0.9021`），暂存待重制。",
        "1352": "待修图 · 已将“下背部卷曲”规范为俯卧下背挺身并调整主目标为 `lower back`（下背）；原图第 2 帧脚鞋上移 `19 px` 而小腿/臀跨帧横向拉剪 `7–13 px`（`sc=0.923`），暂存待重制。",
        "0429": "待修图 · 已纠正步骤中错写的“手掌朝向身体”（锤式）为旋前反握（手背朝前）；原图第 1 帧整体偏左 `13 px`，第 2 帧双脚（`dy=+5`）与头部（`dx=+1, dy=0`, `sc=0.9329`）存在 `5 px` 纵向拉伸，暂存待重制。",
        "1355": "待修图 · 已将模糊名称“单臂靠墙”明确为扶墙单臂背阔肌伸展推撑（单臂单侧计次）并补 `墙面` 支持；原图第 1 帧墙面右移 `40 px`，第 2 帧墙面原地不动而双脚向左大幅跳移 `47 px`，暂存待重制。",
        "0431": "待修图 · 已规范为哑铃单腿登阶（单腿单侧计次）并补 `稳固踏台` 支持；原图第 0 帧触底（y=479）、第 2 帧头冠触顶（y=0）且跳箱跨帧移位约 `20 px`，暂存待重制。",
    }

    result = {
        "batch": "20261008_review30",
        "version": "1.2.35",
        "version_code": 2026100801,
        "apk_name": "时光屋-1.2.35-第三十批动作复核.apk",
        "output": "build/review30-20261008",
        "report": "docs/releases/2026-10-08-review-batch30.md",
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
        "batch": "20261008_review30",
        "expected_checks": 10,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20261008_review30")


if __name__ == "__main__":
    main()
