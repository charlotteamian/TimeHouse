#!/usr/bin/env python3
"""Review nine: independent catalog expectations, supporting apparatus and real loops."""
from pathlib import Path
from io import BytesIO
from PIL import Image,ImageChops,ImageOps
exec(Path('scripts/qa_review_flow.py').read_text().split('\nstop()\noriginal =')[0])
new=['0277','0312','0315','0317']; ids=new+['0279','0282','0284','0314','0316','0443']
names={e['id']:e['name_zh'] for e in json.loads(Path('app/src/main/assets/exercises_1324.json').read_text())['exercises']}
stop(); original=adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml')
try:
    raw=adb('shell','am','instrument','-w','-e','catalog',','.join('dataset_1324_'+s for s in ids),'com.restartday.fitness.qa/.UiSnapshot').decode()
    match=re.search(r'INSTRUMENTATION_RESULT: catalog=(\S+)',raw); assert match,raw
    catalog=json.loads(base64.b64decode(match.group(1))); (out/'loaded-catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n'); row=lambda x:catalog['dataset_1324_'+x]
    check(not any('dataset_1324_'+x in known for x in new),'All four candidates remain unreviewed during initial validation')
    check('supportReviewInvalidation=1' in raw,'Changed supporting equipment invalidates stale personal approval')
    check(row('0277')['primary']==['腹肌'] and row('0312')['primary']==['肱二头肌','前臂'] and all(row(x)['primary']==['肱二头肌'] for x in ['0315','0317']),'Sit-up and curl primary muscle groups match their actual variants')
    check(row('0277')['patterns']==['核心','躯干屈曲'] and row('0312')['patterns']==['屈肘','站姿稳定','辅助'] and all(row(x)['patterns']==['屈肘','辅助'] for x in ['0315','0317']),'Loaded movement patterns distinguish sit-up, standing curl and supported curls')
    check(all(not row(x)['isHold'] and not row(x)['perSide'] and row(x)['knee']=='NONE' for x in new),'Four bilateral repetition prescriptions and knee screening load correctly')
    check(row('0277')['lower_back']=='MEDIUM' and row('0277')['shoulder']=='NONE','Decline sit-up loads conservative back screening')
    check(row('0312')['lower_back']=='LOW' and row('0312')['shoulder']=='MEDIUM','Standing hammer curl retains standing back and shoulder screening')
    check(all(row(x)['lower_back']=='NONE' and row(x)['shoulder']=='MEDIUM' for x in ['0315','0317']),'Supported curls load the intended shoulder screening and supported back profile')
    check(not row('0312')['available']['自重'] and row('0312')['available']['哑铃'] and row('0312')['requiredEquipment']==[],'Hammer curl requires dumbbells without extra apparatus')
    check(all(row(x)['requiredEquipment']==['带勾脚的下斜训练凳'] and row(x)['available']['带勾脚的下斜训练凳'] and not row(x)['available']['自重'] and not row(x)['available']['哑铃|下斜训练凳'] for x in ['0277','0282']),'Decline sit-ups require the hooked-foot bench, not bodyweight alone or a generic bench')
    check(all(row(x)['requiredEquipment']==['上斜训练凳'] and row(x)['available']['哑铃|上斜训练凳'] and not row(x)['available']['上斜训练凳'] and not row(x)['available']['哑铃'] and not row(x)['available']['哑铃|平板训练凳'] for x in ['0315','0317']),'Both incline curls require dumbbells AND the correct incline bench')
    check(all(row(x)['available']['哑铃|上斜训练凳'] and not row(x)['available']['哑铃'] and not row(x)['available']['哑铃|平板训练凳'] for x in ['0314','0316']),'Pending incline presses still enforce their bench requirements')
    check(row('0279')['available']['稳固踏台'] and not row('0279')['available']['自重'],'Pending decline push-up requires its stable platform')
    check(row('0284')['name']=='扶墙台阶提踵' and row('0284')['available']['稳固踏台|墙面'] and not any(row('0284')['available'][x] for x in ['自重','稳固踏台','墙面']),'Wall-supported calf raise requires both wall AND platform')
    configs={'0277':'带勾脚的下斜训练凳','0312':'哑铃','0315':'哑铃|上斜训练凳','0317':'哑铃|上斜训练凳'}
    for xid in new:
        item={'id':'dataset_1324_'+xid,'sets':1,'reps':'8','rpe':'7','rest':60,'kind':'REPS','hold':0,'perSide':False,'tempo':3,'reason':'','restAfter':0}
        workout={'version':1,'title':'本批动作播放核查','intensity':'MEDIUM','reason':'QA','safety':'QA','limited':False,'notes':[],'budget':0,'active':False,'items':[item]}
        if xid!='0312':
            state_with(reviewedOnlyV1=False,equipment='自重|哑铃',workoutDraft=json.dumps(workout,ensure_ascii=False));tap('查看课程 →');tap('开始这一练 →')
            check('还缺少必需器械' in texts() and not draft()['active'],names[xid]+' cannot start without its supporting bench')
        state_with(reviewedOnlyV1=False,equipment=configs[xid],workoutDraft=json.dumps(workout,ensure_ascii=False));tap('查看课程 →');tap('开始这一练 →')
        check(draft()['active'],names[xid]+' enters normal training with the correct equipment')
        state_with(favorites='dataset_1324_'+xid);tap('动作库');tap('已标心');tap(names[xid]);check('暂停示范' in texts(),names[xid]+' detail plays its demonstration');snapshot(xid+'-detail')
        node=next(n for n in ui().iter('node') if n.get('class')=='android.widget.ImageView');bounds=tuple(map(int,re.findall(r'-?\d+',node.get('bounds'))));frames=[]
        for i in range(10):
            im=Image.open(BytesIO(adb('exec-out','screencap','-p'))).convert('RGB').crop(bounds);im.save(out/f'{xid}-play-{i}.png');frames.append(im);time.sleep(.3)
        check(any(ImageChops.difference(frames[0],im).getbbox() for im in frames[1:]),names[xid]+' changes poses throughout a captured Android loop')
        frames[0].save(out/f'{xid}-android-loop.gif',save_all=True,append_images=frames[1:],duration=400,loop=0)
        sheet=Image.new('RGB',(1200,600),'white')
        for i,n in enumerate([0,1,2,3,4,6,8,9]):sheet.paste(ImageOps.pad(frames[n],(300,300),color='white'),((i%4)*300,(i//4)*300))
        sheet.save(out/f'{xid}-playback-contact.jpg')
    decoded=adb('shell','am','instrument','-w','-e','media',','.join('dataset_motion_'+x for x in new),'com.restartday.fitness.qa/.UiSnapshot').decode();check('decodedAnimations=4' in decoded,'Android decodes all four candidates as animations')
finally:
    write_state(original);launch()
