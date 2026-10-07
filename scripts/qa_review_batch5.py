#!/usr/bin/env python3
"""Exercise-five checks: per-side prescriptions, metadata, and real Android loops."""
from pathlib import Path
from io import BytesIO
from PIL import Image,ImageChops
exec(Path('scripts/qa_review_flow.py').read_text().split('\nstop()\noriginal =')[0])
ids=['1427','0298','0001','0292','0295','0296','0297']
names={e['id']:e['name_zh'] for e in json.loads(Path('app/src/main/assets/exercises_1324.json').read_text())['exercises']}
stop();original=adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml')
try:
    raw=adb('shell','am','instrument','-w','-e','catalog',','.join('dataset_1324_'+s for s in ids),'com.restartday.fitness.qa/.UiSnapshot').decode()
    match=re.search(r'INSTRUMENTATION_RESULT: catalog=(\S+)',raw);assert match,raw
    catalog=json.loads(base64.b64decode(match.group(1)))
    (out/'loaded-catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    row=lambda xid:catalog['dataset_1324_'+xid]
    check(all(row(x)['perSide'] for x in ['1427','0298','0297']),'Hip abduction and unilateral curls count both sides')
    check(all(not row(x)['isHold'] for x in ids),'All corrected movements retain dynamic repetition timing')
    check('髋外展' in row('1427')['patterns'] and '髋外展肌群' in row('1427')['primary'] and row('1427')['knee']=='MEDIUM','Hip abduction retains its movement target and conservative leg screening')
    check(row('0298')['primary']==['肱二头肌','肱肌'] and row('0298')['shoulder']=='MEDIUM','Cross-body curl uses elbow-flexor targets and shoulder screening')
    check(row('0001')['primary']==['腹肌'] and not row('0001')['perSide'] and row('0001')['lower_back']=='MEDIUM','Sit-up uses total repetitions and retains back screening')
    check('背阔肌' in row('0292')['primary'] and row('0292')['lower_back']=='MEDIUM','Supported row no longer treats biceps as the main back muscle')
    check(row('0295')['name']=='哑铃翻举' and row('0296')['name']=='哑铃窄握卧推','Clean and close-grip bench press names match their intended movement')
    pending=['0001','0292','1428','0295','3016','0296','0297','0002']
    check(all('dataset_1324_'+x not in known for x in pending) and all('dataset_1324_'+x in known for x in ['1427','0298']),'Only the two fully reviewed candidates gain approval')
    for xid in ['1427','0298','0001']:
        state_with();tap('动作库')
        if xid!='0001':tap('复核筛选：全部状态');tap('已复核')
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
    decoded=adb('shell','am','instrument','-w','-e','media','dataset_motion_1427,dataset_motion_0298,dataset_motion_0001','com.restartday.fitness.qa/.UiSnapshot').decode()
    check('decodedAnimations=3' in decoded,'Android decodes all three repaired assets as animation')
finally:
    write_state(original);launch()
