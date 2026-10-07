#!/usr/bin/env python3
"""September user-report regression, emulator only, restores local preferences."""
from pathlib import Path
exec(Path('scripts/qa_review_flow.py').read_text().split('\nstop()\noriginal =')[0])

def set_text(description,value):
    result=adb('shell','am','instrument','-w','-e','setTextDesc',shlex.quote(description),'-e','setTextBase64',
               base64.b64encode(str(value).encode()).decode(),'com.restartday.fitness.qa/.UiSnapshot').decode()
    if 'textSet=1' not in result: raise AssertionError(result)

def checked(label):
    return any(n.get('text')==label and n.get('checked')=='true' for n in ui().iter('node'))

def record():return json.loads(prefs()['records'])[0]

stop();original=adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml')
(out/'original-prefs.xml').write_bytes(original)
try: ET.fromstring(original)
except ET.ParseError: original=b'<?xml version="1.0" encoding="utf-8"?><map />'

try:
    state_with(reviewedOnlyV1=False,includeUnverified=True,records='[]')
    tap('为我安排这一练 →');base=draft()
    check(bool(base['items']) and all(i['id'] in known for i in base['items']), 'Home rejects unreviewed despite both legacy opt-outs')
    check(all(15<=i['rest']<=30 and i['restAfter']==75 for i in base['items']), 'Daily prescriptions separate short set rests and 75-second exercise rests')
    tap('调整组数、次数、休息与重量')
    if checked('按秒计时'):tap('按秒计时')
    for desc,value in [('计划组数',2),('每组次数或秒数',30),('组间休息（秒）',10),('动作间休息（秒）',75),('重量（选填，如单只 5 kg）','7.5 kg')]:set_text(desc,value)
    snapshot('dose-editor')
    tap('保存安排');edited=draft()['items'][0]
    check(edited['sets']==2 and edited['reps']=='30' and edited['rest']==10 and edited['weight']=='7.5 kg', 'Preview edits reach structured dose and weight')
    stop();launch();tap('查看课程 →')
    check(draft()['items'][0]==edited,'Edited prescription survives process death')
    tap('开始这一练 →');tap('准备好了，开始这一组');time.sleep(3.4);tap('完成本组，休息')
    check(draft()['phase']=='REST' and draft()['phaseDuration']==10000,'Edited 10-second rest controls the actual timer')
    tap('调整本动作安排');set_text('组间休息（秒）',0);tap('保存安排')
    check(draft()['paused'] and draft()['phaseDuration']==0 and draft()['set']==1,'Active edit shortens timer, preserves completed set, and pauses safely')
    tap('继续训练 →');time.sleep(3.4)
    check(draft()['phase']=='WORK' and draft()['set']==1,'Zero rest resumes into next set without getting stuck or double counting')
    tap('完成动作 ✓')
    check(draft()['phase']=='REST' and draft()['index']==1 and draft()['phaseDuration']==75000 and not draft()['running'], 'Exercise transition is a separate 75-second rest')
    check(any('动作间休息' in t for t in texts()), 'Transition timer is labelled exercise rest')
    tap('结束并保存');tap('结束并保存')
    check(record()['details'][0]['dose']['reps']=='30' and record()['details'][0]['weight']=='7.5 kg' and record()['details'][0]['completed']==2, 'Finish snapshots dose, weight and actual completed sets')
    tap('记录');tap('写心得 / 备注');set_text('训练心得 / 备注','肩膀轻松，下次加重量 <>&');tap('保存心得')
    check(record()['note']=='肩膀轻松，下次加重量 <>&','Dedicated note editor stores Unicode and special characters')
    tap('修改动作、次数与重量');tap('1. '+record()['details'][0]['name'])
    for desc,value in [('计划组数',3),('实际完成组数',3),('每组次数或秒数',40),('重量（选填，如单只 5 kg）','10 kg')]:set_text(desc,value)
    tap('保存安排')
    check(record()['details'][0]['dose']['reps']=='40' and record()['details'][0]['weight']=='10 kg' and record()['itemStats'][0].split('|')[1]=='3', 'History editing updates prescription, load and weekly-volume data')
    stop();launch();tap('记录');snapshot('record-edited')
    check(record()['note']=='肩膀轻松，下次加重量 <>&' and record()['details'][0]['dose']['reps']=='40', 'History changes survive relaunch')
    old={'time':'09-16 08:08','title':'旧版训练','duration':'17:17','epoch':int(time.time()*1000)-3600000,'total':1,'done':1,'note':'旧心得',
         'items':['✓ 交替拍肩 · 1:49 · 3 组 · 保留旧说明'],'itemStats':['exercise_legacy_shoulder|3|1'],
         'hrAvg':99,'hrMax':141,'hrMin':73,'hrReliable':True,'hrSeries':'[[0,73],[30,99],[60,141]]','hrSamples':203,'hrCoverage':100,'hrSource':'QA 心率',
         'metrics':{'activeKcal':{'value':120,'sources':['com.garmin.android.apps.connectmobile']},'totalKcal':{'value':150},'steps':{'value':234},'distanceM':{'value':180}}}
    state_with(records=json.dumps([old],ensure_ascii=False));tap('记录');snapshot('watch-chart')
    check(any('活动消耗：120 千卡' in t for t in texts()) and any('总热量：150' in t for t in texts()), 'Records show activity and total energy separately')
    check(any('心率变化图' in n.get('content-desc','') for n in ui().iter('node')), 'Stored heart samples have an accessible chart')
    tap('修改动作、次数与重量');tap('1. 交替拍肩')
    check(any('旧记录没有保存次数和重量' in t for t in texts()),'Old doses remain unknown until explicitly supplied')
    for desc,value in [('计划组数',3),('每组次数或秒数',30),('重量（选填，如单只 5 kg）','0 kg')]:set_text(desc,value)
    tap('保存安排')
    check(record()['details'][0]['dose']['reps']=='30' and record()['details'][0]['original']==old['items'][0], 'Legacy record accepts 30 reps while preserving original evidence')
    tap('写心得 / 备注');set_text('训练心得 / 备注','旧记录补记');tap('保存心得')
    check(record()['hrAvg']==99 and record()['metrics']['activeKcal']['value']==120,'Editing notes and actions preserves synchronized health data')
    stop();launch();tap('记录');snapshot('legacy-record-edited')
    check(record()['details'][0]['dose']['reps']=='30' and record()['note']=='旧记录补记', 'Legacy migration and edits persist together')
    # Previously generated unreviewed preview must not reappear after upgrade.
    stale=json.loads(json.dumps(base));stale['items'][0]['id']='exercise_romanian_deadlift'
    # choose a real unreviewed id from catalog rather than an absent-id failure
    catalog=json.loads(Path('app/src/main/assets/exercises_1324.json').read_text())['exercises']
    stale['items'][0]['id']=next('dataset_1324_'+e['id'] for e in catalog if 'dataset_1324_'+e['id'] not in known)
    state_with(workoutDraft=json.dumps(stale),records='[]',reviewedOnlyV1=False)
    check(not draft() and prefs().get('unreviewedWorkoutDraft'),'Upgrade quarantines unreviewed preview while retaining its original data')
    print('ALL USER FIX CHECKS PASSED',flush=True)
finally:
    write_state(original);launch();print('Original emulator preferences restored.',flush=True)
