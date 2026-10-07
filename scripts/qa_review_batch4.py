#!/usr/bin/env python3
"""Review-four regression: alternating press and corrected bench exercise labels."""
from pathlib import Path
from io import BytesIO
from PIL import Image,ImageChops
exec(Path('scripts/qa_review_flow.py').read_text().split('\nstop()\noriginal =')[0])
stop();original=adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml')
try:
    ids=['0286','0287','0288','0290','0291']
    raw=adb('shell','am','instrument','-w','-e','catalog',','.join('dataset_1324_'+s for s in ids),'com.restartday.fitness.qa/.UiSnapshot').decode()
    match=re.search(r'INSTRUMENTATION_RESULT: catalog=(\S+)',raw);assert match,raw
    catalog=json.loads(base64.b64decode(match.group(1)))
    (out/'loaded-catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    press=catalog['dataset_1324_0286']
    check(press['name']=='哑铃交替肩上推举' and '垂直推' in press['patterns'],'Alternating press has the correct movement name and pattern')
    check(not press['isHold'] and not press['perSide'],'Alternating presses count total reps rather than static holds or doubled sides')
    check(press['shoulder']=='MEDIUM' and press['lower_back']=='MEDIUM','Overhead press retains shoulder and back screening tags')
    expected={'0287':'哑铃坐姿阿诺德推举','0288':'哑铃仰卧上拉','0290':'哑铃坐姿肩上推举','0291':'哑铃触凳深蹲'}
    check(all(catalog['dataset_1324_'+s]['name']==name for s,name in expected.items()),'Four bench exercise names match their actual movement')
    state_with();tap('动作库');tap('复核筛选：全部状态');tap('已复核');tap('哑铃交替肩上推举')
    check('暂停示范' in texts() and any('已复核' in t for t in texts()),'Corrected press is playable from reviewed-only library')
    snapshot('alternating-press')
    node=next(n for n in ui().iter('node') if n.get('class')=='android.widget.ImageView')
    bounds=tuple(map(int,re.findall(r'-?\d+',node.get('bounds'))));frames=[]
    for i in range(7):
        im=Image.open(BytesIO(adb('exec-out','screencap','-p'))).convert('RGB').crop(bounds);im.save(out/f'press-play-{i}.png');frames.append(im);time.sleep(.3)
    check(any(ImageChops.difference(frames[0],im).getbbox() for im in frames[1:]),'Alternating press cycles through poses on Android')
    decoded=adb('shell','am','instrument','-w','-e','media','dataset_motion_0286','com.restartday.fitness.qa/.UiSnapshot').decode()
    check('decodedAnimations=1' in decoded,'Android decodes the repaired press as animation')
    ledger=json.loads(Path('app/src/main/assets/exercise_reviews.json').read_text())
    check(not any(e['id']=='dataset_1324_'+s for s in expected for e in ledger['reviewed']),'Correcting bench labels does not grant review approval')
finally:
    write_state(original);launch()
