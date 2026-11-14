#!/usr/bin/env python3
"""Author Batch 22 (20260930_review22) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["0685", "0382", "0687", "0384", "0688", "0385", "0689", "0386", "0690", "0387"]
    review_candidates = ["0385", "0387"]

    definition_updates = {
        "0685": {
            "name_zh": "原地高抬腿跑",
            "category": "cardio",
            "equipment": "body weight",
            "target": "cardiovascular system",
            "muscle_group": "",
            "secondary_muscles": ["quadriceps", "hamstrings", "calves", "glutes"],
            "movement_patterns_zh": ["有氧", "跑跳"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与髋同宽自然直立，核心收紧、肩部放松，双肘微屈置于体侧准备摆臂。",
                "由单脚前掌蹬地稳定重心，另一侧屈膝屈髋将大腿主动向上高抬接近与地面平行，同时对侧手臂顺势向前上方自然摆起。",
                "随后有节奏地快速交替落脚与抬腿，保持躯干挺直不后仰且落地轻盈有弹性。",
                "全程维持平稳均匀呼吸按预定时间或次数完成练习。",
            ],
        },
        "0382": {
            "name_zh": "站姿哑铃反握弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽站立、收紧核心与臀部，双手正手反式握法（掌心朝向大腿后侧与地面）各持一只哑铃自然垂于体前外侧。",
                "将双侧上臂夹紧贴近体侧，手腕保持中立挺直不向后折腕。",
                "呼气保持大臂固定不动，由肱桡肌、肱肌与肱二头肌发力向上屈肘弯举哑铃至胸肩高度前方。",
                "在顶端短暂停顿收缩后，吸气缓慢伸肘下放回起始伸展位；每次弯举与还原计一次。",
            ],
        },
        "0687": {
            "name_zh": "坐姿屈膝俄罗斯转体",
            "category": "waist",
            "equipment": "body weight",
            "target": "abs",
            "muscle_group": "",
            "secondary_muscles": ["obliques", "core", "hip flexors"],
            "movement_patterns_zh": ["核心旋转", "核心稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "屈膝坐于地面或训练垫上，双脚脚跟稳踩地面，核心收紧使脊柱保持延伸平直并向后微仰约四十五度。",
                "双手于胸前轻握或合掌，保持肩带下沉不圆背，骨盆与下肢尽量稳定不晃动。",
                "呼气由腹内外斜肌发力带动上背与肩胸整块向一侧水平扭转，视线随双手自然跟随。",
                "吸气转回正中再向另一侧扭转，左右交替有控制地完成预定次数。",
            ],
        },
        "0384": {
            "name_zh": "牧师凳哑铃反握弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲"],
            "required_equipment_zh": ["牧师凳"],
            "instructions_zh": [
                "坐在牧师凳（斜托凳）上，胸部轻贴斜托垫上沿，双侧上臂后侧平贴斜托垫面、双脚稳踩地面。",
                "双手采用旋前正手反式握（掌心朝下、指节朝前上方）各持一只哑铃垂于斜托垫下方，手腕保持中立不塌腕。",
                "锁定上臂全程紧贴斜托垫不借力晃肩，呼气由前臂屈肌、肱肌与肱二头肌协同向上弯举哑铃至接近肩前。",
                "在顶峰短暂停顿后，吸气缓慢有控制地伸肘下放回底端；每次弯举与慢放计一次。",
            ],
        },
        "0688": {
            "name_zh": "直臂肩胛引体向上",
            "category": "back",
            "equipment": "body weight",
            "target": "traps",
            "muscle_group": "",
            "secondary_muscles": ["lats", "rhomboids", "rear delts", "forearms"],
            "movement_patterns_zh": ["垂直拉"],
            "required_equipment_zh": ["单杠"],
            "instructions_zh": [
                "双手略宽于肩以正握抓稳高位单杠，全身直臂放松悬垂，小腿微交叠收紧核心避免晃动。",
                "保持双肘全程几乎伸直不弯折，注意力集中在两侧肩胛骨位置。",
                "呼气主动向下压沉并微向脊柱中线内收肩胛骨，让身体小幅度整体向上抬升数厘米、远离双耳。",
                "在顶峰稳定控住一至两秒感受中下斜方肌发力，吸气缓慢放松肩胛回到充分悬垂位；每次下沉肩胛与还原计一次。",
            ],
        },
        "0385": {
            "name_zh": "坐姿扶腿哑铃反握腕弯举",
            "category": "lower arms",
            "equipment": "dumbbell",
            "target": "forearms",
            "muscle_group": "",
            "secondary_muscles": ["wrist extensors", "brachialis"],
            "movement_patterns_zh": ["腕屈伸"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "坐在稳固的平板训练凳边沿，双脚平踏地面、核心微收保持躯干稳定，双手采用旋前握法（掌心朝下）各持一只哑铃。",
                "将双侧前臂平稳贴放在大腿上方，使双腕与手背悬伸于膝盖前缘正前方。",
                "保持前臂与手肘全程贴实大腿不动，呼气由前臂伸肌主导向上伸腕抬起手背与哑铃。",
                "在顶端充分感受前臂外侧紧缩并短暂停顿后，吸气有控制地缓缓下垂回腕部伸展低位；每次抬腕与下放计一次。",
            ],
        },
        "0689": {
            "name_zh": "平凳坐姿直腿抬腿",
            "category": "waist",
            "equipment": "body weight",
            "target": "abs",
            "muscle_group": "",
            "secondary_muscles": ["hip flexors", "quadriceps"],
            "movement_patterns_zh": ["核心", "屈髋抬腿"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "坐在平板训练凳前端一侧，双手在臀部两侧抓紧凳面边缘稳定躯干，双脚轻踩或微悬于地面前下方，微屈双膝或伸直双腿。",
                "微收骨盆并略微后倾保持核心绷紧，避免腰椎过度塌陷或耸肩借力。",
                "呼气由下腹肌与髋屈肌发力，保持双腿伸直缓慢向上平举抬高至接近与凳面平行。",
                "在顶峰短暂停顿后，吸气缓慢有控制地下放双腿回到接近地面起始位；每次抬腿与下放计一次。",
            ],
        },
        "0386": {
            "name_zh": "俯身哑铃旋腕后束飞鸟",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "rhomboids"],
            "movement_patterns_zh": ["水平外展", "俯身稳定", "髋铰链"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽站立并微屈膝，屈髋俯身保持腰背平直，双手对握（掌心相对）各持一只哑铃自然下垂于肩下方。",
                "保持肘关节微屈固定角度且肩带下沉不耸肩。",
                "呼气由三角肌后束发力向身体两侧横向外展抬起双臂，在抬升接近水平位置时顺势微旋前臂使掌心朝向后下方或地面。",
                "在顶峰短暂停顿感受肩后束收紧后，吸气反向旋回对握位缓慢放回起始垂悬位置；每次展开与下放计一次。",
            ],
        },
        "0690": {
            "name_zh": "座椅俯身下背拉伸",
            "category": "back",
            "equipment": "body weight",
            "target": "lats",
            "muscle_group": "",
            "secondary_muscles": ["lower back", "glutes", "hamstrings"],
            "movement_patterns_zh": ["拉伸", "髋铰链"],
            "required_equipment_zh": ["直立靠背训练凳"],
            "instructions_zh": [
                "端坐在稳固的直立靠背训练凳或座椅上，双脚分开平踩地面，保持腰背自然延伸、双肩下沉。",
                "吸气准备后，呼气沿着脊柱与髋关节缓缓向前低头拱背伏贴向双腿上方，双臂顺势向下自然垂落或轻触小腿外侧。",
                "在感受中下背部与竖脊肌温和牵伸舒适的位置短暂停顿呼吸，勿强行用力下压以免腰椎不适。",
                "吸气收紧核心逐节起身还原回端正坐姿；每次俯身牵伸与回位计一次。",
            ],
        },
        "0387": {
            "name_zh": "平凳坐姿哑铃交替前平举",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "pectorals"],
            "movement_patterns_zh": ["肩屈曲"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "端坐在稳固的平板训练凳上，双脚分开稳踩地面、挺胸收腹保持躯干直立不后仰，双手掌心朝内各持一只哑铃自然垂于大腿外侧。",
                "保持非训练侧手臂垂放稳住哑铃，训练侧手肘微屈锁定轻微角度、肩带下沉不耸肩。",
                "呼气由三角肌前束主导将一侧哑铃沿身体前方弧线平举抬高至与肩同高（手臂大致平行地面）。",
                "在顶点短暂停顿后缓慢有控制地放回大腿外侧，随后换另一侧手臂交替上举（图示演示单侧上举轨迹，实际练习左右交替计次）。",
            ],
        },
    }

    sources = {
        "0385": "https://exrx.net/WeightExercises/WristExtensors/DBReverseWristCurl",
        "0387": "https://www.strengthlog.com/dumbbell-front-raise/",
    }

    review_notes = {
        "0385": "核对“坐姿扶腿哑铃反握腕弯举”旋前正手掌心朝下伸腕轨迹与前臂伸肌／肱桡肌目标肌群，补齐平板训练凳必需支撑器械；原四帧经第 2 帧微移 `(0, +1)` 配准后平凳左右支腿、双脚及头部四锚点残差 ≤ 1.41 px（匹配分 ≥ 0.9787）。",
        "0387": "核对“平凳坐姿哑铃交替前平举”前举轨迹、非工作侧悬垂保持、三角肌前束主目标及斜方肌／胸肌联动，补齐平板训练凳支撑与不后仰左右交替说明；原四帧经第 2 帧 `(0, +1)` 配准后平凳左支腿、双脚、静止右臂及头冠四锚点残差 ≤ 1.0 px（匹配分 ≥ 0.9638）。",
    }

    pending = {
        "0685": "待修图 · 已规范为原地高抬腿跑（与跑步机动作 0684 明确区分）并补齐有氧／跑跳标签；原图第 1、2 帧高抬腿时头部相对支撑脚底发生 6–10 px 纵向身高及躯干比例错位，暂存待重制。",
        "0382": "待修图 · 已规范为站姿哑铃反握弯举并补齐站姿稳定下背低负荷标签；原图第 2 帧顶峰弯举时双脚不动而头部相对脚底向下收缩约 8–10 px（height=452 vs 462），暂存待重制。",
        "0687": "待修图 · 已核对坐姿屈膝俄罗斯转体动作要点（按图谱纠正为脚跟踩地而非抬离地面）；原图第 1、2 帧仅为同侧相似姿势缺少左右对称反向转体且髋臀与头肩比例偏差 8–12 px，暂存待重制。",
        "0384": "待修图 · 已纠正原步骤与英语名称矛盾（reverse curl 为掌心朝下旋前握而非原误写“掌心朝上”）并补齐牧师凳必需支撑；原图第 2 帧牧师凳配准后头部相对凳面出现约 4–5 px 纵向压低错位（匹配分 0.8746），暂存待重制。",
        "0688": "待修图 · 已规范为直臂肩胛引体向上（避开静态计时词“悬垂”）并补齐单杠支撑；原图第 1 帧头部与髋部反而下掉约 6 px，第 2 帧屈肘近 90° 做成了完整引体向上而非直臂肩胛下沉，动作示范有误，暂存待重制。",
        "0689": "待修图 · 已规范为平凳坐姿直腿抬腿并补齐平板训练凳支撑与核心负荷标签；原图第 2 帧平凳右支腿相对第 0 帧水平缩窄约 15 px 且头胸存在独立偏移，暂存待重制。",
        "0386": "待修图 · 已规范为俯身哑铃旋腕后束飞鸟并补齐俯身稳定／髋铰链下背负荷；原图第 2 帧右侧哑铃触及右边缘 x=479 且头部与前胫骨相对双脚存在 4–5 px 独立偏移，暂存待重制。",
        "0690": "待修图 · 已规范为座椅俯身下背拉伸并补齐直立靠背训练凳支撑；原图第 2 帧俯身屈曲时靠背椅椅背与前后椅腿发生约 12 px 水平宽度缩放错位，暂存待重制。",
    }

    result = {
        "batch": "20260930_review22",
        "version": "1.2.27",
        "version_code": 2026093001,
        "apk_name": "时光屋-1.2.27-第二十二批动作复核.apk",
        "output": "build/review22-20260930",
        "report": "docs/releases/2026-09-30-review-batch22.md",
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
        "batch": "20260930_review22",
        "expected_checks": 13,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20260930_review22")


if __name__ == "__main__":
    main()
