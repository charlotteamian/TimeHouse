#!/usr/bin/env python3
"""Emulator-only public update installation; preserve the original fitness preferences."""
from pathlib import Path
import hashlib
import threading

# Reuse the established serial guard, UI snapshots and preference helpers.
exec(Path('scripts/qa_today_flow.py').read_text().split('\nstop()\noriginal =')[0])

report = {'serial': a.serial, 'checks': checks, 'phase': 'starting'}
report_path = out / 'public-install-report.json'
record_title = 'QA 合成记录 · 公开更新保留验证'
record_note = 'SYNTHETIC QA ONLY: no real workout or AI credential.'
placeholder_key = 'qa-disabled-placeholder'


def checkpoint(phase=None):
    if phase:
        report['phase'] = phase
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2))


def optional_fitness_state():
    result = subprocess.run([a.adb, '-s', a.serial, 'exec-out', 'run-as', pkg, 'cat',
                             'shared_prefs/fitness_state.xml'], capture_output=True, timeout=30)
    if result.returncode == 0:
        return result.stdout
    if b'No such file or directory' in result.stderr + result.stdout:
        return None
    raise AssertionError('Could not read fitness preferences: ' + result.stderr.decode(errors='replace'))


def values(raw):
    root = ET.fromstring(raw or b'<map />')
    return {node.get('name'): node.text if node.tag == 'string' else node.get('value') for node in root}


def installed_version():
    text = adb('shell', 'dumpsys', 'package', pkg).decode()
    match = re.search(r'\bversionCode=(\d+)', text)
    return int(match.group(1)) if match else None


def foreground():
    text = adb('shell', 'dumpsys', 'activity', 'activities').decode()
    for line in text.splitlines():
        if 'mResumedActivity' in line or 'topResumedActivity' in line:
            match = re.search(r'([\w.]+/[\w.$]+)', line)
            if match:
                return match.group(1)
    return ''


def is_installer(component):
    package = component.split('/', 1)[0]
    return package in ('com.android.packageinstaller', 'com.google.android.packageinstaller') or (
        package in ('com.android.permissioncontroller', 'com.google.android.permissioncontroller')
        and 'install' in component.lower())


def wait_for(predicate, timeout, message):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(.4)
    raise AssertionError(message)


def tap_any(labels):
    current = texts()
    for label in labels:
        if label in current:
            tap(label)
            return label
    raise AssertionError('Missing UI control: ' + ' / '.join(labels))


def permission_allowed():
    result = adb('shell', 'appops', 'get', pkg, 'REQUEST_INSTALL_PACKAGES').decode()
    return bool(re.search(r'REQUEST_INSTALL_PACKAGES:\s*allow\b', result))


def preserve_blob(label, raw):
    path = out / (label + '-fitness-state.xml')
    if raw is not None:
        path.write_bytes(raw)
    report[label] = {'exists': raw is not None, 'bytes': len(raw) if raw is not None else 0,
                     'sha256': hashlib.sha256(raw).hexdigest() if raw is not None else None,
                     'file': path.name if raw is not None else None}
    checkpoint()


def assert_synthetic_data(raw):
    state = values(raw)
    records = json.loads(state.get('records') or '[]')
    check(len(records) == 1 and records[0].get('title') == record_title
          and records[0].get('note') == record_note
          and records[0].get('itemStats') == ['qa_public_update|1|1'],
          'Synthetic workout record survives the public update')
    check(state.get('aiEnabled') == 'false' and state.get('aiApiKey') == placeholder_key,
          'Disabled AI and its synthetic placeholder remain unchanged')


def download_fixture():
    command = [a.adb, '-s', a.serial, 'shell', 'am', 'instrument', '-w', '-e', 'mode', 'download',
               'com.restartday.fitness.qa/.GitHubUpdateFixture']
    timed_out = threading.Event()
    lines = []
    with (out / 'anonymous-download-instrumentation.txt').open('w') as log:
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True, bufsize=1) as process:
            def timeout():
                timed_out.set()
                process.kill()
            timer = threading.Timer(13 * 60, timeout)
            timer.start()
            try:
                for line in process.stdout:
                    lines.append(line)
                    log.write(line)
                    log.flush()
                    print(line.rstrip(), flush=True)
                process.wait()
            finally:
                timer.cancel()
    result = ''.join(lines)
    if timed_out.is_set() or process.returncode != 0 or 'INSTRUMENTATION_CODE: -1' not in result \
            or 'INSTRUMENTATION_RESULT: failure=' in result:
        raise AssertionError('Anonymous download fixture failed; see instrumentation log')
    metadata = json.loads(adb('exec-out', 'run-as', pkg, 'cat', 'cache/updates/qa-verified.json'))
    (out / 'verified-update-metadata.json').write_text(json.dumps(metadata, indent=2))
    return metadata


