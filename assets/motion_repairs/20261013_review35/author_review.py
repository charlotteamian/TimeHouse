#!/usr/bin/env python3
"""Author Batch 35 (20261013_review35) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["1419", "1282", "1421", "1283", "1422", "1284", "1423", "1285", "1424", "1286"]
    review_candidates = ["1422"]

    definition_updates = {
        "1419": {
            "name_zh": "单侧仰卧直腿摆髋铁十字拉伸",
            "category": "upper legs",
            "equipment": "body weight",
            "target": "glutes",
            "muscle_group": "",
            "secondary_muscles": ["hamstrings", "quadriceps", "obliques"],
            "movement_patterns_zh": ["拉伸", "核心旋转"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "仰卧在训练垫上，双臂向两侧水平打开伸直（掌心贴稳地面固定肩胛），并腿向上抬起与地面接近垂直、保持双膝尽量伸直。",
                "收紧核心贴稳下背不猛甩腰椎。",
                "吸气缓慢将并拢的双腿向体侧地面降落靠近一侧手掌方向（过程中保持双肩全程贴地不耸离），感受臀侧与后链舒展扭转拉伸。",
                "在舒适牵伸位短暂停留后呼气由侧腹发力带动双腿回到垂直正中；交替两侧各完成规定次数。",
            ],
        },
        "1282": {
            "name_zh": "健身球仰斜哑铃单臂推举",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["shoulders", "triceps", "core"],
            "movement_patterns_zh": ["推", "核心稳定"],
            "required_equipment_zh": ["瑜伽球"],
            "instructions_zh": [
                "坐在瑜伽球上工作手单持哑铃，双脚前移滚躺至上背及肩颈稳靠球面呈斜卧姿，另一手搭放体侧辅助稳定骨盆、双脚稳踩地面。",
                "收紧腹臀核心防止球面左右旋转倾斜，工作手将哑铃持于胸肩外上方、掌心朝前。",
                "呼气由上胸肌、三角肌前束与肱三头肌协同向上微内收推举哑铃至臂接近伸直。",
                "在顶点短暂停顿后有控制地缓缓下放回肩胸侧起点；单臂完成规定次数后换手。",
            ],
        },
        "1421": {
            "name_zh": "俯撑屈肘降前臂俯卧撑",
            "category": "lower arms",
            "equipment": "body weight",
            "target": "forearms",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "chest", "shoulders"],
            "movement_patterns_zh": ["推", "水平推"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "从直臂俯撑起始位开始，双手掌压实置于双肩正下方地面，躯干从头至踝呈一条直线。",
                "锁紧腹臀不塌腰撅臀，双肘贴近体侧。",
                "吸气先屈肘平稳放低上身至双前臂依次轻稳落贴地面，使肘关节落于肩下方前臂俯撑位。",
                "呼气发力由前臂、肱三头肌与胸肩前推掌根将双肘推直回到高俯撑起始位；每次落臂推回计一次。",
            ],
        },
        "1283": {
            "name_zh": "健身球仰斜哑铃推举",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["shoulders", "triceps", "core"],
            "movement_patterns_zh": ["推", "核心稳定"],
            "required_equipment_zh": ["瑜伽球"],
            "instructions_zh": [
                "坐在瑜伽球上双手各持一只哑铃，双脚前挪滚躺至上背贴稳球面呈仰斜卧姿，双脚分开踩实地面。",
                "收紧核心与臀部维持球体稳固，双手将哑铃举于胸肩两侧上方、掌心朝前下斜方向。",
                "呼气由胸大肌、三角肌与肱三头肌发力向上推举哑铃至手臂接近伸直（哑铃呈自然微内收汇聚）。",
                "在顶点短暂停顿后，吸气控制下放回肩侧起始位；每次推回计一次。",
            ],
        },
        "1422": {
            "name_zh": "仰卧骨盆后倾臀桥",
            "category": "upper legs",
            "equipment": "body weight",
            "target": "glutes",
            "muscle_group": "",
            "secondary_muscles": ["hamstrings", "core"],
            "movement_patterns_zh": ["髋铰链", "核心控制"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "仰卧在训练垫上，双腿屈膝约与髋同宽、全脚掌踩稳垫面，双臂自然伸直平放体侧、掌心向下贴实垫面。",
                "呼气收紧核心先温和向上后倾骨盆使下背轻轻贴平垫面。",
                "顺势由臀大肌与腘绳肌协同发力推高髋部离地，直至肩、髋、膝呈一条平稳斜线（避免腰椎过度反弓顶出）。",
                "在顶端挤压臀部停顿片刻后有控制地逐节放落回仰卧起点；每次顶髋回落计一次。",
            ],
        },
        "1284": {
            "name_zh": "健身球仰卧哑铃直臂上拉",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["lats", "triceps", "shoulders"],
            "movement_patterns_zh": ["肩伸展", "过顶伸展"],
            "required_equipment_zh": ["瑜伽球"],
            "instructions_zh": [
                "坐在瑜伽球上双手持同一只哑铃并前移双脚滚躺至上背与肩胛稳架于球顶、臀部略收稳成桥形、双脚踩实地面。",
                "双手叠掌托住哑铃一端内片举于胸口正上方，双肘微留缓冲不锁死并收紧核心避免肋骨过度上翻。",
                "吸气以肩为轴将哑铃沿头顶方向缓慢向后下方画弧下放至大臂接近与地面平行、胸廓与背阔充分伸展。",
                "呼气由胸大肌、背阔肌与前锯肌发力沿原弧线拉回胸口正上方；每次下放拉回计一次。",
            ],
        },
        "1423": {
            "name_zh": "平凳俯卧反向挺身举腿",
            "category": "upper legs",
            "equipment": "body weight",
            "target": "glutes",
            "muscle_group": "",
            "secondary_muscles": ["hamstrings", "lower back"],
            "movement_patterns_zh": ["髋铰链", "后链伸展"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "俯卧在稳固的平板训练凳上，使骨盆髂前上棘刚好位于凳面边缘、双腿自然伸直垂悬于凳端外侧。",
                "双肘屈放凳端或双手紧抓凳边脚架稳住上身与躯干位置不滑动。",
                "呼气集中由臀大肌与腘绳肌协同发力带动伸直的双腿向上平稳抬起至与躯干平齐或略高（避免靠猛晃借力过度折腰）。",
                "在顶峰紧缩臀部停顿片刻后，吸气控制速率缓缓放落回凳边垂悬位；每次抬放计一次。",
            ],
        },
        "1285": {
            "name_zh": "平凳仰卧哑铃单臂飞鸟",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["shoulders"],
            "movement_patterns_zh": ["水平推", "核心稳定"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "仰卧在平板训练凳上双脚平踩地面、非工作手轻按腹侧辅助稳定，工作手单持一只哑铃垂直举于肩胸上方（掌心向内）。",
                "锁稳核心抗旋转不让身躯向工作侧翻倒，工作肘保持微屈缓冲角。",
                "吸气缓慢沿宽弧线向工作侧斜下方打开哑铃直至大臂与地面接近平行、胸肌充分牵伸。",
                "呼气由工作侧胸肌主导收缩沿原弧线拉回胸前上方；单臂完成规定次数后换手。",
            ],
        },
        "1424": {
            "name_zh": "单侧坐姿跨踝压膝臀肌拉伸",
            "category": "upper legs",
            "equipment": "body weight",
            "target": "glutes",
            "muscle_group": "",
            "secondary_muscles": ["hamstrings"],
            "movement_patterns_zh": ["拉伸", "下肢"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "坐在地上或训练垫上，先伸直支撑侧腿于身前，同侧手向斜后方撑稳地面支撑躯干挺拔。",
                "将待拉伸侧膝盖屈曲、同侧外踝轻松搭跨在直伸大腿上方靠近膝盖处。",
                "呼气保持腰背挺拔并用空余手轻柔温和地向下按压屈曲侧膝盖，加深对侧臀大肌与梨状肌拉伸感。",
                "在舒适牵伸位平稳呼吸15至25秒后放松回位；每侧完成后换另一侧腿。",
            ],
        },
        "1286": {
            "name_zh": "健身球仰卧哑铃单臂胸飞鸟",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["shoulders", "triceps", "core"],
            "movement_patterns_zh": ["水平推", "核心稳定"],
            "required_equipment_zh": ["瑜伽球"],
            "instructions_zh": [
                "坐在瑜伽球上工作手单持哑铃，双脚前移滚躺至上背与肩胛稳靠球面成水平仰卧桥状、另一手轻搭躯干或外侧维持平衡。",
                "收紧臀肌与腹部避免球面左右晃动，工作手将哑铃举于胸上方（掌心朝内、微屈肘）。",
                "吸气沿宽弧线缓缓向单侧展开哑铃至大臂接近水平、胸部充分打开拉伸。",
                "呼气由工作侧胸大肌发力夹胸将哑铃拉回胸口上方；单臂完成规定次数后换手。",
            ],
        },
    }

    sources = {
        "1422": "https://exrx.net/WeightExercises/GluteusMaximus/BWGluteBridge",
    }

    review_notes = {
        "1422": "规范为仰卧骨盆后倾臀桥（避免任何静态持姿误触发关键词）并明确臀大肌主目标及腘绳肌／核心协同；原图第 2 帧经 `(0, +4)` 纯整数平移配准后垫面足侧、垫面头侧、双脚掌、撑地双手与头颈五大锚点全部 `0.0 px` 精确对齐（匹配分 `>= 0.9607`），无边缘截断，Frame 4 = Frame 2，2.36 秒循环。",
    }

    pending = {
        "1419": "待修图 · 已补充核心旋转与双肩贴地约束（保留单侧计次）；原图肩臂延伸展开跨越三帧高度变化较大且躯干发生纵向移位，暂存待重制。",
        "1282": "待修图 · 已补充 `瑜伽球` 支持并保留单臂计次；原图瑜伽球轮廓及阴影在三帧间发生变化（`ball best_sc=0.9034–0.9126`），头仰角度亦不同，暂存待重制。",
        "1421": "待修图 · 已改名为俯撑屈肘降前臂俯卧撑以明确高俯撑起落节奏；原图第 2 帧右鞋尖触 `x=479` 且下肢占比缩放错位（`legs_shorts sc=0.8354`），暂存待重制。",
        "1283": "待修图 · 已补充 `瑜伽球` 必需支持与仰斜哑铃推举要点；原图第 1 帧瑜伽球（`dx=+5`）与双脚（`dx=0`）出现 `5 px` 异步滑动及头部缩移，暂存待重制。",
        "1284": "待修图 · 已纠正原上游严重错译“哑铃球上拉下推”为健身球仰卧哑铃直臂上拉，补充 `瑜伽球` 及过顶伸展肩负筛查；原图球体位置随肩屈大幅上下位移压缩，暂存待重制。",
        "1423": "待修图 · 已彻底清除易误触发静态计时的“平板”字样改名为平凳俯卧反向挺身举腿，补充 `平板训练凳` 支持；原图第 0 帧与第 1、2 帧长凳右支架横向跨度相差约 `40 px`（长凳变形拉长），暂存待重制。",
        "1285": "待修图 · 已补充 `平板训练凳` 支持并保留单臂计次；原图第 2 帧长凳左支架（`dx=-22, dy=+25`）与右支架（`dx=0, dy=+34`）存在 `22 px` 透视剪变错位，暂存待重制。",
        "1424": "待修图 · 已规范为单侧坐姿跨踝压膝臀肌拉伸（触发单侧）；原图第 2 帧全身尺度与地面坐姿位置大幅跳升（`dy=+45` 差异），暂存待重制。",
        "1286": "待修图 · 已补充 `瑜伽球` 必需支持并保留单臂计次；原图三帧球面及脚跟相对移位达 `19–20 px` 且存在非刚性滚动，暂存待重制。",
    }

    result = {
        "batch": "20261013_review35",
        "version": "1.2.40",
        "version_code": 2026101301,
        "apk_name": "时光屋-1.2.40-第三十五批动作复核.apk",
        "output": "build/review35-20261013",
        "report": "docs/releases/2026-10-13-review-batch35.md",
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
        "batch": "20261013_review35",
        "expected_checks": 10,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20261013_review35")


if __name__ == "__main__":
    main()
