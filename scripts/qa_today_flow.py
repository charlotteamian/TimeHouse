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
parser.add_argument('--output', default='build/qa-20260906')
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
                screen = re.findall(r'(\d+)x(\d+)', adb('shell', 'wm', 'size').decode())[-1]
                if 40 <= y1 < y2 <= int(screen[1]) - 20 and x2 > x1:
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

stop()
original = adb('exec-out', 'run-as', pkg, 'cat', 'shared_prefs/fitness_state.xml')
(out/'original-prefs.xml').write_bytes(original)
try: ET.fromstring(original)
except ET.ParseError: original=b'<?xml version="1.0" encoding="utf-8"?><map />'

size_before = adb('shell', 'wm', 'size').decode()
density_before = adb('shell', 'wm', 'density').decode()
font_before = adb('shell', 'settings', 'get', 'system', 'font_scale').decode().strip()
try:
    fixture()
    snapshot('today-home')
    check('为我安排这一练 →' in texts(), 'Home exposes short workout without setup')
    tap('为我安排这一练 →')
    snapshot('workout-preview')
    base = draft()
    check(bool(base['items']) and not base['active'], 'Offline course generated and persisted before starting')
    check('开始这一练 →' in texts(), 'Start action visible above the exercise list')
    stop(); launch()
    tap('查看课程 →')
    check(draft()['items'] == base['items'], 'Preview survives process restart without regeneration')
    tap('开始这一练 →')
    tap('准备好了，开始这一组')
    time.sleep(3.5)
    snapshot('training-work')
    check(draft()['phase'] == 'WORK', 'Count-in enters workout')
    tap('完成本组，休息')
    state = draft()
    check(state['phase'] == 'REST' and state['set'] == 1, 'Completed set enters rest with exact set count')
    adb('shell', 'input', 'keyevent', '3')
    time.sleep(.3)
    paused = draft()
    time.sleep(2)
    launch()
    snapshot('training-paused')
    restored = draft()
    check(restored['elapsed'] == paused['elapsed'] and restored['phaseStart'] == paused['phaseStart'],
          'Background time excluded from total and rest countdown')
    stop(); launch()
    tap('回到训练 →')
    check(draft()['set'] == 1 and draft()['phase'] == 'REST' and '继续训练 →' in texts(),
          'Killed process restores paused rest and completed set')
    tap('继续训练 →')
    before = draft()['phaseDuration']
    tap('+20 秒')
    check(draft()['phaseDuration'] == before + 20000, 'Rest extension persists')
    tap('结束并保存')
    tap('结束并保存')
    snapshot('training-receipt')
    records = json.loads(prefs()['records'])
    check(len(records) == 1 and sum(int(x.split('|')[1]) for x in records[0]['itemStats']) == 1,
          'Early finish preserves exactly the completed set')
    check(not prefs().get('workoutDraft'), 'Finish clears active checkpoint')
    stop(); launch()
    check(len(json.loads(prefs()['records'])) == 1 and not draft(), 'Restart does not duplicate finished record')
    snapshot('today-with-footprint')
    check(any('本周动了 1 天' in x for x in texts()), 'Weekly footprint reflects actual completed work')
    tap('自己安排')
    adb('shell', 'input', 'keyevent', '4')
    check('给自己一点时间' in texts(), 'Android system back returns from custom setup to today')

    # Timed holds must not silently complete while the app is gone.
    hold = dict(base)
    hold['items'] = [dict(base['items'][0], kind='HOLD', hold=30, perSide=True, sets=2)]
    hold.update(active=True, index=0, set=0, phase='WORK', started=int(time.time()*1000),
                elapsed=10000, phaseStart=0, phaseDuration=60000, exerciseStart=0,
                running=True, switched=False, results=[], stats=[])
    fixture(hold)
    tap('回到训练 →')
    check('50 秒' in texts(), 'Timed per-side hold restores remaining seconds')
    tap('继续训练 →')
    time.sleep(2)
    adb('shell', 'input', 'keyevent', '223')
    for _ in range(50):
        if draft().get('paused'): break
        time.sleep(.1)
    check(draft().get('paused'), 'Screen-off transition reaches paused lifecycle state')
    sleeping = draft()
    time.sleep(2)
    adb('shell', 'input', 'keyevent', '224')
    adb('shell', 'wm', 'dismiss-keyguard')
    launch()
    print('LOCK CHECK', {k: sleeping[k] for k in ('elapsed', 'set', 'phase')},
          {k: draft()[k] for k in ('elapsed', 'set', 'phase')}, flush=True)
    check(draft()['elapsed'] == sleeping['elapsed'] and draft()['set'] == 0,
          'Screen lock freezes hold without falsely completing a set')
    check(draft()['items'][0]['perSide'] is True, 'Per-side prescription survives restore')

    # A near-finished timer must advance exactly once after explicit resume.
    hold.update(elapsed=59900)
    fixture(hold)
    tap('回到训练 →'); tap('继续训练 →')
    time.sleep(.5)
    check(draft()['phase'] == 'REST' and draft()['set'] == 1, 'Timed hold completes one set exactly once')
    check(not json.loads(prefs()['records']), 'Intermediate progress is not a completed session record')

    fixture()
    adb('shell', 'wm', 'size', '720x1280')
    adb('shell', 'wm', 'density', '320')
    adb('shell', 'settings', 'put', 'system', 'font_scale', '1.3')
    stop(); launch()
    snapshot('small-large-font-home')
    tap('为我安排这一练 →')
    snapshot('small-large-font-preview')
    check('开始这一练 →' in texts(), '360dp screen with 130 percent font retains accessible start action')
    tap('开始这一练 →')
    snapshot('small-large-font-session')
    check('结束并保存' in texts(), 'Small screen keeps end-session control reachable')
    print('ALL UI CHECKS PASSED', flush=True)
finally:
    size_override = re.search(r'Override size: (\d+x\d+)', size_before)
    density_override = re.search(r'Override density: (\d+)', density_before)
    adb('shell', 'wm', 'size', size_override.group(1) if size_override else 'reset')
    adb('shell', 'wm', 'density', density_override.group(1) if density_override else 'reset')
    if font_before == 'null':
        adb('shell', 'settings', 'delete', 'system', 'font_scale')
    else:
        adb('shell', 'settings', 'put', 'system', 'font_scale', font_before)
    write_state(original)
    launch()
    print('Original emulator preferences restored.', flush=True)
