#!/usr/bin/env python3
"""Emulator-only UI regression. Preserves and restores the original app preferences."""
import argparse
import base64
import json
import re
import shlex
import subprocess
import time
import xml.etree.ElementTree as ET
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--serial', required=True)
parser.add_argument('--adb', default=str(Path.home() / 'Library/Android/sdk/platform-tools/adb'))
parser.add_argument('--output', default='build/qa-20260909-routines')
a = parser.parse_args()
if not a.serial.startswith('emulator-'):
    raise SystemExit('This test only runs on an explicitly selected emulator.')
out = Path(a.output)
out.mkdir(parents=True, exist_ok=True)
pkg = 'com.restartday.fitness'
checks = []

def adb(*args, data=None):
    return subprocess.run([a.adb, '-s', a.serial, *args], input=data,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=30).stdout

def prefs():
    root = ET.fromstring(adb('exec-out', 'run-as', pkg, 'cat', 'shared_prefs/fitness_state.xml'))
    return {x.get('name'): x.text if x.tag == 'string' else x.get('value') for x in root}

def draft():
    return json.loads(prefs().get('workoutDraft') or '{}')

def launch():
    adb('shell', 'am', 'start', '-W', '-n', pkg + '/.app.MainActivity')
    time.sleep(.6)

def stop():
    adb('shell', 'am', 'force-stop', pkg)

def write_state(raw):
    stop()
    adb('shell', 'run-as', pkg, 'mkdir', '-p', 'shared_prefs')
    adb('shell', 'run-as', pkg, 'sh', '-c', shlex.quote('cat > shared_prefs/fitness_state.xml'), data=raw)

def fixture(workout=None):
    root = ET.Element('map')
    ET.SubElement(root, 'boolean', name='aiEnabled', value='false')
    ET.SubElement(root, 'boolean', name='voiceEnabled', value='false')
    ET.SubElement(root, 'string', name='records').text = '[]'
    if workout:
        ET.SubElement(root, 'string', name='workoutDraft').text = json.dumps(workout, ensure_ascii=False)
    write_state(ET.tostring(root, encoding='utf-8', xml_declaration=True))
    launch()

def ui():
    result = adb('shell', 'am', 'instrument', '-w',
                 'com.restartday.fitness.qa/.UiSnapshot').decode()
    match = re.search(r'INSTRUMENTATION_RESULT: ui=(\S+)', result)
    if not match:
        raise AssertionError('Snapshot failed: ' + result)
    return ET.fromstring(base64.b64decode(match.group(1)))

def texts():
    return [n.get('text', '') for n in ui().iter('node')]

def visible_node(label, swipes=0):
    for attempt in range(swipes + 1):
        for n in ui().iter('node'):
            if n.get('text') == label or n.get('content-desc') == label:
                x1, y1, x2, y2 = map(int, re.findall(r'-?\d+', n.get('bounds')))
                if x2 > x1 and y2 > y1:
                    return n, (x1, y1, x2, y2)
        if attempt < swipes:
            adb('shell', 'input', 'swipe', '500', '1550', '500', '650', '220')
    raise AssertionError('Missing visible UI control: ' + label)

