# Batch 127 Review Evidence (`20270113_review127`)

## Selection & Sources
- Inspected 10 unreviewed records: `2297`, `2311`, `2315`, `2318`, `2328`, `2330`, `2331`, `2334`, `2335`, `2364`.
- Inspected `selected.json`, `contact-1.jpg`, `contact-2.jpg`, 4-frame strips `frames_2297.png` & `frames_2328.png`, frame counts, borders, and IoU metrics across all 10 WebPs (2 non-compliant 4-frame WebPs, 7 with 10 frames, 1 with 2 frames).

## Approved Candidates (`0`)
- None approved in Batch 127: `2297` & `2328` fail pure white background (`[254,253,253]`/`[253,254,253]`), margins (`R:2`/`R:13 < 15`), and Frame 3 vertical/horizontal jump (`iou370=0.5215`/`0.5321 < 0.96`), while all remaining 8 fail frame count (`10`/`2`) and borders (`< 15px`), with `2318` having a severe double-head glitch in F3 and `2331` having bottom-edge chopped artifacts.

## Deferred Decisions (10 Deferred -> `待修图`)
- `2297` (`瑜伽球双手扶头大跨度卷腹`): 4-frame WebP fails border (`R:2`), bg (`[254,253,253]`), and Frame 3 upward jump (`iou370=0.5215`); removed parens and unified `"瑜伽球"`.
- `2311` (`楼梯台阶机攀登踩踏`): 10 frames (`T:14, B:14`); removed hold trigger words `"支撑"`/`"保持"`.
- `2315` (`器械坐姿膝垫负重提踵`): 10 frames (`L:14, R:13`); removed `"（杠杆）"` and `"保持"`.
- `2318` (`器械坐姿双柄推肩`): 10 frames (`T:14, B:14`) with severe double-head overlap glitch in Frame 3; removed `"（第三式）（杠杆）"`.
- `2328` (`瑜伽球窄距俯卧撑`): 4-frame WebP fails border (`R:13`), bg (`[253,254,253]`), and Frame 3 ball jump (`iou370=0.5321`); removed `"保持"`.
- `2330` (`龙门架坐姿全程宽握高位下拉`): 2 frames (`L:14, R:14`); removed `"保持"` and clarified full range-of-motion steps.
- `2331` (`立式固定器械健身车骑行`): 10 frames (`T:14, B:13`) with chopped black circle caps along bottom edge; disambiguated from `2138`, removed `"保持"`.
- `2334` (`倒蹬机斜卧直腿提踵`): 10 frames (`L:14, R:14`); standardized 45-degree sled calf press steps and removed `"保持"`.
- `2335` (`固定器械坐姿膝垫提踵`): 10 frames (`L:14, R:14`); fixed copy-pasted `"align shoulders"` step to thigh/knee pad setup.
- `2364` (`辅助跪姿宽握双杠偏胸臂屈伸`): 10 frames (`L:14, R:14`); fixed mistranslated `"胸下压（跪姿）"`, removed parens and `"保持"`.
