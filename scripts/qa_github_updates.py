#!/usr/bin/env python3
"""Emulator settings checks; restore preferences and never use a real API token."""
from pathlib import Path

# Use the same read-only UI snapshot and state restoration helpers as existing QA.
exec(Path('scripts/qa_today_flow.py').read_text().split('\nstop()\noriginal =')[0])


def set_text(value):
    result = adb('shell', 'am', 'instrument', '-w', '-e', 'setTextDesc',
                 shlex.quote('GitHub 只读访问令牌'), '-e', 'setTextBase64',
                 shlex.quote(base64.b64encode(value.encode()).decode()),
                 'com.restartday.fitness.qa/.UiSnapshot').decode()
    if 'textSet=1' not in result:
        raise AssertionError('Token input could not be filled')


stop()
original = adb('exec-out', 'run-as', pkg, 'cat', 'shared_prefs/fitness_state.xml')
token_path = 'shared_prefs/github_updates.xml'
saved_token = subprocess.run([a.adb, '-s', a.serial, 'exec-out', 'run-as', pkg, 'cat', token_path],
                             capture_output=True).stdout
fake_token = 'github_pat_' + 'invalid' * 12
try:
    adb('shell', 'run-as', pkg, 'rm', '-f', token_path)
    launch()
    tap('设置')
    check('应用更新' in texts() and '检查更新' in texts(), 'Settings exposes the update button')
    snapshot('settings-update')
    tap('检查更新')
    check('配置私有更新' in texts(), 'First check opens private-access configuration')
    set_text('invalid')
    tap('保存')
    check('配置私有更新' in texts(), 'Malformed token does not close configuration')
    set_text(fake_token)
    tap('保存')
    encrypted = adb('exec-out', 'run-as', pkg, 'cat', token_path)
    check(fake_token.encode() not in encrypted and b'encrypted_token' in encrypted,
          'Token is stored as ciphertext, without plaintext')
    stop()
    launch()
    tap('设置')
    check(any('已配置访问令牌' in value for value in texts()), 'Keystore token can be read after process restart')
    tap('检查更新')
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        if any('令牌无效' in value for value in texts()):
            break
        time.sleep(.4)
    check(any('令牌无效' in value for value in texts()), 'GitHub authentication failure has an actionable message')
    snapshot('authentication-error')
    tap('清除访问令牌')
    check(any('首次使用需配置' in value for value in texts()), 'Token can be removed without changing fitness data')
    remaining = adb('exec-out', 'run-as', pkg, 'cat', token_path)
    check(b'encrypted_token' not in remaining, 'Removing a token deletes its ciphertext')
    snapshot('token-cleared')
finally:
    stop()
    if saved_token:
        adb('shell', 'run-as', pkg, 'sh', '-c', shlex.quote('cat > ' + token_path), data=saved_token)
    else:
        adb('shell', 'run-as', pkg, 'rm', '-f', token_path)
    write_state(original)
    launch()
    print('Original emulator preferences restored.', flush=True)
