#!/usr/bin/env python3
"""Emulator-only regression for app-private GIFs and expired legacy content URIs."""
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
parser.add_argument('--output', default='build/qa-20260912-custom-media')
a = parser.parse_args()
if not a.serial.startswith('emulator-'):
    raise SystemExit('This test only runs on an explicitly selected emulator.')

out = Path(a.output)
out.mkdir(parents=True, exist_ok=True)
pkg = 'com.restartday.fitness'
private_rel = 'files/exercise_media/qa_motion.gif'
private_uri = 'file:///data/user/0/' + pkg + '/' + private_rel
source_gif = Path(__file__).resolve().parents[1] / 'assets/motion_sources/glute_bridge.gif'
checks = []

def adb(*args, data=None):
    return subprocess.run([a.adb, '-s', a.serial, *args], input=data,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=True, timeout=30).stdout

def stop():
    adb('shell', 'am', 'force-stop', pkg)

def prefs():
    root = ET.fromstring(adb('exec-out', 'run-as', pkg, 'cat', 'shared_prefs/fitness_state.xml'))
    return {x.get('name'): x.text if x.tag == 'string' else x.get('value') for x in root}

def launch():
    adb('shell', 'am', 'start', '-W', '-n', pkg + '/.app.MainActivity')
    time.sleep(.8)

def write_state(raw):
    stop()
    adb('shell', 'run-as', pkg, 'mkdir', '-p', 'shared_prefs')
    adb('shell', 'run-as', pkg, 'sh', '-c', shlex.quote('cat > shared_prefs/fitness_state.xml'), data=raw)

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
    for attempt in range(8):
        for n in ui().iter('node'):
            if n.get('class') != 'android.widget.EditText' and (n.get('text') == label or n.get('content-desc') == label):
                x1, y1, x2, y2 = map(int, re.findall(r'-?\d+', n.get('bounds')))
                if x2 > x1 and y2 > y1:
                    adb('shell', 'input', 'tap', str((x1+x2)//2), str((y1+y2)//2))
                    time.sleep(.3)
                    return
        adb('shell', 'input', 'swipe', '500', '1550', '500', '650', '220')
    raise AssertionError('Missing UI control: ' + label)

def enter(label, value):
    for attempt in range(8):
        for n in ui().iter('node'):
            if n.get('class') == 'android.widget.EditText' and (
                    n.get('text') == label or n.get('content-desc') == label
                    or label == '搜索动作、肌群或器械'):
                x1, y1, x2, y2 = map(int, re.findall(r'-?\d+', n.get('bounds')))
                if x2 > x1 and y2 > y1:
                    adb('shell', 'input', 'tap', str((x1+x2)//2), str((y1+y2)//2))
                    adb('shell', 'input', 'keycombination', '113', '29')
                    adb('shell', 'input', 'keyevent', 'KEYCODE_DEL')
                    adb('shell', 'input', 'text', value.replace(' ', '%s'))
                    adb('shell', 'input', 'keyevent', 'BACK')
                    time.sleep(.2)
                    return
        adb('shell', 'input', 'swipe', '500', '1500', '500', '650', '200')
    raise AssertionError('Missing input: ' + label)

def snapshot(name):
    ET.ElementTree(ui()).write(out / (name + '.xml'), encoding='utf-8')
    (out / (name + '.png')).write_bytes(adb('exec-out', 'screencap', '-p'))

def check(value, label):
    if not value:
        raise AssertionError(label)
    checks.append(label)
    print('PASS ' + label, flush=True)
    (out / 'ui-checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2))

stop()
original = adb('exec-out', 'run-as', pkg, 'cat', 'shared_prefs/fitness_state.xml')
try:
    adb('push', str(source_gif), '/data/local/tmp/qa_motion.gif')
    adb('shell', 'run-as', pkg, 'mkdir', '-p', 'files/exercise_media')
    adb('shell', 'run-as', pkg, 'cp', '/data/local/tmp/qa_motion.gif', private_rel)

    custom = [
        {'id': 'custom_qa_gif', 'name': 'QA-GIF', 'regions': ['臀'],
         'equipment': ['壶铃'], 'instruction': '测试 GIF', 'media': private_uri},
        {'id': 'custom_qa_broken', 'name': 'QA-Broken', 'regions': ['腿'],
         'equipment': ['自重'], 'instruction': '测试失效链接',
         'media': 'content://com.android.providers.media.documents/document/image%3A999999'}
    ]
    root = ET.Element('map')
    ET.SubElement(root, 'boolean', name='aiEnabled', value='false')
    ET.SubElement(root, 'boolean', name='voiceEnabled', value='false')
    ET.SubElement(root, 'string', name='equipment').text = '自重|壶铃'
    ET.SubElement(root, 'string', name='customExercises').text = json.dumps(custom, ensure_ascii=False)
    write_state(ET.tostring(root, encoding='utf-8', xml_declaration=True))
    launch()

    tap('动作库'); enter('搜索动作、肌群或器械', 'QA-GIF'); tap('搜索'); tap('QA-GIF')
    current = texts()
    check('♡ 标心' in current and not any('本地示范已失效' in x for x in current),
          'App-private GIF decodes in custom exercise detail')
    snapshot('gif-detail-first-launch')
    tap('关闭'); stop(); launch()
    tap('动作库'); enter('搜索动作、肌群或器械', 'QA-GIF'); tap('搜索'); tap('QA-GIF')
    current = texts()
    check('♡ 标心' in current and not any('本地示范已失效' in x for x in current),
          'App-private GIF still decodes after process restart')
    tap('编辑')
    check('器械选择' in [n.get('content-desc', '') for n in ui().iter('node')],
          'Existing custom exercise exposes editable equipment')
    tap('器械选择'); tap('TRX 悬挂带'); tap('保存')
    saved_custom = json.loads(prefs()['customExercises'])
    check(saved_custom[0]['equipment'] == ['TRX 悬挂带'],
          'Editing custom exercise equipment updates persisted data')

    tap('全部'); enter('搜索动作、肌群或器械', 'QA-Broken'); tap('搜索'); tap('QA-Broken')
    check(any('本地示范已失效' in x for x in texts()),
          'Expired legacy content URI shows a visible recovery state')
    tap('本地示范已失效\n点此重新选择')
    current = texts()
    check(any('旧版只保存了相册临时地址' in x for x in current) and '重新选择' in current,
          'Expired content URI offers reselect instead of a broken browser link')
    snapshot('expired-content-uri')
    print('Custom media UI regression completed', flush=True)
finally:
    write_state(original)
    adb('shell', 'run-as', pkg, 'rm', '-f', private_rel)
    adb('shell', 'rm', '-f', '/data/local/tmp/qa_motion.gif')
    launch()