def tap(label):
    for attempt in range(5):
        for n in ui().iter('node'):
            if n.get('text') == label or n.get('content-desc') == label:
                x1, y1, x2, y2 = map(int, re.findall(r'-?\d+', n.get('bounds')))
                if y2 > y1 and x2 > x1:
                    adb('shell', 'input', 'tap', str((x1+x2)//2), str((y1+y2)//2))
                    time.sleep(.2)
                    return
        size = re.findall(r'(\d+)x(\d+)', adb('shell', 'wm', 'size').decode())[-1]
        width, height = map(int, size)
        adb('shell', 'input', 'swipe', str(width//2), str(int(height*.75)),
            str(width//2), str(int(height*.3)), '280')
    raise AssertionError('Missing UI control: ' + label)

def snapshot(name):
    tree = ui()
    ET.ElementTree(tree).write(out / (name + '.xml'), encoding='utf-8')
    (out / (name + '.png')).write_bytes(adb('exec-out', 'screencap', '-p'))

def check(value, label):
    if not value:
        raise AssertionError(label)
    checks.append(label)
    print('PASS ' + label, flush=True)
    (out / 'ui-checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2))

# Run sequentially with other emulator tests: the preferences fixture is restored in finally.
def enter(label, value):
    for attempt in range(8):
        for n in ui().iter('node'):
            if n.get('class') == 'android.widget.EditText' and (n.get('text') == label or n.get('content-desc') == label):
                x1,y1,x2,y2 = map(int,re.findall(r'-?\d+', n.get('bounds')))
                if x2>x1 and y2>y1:
                    adb('shell','input','tap',str((x1+x2)//2),str((y1+y2)//2))
                    adb('shell','input','keycombination','113','29')
                    adb('shell','input','keyevent','KEYCODE_DEL')
                    if value: adb('shell','input','text',value.replace(' ','%s'))
                    adb('shell','input','keyevent','BACK')
                    time.sleep(.15)
                    return
        adb('shell','input','swipe','500','1500','500','650','200')
    raise AssertionError('Missing input '+label)

def top():
    for _ in range(4): adb('shell', 'input', 'swipe', '500', '450', '500', '1800', '100')

stop()
original = adb('exec-out', 'run-as', pkg, 'cat', 'shared_prefs/fitness_state.xml')
try:
    root = ET.Element('map')
    ET.SubElement(root, 'boolean', name='aiEnabled', value='false')
    ET.SubElement(root, 'boolean', name='voiceEnabled', value='false')
    ET.SubElement(root, 'boolean', name='quickGentle', value='false')
    ET.SubElement(root, 'int', name='quickMinutes', value='25')
    ET.SubElement(root, 'string', name='equipment').text = '壶铃|TRX 悬挂带|哑铃'
    write_state(ET.tostring(root, encoding='utf-8', xml_declaration=True)); launch()
    snapshot('today-buttons')
    _, b8 = visible_node('8 分钟'); _, b15 = visible_node('15 分钟'); _, b25 = visible_node('25 分钟')
    check(b15[0] - b8[2] >= 12 and b25[0] - b15[2] >= 12,
          'Quick-duration buttons have visible horizontal gaps')
    tap('为我安排这一练 →')
    state = draft()
    check(len(state['items']) == 5, 'Daily 25-minute plan has five movement roles')
    check(all(x['rpe'] == '7-8' for x in state['items']), 'Daily prescription uses RPE 7–8')
    first_ids = [x['id'] for x in state['items']]
    snapshot('daily-plan')
    tap('‹ 回到今天')
    tap('重新安排')
    tap('为我安排这一练 →')
    rotated = draft()
    changed = sum(a != b for a, b in zip(first_ids, [x['id'] for x in rotated['items']]))
    check(changed >= 2, 'Regeneration rotates at least two same-role exercises')
    check(any('轮换规则' in note for note in rotated['notes']), 'Plan explains its scientific rotation rule')
    tap('‹ 回到今天')
    tap('重新安排')
    tap('我的动作组 · 保存组合直接练')
    tap('＋ 新建动作组')
    tap('保存动作组')
    check('动作组未能完成' in texts(), 'Empty routines rejected without leaving editor')
    tap('知道了')
    enter('动作组名称', 'QA-Circuit')
    enter('来源或训练备注（选填）', 'Source-QA')
    enter('循环轮数（顺序训练时不使用）', '2')
    enter('轮间休息秒数', '60')
    tap('循环训练：依次做完全部动作，再重复下一轮')
    tap('＋ 从动作库添加')
    enter('搜索名称或器械', 'TRX')
    tap('TRX 反向划船 · TRX 悬挂带')
    enter('每组次数或秒数（次数可填 8-12）', '12')
    enter('组间 / 动作后休息秒数', '20')
    enter('重量与动作备注（如壶铃 16 kg）', 'body-angle')
    tap('保存动作')
    tap('＋ 新增库里没有的动作')
    enter('动作名称', 'QA-Timed')
    enter('动作要点或来源', 'source-link')
    tap('器械选择'); tap('壶铃')
    tap('添加并设处方')
    tap('按秒计时（不勾选则按次数）')
    enter('每组次数或秒数（次数可填 8-12）', '45')
    enter('重量与动作备注（如壶铃 16 kg）', '16kg')
    tap('保存动作')
    _, edit_bounds = visible_node('编辑次数、计时与重量', swipes=8)
    _, down_bounds = visible_node('下移')
    _, remove_bounds = visible_node('移除')
    check(down_bounds[1] - edit_bounds[3] >= 12,
          'Routine edit and ordering buttons have vertical breathing room')
    check(remove_bounds[0] - down_bounds[2] >= 12,
          'Routine ordering buttons have horizontal breathing room')
    snapshot('routine-editor')
    tap('保存动作组')
    stored = json.loads(prefs()['routinesV1'])[0]
    check(stored['name'] == 'QA-Circuit' and stored['rounds'] == 2 and stored['circuit'], 'Routine name and circuit settings saved from UI')
    check(len(stored['items']) == 2 and stored['items'][1]['hold'] == 45 and stored['items'][1]['reason'] == '16kg', 'External action, seconds and weight note persisted')
    custom = json.loads(prefs()['customExercises'])
    check(custom[0]['equipment'] == ['壶铃'], 'Custom exercise equipment selection persisted')
    stop(); launch(); tap('我的动作组 · 保存组合直接练')
    snapshot('saved-routine')
    tap('编辑动作组')
    tap('下移')
    tap('保存动作组')
    changed = json.loads(prefs()['routinesV1'])[0]
    check(changed['items'][0]['id'] == stored['items'][1]['id'], 'Reordering persists through save')
    tap('编辑动作组'); tap('下移'); tap('保存动作组')
    tap('练这组 →')
    expanded = draft()
    check(len(expanded['items']) == 4 and expanded['items'][0]['id'] == expanded['items'][2]['id'] and expanded['items'][1]['id'] == expanded['items'][3]['id'], 'Circuit expands A B A B')
    check(expanded['items'][0]['restAfter'] == 20 and expanded['items'][1]['restAfter'] == 60 and expanded['items'][3]['restAfter'] == 0, 'Action and round rest boundaries retained')
    tap('开始这一练 →'); tap('准备好了，开始这一组'); time.sleep(3.4)
    tap('完成动作 ✓')
    check(draft()['phase'] == 'REST' and draft()['index'] == 1, 'Completed circuit action enters transition rest for next action')
    snapshot('circuit-rest')
    adb('shell', 'input', 'keyevent', 'HOME'); time.sleep(.4); stop(); launch()
    tap('回到训练 →')
    check(draft()['phase'] == 'REST' and draft()['index'] == 1 and draft()['paused'], 'Process restart restores circuit rest and cursor paused')
    tap('继续训练 →'); tap('休息好了'); time.sleep(3.4)
    check(draft()['phase'] == 'WORK' and draft()['phaseDuration'] == 45000, 'Saved timed action runs as exact 45-second countdown')
    snapshot('timed-work')
    tap('完成动作 ✓')
    check(draft()['index'] == 2 and draft()['phaseDuration'] == 60000, 'End of circuit round uses 60-second round rest')
    tap('结束并保存'); tap('结束并保存')
    records = json.loads(prefs()['records'])
    check(bool(records), 'Partial circuit saved as training record')
    check(json.loads(prefs()['routinesV1'])[0]['items'] == stored['items'], 'Training never mutates saved routine')
    top(); tap('今天'); tap('我的动作组 · 保存组合直接练')
    tap('删除动作组'); tap('删除')
    check(json.loads(prefs()['routinesV1']) == [], 'Deleting saved routine works')
    print('Routine UI regression completed', flush=True)
finally:
    write_state(original)
    launch()
