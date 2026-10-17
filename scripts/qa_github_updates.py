#!/usr/bin/env python3
"""Emulator public-update checks; restore fitness data and retire legacy credentials."""
from pathlib import Path

# Use the same read-only UI snapshot and state restoration helpers as existing QA.
exec(Path('scripts/qa_today_flow.py').read_text().split('\nstop()\noriginal =')[0])


def update_fixture(mode):
    result = adb('shell', 'am', 'instrument', '-w', '-e', 'mode', mode,
                 'com.restartday.fitness.qa/.GitHubUpdateFixture').decode()
    if 'INSTRUMENTATION_CODE: -1' not in result or 'INSTRUMENTATION_RESULT: failure=' in result:
        raise AssertionError('Update fixture failed: ' + result)
    return result


def no_credential_controls():
    labels = texts()
    return not any(label in labels for label in (
        '配置私有更新', '配置 GitHub 访问', '配置访问令牌', '清除访问令牌', '保存访问令牌'))


def optional_fitness_state():
    result = subprocess.run([a.adb, '-s', a.serial, 'exec-out', 'run-as', pkg, 'cat',
                             'shared_prefs/fitness_state.xml'], capture_output=True, timeout=30)
    if result.returncode == 0:
        return result.stdout
    if b'No such file or directory' in result.stderr + result.stdout:
        return None
    raise AssertionError('Could not read fitness preferences: ' + result.stderr.decode(errors='replace'))


def fitness_values():
    root = ET.fromstring(optional_fitness_state() or b'<map />')
    return {node.get('name'): node.text if node.tag == 'string' else node.get('value') for node in root}


stop()
original = optional_fitness_state()
baseline = fitness_values()
try:
    seeded = update_fixture('seed-legacy')
    check('Retired encrypted credential fixture seeded' in seeded,
          'Legacy encrypted update credential and Keystore key are seeded')
    launch()
    tap('设置')
    check('应用更新' in texts() and '检查更新' in texts(), 'Settings exposes the update button')
    check(any('无需登录或访问令牌' in value for value in texts()),
          'Settings explains that public updates need no account configuration')
    check(no_credential_controls(), 'Settings has no credential configuration controls')
    snapshot('settings-public-update')
    tap('检查更新')
    deadline = time.monotonic() + 60
    completed = False
    while time.monotonic() < deadline:
        labels = texts()
        completed = any('当前已是最新版本' in value or '发现新版本' in value
                        or value.startswith('更新到 ') or value == '下载并安装' for value in labels)
        if completed:
            break
        time.sleep(.4)
    check(completed, 'Update check reaches a newer-version or latest-version result anonymously')
    check(no_credential_controls(), 'Checking public updates does not request a credential')
    snapshot('anonymous-update-result')
    if '稍后' in texts():
        tap('稍后')
    cleared = update_fixture('assert-legacy-cleared')
    check('Retired credential preferences and key removed' in cleared,
          'First launch deletes retired update preferences and Keystore key')
    check(fitness_values() == baseline, 'Update checks and credential retirement preserve fitness preferences')
    launch()
    tap('设置')
    check(no_credential_controls(), 'Restart keeps public update controls without credential setup')
    snapshot('public-update-after-restart')
    stop()
    update_fixture('assert-legacy-cleared')
    check(fitness_values() == baseline, 'Restart does not recreate retired credentials or alter fitness data')
finally:
    stop()
    if original is None:
        adb('shell', 'run-as', pkg, 'rm', '-f', 'shared_prefs/fitness_state.xml',
            'shared_prefs/fitness_state.xml.bak')
    else:
        write_state(original)
    launch()
    print('Original emulator fitness preferences restored; retired update credentials stay removed.', flush=True)
