#!/usr/bin/env python3
"""Observe real cover playback and reviewed TRX selection on the emulator."""
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageChops
exec(Path('scripts/qa_review_flow.py').read_text().split('\nstop()\noriginal =')[0])

def visible_cover():
    for attempt in range(5):
        for node in ui().iter('node'):
            if node.get('content-desc')=='动态封面，点开查看示范':
                bounds=tuple(map(int,re.findall(r'-?\d+',node.get('bounds'))))
                if bounds[2]>bounds[0] and bounds[3]-bounds[1]>100:
                    return bounds
        width,height=map(int,re.findall(r'(\d+)x(\d+)',adb('shell','wm','size').decode())[-1])
        adb('shell','input','swipe',str(width//2),str(int(height*.75)),str(width//2),str(int(height*.35)),'300')
    raise AssertionError('No visible dynamic cover')

def cover_moves(label):
    bounds=visible_cover(); captured=[]
    for i in range(7):
        im=Image.open(BytesIO(adb('exec-out','screencap','-p'))).convert('RGB').crop(bounds)
        im.save(out/f'{label}-{i}.png');captured.append(im)
        time.sleep(.29)
    check(any(ImageChops.difference(captured[0],im).getbbox() for im in captured[1:]),label)

stop();original=adb('exec-out','run-as',pkg,'cat','shared_prefs/fitness_state.xml')
try:
    state_with()
    tap('动作库');tap('复核筛选：全部状态');tap('已复核')
    cover_moves('Library covers actually change poses')
    adb('shell','input','keyevent','3');time.sleep(.4);launch()
    cover_moves('Covers resume after background return')
    tap('复核筛选：已复核');tap('待修图')
    repair_count=sum(r['note'].startswith('待修图') for r in json.loads(Path('app/src/main/assets/exercise_reviews.json').read_text())['pending'])
    check(any(f'共 {repair_count} 个' in s for s in texts()),'Inspected drift problems are queued for repair')
    snapshot('repair-queue')
    state_with(reviewedOnlyV1=True,equipment='TRX 悬挂带|自重')
    tap('为我安排这一练 →')
    planned=draft()['items']
    check(any(x['id']=='dataset_1324_0808' for x in planned),'Reviewed TRX row enters TRX workout')
    rows=json.loads(Path('app/src/main/assets/exercises_1324.json').read_text())['exercises']
    available_supports={'TRX 悬挂带','自重'}
    allowed={'dataset_1324_'+r['id'] for r in rows if r['equipment'] in {'body weight','suspension trainer'} and set(r.get('required_equipment_zh',[])) <= available_supports} & known
    check(planned and all(x['id'] in allowed for x in planned),'TRX selection does not include dumbbells or misclassified rings/bar')
    snapshot('trx-workout')
    tap('开始这一练 →')
    cover_moves('Active workout retains dynamic covers')
    state_with()
    tap('动作库')
    tap('搜索动作、肌群或器械');adb('shell','input','text','TRX');tap('搜索')
    check(any('共 4 个' in s for s in texts()),'TRX search contains three corrected dataset movements plus one seed')
    tap('复核筛选：全部状态');tap('已复核')
    check(any('共 1 个' in s for s in texts()) and '悬挂带划船' in texts(),'TRX and reviewed filters combine correctly')
    tap('悬挂带划船');snapshot('trx-detail')
    check(any('TRX 悬挂带' in s for s in texts()),'Reviewed row declares the required TRX equipment')
    decoded=adb('shell','am','instrument','-w','-e','media','dataset_motion_0426,dataset_motion_0808','com.restartday.fitness.qa/.UiSnapshot').decode()
    check('decodedAnimations=2' in decoded,'Android decodes both repaired assets as animation')
finally:
    write_state(original);launch()
