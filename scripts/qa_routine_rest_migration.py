#!/usr/bin/env python3
from pathlib import Path
exec(Path('scripts/qa_user_fixes.py').read_text().split('\nstop();original=')[0])
stop();original=adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml')
try: ET.fromstring(original)
except ET.ParseError: original=b'<?xml version="1.0" encoding="utf-8"?><map />'
try:
    state_with(records='[]');tap('为我安排这一练 →');items=draft()['items'][:2]
    for item in items:item.update(sets=1,kind='REPS',reps='12',rest=20,restAfter=0,reason='原有动作备注',weight='')
    old={'version':1,'id':'qa-rest','name':'旧循环','note':'迁移验证','circuit':True,'rounds':2,'roundRest':60,'items':items}
    state_with(records='[]',routinesV1=json.dumps([old],ensure_ascii=False));tap('我的动作组 · 保存组合直接练');tap('练这组 →')
    expanded=draft()['items']
    check([i['restAfter'] for i in expanded]==[20,60,20,0],'Version 1 routines retain their original exercise and round rests')
    tap('‹ 回到今天');tap('我的动作组 · 保存组合直接练');tap('编辑动作组');tap('编辑次数、计时与重量')
    set_text('组间休息（秒）',10);set_text('动作间休息（秒）',75);set_text('重量（选填，如单只 5 kg）','10 kg');tap('保存安排');tap('保存动作组')
    saved=json.loads(prefs()['routinesV1'])[0]
    check(saved['version']==2 and saved['items'][0]['rest']==10 and saved['items'][0]['restAfter']==75,'Edited routines migrate to separate persistent rest fields')
    check(saved['items'][0]['weight']=='10 kg' and saved['items'][0]['reason']=='原有动作备注','Weight field preserves existing action notes')
    stop();launch();tap('我的动作组 · 保存组合直接练');tap('练这组 →')
    changed=draft()['items']
    check([i['restAfter'] for i in changed]==[75,60,75,0] and changed[0]['weight']=='10 kg','Version 2 routines execute saved breaks and weights after relaunch')
    snapshot('migrated-routine-preview')
    print('ALL ROUTINE MIGRATION CHECKS PASSED',flush=True)
finally:write_state(original);launch();print('Original emulator preferences restored.',flush=True)
