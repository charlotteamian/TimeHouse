#!/usr/bin/env python3
"""Author Batch 34 (20261012_review34) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["1401", "1277", "1403", "1278", "1405", "1279", "1407", "1280", "1418", "1281"]
    review_candidates = []

    definition_updates = {
        "1401": {
            "name_zh": "单杠双力臂",
            "category": "back",
            "equipment": "body weight",
            "target": "lats",
            "muscle_group": "",
            "secondary_muscles": ["biceps", "triceps", "forearms", "chest"],
            "movement_patterns_zh": ["拉", "垂直拉", "水平推"],
            "required_equipment_zh": ["单杠"],
            "instructions_zh": [
                "双手略宽于肩采用高扣正握悬垂握稳上方单杠横杆，双臂充分伸直、核心与双腿微微收紧稳定。",
                "呼气由背阔肌与上背爆发性发力上拉，将胸部与下腹部带向单杠横杆近端并顺势前压翻转双腕。",
                "借推力过渡越过横杆平面后由肱三头肌与胸肌协同向下撑直双臂使肩部高于单杠。",
                "在顶端短暂停顿控制重心，随后有控制地曲肘落回杠下垂悬位并缓慢伸直手臂；每次完整翻撑计一次。",
            ],
        },
        "1277": {
            "name_zh": "健身球仰卧哑铃飞鸟",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["shoulders", "triceps"],
            "movement_patterns_zh": ["水平推", "核心稳定"],
            "required_equipment_zh": ["瑜伽球"],
            "instructions_zh": [
                "坐在稳固的瑜伽球上双手各持一只哑铃，双脚稳稳向前挪步并顺势滚躺至上背与肩颈贴实球面、臀部抬平与膝成直角。",
                "双手掌心相对将哑铃举于胸口正上方、双肘保留微屈缓冲并锁紧核心稳住球体不晃。",
                "吸气保持肘角不变沿宽弧线向体侧缓缓展开哑铃至大臂与躯干接近水平、胸肌充分拉伸。",
                "呼气由胸大肌协同三角肌发力沿原弧线夹紧拉回胸上方起始位；每次展开夹回计一次。",
            ],
        },
        "1403": {
            "name_zh": "单侧站姿颈部侧屈拉伸",
            "category": "neck",
            "equipment": "body weight",
            "target": "levator scapulae",
            "muscle_group": "",
            "secondary_muscles": ["trapezius", "sternocleidomastoid"],
            "movement_patterns_zh": ["颈部", "拉伸", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽自然站直，双臂自然垂于体侧、双肩放松主动下沉远离双耳。",
                "挺胸收腹保持躯干与骨盆中立静止不随之侧倾。",
                "呼气缓慢温和地将头部向一侧倾倒（耳朵靠近同侧肩膀，面庞仍保持朝正前方不旋转），感受对侧斜方肌上束与肩胛提肌舒展牵伸。",
                "在舒适牵伸位置平稳呼吸15至20秒后缓缓回正头颈；每侧完成规定次数后换另一侧。",
            ],
        },
        "1278": {
            "name_zh": "上斜凳靠球哑铃飞鸟",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["shoulders"],
            "movement_patterns_zh": ["水平推", "核心稳定"],
            "required_equipment_zh": ["上斜训练凳", "瑜伽球"],
            "instructions_zh": [
                "将上斜训练凳调整至约45度并在凳背稳妥架靠瑜伽球支撑，坐在凳面上双脚平踩稳地面、双手各持哑铃掌心相对举于胸上方。",
                "双肘始终维持轻微弯曲缓冲，沉肩贴稳靠背核心保持稳定。",
                "吸气缓慢沿宽广弧线向两侧下放哑铃直至大臂与地面接近平行、胸肌充分舒展。",
                "呼气由胸大肌发力夹紧将哑铃沿原弧线拉回胸口正上方；每次展开夹回计一次。",
            ],
        },
        "1405": {
            "name_zh": "站姿前扣掌展背扩胸拉伸",
            "category": "back",
            "equipment": "body weight",
            "target": "lats",
            "muscle_group": "",
            "secondary_muscles": ["shoulders", "chest"],
            "movement_patterns_zh": ["拉伸", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽直立站稳，双臂在胸前自然伸直并与地面平行，双手十指相扣、掌心翻转朝向前方。",
                "收紧腹部维持下背稳定不向前顶腰。",
                "呼气控制双肩顺势向前微展拉开肩胛间隙，低头微含胸将双手轻柔向前下方延伸感受上背、背阔肌与肩带展开。",
                "在舒适延伸感位置保持均匀呼吸15至20秒后缓缓回正起身；按次重复完成。",
            ],
        },
        "1279": {
            "name_zh": "上斜哑铃单臂飞鸟",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["shoulders", "triceps"],
            "movement_patterns_zh": ["水平推", "核心稳定"],
            "required_equipment_zh": ["上斜训练凳"],
            "instructions_zh": [
                "将上斜训练凳调整至30至45度，仰卧靠稳凳面、双脚平踩地面、非工作手轻搭腹侧辅助稳定骨盆，工作手单持一只哑铃垂直举于胸前上方（掌心向内）。",
                "锁稳核心抗旋转不使肩背随重量向工作侧翻斜，工作肘始终微屈锁定。",
                "吸气控制重心将哑铃沿宽大弧线缓缓向单侧斜下方展开至胸肌上缘充分牵伸。",
                "呼气由工作侧胸大肌发力夹胸将哑铃沿原弧线收回胸口上方；单臂完成规定次数后换手。",
            ],
        },
        "1407": {
            "name_zh": "单侧扶墙弓步前推小腿拉伸",
            "category": "lower legs",
            "equipment": "body weight",
            "target": "calves",
            "muscle_group": "",
            "secondary_muscles": ["hamstrings", "ankles"],
            "movement_patterns_zh": ["拉伸", "下肢"],
            "required_equipment_zh": ["墙面"],
            "instructions_zh": [
                "面对墙面站立保持约一臂距离，双手平扶墙面与胸肩等高维持支撑。",
                "一侧脚向后方退开一大步、后腿保持膝盖充分伸直且后脚跟全程平压地面不翘起。",
                "呼气屈肘同时前膝稳定前推、重心温和前移压向墙面，感受后侧小腿深层持续拉伸感。",
                "在舒适伸展位保持平稳呼吸20至30秒后推墙回正起身；每侧完成后换另一条腿。",
            ],
        },
        "1280": {
            "name_zh": "健身球仰斜哑铃单臂飞鸟",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["shoulders", "core"],
            "movement_patterns_zh": ["水平推", "核心稳定"],
            "required_equipment_zh": ["瑜伽球"],
            "instructions_zh": [
                "坐在瑜伽球上工作手单持哑铃，双脚前移滚躺至上背与肩颈靠稳球面成略斜卧姿，另一手搭稳体侧或腹前维持骨盆平衡，哑铃举于胸上方掌心朝内。",
                "收紧腹臀核心防止球面左右倾斜转动，工作肘微屈锁定。",
                "吸气控制速率向单侧缓缓展开哑铃至大臂接近水平、胸部上束充分牵伸。",
                "呼气由胸肌发力沿原弧线拉回哑铃至胸前上方；单臂完成规定次数后换手。",
            ],
        },
        "1418": {
            "name_zh": "深蹲起身单腿抱膝贴胸",
            "category": "upper legs",
            "equipment": "body weight",
            "target": "glutes",
            "muscle_group": "",
            "secondary_muscles": ["hamstrings", "quadriceps"],
            "movement_patterns_zh": ["下肢", "单侧稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚约与肩同宽自然直立站稳，核心收紧。",
                "吸气先向后屈髋顺畅下蹲至大腿接近水平，保持膝盖对齐脚尖方向与背部平直。",
                "呼气顺势起身并保持单侧支撑腿踩稳地面，随势抬起另一侧膝盖至胸前用双手轻轻环抱贴近胸口，感受支撑平衡与对侧臀肌伸展。",
                "在抱膝位稳控1至2秒后落脚回位并下蹲交替抬另一侧腿；按左右交替规定次数执行。",
            ],
        },
        "1281": {
            "name_zh": "上斜哑铃单臂推举",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["shoulders", "triceps", "core"],
            "movement_patterns_zh": ["推", "核心稳定"],
            "required_equipment_zh": ["上斜训练凳"],
            "instructions_zh": [
                "稳卧于上斜训练凳上，双脚平踩地面、非工作手轻扶体侧大腿或凳面协助抗旋转，工作手正握一只哑铃置于肩胸外侧、掌心朝前下斜方向。",
                "收紧核心紧贴凳背避免躯干扭转偏移。",
                "呼气由上胸与三角肌前束、肱三头肌发力向上稍内收推举哑铃至臂接近伸直。",
                "在顶点短暂停顿后，吸气有控制地缓缓下放回到肩胸侧起推位；单臂完成规定次数后换手。",
            ],
        },
    }

    sources = {}
    review_notes = {}

    pending = {
        "1401": "待修图 · 已纠正原严重错译“垂直杆引体向上”（muscle-up 为翻腕越杠）为单杠双力臂，补充 `单杠` 支持与双力臂发力顺序；原图第 2 帧翻杠高度下门架整体按比例缩小且双臂与横杆重排，暂存待重制。",
        "1277": "待修图 · 已补充 `瑜伽球` 必需支持并清理原步骤中的零宽字符错误；原图健身球（`dx=+15/+21`）与地面双脚（`dx=+12/+11`）存在不同步平移缩放，暂存待重制。",
        "1403": "待修图 · 已规范为单侧站姿颈部侧屈拉伸并修正 `levator scapulae`／`sternocleidomastoid` 颈侧肌群提示（触发单侧）；原图 F1 `(+17,0)` 对齐后，F2 `(+1,+1)` 下腹肋区虽达 `0.9631` 但双脚仅 `0.9571`（`0,+1` 时则腹肋 `0.9227`），存在 `1 px` 身体侧偏未能所有支点同步 `>= 0.96`，暂存待重制。",
        "1278": "待修图 · 已依实图靠球上斜凳特征补齐 `上斜训练凳` 与 `瑜伽球` 双重必需器械；原图凳脚（`dx=+22/+19, dy=+26`）与双脚在 F1/F2 间异步平移达 `22–26 px` 且右缘哑铃靠近边界，暂存待重制。",
        "1405": "待修图 · 已规范站姿前扣掌展背扩胸拉伸四步要点；原图关键帧顺序混乱（`F0` 与 `F2` 均直立，`F1` 与 `F3` 前含）且第 1 帧头部（`dx=+35`）对双脚（`dx=+11`）平移跨度不一，暂存待重制。",
        "1279": "待修图 · 已补充 `上斜训练凳` 支持并保持单臂计次；原图第 1、2 帧头部偏移 `dx=+15` 而凳右支脚 `dx=+2/+0`（相差 `13–15 px`），暂存待重制。",
        "1407": "待修图 · 已补充 `墙面` 支持并规范单侧扶墙弓步前推小腿拉伸；原图从第 0 帧双足并立切入第 1、2 帧弓步时墙面、手掌与双脚同步位置变化，无法平移配准，暂存待重制。",
        "1280": "待修图 · 已补充 `瑜伽球` 支持并纠正“越过胸部”生硬译文；原图第 2 帧单臂展开哑铃触右缘 `x=479` 裁切，且球体与双脚偏移不一致，暂存待重制。",
        "1418": "待修图 · 已纠正英文原名 typo（`keens -> knees`）及矛盾的“蹲下时抱膝”描述为深蹲起身单腿抱膝贴胸；原图深蹲（F1）与站立单腿抱膝（F2）之间重心足迹大幅偏移旋转，暂存待重制。",
        "1281": "待修图 · 已补充 `上斜训练凳` 支持并规范上斜哑铃单臂推举要点；原图经 F1 `(+15,0)`、F2 `(0,+4)` 配准后长凳与双脚虽重合（`>= 0.9678`），但第 2 帧头部面廓仍发生 `1–2 px` 仰倾偏离（`head_face sc=0.9390, best=0.9457`），暂存待重制。",
    }

    result = {
        "batch": "20261012_review34",
        "version": "1.2.39",
        "version_code": 2026101201,
        "apk_name": "时光屋-1.2.39-第三十四批动作复核.apk",
        "output": "build/review34-20261012",
        "report": "docs/releases/2026-10-12-review-batch34.md",
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
        "batch": "20261012_review34",
        "expected_checks": 16,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20261012_review34")


if __name__ == "__main__":
    main()
