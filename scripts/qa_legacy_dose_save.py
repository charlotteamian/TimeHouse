#!/usr/bin/env python3
"""Screenshot regression for legacy records: save reps without hidden blank-set error."""
from pathlib import Path
import os
exec(Path('scripts/qa_user_fixes.py').read_text().split('\nstop();original=')[0])
old={'time':'09-16 08:08','title':'旧版硬拉记录','duration':'17:17','epoch':int(time.time()*1000)-3600000,'total':1,'done':1,'note':'较为轻松，早上起来身体疲惫','feel':'轻松','pain':'无',
     'items':['✓ 哑铃罗马尼亚硬拉 · 1:49 · 3 组 · 保留旧说明'],'itemStats':['exercise_legacy_rdl|3|1'],
     'hrAvg':99,'hrMax':141,'hrMin':73,'hrReliable':True,'hrSeries':'[[0,73],[30,99],[60,141]]','hrSamples':203,'hrCoverage':100,'hrSource':'QA 心率',
     'metrics':{'activeKcal':{'value':120},'steps':{'value':234}}}
def open_entry():
    tap('修改动作、次数与重量');tap('1. 哑铃罗马尼亚硬拉')
def field_value(desc):
    return next(n.get('text','') for n in ui().iter('node') if n.get('content-desc')==desc)
def field_error(desc):
    return next(n.get('error','') for n in ui().iter('node') if n.get('content-desc')==desc)
stop();original=adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml');(out/'original-prefs.xml').write_bytes(original)
try:
    state_with(records=json.dumps([old],ensure_ascii=False));tap('记录');open_entry()
    if os.environ.get('QA_EXPECT_LEGACY_FAILURE')=='1':
        check(field_value('计划组数')=='','Baseline reproduces blank planned sets despite three recorded completed sets')
        set_text('每组次数或秒数','15');tap('保存安排');snapshot('reported-save-error')
        check(field_error('每组次数或秒数')=='组数和休息请填写整数','Baseline reproduces misleading integer error after entering 15 reps')
        check(not record().get('details',[{}])[0].get('dose'),'Baseline cannot save the supplied repetitions')
    else:
        check(field_value('计划组数')=='3' and field_value('实际完成组数')=='3','Legacy planned-set suggestion uses the three recorded completed sets')
        check(any('可修改' in x and '完成组数' in x for x in texts()),'Suggestion is explicitly explained rather than presented as known old plan')
        check(field_value('每组次数或秒数')=='','Unknown old repetitions are not invented')
        set_text('每组次数或秒数','15');tap('保存安排');snapshot('legacy-save-fixed')
        check(record()['details'][0]['dose']['sets']==3 and record()['details'][0]['dose']['reps']=='15' and record()['details'][0]['completed']==3,'Entering only 15 reps now saves the three-set legacy record')
        check(record()['details'][0]['weight']=='' and record()['details'][0]['original']==old['items'][0],'Unknown weight and original historical text remain intact')
        check(record()['note']==old['note'] and record()['hrAvg']==99 and record()['metrics']==old['metrics'],'Saving the old dose preserves notes and synchronized health data')
        stop();launch();tap('记录');check(record()['details'][0]['dose']['reps']=='15','Corrected dose survives app restart')
        open_entry();set_text('计划组数','');tap('保存安排');snapshot('planned-sets-error')
        check(field_error('计划组数')=='请填写计划组数','Empty planned sets receive a specific visible field error')
        set_text('计划组数','3');set_text('组间休息（秒）','');tap('保存安排');snapshot('rest-error')
        check(field_error('组间休息（秒）')=='请填写组间休息（秒）','Empty rest receives a rest-field error')
        set_text('组间休息（秒）','0');set_text('实际完成组数','4');tap('保存安排')
        check(field_error('实际完成组数')=='实际完成组数须为 0–3','Completed sets greater than planned sets are rejected on their own field')
        set_text('实际完成组数','3');set_text('每组次数或秒数','15-10');tap('保存安排')
        check('区间上限不能小于下限' in field_error('每组次数或秒数'),'Descending repetition range is rejected on the dose field')
        set_text('每组次数或秒数','9999999999999999999999');tap('保存安排')
        check('次数请填 1–500' in field_error('每组次数或秒数'),'Overflowing repetitions report dose bounds, not a sets/rest error')
        set_text('每组次数或秒数','10-15');tap('保存安排')
        check(record()['details'][0]['dose']['reps']=='10-15' and record()['details'][0]['dose']['rest']==0,'Valid repetition range and zero rest save after correcting field errors')
        open_entry();tap('按秒计时');set_text('每组次数或秒数','4');tap('保存安排')
        check(field_error('每组次数或秒数')=='计时请填 5–3600 秒','Hold-duration bounds remain enforced')
        set_text('每组次数或秒数','30');tap('保存安排')
        check(record()['details'][0]['dose']['kind']=='HOLD' and record()['details'][0]['dose']['hold']==30,'Valid timed prescription still saves through the shared editor')
finally:
    write_state(original);launch()
