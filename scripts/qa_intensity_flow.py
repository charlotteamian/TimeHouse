#!/usr/bin/env python3
"""Regression for default vs explicit workout intensity. Emulator only; restores preferences."""
from pathlib import Path
exec(Path('scripts/qa_routines_flow.py').read_text().split('\nstop()\noriginal =')[0])
raw_draft = draft
def draft():
    for _ in range(30):
        d = raw_draft()
        if 'intensity' in d: return d
        time.sleep(.5)
    snapshot('missing-draft')
    raise AssertionError('No generated draft: ' + str(texts()))
stop()
original = adb('exec-out', 'run-as', pkg, 'cat', 'shared_prefs/fitness_state.xml')
def seed(default='LOW', override='', assessment=None, pain=''):
    root=ET.Element('map')
    for k,v in {'intensity':default,'quickIntensityOverrideV2':override,'equipment':'自重|哑铃|壶铃|TRX 悬挂带','lowerBackPain':pain,'records':'[]'}.items():
        ET.SubElement(root,'string',name=k).text=v
    ET.SubElement(root,'int',name='quickMinutes',value='25')
    ET.SubElement(root,'boolean',name='voiceEnabled',value='false')
    if assessment: ET.SubElement(root,'string',name='assessment').text=json.dumps(assessment)
    write_state(ET.tostring(root,encoding='utf-8',xml_declaration=True));launch()
def regenerate():
    tap('‹ 回到今天');tap('重新安排');tap('为我安排这一练 →')
try:
    seed()
    tap('轻松模式 · 点此切换为日常强度');tap('为我安排这一练 →')
    d=draft()
    check(d['intensity']=='MEDIUM' and not d['limited'], 'Manual daily overrides low default')
    check(prefs()['intensity']=='LOW' and prefs()['quickIntensityOverrideV2']=='MEDIUM', 'Generation preserves low default and explicit medium choice')
    check(any(i['rpe']=='7-8' for i in d['items']), 'Manual medium reaches actual RPE prescription')
    snapshot('manual-medium-default-low')
    stop();launch();tap('查看课程 →');regenerate()
    check(draft()['intensity']=='MEDIUM' and prefs()['intensity']=='LOW','Manual selection survives restart and regeneration')
    tap('设置');tap('高');tap('今天');tap('重新安排');tap('为我安排这一练 →')
    check(draft()['intensity']=='MEDIUM' and prefs()['intensity']=='HIGH','Changing default does not override explicit selection')
    tap('‹ 回到今天');tap('重新安排');tap('恢复跟随默认强度');tap('为我安排这一练 →')
    check(draft()['intensity']=='HIGH','Follow default explicitly re-enables current high default')
    seed()
    tap('为我安排这一练 →');low=draft()
    tap('设置');tap('中');tap('今天');tap('重新安排');tap('为我安排这一练 →');medium=draft()
    check(medium['intensity']=='MEDIUM','Changing default low to medium affects next generated plan')
    check([i['id'] for i in low['items']] != [i['id'] for i in medium['items']], 'Low and medium choose different exercises with same equipment/time')
    check([i['rpe'] for i in low['items']] != [i['rpe'] for i in medium['items']], 'Low and medium use different prescriptions')
    snapshot('default-medium-regenerated')
    seed('LOW', 'MEDIUM',pain='SEVERE')
    tap('为我安排这一练 →');d=draft()
    check(d['limited'] and d['intensity']=='LOW' and '腰部伤痛设为急性' in d['safety'], 'Actual severe pain is respected and exact cause displayed')
    check(prefs()['quickIntensityOverrideV2']=='MEDIUM','Safety downgrade does not erase requested intensity')
    snapshot('specific-pain-reason')
    seed('LOW','MEDIUM',{'level':'BEGINNER','cap':'LOW','clearance':False})
    tap('为我安排这一练 →')
    check(draft()['intensity']=='MEDIUM','Legacy cap without positive safety screening does not silently override explicit choice')
    seed('LOW','MEDIUM',{'level':'BEGINNER','cap':'LOW','clearance':True,'date':'2026-08-01'})
    tap('为我安排这一练 →')
    check(draft()['intensity']=='LOW' and '2026-08-01' in draft()['safety'], 'Positive safety assessment retains limit with date and exact reason')
    tap('设置')
    check(any('当前评估（2026-08-01）' in value for value in texts())
          and '查看 / 修改' in texts() and '重新评估' in texts()
          and '删除体能评估' in texts(),
          'Settings exposes current assessment with modify, redo and delete actions')
    snapshot('assessment-management')
    tap('查看 / 修改')
    check(any('旧版评估' in value and '无法准确回填' in value for value in texts())
          and '保存评估修改' in texts(),
          'Legacy assessment can be reviewed and edited without invented answers')
    tap('返回')
    tap('删除体能评估'); tap('确认删除')
    check(not prefs().get('assessment') and not prefs().get('workoutDraft')
          and any('当前：未评估' in value for value in texts()),
          'Deleting assessment restores unassessed state and invalidates stale prepared workout')
    tap('今天'); tap('为我安排这一练 →')
    current = draft()
    check(current['intensity']=='MEDIUM' and not current['limited'] and '2026-08-01' not in current['safety'],
          'Next daily workout immediately stops using deleted assessment date and safety cap')
    editable = {'version':2,'level':'BEGINNER','cap':'LOW','clearance':True,'date':'2026-08-02',
                'input':{'heartCondition':False,'chestPainActivity':False,'chestPainRest':False,
                         'dizziness':False,'boneJointProblem':True,'bloodPressureMeds':False,
                         'otherReason':False,'trainingMonths':18,'weeklySessions':3,
                         'pushupMax':16,'plankSeconds':75,'squatCount60s':38}}
    seed('LOW','MEDIUM',editable); tap('设置'); tap('查看 / 修改')
    bone_label = '是否有会因运动加重的骨骼/关节问题？'
    bone = None
    for _ in range(8):
        bone = next((n for n in ui().iter('node') if n.get('text') == bone_label), None)
        if bone is not None: break
        adb('shell','input','swipe','500','1500','500','650','200')
    check(bone is not None and bone.get('checked') == 'true',
          'Saved assessment safety answers are restored into the modify form')
    tap(bone_label); tap('保存评估修改')
    saved = json.loads(prefs()['assessment'])
    check(not saved['clearance'] and not saved['input']['boneJointProblem']
          and [saved['input'][key] for key in ('trainingMonths','weeklySessions','pushupMax','plankSeconds','squatCount60s')]
          == [18,3,16,75,38],
          'Editing an assessment persists corrected safety answers without losing history or tests')
    seed('LOW');tap('自己安排');tap('中');tap('不知道练什么')
    check(draft()['intensity']=='MEDIUM' and prefs()['intensity']=='LOW','Custom workout manual medium also overrides default without rewriting it')
    seed('LOW')
    stop()
    root=ET.fromstring(adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml'))
    for node in list(root):
        if node.get('name')=='quickIntensityOverrideV2':root.remove(node)
    ET.SubElement(root,'boolean',name='quickGentle',value='false')
    write_state(ET.tostring(root,encoding='utf-8',xml_declaration=True));launch()
    tap('为我安排这一练 →')
    check(draft()['intensity']=='MEDIUM' and prefs()['intensity']=='LOW','Upgrade preserves legacy manually chosen daily mode above low default')
finally:
    write_state(original);launch()
