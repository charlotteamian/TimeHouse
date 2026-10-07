#!/usr/bin/env python3
"""Newly reviewed entries must enter real training with the required bench."""
from pathlib import Path
exec(Path('scripts/qa_review_flow.py').read_text().split('\nstop()\noriginal =')[0])
new=['0318','0320','0322'];names={e['id']:e['name_zh'] for e in json.loads(Path('app/src/main/assets/exercises_1324.json').read_text())['exercises']}
stop();original=adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml');(out/'original-prefs.xml').write_bytes(original)
try:
    check(all('dataset_1324_'+x in known for x in new),'All three new entries are in the final bundled ledger')
    raw=adb('shell','am','instrument','-w','-e','catalog',','.join('dataset_1324_'+x for x in new),'com.restartday.fitness.qa/.UiSnapshot').decode()
    match=re.search(r'INSTRUMENTATION_RESULT: catalog=(\S+)',raw);assert match,raw
    catalog=json.loads(base64.b64decode(match.group(1)));(out/'loaded-safety.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    check(all(catalog['dataset_1324_'+x]['safeWithRequiredEquipment'] for x in new),'All three loaded candidates pass the real recommendation filter with full equipment')
    check(all(not catalog['dataset_1324_'+x]['safeSevereShoulder'] for x in new),'Severe shoulder pain excludes all three through the real recommendation filter')
    for xid in new:
        item={'id':'dataset_1324_'+xid,'sets':1,'reps':'8','rpe':'7','rest':30,'kind':'REPS','hold':0,'perSide':False,'tempo':3,'reason':'','restAfter':0}
        workout={'version':1,'title':'新复核动作开练验证','intensity':'MEDIUM','reason':'QA','safety':'QA','limited':False,'notes':[],'budget':0,'active':False,'items':[item]}
        state_with(equipment='自重|哑铃',workoutDraft=json.dumps(workout,ensure_ascii=False));tap('查看课程 →');tap('开始这一练 →')
        check('还缺少必需器械' in texts() and not draft()['active'],names[xid]+' cannot start without incline bench')
        state_with(equipment='哑铃|上斜训练凳',workoutDraft=json.dumps(workout,ensure_ascii=False));tap('查看课程 →');tap('开始这一练 →')
        check(draft()['active'] and draft()['items'][0]['id']=='dataset_1324_'+xid,names[xid]+' enters normal training when equipment is complete');snapshot(xid+'-session')
        tap('准备好了，开始这一组')
        deadline=time.monotonic()+6
        while draft()['phase']=='COUNT_IN' and time.monotonic()<deadline: time.sleep(.25)
        check(draft()['phase']=='WORK' and not draft()['items'][0]['perSide'],names[xid]+' starts one bilateral repetition set after count-in without duplicating sides')
    print('ALL BATCH TEN FINAL CHECKS PASSED',flush=True)
finally:
    write_state(original);launch()
