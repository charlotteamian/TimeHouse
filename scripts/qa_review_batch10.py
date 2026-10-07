#!/usr/bin/env python3
"""Batch ten candidates: catalog semantics, required supports, real loops and review gate."""
from pathlib import Path
from io import BytesIO
from PIL import Image,ImageChops,ImageOps
exec(Path('scripts/qa_review_flow.py').read_text().split('\nstop()\noriginal =')[0])
new=['0318','0320','0322'];ids=new+['0456','0457','0319','0459','0464','0321','0466']
names={e['id']:e['name_zh'] for e in json.loads(Path('app/src/main/assets/exercises_1324.json').read_text())['exercises']}
stop();original=adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml');(out/'original-prefs.xml').write_bytes(original)
try:
    raw=adb('shell','am','instrument','-w','-e','catalog',','.join('dataset_1324_'+s for s in ids),'com.restartday.fitness.qa/.UiSnapshot').decode()
    match=re.search(r'INSTRUMENTATION_RESULT: catalog=(\S+)',raw);assert match,raw
    catalog=json.loads(base64.b64decode(match.group(1)));(out/'loaded-catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n');row=lambda x:catalog['dataset_1324_'+x]
    check(not any('dataset_1324_'+x in known for x in new),'All three candidates remain unreviewed during initial checks')
    check('supportReviewInvalidation=1' in raw,'Supporting equipment changes invalidate stale personal approval')
    check(all(row(x)['primary']==['肱二头肌'] for x in new),'Curl primary muscle groups are biceps; forearms remain secondary')
    check(all(row(x)['patterns']==['屈肘','辅助'] for x in new),'Supported curls use elbow-flexion accessory patterns')
    check(all(not row(x)['isHold'] and not row(x)['perSide'] for x in new),'All three synchronous curls use bilateral repetitions')
    check(all(row(x)['shoulder']=='MEDIUM' and row(x)['lower_back']=='NONE' and row(x)['knee']=='NONE' for x in new),'Supported curls retain medium shoulder and supported back/knee screening')
    check(all(row(x)['requiredEquipment']==['上斜训练凳'] and row(x)['available']['哑铃|上斜训练凳'] for x in new),'Candidates load the required incline bench and dumbbell combination')
    check(all(not any(row(x)['available'][c] for c in ['自重','哑铃','上斜训练凳','哑铃|平板训练凳']) for x in new),'Missing dumbbells or the correct bench excludes each candidate')
    check(all(row(x)['requiredEquipment']==['上斜训练凳'] and not row(x)['available']['哑铃'] for x in ['0319','0321']),'Pending fly and press also require the incline bench')
    check(row('0459')['name']=='凳上俯卧交替打腿' and row('0459')['primary']==['臀肌'] and row('0459')['lower_back']=='MEDIUM' and row('0459')['available']['平板训练凳'] and not row('0459')['available']['自重'],'Prone flutter corrects position, target, back screening and bench requirement')
    check(row('0466')['requiredEquipment']==['单杠'] and row('0466')['available']['单杠'] and not row('0466')['available']['自重'],'Sternum chin-up requires its pull-up bar')
    for xid in new:
        state_with(favorites='dataset_1324_'+xid);tap('动作库');tap('已标心');tap(names[xid]);check('暂停示范' in texts() and any('未复核' in s for s in texts()),names[xid]+' plays while retaining its unreviewed label');snapshot(xid+'-detail')
        node=next(n for n in ui().iter('node') if n.get('class')=='android.widget.ImageView');bounds=tuple(map(int,re.findall(r'-?\d+',node.get('bounds'))));frames=[]
        for i in range(12):
            im=Image.open(BytesIO(adb('exec-out','screencap','-p'))).convert('RGB').crop(bounds);im.save(out/f'{xid}-play-{i}.png');frames.append(im);time.sleep(.28)
        check(any(ImageChops.difference(frames[0],im).getbbox() for im in frames[1:]),names[xid]+' changes poses during captured Android loops')
        frames[0].save(out/f'{xid}-android-loop.gif',save_all=True,append_images=frames[1:],duration=400,loop=0)
        sheet=Image.new('RGB',(1200,900),'white')
        for i,f in enumerate(frames):sheet.paste(ImageOps.pad(f,(300,300),color='white'),((i%4)*300,(i//4)*300))
        sheet.save(out/f'{xid}-playback-contact.jpg')
        item={'id':'dataset_1324_'+xid,'sets':1,'reps':'8','rpe':'7','rest':30,'kind':'REPS','hold':0,'perSide':False,'tempo':3,'reason':'','restAfter':0}
        workout={'version':1,'title':'候选门控核查','intensity':'MEDIUM','reason':'QA','safety':'QA','limited':False,'notes':[],'budget':0,'active':False,'items':[item]}
        state_with(reviewedOnlyV1=False,equipment='哑铃|上斜训练凳',workoutDraft=json.dumps(workout,ensure_ascii=False))
        check(not draft() and prefs().get('unreviewedWorkoutDraft'),names[xid]+' cannot bypass 1.2.14 mandatory review gate')
    decoded=adb('shell','am','instrument','-w','-e','media',','.join('dataset_motion_'+x for x in new),'com.restartday.fitness.qa/.UiSnapshot').decode();check('decodedAnimations=3' in decoded,'Android decodes all three candidate demonstrations as animations')
finally:
    write_state(original);launch()
