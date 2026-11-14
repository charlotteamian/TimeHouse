#!/usr/bin/env python3
"""Author Batch 16 (20260924_review16) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["0513", "0351", "0514", "0352", "0555", "0353", "0558", "0354", "0570", "0355"]
    review_candidates = ["0351", "0352", "0353", "0354", "0570", "0355"]

    definition_updates = {
        "0513": {
            "name_zh": "跳跃深蹲（第二式）",
            "category": "upper legs",
            "equipment": "body weight",
            "target": "glutes",
            "muscle_group": "",
            "secondary_muscles": ["quads", "hamstrings", "calves"],
            "movement_patterns_zh": ["下肢推", "爆发力"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚略宽于肩站立，脚尖微朝外，收紧核心与背部保持脊柱中立。",
                "吸气屈髋屈膝下蹲至大腿至少与地面平行，双臂自然在身前维持平衡。",
                "呼气由臀大肌、股四头肌与小腿协同爆发蹬地，垂直向上跳起并充分伸展髋、膝与踝关节。",
                "前脚掌轻柔落地并顺势屈膝缓冲回落至深蹲姿势；每次深蹲跳起与缓冲落地计一次。",
            ],
        },
        "0351": {
            "name_zh": "哑铃仰卧双臂屈伸",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["delts", "forearms"],
            "movement_patterns_zh": ["肘伸展", "过顶伸展"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "仰卧在稳固的平板训练凳上，头、上背与臀部贴实凳面，双脚平踩地面，双手掌心相对各持一只哑铃垂直举于肩部正上方。",
                "固定上臂位置贴近头部两侧不前后晃动，吸气缓慢屈肘将哑铃向头部后上方弧线下放。",
                "下放至前臂越过水平位、哑铃位于头部后侧且肱三头肌充分拉伸时短暂停顿。",
                "呼气收缩肱三头肌伸肘将哑铃沿原弧线推回肩部正上方起始位；每次屈肘下放与伸肘推回计一次。",
            ],
        },
        "0514": {
            "name_zh": "跳跃深蹲",
            "category": "upper legs",
            "equipment": "body weight",
            "target": "glutes",
            "muscle_group": "",
            "secondary_muscles": ["quads", "hamstrings", "calves"],
            "movement_patterns_zh": ["下肢推", "爆发力"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽站立，挺胸收腹，双手虚握或于胸前保持平衡。",
                "吸气屈髋屈膝向后下方蹲至大腿接近或低于与地面平行，保持膝盖与脚尖方向一致。",
                "呼气下肢爆发发力垂直向上跳离地面，髋、膝与踝充分伸直并控制空中姿态。",
                "以柔和的前脚掌着地顺势屈膝缓冲回到深蹲位衔接下一次；每次下蹲、腾空与缓冲计一次。",
            ],
        },
        "0352": {
            "name_zh": "哑铃仰卧对握窄推",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["pectorals", "delts"],
            "movement_patterns_zh": ["水平推"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "仰卧在稳固的平板训练凳上，肩胛骨收紧下沉贴实凳面，双脚踩稳地面，双手以掌心相对的对握紧贴持哑铃停于胸部上方。",
                "双肘保持贴近躯干两侧向后下方滑动，吸气有控制地将哑铃缓慢下放至靠近中下胸上方。",
                "在底端短暂停顿，感受肱三头肌与胸肌协同承重，保持前臂基本垂直地面。",
                "呼气由肱三头肌与胸大肌发力将哑铃垂直向上推至双臂伸直锁定；每次下放与推起计一次。",
            ],
        },
        "0555": {
            "name_zh": "平凳坐姿前踢腿",
            "category": "upper legs",
            "equipment": "body weight",
            "target": "quads",
            "muscle_group": "",
            "secondary_muscles": ["hip flexors", "abs"],
            "movement_patterns_zh": ["下肢推", "核心稳定"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "坐在稳固的平板训练凳前端边缘，双膝弯曲约90度且双脚踩实地面，双手抓紧身体两侧凳边固定躯干。",
                "保持核心收紧且上身微微后倾维持平衡，准备抬腿。",
                "呼气由股四头肌与髋屈肌协同发力向前方抬起并伸直双腿至与地面大致平行，在顶端短暂停顿。",
                "吸气有控制地屈膝缓慢放回双脚踩地起始位；每次伸膝前踢与收回计一次。",
            ],
        },
        "0353": {
            "name_zh": "健身球哑铃单臂集中弯举",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "biceps",
            "muscle_group": "",
            "secondary_muscles": ["forearms", "brachialis"],
            "movement_patterns_zh": ["肘屈曲"],
            "required_equipment_zh": ["瑜伽球"],
            "instructions_zh": [
                "坐在稳固充气的瑜伽球上，双腿大步分开且双脚全掌稳踩地面，上身略微前倾，非训练手扶住对侧大腿保持躯干稳定。",
                "训练手正握（掌心朝前）持一只哑铃自然垂向地面，并将该侧上臂后侧贴靠在同侧大腿内侧作为固定支点。",
                "保持肩部与上臂贴稳大腿内侧不借力甩动，呼气由肱二头肌发力向上弯举哑铃至接近同侧肩前并短暂停顿顶峰收缩。",
                "吸气有控制地缓慢伸肘将哑铃沿原弧线下放至接近伸直位；单侧完成规定次数后换另一侧。",
            ],
        },
        "0558": {
            "name_zh": "摆荡借力双力臂",
            "category": "back",
            "equipment": "body weight",
            "target": "lats",
            "muscle_group": "",
            "secondary_muscles": ["upper back", "pectorals", "triceps", "biceps", "delts", "core"],
            "movement_patterns_zh": ["垂直拉", "高位支撑"],
            "required_equipment_zh": ["单杠"],
            "instructions_zh": [
                "正握抓牢高位单杠，双手略宽于肩，全身伸直悬垂并收紧肩胛带动核心稳定。",
                "通过核心前后流畅的空心-反弓摆荡产生向上与向后的摆动动量。",
                "随身体向后上方摆起瞬间爆发力拉动髋部与胸部靠近横杠，顺势翻转手腕与双肘切入杠上支点位置。",
                "紧接由肱三头肌与胸肌推直双臂完成杠上锁臂，再控制身体屈肘落回直臂悬垂位；每次完整拉起推撑与落回计一次。",
            ],
        },
        "0354": {
            "name_zh": "哑铃俯身单臂后屈伸",
            "category": "upper arms",
            "equipment": "dumbbell",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["delts", "forearms"],
            "movement_patterns_zh": ["肘伸展", "俯身稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽站立、双膝微屈，保持腰背平直屈髋俯身至上身接近水平，非训练手撑稳同侧大腿前方维持平衡。",
                "训练手持哑铃掌心朝内，抬起该侧大臂贴近躯干并固定至与地面平行，前臂自然垂直下垂约成90度作为起始位。",
                "保持大臂完全静止不上下摆动，呼气由肱三头肌发力以肘关节为轴向后上方伸直前臂，在顶端夹紧短暂停顿。",
                "吸气有控制地屈肘将哑铃缓慢还原至90度悬垂起始位；单侧完成规定次数后换另一侧。",
            ],
        },
        "0570": {
            "name_zh": "平凳坐姿收腿",
            "category": "waist",
            "equipment": "body weight",
            "target": "abs",
            "muscle_group": "",
            "secondary_muscles": ["hip flexors"],
            "movement_patterns_zh": ["核心稳定"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "坐在稳固的平板训练凳前缘，双手抓牢臀部两侧凳边，上身略微向后倾，双腿并拢伸直悬空于身前。",
                "收紧下腹部保持骨盆与凳面接触稳定，避免利用腰部前后剧烈摆动借力。",
                "呼气由腹直肌与髋屈肌发力屈膝屈髋，将双膝向胸部方向收紧拉近，在最高点短暂停顿。",
                "吸气有控制地缓缓伸展双腿还原至身前伸直悬空位；每次收腿与伸展计一次。",
            ],
        },
        "0355": {
            "name_zh": "哑铃单臂侧平举",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["traps", "forearms"],
            "movement_patterns_zh": ["外展", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽自然站立，核心与臀部微收维持躯干直立不向负重侧歪斜，训练手掌心朝内持哑铃自然垂于体侧，另一手贴于身侧。",
                "保持肩带下沉不耸肩、肘关节微屈固定角度。",
                "呼气由三角肌中束发力将训练侧手臂向身体正侧方平滑抬起至上臂与地面大致平行，腕部保持中立不高于肘部。",
                "在水平顶点短暂停顿后，吸气有控制地沿原弧线缓慢下放回大腿外侧起始位；单侧完成规定次数后换另一侧。",
            ],
        },
    }

    sources = {
        "0351": "https://exrx.net/WeightExercises/Triceps/DBLyingTriExt",
        "0352": "https://exrx.net/WeightExercises/Triceps/DBCloseGripBenchPress",
        "0353": "https://www.muscleandstrength.com/exercises/single-arm-dumbbell-concentration-curl.html",
        "0354": "https://exrx.net/WeightExercises/Triceps/DBKickback",
        "0570": "https://exrx.net/WeightExercises/RectusAbdominis/BWSeatedKneeRaise",
        "0355": "https://exrx.net/WeightExercises/DeltoidLateral/DBOneArmLateralRaise",
    }

    review_notes = {
        "0351": "将原机械直译“哑铃平躺三头肌伸展”规范为“哑铃仰卧双臂屈伸”，补齐平板训练凳与过顶伸展负荷标签；原四帧经清白并核对后双脚及平凳支点残差 0.0 px（匹配分 0.9965）。",
        "0352": "规范“哑铃仰卧对握窄推”四步要点与平板训练凳支撑，原图仅由顶端与底端两姿往复且缺少半程过渡帧，已按解剖插画规范重制 2×2 四帧并整数配准至 Q0/Q1/Q2(0,-19)/Q1，三支点残差 ≤ 1.0 px（匹配分 ≥ 0.9647）。",
        "0353": "规范“健身球哑铃单臂集中弯举”并补齐瑜伽球必需器械，原四帧经整数平移（F1 +2,0；F2 0,+2）配准后双脚及瑜伽球底座残差 ≤ 1.0 px（匹配分 ≥ 0.9661）。",
        "0354": "将原“哑铃单臂后推”规范为“哑铃俯身单臂后屈伸”，补齐俯身稳定负荷标签；原四帧经整数平移（F1 +2,0；F2 0,-1）配准后双脚、下肢及支撑躯干残差 ≤ 1.0 px（匹配分 ≥ 0.9761）。",
        "0570": "将原“平凳腿拉”规范为“平凳坐姿收腿”并补齐平板训练凳支撑，避免名称误触发静态计时词库；原四帧经清白并核对后平凳前后支架残差 0.0 px（匹配分 0.9982）。",
        "0355": "核对“哑铃单臂侧平举”外展轨迹、单侧计次与站姿下背低负荷标签；原四帧经整数平移（F1 -13,0；F2 -18,-1）配准后双脚及小腿支点残差 0.0 px（匹配分 ≥ 0.9716）。",
    }

    pending = {
        "0513": "待修图 · 已核对跳跃深蹲（第二式）名称与步骤；原图与 0514 完全同图且第 1 帧脚跟间有黑点杂影、第 3 帧右臂缺失及头顶触边仅微离地，待后续按独立批次重制。",
        "0514": "待修图 · 已规范跳跃深蹲步骤与下肢推／爆发力模式；原图第 1 帧脚底存杂影且第 3 帧腾空高度与四肢完整性未达标，待后续重制。",
        "0555": "待修图 · 已将机械直译“踢出坐姿”规范为“平凳坐姿前踢腿”并将主目标从误标的腘绳肌纠正为股四头肌并补平板训练凳；原图第 1 帧左凳脚被裁切、三帧凳宽独立缩放约 18 px 且肌群标红在股四头肌与腘绳肌间跳变，待重制。",
        "0558": "待修图 · 已将“动态引体向上”纠正为与插画匹配的“摆荡借力双力臂”并补单杠支撑；原图第 3 帧拉起上杠后横杠与深蹲架整体下移约 59 px（非同一固定机位），待重制。",
    }

    result = {
        "batch": "20260924_review16",
        "version": "1.2.21",
        "version_code": 2026092401,
        "apk_name": "时光屋-1.2.21-第十六批动作复核.apk",
        "output": "build/review16-20260924",
        "report": "docs/releases/2026-09-24-review-batch16.md",
        "inspected": inspected,
        "definition_updates": definition_updates,
        "sources": sources,
        "review_candidates": review_candidates,
        "pending": pending,
        "registered_media": review_candidates,
        "original_pose_repairs": ["0351", "0353", "0354", "0570", "0355"],
        "generated_images_imported": 1,
        "image_generation_calls": 1,
        "review_notes": review_notes,
    }
    (B / "review-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

    code_files = sorted(R.glob("app/src/main/java/**/*.java"))
    baseline = {str(p.relative_to(R)): sha(p) for p in code_files}
    (B / "code-baseline.json").write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n")

    qa_spec = {
        "batch": "20260924_review16",
        "expected_checks": 25,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20260924_review16")


if __name__ == "__main__":
    main()
