#!/usr/bin/env python3
"""Final focused checks: visible safety downgrade and accurate custom-workout labels."""
from pathlib import Path
# Reuse the emulator-only read/write helpers, without executing the other test suite.
exec(Path('scripts/qa_routines_flow.py').read_text().split('\nstop()\noriginal =')[0])
stop()
original = adb('exec-out', 'run-as', pkg, 'cat', 'shared_prefs/fitness_state.xml')
try:
    root = ET.Element('map')
    ET.SubElement(root,'boolean',name='quickGentle',value='false')
    ET.SubElement(root,'int',name='quickMinutes',value='25')
    ET.SubElement(root,'string',name='lowerBackPain').text='SEVERE'
    ET.SubElement(root,'string',name='equipment').text='壶铃|TRX 悬挂带|哑铃'
    write_state(ET.tostring(root,encoding='utf-8',xml_declaration=True)); launch()
    tap('为我安排这一练 →')
    check(draft()['limited'] and draft()['intensity']=='LOW' and '已降为轻松' in draft()['title'], 'Daily downgrade is explicit in title, state and safety explanation')
    snapshot('visible-downgrade')
    base = {'version':1,'title':'QA transition labels','intensity':'MEDIUM','reason':'QA','safety':'QA','limited':False,'notes':[],'budget':0,'active':False,'items':[
        {'id':'exercise_kettlebell_deadlift','sets':1,'reps':'12','rpe':'7-8','rest':90,'kind':'REPS','hold':0,'perSide':False,'tempo':3,'reason':'16 kg','restAfter':60},
        {'id':'exercise_trx_row','sets':1,'reps':'12','rpe':'7-8','rest':90,'kind':'REPS','hold':0,'perSide':False,'tempo':3,'reason':'','restAfter':0}]}
    fixture(base)
    tap('查看课程 →'); tap('开始这一练 →')
    t=texts()
    check(any('动作后休息 60 秒' in s for s in t) and not any('休息 90 秒' in s for s in t), 'Single-set custom action displays actual transition rest, not unused set rest')
    for _ in range(3):
        if any('暂无动作示范' in s for s in t): break
        adb('shell','input','swipe','500','1600','500','700','200'); t=texts()
    check(any('暂无动作示范' in s for s in t), 'Missing media is clearly identified instead of a generic exercise illustration')
    snapshot('accurate-session-labels')
finally:
    write_state(original); launch()
