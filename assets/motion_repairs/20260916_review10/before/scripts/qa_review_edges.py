#!/usr/bin/env python3
"""Additional review integration checks for saved routines, selection, and missing media."""
from pathlib import Path
exec(Path('scripts/qa_review_flow.py').read_text().split('\nstop()\noriginal =')[0])
stop(); original = adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml')
try:
    item={'id':'exercise_kettlebell_deadlift','sets':1,'reps':'12','rpe':'7','rest':60,'kind':'REPS','hold':0,'perSide':False,'tempo':3,'reason':'','restAfter':0}
    routine={'version':1,'id':'qa_review','name':'旧动作组','note':'','circuit':False,'rounds':1,'roundRest':0,'items':[item]}
    state_with(reviewedOnlyV1=True,routinesV1=json.dumps([routine],ensure_ascii=False))
    tap('我的动作组 · 保存组合直接练'); tap('练这组 →')
    check('这套训练含未复核动作' in texts(), 'Saved routines respect reviewed-only gate')
    tap('知道了'); tap('编辑动作组'); tap('＋ 从动作库添加')
    options=set(); unreviewed=False
    # ListView exposes only visible rows; collect the full list while scrolling.
    expected_options=min(review_count,100)  # Picker explicitly shows at most 100 matches.
    for _ in range(max(5,expected_options+1)):
        tree=ui()
        labels=[n.get('text','') for n in tree.iter('node')]
        before=len(options)
        options.update(s for s in labels if ' · 已复核 · ' in s)
        unreviewed |= any(' · 未复核 · ' in s for s in labels)
        if len(options)==before: break
        node=next(n for n in tree.iter('node') if n.get('class')=='android.widget.ListView')
        x1,y1,x2,y2=map(int,re.findall(r'-?\d+',node.get('bounds')))
        # Overlapping slow scrolls prevent a fling from skipping unseen middle rows.
        height=y2-y1
        adb('shell','input','swipe',str((x1+x2)//2),str(y1+int(height*.75)),str((x1+x2)//2),str(y1+int(height*.35)),'600')
    (out/'reviewed-options.json').write_text(json.dumps(sorted(options),ensure_ascii=False,indent=2)+'\n')
    check(len(options)==expected_options and not unreviewed, 'Routine picker is restricted to reviewed exercises')
    snapshot('reviewed-picker')
    state_with()
    tap('训练选材：全部动作'); tap('仅已复核（候选不足会提示）')
    stop(); launch()
    check('训练选材：仅已复核' in texts() and prefs().get('reviewedOnlyV1')=='true', 'Training scope selection persists after restart')
    tap('动作库'); tap('复核筛选：全部状态'); tap('待补图')
    check(any('共 3 个' in s for s in texts()), 'Missing demonstrations are exposed as a separate queue')
    snapshot('missing-media')
finally:
    write_state(original); launch()
