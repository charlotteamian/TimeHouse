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
                    ime=adb('shell','dumpsys','input_method').decode()
                    if re.search(r'(mInputShown|isInputViewShown|mIsInputViewShown)=true',ime):
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
    fixture()
    tap('我的动作组 · 保存组合直接练')
    tap('＋ 新建动作组')
    enter('动作组名称', 'QA-20-Seconds')
    tap('＋ 新增库里没有的动作')
    enter('动作名称', 'QA-Jumping-Jacks')
    tap('添加并设处方')
    tap('按秒计时（不勾选则按次数）')
    enter('每组次数或秒数（次数可填 8-12）', '20')
    enter('组间 / 动作后休息秒数', '30')
    enter('目标 RPE（选填）', '')
    tap('保存动作')
    snapshot('after-save-action')
    check(any('1 x 20 秒' in t for t in texts()), '20 seconds with blank RPE saves without validation error')
    tap('保存动作组')
    saved=json.loads(prefs()['routinesV1'])[0]
    check(saved['items'][0]['hold']==20 and saved['items'][0]['rpe']=='', '20-second duration and empty RPE persist')
    stop(); launch(); tap('我的动作组 · 保存组合直接练')
    check(json.loads(prefs()['routinesV1'])[0]['items'][0]['rpe']=='', 'Empty RPE survives app restart')
    snapshot('saved-20-seconds-no-rpe')
    tap('练这组 →')
    check(draft()['items'][0]['hold']==20 and draft()['items'][0]['rpe']=='', 'Workout uses saved duration without adding default RPE')
    check(not any('RPE ' in t for t in texts()), 'Preview omits empty RPE label')
    snapshot('20-second-preview')
    tap('开始这一练 →'); tap('准备好了，开始这一组'); time.sleep(3.4)
    check(draft()['phase']=='WORK' and draft()['phaseDuration']==20000, 'Training starts the exact 20-second countdown')
    snapshot('20-second-running')
except Exception:
    snapshot('failure')
    print(texts(),flush=True)
    raise
finally:
    write_state(original)
    launch()
