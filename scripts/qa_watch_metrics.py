#!/usr/bin/env python3
"""Real Health Connect API fixture test on emulator. Restores prefs, permissions and inserted health records."""
from pathlib import Path
exec(Path('scripts/qa_review_flow.py').read_text().split('\nstop()\noriginal =')[0])
TYPES=['HEART_RATE','EXERCISE','ACTIVE_CALORIES_BURNED','TOTAL_CALORIES_BURNED','STEPS','DISTANCE']
original_permissions={}
for target,prefix in [(pkg,'READ_'),(pkg+'.qa','WRITE_')]:
    dump=adb('shell','dumpsys','package',target).decode()
    for kind in TYPES:
        perm='android.permission.health.'+prefix+kind
        original_permissions[(target,perm)]=bool(re.search(re.escape(perm)+r': granted=true',dump))
stop();original=adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml');ids=None
(out/'original-prefs.xml').write_bytes(original)
try: ET.fromstring(original)
except ET.ParseError: original=b'<?xml version="1.0" encoding="utf-8"?><map />'

try:
    for target,perm in original_permissions:adb('shell','pm','grant',target,perm)
    now=int(adb('shell','date','+%s').decode())*1000;start=now-900000;end=start+600000
    result=adb('shell','am','instrument','-w','-e','start',str(start),'-e','end',str(end),pkg+'.qa/.HealthFixture').decode()
    (out/'health-insertion.txt').write_text(result)
    match=re.search(r'INSTRUMENTATION_RESULT: ids=(.*)',result)
    assert match,result
    ids=json.loads(match.group(1));check(len(ids)==8,'Health Connect accepted workout metrics, an unrelated long session and out-of-window energy')
    sample={'time':'09-16 08:08','title':'健康连接同步验证','duration':'10:00','epoch':end,'startEpoch':start,'total':1,'done':1,'items':['✓ 交替拍肩 · 10:00 · 3 组'],'itemStats':['qa|3|1'],'note':'真实 API 测试数据'}
    state_with(records=json.dumps([sample],ensure_ascii=False));tap('记录')
    for _ in range(30):
        record=json.loads(prefs()['records'])[0]
        if record.get('metrics',{}).get('activeKcal') and record.get('hrAvg'):break
        time.sleep(.4)
    (out/'synced-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
    metrics=record.get('metrics',{})
    check(abs(metrics['activeKcal']['value']-120)<.01,'120000 API calories converts to 120 kcal and excludes adjacent 900 kcal')
    check(abs(metrics['totalKcal']['value']-150)<.01,'Total energy is independently 150 kcal, not added to active energy')
    check(metrics['steps']['value']==234 and metrics['distanceM']['value']==180,'Step count and distance match platform records')
    check(record['hrSamples']==60 and record['hrAvg']>0,'Heart-rate samples read through the same matched workout window')
    check(metrics['activeKcal']['sources']==[pkg+'.qa'],'Synced energy retains provider provenance')
    check('QA unrelated' not in metrics.get('windowLabel','') and 'QA workout' in metrics.get('windowLabel',''), 'Exact workout match outranks a much longer overlapping session')
    snapshot('synced-health-record')
    # A partial grant must still read available energy without requiring heart rate.
    stop()
    for kind in TYPES:
        if kind!='ACTIVE_CALORIES_BURNED':adb('shell','pm','revoke',pkg,'android.permission.health.READ_'+kind)
    state_with(records=json.dumps([sample],ensure_ascii=False));tap('记录')
    for _ in range(30):
        partial=json.loads(prefs()['records'])[0]
        if partial.get('metrics',{}).get('activeKcal'):break
        time.sleep(.4)
    check(partial['metrics']['activeKcal']['value']==120 and not partial.get('hrAvg') and 'totalKcal' not in partial['metrics'], 'Partial energy-only permission works without inventing heart rate or total energy')
    snapshot('partial-energy-permission')
    # Empty interval must display unknown, never a fabricated zero or HR-based estimate.
    missing=dict(sample,epoch=start-300000,startEpoch=start-900000)
    state_with(records=json.dumps([missing],ensure_ascii=False));tap('记录');time.sleep(1)
    blank=json.loads(prefs()['records'])[0]
    check('activeKcal' not in blank.get('metrics',{}),'No platform data remains missing rather than zero')
    check('消耗热量：暂无数据' in texts(),'Missing-calorie state is explicit in the record')
    print('ALL WATCH METRICS CHECKS PASSED',flush=True)
finally:
    stop()
    if ids is not None:
        result=adb('shell','am','instrument','-w','-e','delete',shlex.quote(json.dumps(ids,separators=(',',':'))),pkg+'.qa/.HealthFixture').decode()
        (out/'health-cleanup.txt').write_text(result)
        if 'deleted=true' not in result:raise AssertionError('Fixture cleanup failed: '+result)
    for (target,perm),granted in original_permissions.items():adb('shell','pm','grant' if granted else 'revoke',target,perm)
    write_state(original);launch();print('Original preferences and permissions restored; fixture health records deleted.',flush=True)
