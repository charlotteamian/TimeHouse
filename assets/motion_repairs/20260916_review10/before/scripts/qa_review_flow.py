#!/usr/bin/env python3
"""Emulator-only review, playback and training-scope regression; restores preferences."""
from pathlib import Path
exec(Path('scripts/qa_today_flow.py').read_text().split('\nstop()\noriginal =')[0])
known={r['id'] for r in json.loads(Path('app/src/main/assets/exercise_reviews.json').read_text())['reviewed']}
review_count=len(known)
total=1355

def state_with(**values):
    root = ET.Element('map')
    ET.SubElement(root,'boolean',name='aiEnabled',value='false')
    ET.SubElement(root,'boolean',name='voiceEnabled',value='false')
    for key,value in values.items():
        if isinstance(value,bool): ET.SubElement(root,'boolean',name=key,value=str(value).lower())
        else: ET.SubElement(root,'string',name=key).text=value
    write_state(ET.tostring(root,encoding='utf-8',xml_declaration=True)); launch()

stop()
original = adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml')
try:
    state_with(verified='custom_inverted_row_unverified')
    tap('动作库')
    check(any(f'已复核 {review_count} · 未复核 {total-review_count}' in s for s in texts()), 'Only explicit reviews; legacy verification is not migrated')
    snapshot('library-initial')
    tap('复核筛选：全部状态'); tap('已复核')
    check(any(f'共 {review_count} 个' in s for s in texts()), 'Library review filter contains exactly the reviewed baseline')
    snapshot('reviewed-library')
    time.sleep(.8)
    snapshot('reviewed-library-later')
    tap('哑铃弯举')
    tap('暂停示范')
    check('播放示范' in texts(), 'Detail demonstration can be paused')
    snapshot('paused-detail')
    tap('复核这个动作')
    check(any(n.get('text')=='标为已复核' and n.get('enabled')=='false' for n in ui().iter('node')), 'Approval requires all four checklist items')
    tap('标为未复核'); tap('待修图 · 重影或姿势异常')
    check(any(f'已复核 {review_count-1} · 未复核 {total-review_count+1}' in s for s in texts()), 'Personal rejection overrides bundled approval')
    stop(); launch(); tap('动作库')
    tap('复核筛选：全部状态'); tap('待修图')
    check('哑铃弯举' in texts(), 'Repair reason and rejected review survive restart')
    tap('哑铃弯举'); tap('复核这个动作')
    for label in ['名称、器械和目标肌群一致','文字步骤与动作逻辑一致','示范姿势、支撑点和顺序正确','完整看过播放，无明显重影或错图']:
        tap(label)
    tap('标为已复核')
    check(json.loads(prefs()['exerciseReviewsV1'])['dataset_1324_0294']['approved'], 'Explicit personal approval is persisted')
    state_with(reviewedOnlyV1=True,equipment='自重|哑铃')
    tap('为我安排这一练 →')
    planned = draft()['items']
    check(planned and all(x['id'] in known for x in planned), 'Quick training draws only from reviewed exercises')
    snapshot('reviewed-workout')
    tap('开始这一练 →')
    snapshot('start-attempt')
    check(draft()['active'], 'Reviewed workout enters normal session flow')
    snapshot('reviewed-session')
    state_with(reviewedOnlyV1=True,equipment='壶铃',shoulderPain='SEVERE',lowerBackPain='SEVERE',kneePain='SEVERE')
    tap('为我安排这一练 →')
    check(not draft().get('items'), 'No silent fallback to unreviewed exercises when safe pool is empty')
    check(any('复核范围' in s for s in texts()), 'Empty candidate pool provides actionable explanation')
    old={'version':1,'title':'旧训练','intensity':'MEDIUM','reason':'QA','safety':'QA','limited':False,'notes':[],'budget':0,'active':False,'items':[
        {'id':'exercise_kettlebell_deadlift','sets':1,'reps':'12','rpe':'7','rest':90,'kind':'REPS','hold':0,'perSide':False,'tempo':3,'reason':'','restAfter':0}]}
    state_with(reviewedOnlyV1=True,workoutDraft=json.dumps(old,ensure_ascii=False))
    tap('查看课程 →'); tap('开始这一练 →')
    check('这套训练含未复核动作' in texts() and not draft()['active'], 'Old saved draft cannot bypass reviewed-only start gate')
    # Same exercise id with a changed media override must lose its previous review.
    state_with(mediaOverrides=json.dumps({'dataset_1324_0294':'raw:dataset_motion_0662'}))
    tap('动作库')
    check(any(f'已复核 {review_count-1} · 未复核 {total-review_count+1}' in s for s in texts()), 'Changing media invalidates a bundled review')
    snapshot('changed-media')
finally:
    write_state(original); launch()
