#!/usr/bin/env python3
"""Author Batch 27 (20261005_review27) metadata updates, review notes, and QA spec."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[2]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    inspected = ["0815", "0409", "0816", "0410", "0817", "0411", "0826", "0413", "0858", "0414"]
    review_candidates = []

    definition_updates = {
        "0815": {
            "name_zh": "平凳直腿触地臂屈伸",
            "category": "upper arms",
            "equipment": "body weight",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["chest", "shoulders"],
            "movement_patterns_zh": ["推", "伸肘"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "背对稳固的平板训练凳坐起，双手与肩同宽反扶于长凳前端边缘、手指朝向正前方，臀部前滑离开凳面并向前伸直双腿以脚跟着地。",
                "下沉肩带、挺胸收腹，使中上背紧贴凳缘轨迹稳定而不耸肩前扣。",
                "吸气缓慢屈肘垂直下放臀部接近或轻触地面，控制肘尖向后微夹而非大幅外撇。",
                "呼气由肱三头肌主导用力推直双肘回到高撑起始位；每次下放与推起计一次。",
            ],
        },
        "0409": {
            "name_zh": "扶墙台阶哑铃单腿提踵",
            "category": "lower legs",
            "equipment": "dumbbell",
            "target": "calves",
            "muscle_group": "",
            "secondary_muscles": ["soleus", "ankles"],
            "movement_patterns_zh": ["单腿", "踝跖屈"],
            "required_equipment_zh": ["稳固踏台", "墙面"],
            "instructions_zh": [
                "站在稳固踏台边缘，非扶墙同侧手臂垂握一只哑铃，另一侧手轻扶前方墙面维持平衡；工作侧前脚掌前三分之一踩实台缘、脚跟悬空下垂，另一脚勾起离开踏台。",
                "保持工作腿膝关节微留缓冲不锁死，躯干与骨盆保持竖直稳定。",
                "吸气先缓慢将工作侧脚跟沉低于踏台平面充分拉伸小腿，随后呼气由小腿三头肌发力向上踮起脚跟至最高顶峰。",
                "在顶点短暂停顿收紧小腿后，吸气有控制地降回最低点；单腿完成规定次数后换腿换手。",
            ],
        },
        "0816": {
            "name_zh": "站立俯身徒手三头肌推伸",
            "category": "upper arms",
            "equipment": "body weight",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["delts", "upper back"],
            "movement_patterns_zh": ["伸肘", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽微屈膝站稳，收紧核心屈髋将上身前倾约45度并保持背部平直。",
                "屈肘将双上臂夹紧抬高贴近躯干两侧至与上背大致平行，双手微握贴近胸腹前侧。",
                "锁定上臂与肘关节位置固定不动，呼气由肱三头肌主动发力将双前臂沿直线向后上方彻底伸直。",
                "在手臂伸直顶点感受三头肌收缩后，吸气有控制地屈肘收回前侧起始屈曲位；每次后伸与收回计一次。",
            ],
        },
        "0410": {
            "name_zh": "后脚架凳哑铃单腿分腿蹲",
            "category": "upper legs",
            "equipment": "dumbbell",
            "target": "quads",
            "muscle_group": "",
            "secondary_muscles": ["glutes", "hamstrings", "calves"],
            "movement_patterns_zh": ["下肢推", "单腿"],
            "required_equipment_zh": ["平板训练凳"],
            "instructions_zh": [
                "背对平板训练凳站立、双手自然垂握哑铃在体侧，将一侧脚脚背稳搭在身后平凳面，前侧支撑腿向前迈步站稳。",
                "保持躯干略前倾且腰背挺直、核心收紧，前膝与前脚尖朝向保持一致。",
                "吸气缓慢屈曲前侧髋、膝关节垂直下蹲，直到前大腿接近与地面平行且后膝接近地面但不重砸。",
                "呼气以前脚全掌发力蹬地伸膝推回高位站立；单腿完成规定次数后换腿重复。",
            ],
        },
        "0817": {
            "name_zh": "站姿过顶单臂三头肌拉伸",
            "category": "upper arms",
            "equipment": "body weight",
            "target": "triceps",
            "muscle_group": "",
            "secondary_muscles": ["shoulders"],
            "movement_patterns_zh": ["拉伸", "过顶伸展"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽自然直立，沉肩收紧核心避免腰椎过度前凸。",
                "将一侧手臂高举过头顶并充分屈肘，使前臂和手掌顺势落于同侧上背肩胛之间。",
                "用另一侧手轻轻抓扶高举侧的肘关节上方，呼气温和向脑后内侧牵拉至肱三头肌长头出现清晰而舒适的伸展感。",
                "维持平稳呼吸持续牵伸15至30秒后缓缓放松放下手臂，再换另一侧交替完成。",
            ],
        },
        "0411": {
            "name_zh": "哑铃手枪式单腿深蹲",
            "category": "upper legs",
            "equipment": "dumbbell",
            "target": "quads",
            "muscle_group": "",
            "secondary_muscles": ["glutes", "hamstrings", "calves"],
            "movement_patterns_zh": ["下肢推", "单腿"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚窄站准备，双手各持一只较轻重量哑铃自然垂于髋侧，核心收紧并将一侧腿伸直向前平抬离地。",
                "单脚全掌（含大脚趾根、小脚趾根与脚跟）踩稳地面维持足弓稳定，非支撑腿全程悬空向前伸出。",
                "吸气主动屈髋屈膝缓慢沿直线垂直坐低，同时手臂顺势在身体两侧前平衡控制、避免圆背代偿。",
                "下降至控制极限深蹲位后，呼气由前侧股四头肌与臀肌合力发力踩稳全脚推回直立位；单腿完成规定次数后换腿。",
            ],
        },
        "0826": {
            "name_zh": "高架抓杠垂直举腿",
            "category": "waist",
            "equipment": "body weight",
            "target": "abs",
            "muscle_group": "",
            "secondary_muscles": ["hip flexors", "obliques", "forearms"],
            "movement_patterns_zh": ["核心屈曲", "下腹控制"],
            "required_equipment_zh": ["单杠"],
            "instructions_zh": [
                "双手正握高架单杠或抬腿架上方高把手，双臂伸直并主动下沉肩胛悬吊稳定身躯，双腿并拢自然垂向地面。",
                "微卷骨盆收紧腹部核心抑制躯干前后摆动惯性。",
                "呼气由下腹肌与髋屈肌发力，保持双腿伸直缓慢向正前方抬起至与地面平行或略高、略带骨盆后倾卷尾。",
                "在水平顶点停顿控稳半秒后，吸气有控制地缓缓下放双腿回到垂直悬吊起始位；每次举腿与下放计一次。",
            ],
        },
        "0413": {
            "name_zh": "哑铃深蹲",
            "category": "upper legs",
            "equipment": "dumbbell",
            "target": "quads",
            "muscle_group": "",
            "secondary_muscles": ["glutes", "hamstrings", "calves"],
            "movement_patterns_zh": ["下肢推", "双腿"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚略宽于肩站立、脚尖微微外展，双手各握一只哑铃自然垂于体侧或大腿外侧，挺胸沉肩收紧核心。",
                "膝盖对准第二、三脚趾方向保持一致，脊柱处于自然中立位。",
                "吸气同时屈髋屈膝向后下方有控制地下蹲，直到大腿大致与地面平行且双脚全掌稳踩地面不离地。",
                "在蹲底略控后，呼气发力均匀通过全脚掌伸髋伸膝蹬回直立起始位；每次下蹲与站起计一次。",
            ],
        },
        "0858": {
            "name_zh": "间歇冲刺跑",
            "category": "cardio",
            "equipment": "body weight",
            "target": "cardiovascular system",
            "muscle_group": "",
            "secondary_muscles": ["quads", "hamstrings", "glutes", "calves", "abs"],
            "movement_patterns_zh": ["心肺", "高速跑动"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "在平坦空旷跑道或场地站立热身准备，双脚与髋同宽、身体略微前倾呈起跑姿势，核心收紧。",
                "发力前摆双臂带动高位提膝与有力后蹬，进行短距离（如50米）或短时高强全力冲刺跑。",
                "跑动全程保持肩颈放松、核心紧绷与前后直臂高效摆臂节奏。",
                "接近终点时逐步减速缓冲慢走恢复心率，休息30至90秒后再进行下一组冲刺；按间歇组数计时完成。",
            ],
        },
        "0414": {
            "name_zh": "哑铃站立交替过头推举",
            "category": "shoulders",
            "equipment": "dumbbell",
            "target": "delts",
            "muscle_group": "",
            "secondary_muscles": ["triceps", "traps", "core"],
            "movement_patterns_zh": ["垂直推", "过顶伸展", "站姿稳定"],
            "required_equipment_zh": [],
            "instructions_zh": [
                "双脚与肩同宽稳踩地面站直，双手正握各持一只哑铃举起停于肩部外侧上方、掌心朝前、前臂基本垂直地面。",
                "收紧腹肌与臀肌锁住肋骨，避免单侧过顶推起时腰椎过度反弓或躯干大幅侧歪。",
                "保持另一侧哑铃稳停肩高，呼气由工作侧三角肌与肱三头肌发力垂直向上推举哑铃过头顶至肘部接近伸直（留微屈缓冲）。",
                "吸气控制下放回肩高位置，再立即换对侧手臂交替推举；双侧交替稳定完成规定次数。",
            ],
        },
    }

    sources = {}
    review_notes = {}

    pending = {
        "0815": "待修图 · 已纠正原上游严重误译（triceps dips floor 原错译“地板三头肌下压”）为平凳直腿触地臂屈伸并补齐平板训练凳；原图第 1、2 帧长凳相对双脚跟发生 6–7 px 横纵独立漂移与长凳变形（bench sc=0.7438 / heels sc=0.5272），暂存待重制。",
        "0409": "待修图 · 已规范为扶墙台阶哑铃单腿提踵（单腿单侧计次）并补齐稳固踏台与墙面两项所需支持；经精确像素配准测试，第 1 帧中墙面（+25, -1）与台阶（+28, 0）存在 3–4 px 水平剪切错位（踏台挤入墙缘且前脚掌位于 +32, 0），无法同时满足固定支点残差 ≤ 2.0 px 与匹配分 ≥ 0.96，暂存待重制。",
        "0816": "待修图 · 已重写破损文字步骤（原文错写屈肘降至地面）为站立俯身徒手三头肌推伸；原图第 0 帧直立平举错高亮三角肌前束而第 1、2 帧前倾后伸高亮肱三头肌，且三帧站立脚位连续横跳，暂存待重制。",
        "0410": "待修图 · 已规范为后脚架凳哑铃单腿分腿蹲（单腿单侧计次）并补齐平板训练凳；原图第 1、2 帧中平凳底座（-14, -3 / 0, +11, sc=0.86）与前方支撑脚（-22, +1 / -27, +12, sc=0.78）存在 13–27 px 横向背离与平凳形态漂移，暂存待重制。",
        "0817": "待修图 · 已规范为站姿过顶单臂三头肌拉伸（单臂单侧计次）；原图裤腰位于 y=207..289 而第 0 帧脚尖落在 y=479（贴底边且较第 1、2 帧 y=454 多伸长 25 px），且第 2 帧头顶高举前臂顶边缘（y=0, top3=61px）发生明显上缘截断，暂存待重制。",
        "0411": "待修图 · 已修正主目标为股四头肌与哑铃手枪式单腿深蹲步骤（单腿单侧计次）；原图三帧支撑脚位置不断跳移且比例改变（stance_foot sc=0.6637 / 0.2665），无法纯平移配准，暂存待重制。",
        "0826": "待修图 · 已避开“悬垂”静态词库误判并将实图握法更正为高架抓杠垂直举腿（补齐单杠支持）；原图第 2 帧正上方存在严重的邻格串图残脚伪影（y=0..12），第 0 帧底架触底（y=479），暂存待重制。",
        "0413": "待修图 · 已修正哑铃深蹲主目标为股四头肌并清理重复次要肌群；原图第 2 帧头顶正上方出现一对邻格串图残脚（y=0..15），同时第 0、1 帧脚底触底（y=479）且站距随帧漂移，暂存待重制。",
        "0858": "待修图 · 已纠正原误译“风速冲刺”与错分部位（waist/abs → cardio/cardiovascular system）为间歇冲刺跑并补齐四步说明；原图全幅跨步起跑及腾空冲刺位移无固定支点，暂存待重制。",
        "0414": "待修图 · 已规范哑铃站立交替过头推举并补齐站姿核心抗伸控制步骤；原图第 2 帧在静止脚位（dy=+4）、裤腰（dy=-2）、头部（dy=-8）与左侧待推哑铃（dx=+5, dy=-11）间出现 15 px 纵向拉伸及非工作侧偏移（sc=0.8178），且四帧循环仅单侧局部上推并未交替双臂，暂存待重制。",
    }

    result = {
        "batch": "20261005_review27",
        "version": "1.2.32",
        "version_code": 2026100501,
        "apk_name": "时光屋-1.2.32-第二十七批动作复核.apk",
        "output": "build/review27-20261005",
        "report": "docs/releases/2026-10-05-review-batch27.md",
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
        "batch": "20261005_review27",
        "expected_checks": 16,
        "review_candidates": review_candidates,
        "deferred_candidates": list(pending.keys()),
    }
    (B / "qa-spec.json").write_text(json.dumps(qa_spec, ensure_ascii=False, indent=2) + "\n")
    print("Authored review-result.json, code-baseline.json, and qa-spec.json for 20261005_review27")


if __name__ == "__main__":
    main()
