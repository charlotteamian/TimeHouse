#!/usr/bin/env python3
"""生成训练引导用的中文语音提示（res/raw/voice_*.ogg，Opus 编码）。

为什么预生成而不是用系统 TTS：
  - 报数必须准点。系统 TextToSpeech 有排队和初始化延迟，"三" 很容易落到第四秒上。
  - 国产 ROM 不保证装了中文 TTS 引擎，装了也各不相同，音色和时长不可控。
  预生成的短音频用 SoundPool 播放，延迟在毫秒级，且离线可用。

词表是固定的（准备/开始/换边/完成 + 一到十），所以一次生成、随包发布即可。

用法：
    python3 scripts/generate_voice_cues.py           # 生成缺失的
    python3 scripts/generate_voice_cues.py --force   # 全部重新生成
    python3 scripts/generate_voice_cues.py --check    # 只校验产物是否齐全

依赖 macOS 的 `say`（中文音色 Tingting）和 ffmpeg（转 Ogg/Opus）。
Opus 而不是 Vorbis：homebrew 的 ffmpeg 默认不带 libvorbis，而 libopus 是有的；
Android 从 API 21 起原生支持 Ogg 容器里的 Opus，minSdk 28 完全够。
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "app/src/main/res/raw"

VOICE = "Tingting"
# 稍微放慢一点，训练时更听得清；默认 175 词/分对报数偏快。
RATE = 160
# Opus 内部固定 48kHz，直接按它输出免得重采样两次。
SAMPLE_RATE = 48000

# 文件名（不含扩展名） -> 要念的中文
CUES: dict[str, str] = {
    "voice_ready": "准备",
    "voice_go": "开始",
    "voice_switch": "换边",
    "voice_done": "完成",
    "voice_rest": "休息",
    "voice_next": "下一个动作",
}
for value, word in enumerate(
    ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"], start=1
):
    CUES[f"voice_num_{value}"] = word

# 单条提示的时长上限（秒）。超过说明音色或语速不对，报数会压不进一秒的节拍。
MAX_SECONDS = 1.6


def expected_files() -> list[Path]:
    return [RAW_DIR / f"{name}.ogg" for name in sorted(CUES)]


def duration_seconds(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def generate(name: str, text: str, force: bool) -> str:
    target = RAW_DIR / f"{name}.ogg"
    if target.exists() and not force:
        return "skip"
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / f"{name}.wav"
        subprocess.run(
            ["say", "-v", VOICE, "-r", str(RATE), "-o", str(wav),
             "--data-format=LEI16@%d" % SAMPLE_RATE, text],
            check=True,
        )
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
             "-i", str(wav),
             # 掐掉首尾静音，报数才能踩在拍子上。
             "-af", "silenceremove=start_periods=1:start_threshold=-45dB:"
                    "start_silence=0.02,areverse,"
                    "silenceremove=start_periods=1:start_threshold=-45dB:"
                    "start_silence=0.02,areverse",
             "-c:a", "libopus", "-b:a", "32k", "-ac", "1", "-ar", str(SAMPLE_RATE),
             str(target)],
            check=True,
        )
    return "wrote"


def check() -> int:
    missing = [path.name for path in expected_files() if not path.exists()]
    if missing:
        print(f"VoiceCues: 缺少 {len(missing)} 个语音文件: {', '.join(missing)}", file=sys.stderr)
        return 1
    too_long = []
    for path in expected_files():
        seconds = duration_seconds(path)
        if seconds > MAX_SECONDS:
            too_long.append(f"{path.name} {seconds:.2f}s")
    if too_long:
        print(f"VoiceCues: 这些提示太长，报数会跟不上节拍: {', '.join(too_long)}", file=sys.stderr)
        return 1
    print(f"VoiceCues: {len(expected_files())} 个语音提示已校验（均 ≤ {MAX_SECONDS}s）")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="重新生成全部")
    parser.add_argument("--check", action="store_true", help="只校验产物")
    args = parser.parse_args()

    if args.check:
        return check()

    for tool in ("say", "ffmpeg", "ffprobe"):
        if shutil.which(tool) is None:
            print(f"VoiceCues: 找不到 {tool}，无法生成语音", file=sys.stderr)
            return 1

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    wrote = skipped = 0
    for name, text in sorted(CUES.items()):
        if generate(name, text, args.force) == "wrote":
            wrote += 1
        else:
            skipped += 1
    print(f"VoiceCues: 生成 {wrote} 个，跳过 {skipped} 个已存在的")
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
