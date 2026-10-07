#!/usr/bin/env python3
"""Validate third-batch imported behavior and actual loop playback; restore preferences."""
from pathlib import Path
from io import BytesIO
from PIL import Image,ImageChops
exec(Path('scripts/qa_review_flow.py').read_text().split('\nstop()\noriginal =')[0])
ids=['0310','0383','0430','0285','0872','0630','3699']
names={e['id']:e['name_zh'] for e in json.loads(Path('app/src/main/assets/exercises_1324.json').read_text())['exercises']}
stop();original=adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml')
try:
    raw=adb('shell','am','instrument','-w','-e','catalog',','.join('dataset_1324_'+s for s in ids),'com.restartday.fitness.qa/.UiSnapshot').decode()
    matched=re.search(r'INSTRUMENTATION_RESULT: catalog=(\S+)',raw)
    assert matched,raw
    catalog=json.loads(base64.b64decode(matched.group(1)))
    (out/'loaded-catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    check(all(not row['isHold'] for row in catalog.values()),'All seven dynamic exercises use repetitions rather than static holds')
    check(catalog['dataset_1324_0430']['perSide'],'Single-arm overhead extension counts both sides')
    check(all(not catalog['dataset_1324_'+s]['perSide'] for s in ['0285','0630','3699']),'Alternating exercises use total alternating reps without doubling each side')
    check(catalog['dataset_1324_0310']['primary']==['三角肌'],'Front raise no longer declares biceps as a primary muscle')
    check(catalog['dataset_1324_0383']['lower_back']=='MEDIUM' and '髋铰链' not in catalog['dataset_1324_0383']['patterns'],'Bent-over fly carries back load without occupying the hip-hinge slot')
    check(all(catalog['dataset_1324_'+s]['shoulder']=='MEDIUM' and catalog['dataset_1324_'+s]['lower_back']=='MEDIUM' for s in ['0430','0630','3699']),'Overhead and high-support exercises expose shoulder and back load to screening')
    for xid in ids:
        state_with();tap('动作库');tap('复核筛选：全部状态');tap('已复核');tap(names[xid])
        check('暂停示范' in texts() and any('已复核' in t for t in texts()),names[xid]+' is playable in reviewed-only library')
        snapshot(xid+'-detail')
        if xid in ['0430','0285','0872','0630','3699']:
            node=next(n for n in ui().iter('node') if n.get('class')=='android.widget.ImageView' and int(re.findall(r'-?\d+',n.get('bounds'))[3])>int(re.findall(r'-?\d+',n.get('bounds'))[1]))
            bounds=tuple(map(int,re.findall(r'-?\d+',node.get('bounds'))));frames=[]
            for n in range(7):
                im=Image.open(BytesIO(adb('exec-out','screencap','-p'))).convert('RGB').crop(bounds);im.save(out/f'{xid}-play-{n}.png');frames.append(im);time.sleep(.3)
            check(any(ImageChops.difference(frames[0],im).getbbox() for im in frames[1:]),names[xid]+' changes pose during an actual loop')
    decoded=adb('shell','am','instrument','-w','-e','media',','.join('dataset_motion_'+s for s in ids),'com.restartday.fitness.qa/.UiSnapshot').decode()
    check('decodedAnimations=7' in decoded,'Android decodes all seven approved assets as animation')
finally:
    write_state(original);launch()
