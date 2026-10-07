#!/usr/bin/env python3
"""Review seven: actual loaded support conditions, training starts and complete playback."""
from pathlib import Path
from io import BytesIO
from PIL import Image,ImageChops
exec(Path('scripts/qa_review_flow.py').read_text().split('\nstop()\noriginal =')[0])
ids=['0138','0287','0139','0288','0140','0290','0251','0291','0253','0305']
new=['0287','0290','0253','0305']
names={e['id']:e['name_zh'] for e in json.loads(Path('app/src/main/assets/exercises_1324.json').read_text())['exercises']}
stop();original=adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml')
try:
    raw=adb('shell','am','instrument','-w','-e','catalog',','.join('dataset_1324_'+s for s in ids),'com.restartday.fitness.qa/.UiSnapshot').decode()
    match=re.search(r'INSTRUMENTATION_RESULT: catalog=(\S+)',raw);assert match,raw
    catalog=json.loads(base64.b64decode(match.group(1)))
    (out/'loaded-catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    row=lambda xid:catalog['dataset_1324_'+xid]
    check('supportReviewInvalidation=1' in raw,'Required support changes invalidate earlier personal review')
    check(all(row(x)['requiredEquipment']==['直立靠背训练凳'] and not row(x)['available']['哑铃'] and not row(x)['available']['直立靠背训练凳'] and row(x)['available']['哑铃|直立靠背训练凳'] and not row(x)['available']['哑铃|平板训练凳'] for x in ['0287','0290']),'Both seated presses require dumbbells AND an upright backrest bench')
    check(not row('0253')['available']['自重'] and not row('0253')['available']['单杠'] and row('0253')['available']['中立握引体架'],'Neutral pull-up requires its parallel handles, not a plain bar')
    check(all(not row(x)['available']['自重'] and row(x)['available']['单杠'] for x in ['0139','0140']) and not row('0251')['available']['自重'] and row('0251')['available']['双杠'],'Unreviewed pull-ups and dips also retain required apparatus filters')
    check(all(row(x)['available']['哑铃|平板训练凳'] and not row(x)['available']['哑铃'] for x in ['0288','0291']) and row('0305')['available']['哑铃|上斜训练凳'] and not row('0305')['available']['哑铃|平板训练凳'],'Flat and incline bench requirements remain distinct')
    check(all(not row(x)['isHold'] and not row(x)['perSide'] for x in new),'All four candidates use bilateral repetition counting')
    check(all(row(x)['primary']==['三角肌'] and row(x)['shoulder']=='MEDIUM' and row(x)['lower_back']=='MEDIUM' for x in ['0287','0290']),'Presses target deltoids and participate in shoulder-back screening')
    check(row('0253')['primary']==['背阔肌','上背'] and row('0305')['primary']==['斜方肌'] and all(row(x)['shoulder']=='MEDIUM' and row(x)['lower_back']=='MEDIUM' for x in ['0253','0305']),'Pull-up and shrug targets and joint screening match the movements')
    configs={'0287':'哑铃|直立靠背训练凳','0290':'哑铃|直立靠背训练凳','0253':'中立握引体架','0305':'哑铃|上斜训练凳'}
    for xid in new:
        item={'id':'dataset_1324_'+xid,'sets':1,'reps':'8','rpe':'7','rest':60,'kind':'REPS','hold':0,'perSide':False,'tempo':3,'reason':'','restAfter':0}
        workout={'version':1,'title':'本批动作播放核查','intensity':'MEDIUM','reason':'QA','safety':'QA','limited':False,'notes':[],'budget':0,'active':False,'items':[item]}
        state_with(reviewedOnlyV1=False,equipment='自重|哑铃',workoutDraft=json.dumps(workout,ensure_ascii=False))
        tap('查看课程 →');tap('开始这一练 →')
        check('还缺少必需器械' in texts() and not draft()['active'],names[xid]+' cannot start without its support')
        state_with(reviewedOnlyV1=False,equipment=configs[xid],workoutDraft=json.dumps(workout,ensure_ascii=False))
        tap('查看课程 →');tap('开始这一练 →')
        check(draft()['active'],names[xid]+' can enter training with the correct equipment')
        # Use the real library detail without granting a temporary review approval.
        state_with(favorites='dataset_1324_'+xid)
        tap('动作库');tap('已标心')
        tap(names[xid])
        check('暂停示范' in texts(),names[xid]+' detail plays its demonstration')
        snapshot(xid+'-detail')
        node=next(n for n in ui().iter('node') if n.get('class')=='android.widget.ImageView')
        bounds=tuple(map(int,re.findall(r'-?\d+',node.get('bounds'))));frames=[]
        for i in range(10):
            im=Image.open(BytesIO(adb('exec-out','screencap','-p'))).convert('RGB').crop(bounds);im.save(out/f'{xid}-play-{i}.png');frames.append(im);time.sleep(.3)
        check(any(ImageChops.difference(frames[0],im).getbbox() for im in frames[1:]),names[xid]+' changes poses through a captured Android loop')
        frames[0].save(out/f'{xid}-android-loop.gif',save_all=True,append_images=frames[1:],duration=400,loop=0)
        sheet=Image.new('RGB',(1200,600),'white')
        for i,n in enumerate([0,1,2,3,4,6,8,9]):sheet.paste(frames[n].resize((300,300)),((i%4)*300,(i//4)*300))
        sheet.save(out/f'{xid}-playback-contact.jpg')
    decoded=adb('shell','am','instrument','-w','-e','media',','.join('dataset_motion_'+x for x in new),'com.restartday.fitness.qa/.UiSnapshot').decode()
    check('decodedAnimations=4' in decoded,'Android decodes all four candidates as animations')
finally:
    write_state(original);launch()
