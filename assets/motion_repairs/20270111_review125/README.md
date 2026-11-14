# Batch 125 Review Evidence (`20270111_review125`)

## Selection & Sources
- Inspected 10 unreviewed records: `2138`, `2139`, `2141`, `2142`, `2144`, `2186`, `2187`, `2202`, `2203`, `2204`.
- Inspected `selected.json`, `contact-1.jpg`, `contact-2.jpg`, native 4-frame strip `frames_2138.png`, and quantitative WebP telemetry; aligned `2138` setup and continuous pedal-circle form with WorkoutLabs stationary bike guidance (`https://workoutlabs.com/exercise-guide/`) and existing repo cyclic spec (`assets/motion_repairs/20260910/prompts.json#2138`).

## Approved Candidate (`2138` -> `已完成`)
- `2138` (`固定动感单车骑行`, `stationary bike run v. 3`): native 480×480 4-frame cyclic animation (`durations=[590, 590, 590, 590]`, total `2.36s`), pure white background (`[255, 255, 255]`), generous margins (`L:96, R:76, T:33, B:59`), bike stabilizer base & rider upper body anchored (`<=1px` bbox drift, `y>=370 IoU(F1,F3)=0.9754`, `y>=395 IoU(F1,F2)=0.9756`), crisp grayscale anatomy cleanly highlighting quadriceps and calves (`target: "cardiovascular system"`). Removed `（第三式）` and updated saddle/pedal steps while clearing hold triggers.

## Deferred Decisions (9 Deferred -> `待修图`)
- `2139` (`上肢功率车推拉摇臂`): 10-frame WebP (`T:14, B:12`, tiny bottom-right tick in F4); removed hold trigger word.
- `2141` (`椭圆机平稳踩踏练习`): 2-frame WebP (`T:14, B:14`); removed hold trigger words.
- `2142` (`坐姿滑雪训练机双臂下压`): 10-frame WebP (`L:14, R:13`) with sudden rear-view torso flip in Frame 4; clarified seated rail setup.
- `2144` (`直立靠背凳坐姿龙门架胸推`): 2-frame WebP (`L:14, R:14`); added `required_equipment_zh: ["直立靠背训练凳"]`.
- `2186` (`下斜凳仰卧曲杆杠铃臂屈伸`): 2-frame WebP (`L:14, R:14`); added `required_equipment_zh: ["带勾脚的下斜训练凳"]`, removed Latin `ez`.
- `2187` (`平凳仰卧杠铃反握窄距卧推`): 2-frame WebP (`L:14, R:14`); added `required_equipment_zh: ["平板训练凳"]`.
- `2202` (`仰坐滚轴屈膝臀部拉伸`): 10-frame WebP (`L:14, R:14`) with severe translucent/chopped leg ghosting in Frame 3; removed `"支撑"` hold trigger.
- `2203` (`长坐姿滚轮前推伸展`): 2-frame WebP (`L:14, R:14`); rewrote steps cleanly for long-seated wheel rollout.
- `2204` (`俯身滚轮前后身体锯`): 2-frame WebP (`L:14, R:14`); removed `"平板支撑"`/`"保持"` triggers so dynamic core saw uses reps pacing.
