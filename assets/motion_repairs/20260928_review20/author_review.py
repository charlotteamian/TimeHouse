#!/usr/bin/env python3
"""Author Batch 20 (20260928_review20) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["0664", "0372", "0666", "0373", "0668", "0374", "0669", "0375", "0670", "0376"]
    review_candidates = ["0372", "0373", "0376"]

    definition_updates = {
        "0664": {
            "name_zh": "俯卧撑转交替侧伸展",
            "category": "waist",
            "equipment": "body weight",
            "target": "abs",
            "muscle_group": "",
            "secondary_muscles": ["obliques", "pectorals", "delts", "triceps"],
            "movement_patterns_zh": ["水平推", "高位支撑", "核心旋转"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双手略宽于肩踩稳地面进入高撑俯卧撑起始位，核心与臀部收紧使头、背、臀与双脚跟成一条直线。",
                "吸气屈肘有控制地降低胸部接近地面，呼气用力推直双臂回到高撑位。",
                "将重心平稳移至一侧手掌，转髋翻身并把另一侧手臂垂直向上方伸展呈侧面 T 字，保持侧腹发力避免塌腰。",
                "控住片刻后翻转回正双掌撑地再做下一次俯卧撑并交替转向另一侧；每次完成俯卧撑与单侧转体计一次。",
            ],
        },
        "0372": {
            "name_zh": "牧师凳哑铃双臂弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲"],
            "required_equipment_zh": ["牧师凳"],
            "instructions_zh": [
                "坐在牧师凳（斜托凳）上，双脚稳踩地面，胸部贴近斜托垫上沿，双侧上臂后侧平贴斜托垫面、腋窝顶实垫缘。",
                "双手反握（掌心朝前上方）各持一只哑铃垂于斜托垫下方近伸直位置，肘部微留缓冲不完全锁死。",
                "保持上臂全程紧贴斜托垫不动不耸肩，呼气由肱二头肌发力向上弯举哑铃至接近肩前，顶峰挤压短暂停顿。",
                "吸气用两至三秒有控制地缓慢伸肘下放回起始伸展位；每次弯举与慢放还原计一次。",
            ],
        },
        "0666": {
            "name_zh": "单臂前伸俯卧撑",
            "category": "chest",
            "equipment": "body weight",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "delts", "core"],
            "movement_patterns_zh": ["水平推", "高位支撑"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双手略宽于肩撑地进入俯卧撑预备位，收紧核心与臀部，将非支撑侧手臂向前方伸直抬离地面并尽量保持骨盆水平不翻转。",
                "靠支撑侧手臂与胸大肌发力稳定躯干，吸气缓慢屈肘将胸部向地面下方垂直降低。",
                "在底端短暂停顿且悬空手臂全程伸直，避免沉腰或向悬空侧塌斜。",
                "呼气由支撑侧胸大肌、三角肌前束与肱三头肌推起身体回到高支撑伸直位；单侧完成规定次数后换另一侧。",
            ],
        },
        "0373": {
            "name_zh": "平凳坐姿哑铃正握过顶臂屈伸",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "delts"],
            "movement_patterns_zh": ["肘伸展", "过顶伸展"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "端坐在稳固的平板训练凳上，挺胸收紧核心与腰背避免过度反弓，双脚分开稳踩地面。",
                "双手各持一只哑铃以掌心朝前（旋前正握）垂直举过头顶作为起始位，双侧大臂夹紧靠近耳侧且肘尖朝前。",
                "锁定双侧上臂位置固定不动，吸气缓慢屈肘将哑铃向头部后下方降落至前臂充分下探拉伸肱三头肌。",
                "呼气收缩肱三头肌伸直肘关节将哑铃沿原弧线推回过顶锁定位；每次下放与推回计一次。",
            ],
        },
        "0668": {
            "name_zh": "地面仰卧直掌屈膝臀桥",
            "category": "upper legs",
            "equipment": "body weight",
            "target": "glutes",
            "muscle_group": "",
            "secondary_muscles": ["hamstrings", "quads", "lower back"],
            "movement_patterns_zh": ["髋伸展", "髋铰链"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "仰卧在地面或训练垫上，双膝弯曲约90度且双脚踩实地面，双手手臂平放体侧、掌心朝下按住地面辅助稳定。",
                "收紧核心微收骨盆使下背贴近地面，准备由脚跟蹬地发力。",
                "呼气收缩臀大肌与腘绳肌将髋部向上顶起，直至膝、髋与肩呈一条直线并在顶端挤压臀部短暂停顿。",
                "吸气有控制地缓缓下放臀部回到接近地面起始位；每次顶髋与回落计一次。",
            ],
        },
        "0374": {
            "name_zh": "上斜凳俯卧哑铃反握弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲", "俯身稳定"],
            "required_equipment_zh": ["上斜训练凳"],
            "instructions_zh": [
                "将训练凳靠背调至约45度上斜角，俯卧贴靠在上斜凳面上，双脚脚尖稳踩下方地面，双臂自然垂于肩部正下方。",
                "双手正握（掌心朝下/旋前握）各持一只哑铃，使上臂保持垂直地面准备发力。",
                "锁定上臂位置不变，呼气由肱肌、肱二头肌与肱桡肌发力屈肘将哑铃向上弯举至前胸前方并短暂停顿。",
                "吸气有控制地沿原弧线缓慢下放回到垂直悬垂位；每次弯举与还原计一次。",
            ],
        },
        "0669": {
            "name_zh": "站姿单臂胸前斜拉肩后束拉伸",
            "category": "shoulders",
            "equipment": "body weight",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "rhomboids"],
            "movement_patterns_zh": ["水平内收", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽自然站立，收紧核心且肩带下沉不耸肩，保持躯干面向正前方不扭转。",
                "将一侧直臂水平横过胸前伸向对侧肩部，用另一侧手掌轻扣住拉伸侧上臂外侧或肘部前方。",
                "呼气用辅助手缓缓将该直臂向身体内侧与胸口贴近，充分感受三角肌后束与肩胛外侧温和牵伸。",
                "停顿感受拉伸后缓缓放松回位；单侧完成规定次数后换另一侧。",
            ],
        },
        "0375": {
            "name_zh": "平凳仰卧哑铃直臂上拉",
            "category": "chest",
            "equipment": "dumbbell",
            "target": "pectorals",
            "muscle_group": "",
            "secondary_muscles": ["lats", "triceps", "serratus anterior"],
            "movement_patterns_zh": ["过顶伸展", "水平推"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "纵身仰卧在稳固的平板训练凳上，头、上背与臀部贴实凳垫，双脚分开踩实地面，双手叠掌稳托一只哑铃内侧片端垂直举于胸部正上方。",
                "保持双肘微屈固定角度、核心收紧防止下腰过度反弓。",
                "吸气将哑铃以肩关节为轴沿圆弧向头顶后下方缓慢下放，直到大臂与躯干呈一条线或略低于凳面，感受胸大肌与背阔肌充分拉伸。",
                "呼气由胸大肌、前锯肌与背阔肌协同发力，沿原弧线将哑铃拉回胸部正上方起始位；每次下放与上拉计一次。",
            ],
        },
        "0670": {
            "name_zh": "正握颈后引体向上",
            "category": "back",
            "equipment": "body weight",
            "target": "lats",
            "muscle_group": "",
            "secondary_muscles": ["upper back", "biceps", "forearms"],
            "movement_patterns_zh": ["垂直拉"],
            "required_equipment_zh": ["单杠"],
            "instructions_zh": [
                "双手明显宽于肩以正握（掌心朝前）抓牢高位单杠，全身直臂悬垂并微交叠小腿收紧核心。",
                "先完成肩带下沉，保持头部微微前低为后颈过杠留出空间，避免猛甩身体借力。",
                "呼气由背阔肌与大圆肌、中上背部发力将身体垂直向上拉起，引导横杠经过后脑勺下方接近颈后上背高度并短暂停顿。",
                "吸气有控制地缓缓伸直双臂还原至起始悬垂位；每次拉起与还原计一次。",
            ],
        },
        "0376": {
            "name_zh": "哑铃双臂侧平举",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "rhomboids"],
            "movement_patterns_zh": ["外展", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽站立，收紧核心与臀部维持脊柱中立，双手掌心朝内各持一只哑铃自然垂于大腿外侧。",
                "保持肩带下沉不耸肩、肘关节微屈锁定轻微角度（约15度）。",
                "呼气由三角肌中束发力带动双臂同时向身体两侧平举，直到上臂与地面大致平行，手肘高度不低于手腕。",
                "在水平顶点短暂停顿感受肩中束收缩后，吸气有控制地缓慢下放回大腿两侧起始位；每次平举与下放计一次。",
            ],
        },
    }

    sources = {
        "0372": "https://exrx.net/WeightExercises/Biceps/DBPreacherCurl",
        "0373": "https://exrx.net/WeightExercises/Triceps/DBTriExt",
        "0376": "https://exrx.net/WeightExercises/DeltoidLateral/DBLateralRaise",
    }

    review_notes = {
        "0372": "纠正原英译中重大误译（dumbbell preacher curl 实为坐在斜托牧师凳上做弯举，原误译成“哑铃仰卧弯举”）为“牧师凳哑铃双臂弯举”，并补齐牧师凳必需支撑器械；原四帧经整数平移（F1 +1,0）配准后牧师凳前后支架及双脚残差 0.0 px（匹配分 ≥ 0.9687）。",
        "0373": "将原直译“哑铃旋前握三头肌伸展”规范为“平凳坐姿哑铃正握过顶臂屈伸”，补齐平板训练凳与过顶伸展负荷标签；原四帧经整数平移（F1 +9,0；F2 0,+9）配准后平凳与双脚支点残差 ≤ 1.0 px（匹配分 ≥ 0.9771）。",
        "0376": "核对“哑铃双臂侧平举”外展轨迹与三角肌、斜方肌、菱形肌联动及站姿稳定下背低负荷标签；原四帧经清白对齐后双侧下肢小腿、双脚、头胸及髋部四锚点残差 0.0 px（匹配分 ≥ 0.9702）。",
    }

    pending = {
        "0664": "待修图 · 已纠正为俯卧撑转交替侧伸展（避免触发静态计时词库“侧平板／侧桥”及单侧翻倍计次关键词）；原图手掌及双脚支撑点在俯卧与侧转帧存在 15–50 px 独立漂移，暂存待重制。",
        "0666": "待修图 · 已规范为单臂前伸俯卧撑；原图仅有上支撑与底姿两帧交替重复（F2 相对 F0 仅整图上移 20 px，缺少半程过渡姿势），暂存待重制。",
        "0668": "待修图 · 已将“后倾桥”规范为地面仰卧直掌屈膝臀桥并核对步骤；原图第 3 帧顶髋时头肩（dx=-4）与双脚小腿（dx=+10）水平缩放错位 14 px 且高度缩放明显，暂存待重制。",
        "0374": "待修图 · 已纠正为上斜凳俯卧哑铃反握弯举（掌心朝下）并补齐上斜训练凳与俯身稳定标签；原图第 1 帧脚尖贴边截断且第 2、3 帧脚底位置与上身斜凳倾角存在约 4 px 独立偏移与头部贴边缩放，暂存待重制。",
        "0669": "待修图 · 已规范为站姿单臂胸前斜拉肩后束拉伸（单侧计次）并补站姿稳定下背低负荷标签；原图第 3 帧头部（dy=-3）相对双脚（dy=-7）存在约 4 px 纵向身高压缩，暂存待重制。",
        "0375": "待修图 · 已将原错译“哑铃拉下推”纠正为标准名“平凳仰卧哑铃直臂上拉”（dumbbell pullover）并补齐平板训练凳支撑；原图第 3 帧下放哑铃时凳头左端（dx=+21）与凳尾右端（dx=+8）发生约 13 px 独立缩放错位，暂存待重制。",
        "0670": "待修图 · 已纠正为正握颈后引体向上并补齐单杠支撑；原图第 2 帧架体宽度相对第 1 帧缩窄约 45 px 且第 3 帧架顶横梁与底座发生 9 px 纵向压缩，暂存待重制。",
    }

    result = {
        "batch": "20260928_review20",
        "version": "1.2.25",
        "version_code": 2026092801,
        "apk_name": "时光屋-1.2.25-第二十批动作复核.apk",
        "output": "build/review20-20260928",
        "report": "docs/releases/2026-09-28-review-batch20.md",
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
        "batch": "20260928_review20",
        "expected_checks": 16,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20260928_review20")


if __name__ == "__main__":
    main()
