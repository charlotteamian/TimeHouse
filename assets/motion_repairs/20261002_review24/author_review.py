#!/usr/bin/env python3
"""Author Batch 24 (20261002_review24) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["0709", "0393", "0716", "0394", "0717", "0395", "0720", "0396", "0721", "0397"]
    review_candidates = ["0709", "0394", "0721", "0397"]

    definition_updates = {
        "0709": {
            "name_zh": "双杠直臂侧摆抬腿",
            "category": "waist",
            "equipment": "body weight",
            "target": "abs",
            "muscle_group": "",
            "secondary_muscles": ["obliques", "hip flexors", "shoulders"],
            "movement_patterns_zh": ["核心侧屈", "高位支撑"],
            "required_equipment_zh": ["双杠"],
            "instructions_zh": [
                "站于稳固双杠之间，双手紧握平行杠面向上撑直双臂使身体悬空，肩带下沉远离双耳、双腿并拢伸直向下。",
                "收紧核心与下腹稳定上身不前后晃动。",
                "呼气收缩一侧腹内外斜肌与下腹，带动并拢双腿顺势向该侧斜上方弧线抬高。",
                "在侧抬高点短暂停顿后，吸气有控制地缓缓下放回垂悬起始位并向另一侧交替完成；每次抬腿与回落计一次。",
            ],
        },
        "0393": {
            "name_zh": "平凳坐姿哑铃内侧弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "坐在平板训练凳边缘、双腿分开踩稳地面，双手反握（掌心朝上）各持一只哑铃垂于大腿内侧之间，肘背轻靠大腿内侧稳定大臂。",
                "保持腰背挺直并略微前倾使前臂自然垂悬。",
                "呼气锁定上臂位置不动，由肱二头肌短头主导向上弯举哑铃至接近胸前高度。",
                "在顶峰短暂挤压后，吸气有控制地缓慢伸肘下放回起始位；每次弯举与还原计一次。",
            ],
        },
        "0716": {
            "name_zh": "站姿单手侧扳颈部拉伸",
            "category": "neck",
            "equipment": "body weight",
            "target": "levator scapulae",
            "muscle_group": "",
            "secondary_muscles": ["traps", "sternocleidomastoid"],
            "movement_patterns_zh": ["拉伸", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽自然直立，下沉双侧肩带且放松未牵拉侧手臂自然垂于体侧，目视正前方。",
                "将头缓慢向一侧倾斜靠近同侧肩部，保持躯干直立不耸肩侧弯。",
                "举起同侧手掌绕过头顶轻放于对侧颞部上方，用极轻柔渐进的重力辅压增强肩颈外侧牵伸感（切忌猛拉）。",
                "温和牵伸后缓缓松手回正头部；完成单侧规定次数或时长后换另一侧。",
            ],
        },
        "0394": {
            "name_zh": "平凳坐姿俯身哑铃后屈伸",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["delts", "forearms"],
            "movement_patterns_zh": ["肘伸展", "俯身稳定"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "坐在平板训练凳一端，双脚踩稳地面并收紧核心，屈髋前倾上身至胸部靠近大腿上方且腰背保持平直。",
                "双手掌心相对各持一只哑铃，将双侧上臂向上提拉夹紧体侧至大致与地面平行、屈肘成90度作为起始位。",
                "保持上臂与肩胛完全固定不上下摆动，呼气由肱三头肌发力以肘为轴向后上方伸直前臂至全臂呈直线。",
                "在后端顶峰夹紧停顿后，吸气有控制地屈肘还原至90度垂悬起始位；每次后伸与还原计一次。",
            ],
        },
        "0717": {
            "name_zh": "单臂撑起侧卧三头屈伸",
            "category": "upper arms",
            "equipment": "body weight",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["shoulders", "chest", "core"],
            "movement_patterns_zh": ["推", "伸肘"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "侧卧在训练垫上，双腿并拢伸直，上侧手掌平按在下方肩前地面、手肘弯曲贴身，下侧臂抱于胸腰前。",
                "收紧核心与臀腿，保持身体从肩到脚呈一条完整斜直线。",
                "呼气由上侧肱三头肌主导出发用力推压地面撑起上半身离垫，直到该侧支撑臂接近伸直并可自然上展下肢侧躯干稳住重心。",
                "吸气缓慢屈肘有控制地下放体侧回到垫面起始位；单侧完成规定次数后换另一侧。",
            ],
        },
        "0395": {
            "name_zh": "直立靠背凳坐姿哑铃侧平举",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "triceps"],
            "movement_patterns_zh": ["外展"],
            "required_equipment_zh": ["直立靠背训练凳"],
            "instructions_zh": [
                "坐在稳固的直立靠背训练凳上，背部稳靠竖直靠背、双脚稳踩地面，双手掌心朝内各持一只哑铃置于体侧大腿外方。",
                "保持肩带下沉不耸肩且双肘微屈锁住轻微角度。",
                "呼气由三角肌中束发力带动双臂同时向两侧弧线平举至大致与地面平行。",
                "在水平顶点短暂停顿感受中束收缩后，吸气缓慢有控制地下放回体侧；每次平举与下放计一次。",
            ],
        },
        "0720": {
            "name_zh": "单杠左右交替拉起引体向上",
            "category": "back",
            "equipment": "body weight",
            "target": "lats",
            "muscle_group": "",
            "secondary_muscles": ["biceps", "forearms", "upper back"],
            "movement_patterns_zh": ["垂直拉"],
            "required_equipment_zh": ["单杠"],
            "instructions_zh": [
                "双手宽于肩正握抓稳高位单杠，双臂伸直悬垂并收紧核心使下肢稳住不晃动。",
                "启动背阔肌发力向上拉起身体，同时控制上身略向左侧平移靠近左手侧杠位使下颌高过横杠。",
                "在顶端短暂稳住后缓慢伸肘下降回到正中垂直悬垂位。",
                "紧接着下一次上拉转向右侧靠近右手手位并左右交替进行；每次完整拉起与还原计一次。",
            ],
        },
        "0396": {
            "name_zh": "平凳坐姿哑铃双臂侧平举",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "upper back"],
            "movement_patterns_zh": ["外展"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "端坐在稳固的平板训练凳上，双脚分开稳踩地面、挺胸收紧核心维持脊柱直立，双手掌心朝内各持一只哑铃垂于体侧。",
                "双肘微屈锁住约15度弧角、双肩下沉。",
                "呼气由三角肌中束发力带动双臂同时向身体两侧平举抬至与肩同高。",
                "顶端停顿一瞬后吸气有控制地缓缓下放回大腿外侧；每次抬举与还原计一次。",
            ],
        },
        "0721": {
            "name_zh": "站姿单臂水平牵腕拉伸",
            "category": "lower arms",
            "equipment": "body weight",
            "target": "forearms",
            "muscle_group": "",
            "secondary_muscles": ["wrists", "hands"],
            "movement_patterns_zh": ["拉伸", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽自然直立，肩带下沉放松，将待拉伸侧直臂平举展开后横引至胸前水平高度、手掌掌心朝下、腕部自然下屈。",
                "另一侧手绕到前侧轻握该侧垂腕手背或前臂末端，保持待拉伸臂肩膀不耸起。",
                "呼气用辅助手温柔加压将腕背向躯干侧牵引，感受前臂外侧肌群与腕伸肌温和舒张拉伸，避免暴力压腕。",
                "停顿感受牵伸后缓缓松回起始平伸位；单侧完成规定次数后换另一侧。",
            ],
        },
        "0397": {
            "name_zh": "坐姿扶腿哑铃中立握腕弯举",
            "category": "lower arms",
            "equipment": "dumbbell",
            "target": "forearms",
            "muscle_group": "",
            "secondary_muscles": ["brachioradialis", "wrist flexors", "wrist extensors"],
            "movement_patterns_zh": ["腕屈伸"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "坐在稳固的平板训练凳边沿，双脚稳踩地面、上身微前倾，将双侧前臂平稳贴靠在两侧大腿上方使手腕悬出膝前。",
                "双手采用对握/中立握法（掌心相对、大拇指朝上方）各持一只哑铃自然垂向膝前下方。",
                "保持前臂与手肘全程贴实大腿稳定不动，呼气由前臂桡侧与屈伸肌群发力仅活动腕关节向上勾举哑铃。",
                "在腕部上屈顶端停顿挤压前臂后，吸气缓慢有控制地放回垂直伸展位；每次屈腕与回落计一次。",
            ],
        },
    }

    sources = {
        "0709": "https://exrx.net/WeightExercises/Obliques/BWHangingTwistingLegHipRaise",
        "0394": "https://exrx.net/WeightExercises/Triceps/DBKickback",
        "0721": "https://www.rehabhero.ca/exercise",
        "0397": "https://exrx.net/WeightExercises/WristFlexors/DBWristCurl",
    }

    review_notes = {
        "0709": "纠正原直译“平行杠侧臀”为“双杠直臂侧摆抬腿”（避开静态触发词“支撑”并补齐双杠与高位支撑/核心侧屈标签）；原四帧清白对齐后左右双杠支柱及头肩三锚点残差 ≤ 1.0 px（匹配分 ≥ 0.9810）。",
        "0394": "将原误译“哑铃坐姿后推”规范为“平凳坐姿俯身哑铃后屈伸”，补齐平板训练凳与俯身稳定标签；原四帧经第 2 帧微移 `(0, +3)` 配准后平凳左脚、双脚与头躯干三锚点残差 0.0 px（匹配分 ≥ 0.9770）。",
        "0721": "规范“站姿单臂水平牵腕拉伸”（单侧计次）并核对前臂腕伸肌群高亮、步骤与站姿稳定标签；原四帧经整数平移（`F1 +7,0`、`F2 0,+3`）配准后双脚小腿、髋躯干及头面四锚点残差 ≤ 1.41 px（匹配分 ≥ 0.9817）。",
        "0397": "纠正原上游严重误分类与步骤（原被误设为 `upper arms / biceps` 并误写“弯向肩膀”，实为前臂扶腿中立握腕弯举）为 `lower arms / forearms`、“坐姿扶腿哑铃中立握腕弯举”并补齐平板训练凳；原四帧经第 1 帧平移 `(+20, 0)` 配准后平凳左右支腿、双脚及头躯干四锚点残差 ≤ 1.0 px（匹配分 ≥ 0.9803）。",
    }

    pending = {
        "0393": "待修图 · 已规范为平凳坐姿哑铃内侧弯举并补齐平板训练凳；原图第 1、2 帧弯举时头部相对座椅及双脚发生 2–4 px 纵向压低错位且双大腿前移，暂存待重制。",
        "0716": "待修图 · 已规范为站姿单手侧扳颈部拉伸（单侧计次）；原图第 1、2 帧落地右臂与躯干相对双脚分别存在 2.24 px 与 3.61 px（匹配分 0.9292）分离错位，暂存待重制。",
        "0717": "待修图 · 已将“侧推俯卧撑”规范为单臂撑起侧卧三头屈伸；原图第 1、2 帧支撑手掌与并拢双脚存在明显跨帧滑移（lower_sad 22.41 / 27.05），暂存待重制。",
        "0395": "待修图 · 已规范为直立靠背凳坐姿哑铃侧平举并补齐直立靠背训练凳；原图第 1、2 帧双脚对齐后直立靠背与头冠左缘均出现约 2–3 px 横向左偏，暂存待重制。",
        "0720": "待修图 · 已纠正原误译“侧头下巴”为单杠左右交替拉起引体向上并补齐单杠；原图第 1、2 帧龙门架立柱与顶杠分别发生约 10–17 px 横向与纵向跳移，暂存待重制。",
        "0396": "待修图 · 已规范为平凳坐姿哑铃双臂侧平举并补齐平板训练凳；原图第 2 帧头顶触顶边缘且相对双脚出现约 4 px 纵向身高差，第 1 帧平凳支腿位移，暂存待重制。",
    }

    result = {
        "batch": "20261002_review24",
        "version": "1.2.29",
        "version_code": 2026100201,
        "apk_name": "时光屋-1.2.29-第二十四批动作复核.apk",
        "output": "build/review24-20261002",
        "report": "docs/releases/2026-10-02-review-batch24.md",
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
        "batch": "20261002_review24",
        "expected_checks": 19,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20261002_review24")


if __name__ == "__main__":
    main()
