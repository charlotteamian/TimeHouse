#!/usr/bin/env python3
"""Review six: required supports, saved workouts, fingerprints and playback."""
from pathlib import Path
from io import BytesIO
from PIL import Image,ImageChops
exec(Path('scripts/qa_review_flow.py').read_text().split('\nstop()\noriginal =')[0])
ids=['0129','0304','0292','0020','0301','0302','0303','0130','0299']
names={e['id']:e['name_zh'] for e in json.loads(Path('app/src/main/assets/exercises_1324.json').read_text())['exercises']}
stop();original=adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml')
try:
    raw=adb('shell','am','instrument','-w','-e','catalog',','.join('dataset_1324_'+s for s in ids),'com.restartday.fitness.qa/.UiSnapshot').decode()
    match=re.search(r'INSTRUMENTATION_RESULT: catalog=(\S+)',raw);assert match,raw
    catalog=json.loads(base64.b64decode(match.group(1)))
    (out/'loaded-catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    row=lambda xid:catalog['dataset_1324_'+xid]
    check('supportReviewInvalidation=1' in raw,'Changing required supports invalidates earlier personal approval')
    check(row('0292')['requiredEquipment']==['平板训练凳'] and not row('0292')['available']['哑铃'] and not row('0292')['available']['平板训练凳'] and row('0292')['available']['哑铃|平板训练凳'],'Loaded row requires dumbbells and bench together')
    check(not row('0129')['available']['自重'] and row('0129')['available']['平板训练凳'],'Bodyweight dip cannot bypass bench requirement')
    check(not row('0304')['available']['哑铃|平板训练凳'] and row('0304')['available']['哑铃|上斜训练凳'],'Incline support is distinct from flat bench')
    check(all(not row(x)['available']['哑铃|平板训练凳'] and row(x)['available']['哑铃|下斜训练凳'] for x in ['0301','0302','0303']),'Decline movements require the correct bench configuration')
    check(row('0020')['requiredEquipment']==['平衡板'] and not row('0020')['available']['自重'],'Balance board is not treated as equipment-free')
    check(row('0292')['perSide'] and not row('0129')['perSide'] and not row('0304')['perSide'] and all(not row(x)['isHold'] for x in ['0292','0129','0304']),'Unilateral row and bilateral exercises retain correct repetition timing')
    check(row('0129')['primary']==['肱三头肌'] and row('0304')['primary']==['斜方肌'] and all(row(x)['shoulder']=='MEDIUM' for x in ['0129','0304','0292']) and row('0299')['lower_back']=='MEDIUM','Reviewed targets and shoulder-back screening match the movements')
    item={'id':'dataset_1324_0292','sets':1,'reps':'10','rpe':'7','rest':60,'kind':'REPS','hold':0,'perSide':True,'tempo':3,'reason':'','restAfter':0}
    routine={'version':1,'id':'qa_bench','name':'扶凳复核测试','note':'','circuit':False,'rounds':1,'roundRest':0,'items':[item]}
    state_with(reviewedOnlyV1=True,equipment='哑铃',routinesV1=json.dumps([routine],ensure_ascii=False))
    tap('我的动作组 · 保存组合直接练');tap('练这组 →')
    check('先检查动作组' in texts() and any('平板训练凳' in t for t in texts()),'Saved routine explains missing required bench')
    old={'version':1,'title':'扶凳复核测试','intensity':'MEDIUM','reason':'QA','safety':'QA','limited':False,'notes':[],'budget':0,'active':False,'items':[item]}
    state_with(reviewedOnlyV1=True,equipment='哑铃',workoutDraft=json.dumps(old,ensure_ascii=False))
    tap('查看课程 →');tap('开始这一练 →')
    check('还缺少必需器械' in texts() and not draft()['active'],'Old workout draft cannot start without required support')
    state_with(reviewedOnlyV1=True,equipment='哑铃|平板训练凳',workoutDraft=json.dumps(old,ensure_ascii=False))
    tap('查看课程 →');tap('开始这一练 →')
    check(draft()['active'],'Reviewed row starts normally with dumbbells and bench')
    state_with(equipment='哑铃');tap('设置');tap('平板训练凳');stop();launch()
    check('平板训练凳' in prefs().get('equipment',''),'Required bench can be enabled in settings and persists')
    for xid in ['0129','0304','0292']:
        state_with();tap('动作库')
        tap('复核筛选：全部状态');tap('已复核')
        tap(names[xid]);check('暂停示范' in texts(),names[xid]+' detail plays its demonstration')
        snapshot(xid+'-detail')
        node=next(n for n in ui().iter('node') if n.get('class')=='android.widget.ImageView')
        bounds=tuple(map(int,re.findall(r'-?\d+',node.get('bounds'))));frames=[]
        for i in range(10):
            im=Image.open(BytesIO(adb('exec-out','screencap','-p'))).convert('RGB').crop(bounds);im.save(out/f'{xid}-play-{i}.png');frames.append(im);time.sleep(.3)
        check(any(ImageChops.difference(frames[0],im).getbbox() for im in frames[1:]),names[xid]+' changes poses throughout a captured Android loop')
        frames[0].save(out/f'{xid}-android-loop.gif',save_all=True,append_images=frames[1:],duration=400,loop=0)
        sheet=Image.new('RGB',(1200,600),'white')
        for i,n in enumerate([0,1,2,3,4,6,8,9]):sheet.paste(frames[n].resize((300,300)),((i%4)*300,(i//4)*300))
        sheet.save(out/f'{xid}-playback-contact.jpg')
    decoded=adb('shell','am','instrument','-w','-e','media','dataset_motion_0129,dataset_motion_0304,dataset_motion_0292','com.restartday.fitness.qa/.UiSnapshot').decode()
    check('decodedAnimations=3' in decoded,'Android decodes all three newly reviewed assets as animations')
finally:
    write_state(original);launch()
