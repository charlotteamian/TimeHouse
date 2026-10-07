#!/usr/bin/env python3
"""Review eight: shoulder raise definitions, required benches and actual playback."""
from pathlib import Path
from io import BytesIO
from PIL import Image,ImageChops
exec(Path('scripts/qa_review_flow.py').read_text().split('\nstop()\noriginal =')[0])
new=['0309','0311'];ids=new+['0306','0307','0308','0260','0267']
names={e['id']:e['name_zh'] for e in json.loads(Path('app/src/main/assets/exercises_1324.json').read_text())['exercises']}
stop();original=adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml')
try:
    raw=adb('shell','am','instrument','-w','-e','catalog',','.join('dataset_1324_'+s for s in ids),'com.restartday.fitness.qa/.UiSnapshot').decode()
    match=re.search(r'INSTRUMENTATION_RESULT: catalog=(\S+)',raw);assert match,raw
    catalog=json.loads(base64.b64decode(match.group(1)));(out/'loaded-catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n');row=lambda x:catalog['dataset_1324_'+x]
    check(not any('dataset_1324_'+x in known for x in new),'Both repaired candidates remain unreviewed during initial validation')
    check('supportReviewInvalidation=1' in raw,'Support requirements still invalidate stale personal approval')
    check(all(row(x)['primary']==['三角肌'] and row(x)['patterns'][-1]=='辅助' and '垂直推' not in row(x)['patterns'] for x in new),'Shoulder raises target deltoids and remain accessory movements instead of presses')
    check(row('0311')['name']=='哑铃肩胛平面上举（拇指朝上）' and row('0311')['patterns'][0]=='肩胛平面上举','Scaption label and movement plane load correctly')
    check(all(not row(x)['isHold'] and not row(x)['perSide'] for x in new),'Both raises use bilateral repetitions, not holds or per-side timing')
    check(all(row(x)['shoulder']=='MEDIUM' and row(x)['lower_back']=='LOW' for x in new),'Shoulder screening and standing low-back load load correctly')
    check(all(not row(x)['available']['自重'] and row(x)['available']['哑铃'] for x in new),'Both raises require dumbbells and no extra support')
    check(all(row(x)['available']['哑铃|下斜训练凳'] and not row(x)['available']['哑铃|平板训练凳'] for x in ['0306','0307']) and row('0308')['available']['哑铃|平板训练凳'] and not row('0308')['available']['哑铃'],'Pending fly and extension variants also require the correct benches')
    for xid in new:
        item={'id':'dataset_1324_'+xid,'sets':1,'reps':'8','rpe':'7','rest':60,'kind':'REPS','hold':0,'perSide':False,'tempo':3,'reason':'','restAfter':0}
        workout={'version':1,'title':'本批动作播放核查','intensity':'MEDIUM','reason':'QA','safety':'QA','limited':False,'notes':[],'budget':0,'active':False,'items':[item]}
        state_with(reviewedOnlyV1=False,equipment='哑铃',workoutDraft=json.dumps(workout,ensure_ascii=False));tap('查看课程 →');tap('开始这一练 →')
        check(draft()['active'],names[xid]+' enters normal training with dumbbells')
        state_with(favorites='dataset_1324_'+xid);tap('动作库');tap('已标心');tap(names[xid]);check('暂停示范' in texts(),names[xid]+' detail plays its demonstration');snapshot(xid+'-detail')
        node=next(n for n in ui().iter('node') if n.get('class')=='android.widget.ImageView');bounds=tuple(map(int,re.findall(r'-?\d+',node.get('bounds'))));frames=[]
        for i in range(10):
            im=Image.open(BytesIO(adb('exec-out','screencap','-p'))).convert('RGB').crop(bounds);im.save(out/f'{xid}-play-{i}.png');frames.append(im);time.sleep(.3)
        check(any(ImageChops.difference(frames[0],im).getbbox() for im in frames[1:]),names[xid]+' changes poses throughout a captured Android loop')
        frames[0].save(out/f'{xid}-android-loop.gif',save_all=True,append_images=frames[1:],duration=400,loop=0)
        sheet=Image.new('RGB',(1200,600),'white')
        for i,n in enumerate([0,1,2,3,4,6,8,9]):sheet.paste(frames[n].resize((300,300)),((i%4)*300,(i//4)*300))
        sheet.save(out/f'{xid}-playback-contact.jpg')
    decoded=adb('shell','am','instrument','-w','-e','media',','.join('dataset_motion_'+x for x in new),'com.restartday.fitness.qa/.UiSnapshot').decode();check('decodedAnimations=2' in decoded,'Android decodes the original-pose repair and ImageGen repair as animations')
finally:
    write_state(original);launch()