stop()
original = optional_fitness_state()
report['original_fitness_state_existed'] = original is not None
report['initial_version_code'] = installed_version()
checkpoint()
try:
    end = int(time.time() * 1000)
    synthetic_record = {'time': 'QA 00:01', 'title': record_title, 'duration': '1:00',
                        'epoch': end, 'startEpoch': end - 60000, 'total': 1, 'done': 1,
                        'feel': 'QA 合成', 'pain': '无', 'note': record_note,
                        'items': ['✓ QA 合成动作 · 1:00 · 1 组'],
                        'itemStats': ['qa_public_update|1|1']}
    root = ET.Element('map')
    ET.SubElement(root, 'boolean', name='aiEnabled', value='false')
    ET.SubElement(root, 'boolean', name='voiceEnabled', value='false')
    ET.SubElement(root, 'string', name='aiApiKey').text = placeholder_key
    ET.SubElement(root, 'string', name='records').text = json.dumps([synthetic_record], ensure_ascii=False)
    write_state(ET.tostring(root, encoding='utf-8', xml_declaration=True))
    checkpoint('anonymous-download')
    metadata = download_fixture()
    report['download'] = metadata
    target_code = int(metadata['version_code'])
    check(report['initial_version_code'] is not None and target_code > report['initial_version_code'],
          'Public release is newer than the installed baseline')
    check(True, 'Anonymous download, size, SHA-256, signer, version, provider and partial-file checks pass')
    checkpoint('app-update-ui')
    launch()
    tap('设置')
    snapshot('settings-before-update')
    tap('检查更新')
    wait_for(lambda: any('发现新版本' in text or text.startswith('更新到 ')
                         or text == '下载并安装' for text in texts()), 60,
             'App did not offer the newer public release')
    snapshot('public-update-offer')
    tap('下载并安装')
    wait_for(lambda: '允许安装更新' in texts() or is_installer(foreground()), 180,
             'Verified cached APK did not reach the installation flow')
    report['permission_already_allowed'] = permission_allowed()
    if '允许安装更新' in texts():
        snapshot('installation-permission-prompt')
        tap('去授权')
        wait_for(lambda: foreground().startswith('com.android.settings/'), 30,
                 'Android installation permission settings did not open')
        snapshot('android-installation-permission')
        if not permission_allowed():
            tap_any(('Allow from this source', '允许来自此来源的应用', '允许此来源', '允许来自此来源'))
            wait_for(permission_allowed, 15, 'Installation source switch did not grant permission')
        check(permission_allowed(), 'Android installation permission is granted through its settings UI')
        snapshot('android-installation-permission-granted')
        adb('shell', 'input', 'keyevent', '4')
    wait_for(lambda: is_installer(foreground()), 45,
             'Android package installer did not become the foreground activity')
    component = foreground()
    report['installer_activity'] = component
    check(is_installer(component), 'Foreground activity belongs to the Android package installer')
    wait_for(lambda: any(label in texts() for label in ('Update', 'UPDATE', '更新')), 30,
             'Package installer did not show the Update confirmation')
    snapshot('system-installer-before-update')
    # Persist both sides of the actual install immediately, before any later UI assertions.
    before_install = optional_fitness_state()
    preserve_blob('before-install', before_install)
    checkpoint('confirming-system-update')
    tap_any(('Update', 'UPDATE', '更新'))
    wait_for(lambda: installed_version() == target_code, 180,
             'Package manager did not report the target version after confirming Update')
    after_install = optional_fitness_state()
    preserve_blob('after-install', after_install)
    report['installed_version_code'] = target_code
    report['preferences_byte_identical'] = before_install == after_install
    checkpoint('installed-data-captured')
    check(before_install is not None and before_install == after_install,
          'Fitness preference bytes and SHA-256 are identical immediately before and after installation')
    assert_synthetic_data(after_install)
    snapshot('system-installer-after-update')
    if any(label in texts() for label in ('Done', 'DONE', '完成')):
        tap_any(('Done', 'DONE', '完成'))
    stop()
    adb('shell', 'input', 'keyevent', '3')
    time.sleep(2)
    # The installer may finish a HOME transition after its Update confirmation.
    # Start without am -W, then observe the foreground activity explicitly.
    adb('shell', 'am', 'start', '-n', pkg + '/.app.MainActivity')
    wait_for(lambda: foreground().startswith(pkg + '/'), 45,
             'Updated app did not become the foreground activity')
    time.sleep(2)
    tap('设置')
    tap('检查更新')
    wait_for(lambda: any('当前已是最新版本' in text for text in texts()), 60,
             'Updated app did not report that it is the latest public version')
    check(True, 'Installed app anonymously confirms that it is the latest public release')
    snapshot('updated-settings-latest')
    assert_synthetic_data(optional_fitness_state())
    tap('记录')
    check(any(record_title in text for text in texts()), 'Updated app renders the synthetic workout record')
    snapshot('updated-synthetic-record')
    checkpoint('passed')
except BaseException as error:
    report['failure'] = type(error).__name__ + ': ' + str(error)
    checkpoint('failed')
    try:
        snapshot('failure')
        report['failure_foreground_activity'] = foreground()
    except Exception as snapshot_error:
        report['failure_snapshot_error'] = str(snapshot_error)
    checkpoint()
    raise
finally:
    try:
        stop()
        if original is None:
            adb('shell', 'run-as', pkg, 'rm', '-f', 'shared_prefs/fitness_state.xml',
                'shared_prefs/fitness_state.xml.bak')
        else:
            write_state(original)
        report['original_fitness_preferences_restored'] = optional_fitness_state() == original
        report['final_installed_version_code'] = installed_version()
        if not report['original_fitness_preferences_restored']:
            raise AssertionError('Original fitness preferences were not restored')
        print('Original fitness preferences restored; installed app version is retained.', flush=True)
    except Exception as restore_error:
        report['restore_failure'] = str(restore_error)
        raise
    finally:
        checkpoint()
