#!/usr/bin/env python3
"""Translate the bundled exercise names with a local Ollama model and cache by dataset ID."""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "app/src/main/assets/exercises_1324.json"
OUTPUT = ROOT / "scripts/data/exercise_names_zh.json"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
CJK = re.compile(r"[\u3400-\u9fff]")


def call_ollama(model: str, rows: list[dict[str, str]]) -> dict[str, str]:
    prompt = f"""/no_think
你是专业健身动作术语译审。把下面每个英文动作名翻译成简洁、自然、健身 App 常用的简体中文名称。

要求：
1. 保留器械、姿势、单侧/双侧、握法、角度、辅助方式等区分信息。
2. 使用中国健身房通用术语，例如 barbell=杠铃、dumbbell=哑铃、cable=绳索、band=弹力带、smith=史密斯机、bench press=卧推、row=划船、curl=弯举、extension=伸展。
3. 不添加安全性、功效或证据结论；不解释。
4. 英文专有缩写可保留，但每个结果必须包含中文。
5. 仅返回 JSON 对象，key 必须原样使用输入 id，value 是中文名称；不得遗漏。

待翻译数据：
{json.dumps(rows, ensure_ascii=False)}
"""
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(
            {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "think": False,
                "format": "json",
                "options": {"temperature": 0, "num_ctx": 16384, "num_predict": 4096},
            }
        ).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=300) as response:
        payload = json.load(response)
    result = json.loads(payload["response"])
    if not isinstance(result, dict):
        raise ValueError("Ollama did not return a JSON object")
    return {str(key): str(value).strip() for key, value in result.items()}


def valid_translation(value: str) -> bool:
    return bool(value and CJK.search(value) and len(value) <= 80)


def save(values: dict[str, str]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(dict(sorted(values.items())), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen3-vl:8b-instruct")
    parser.add_argument("--batch-size", type=int, default=50)
    args = parser.parse_args()

    data = json.loads(DATASET.read_text(encoding="utf-8"))
    rows = data["exercises"]
    translations = json.loads(OUTPUT.read_text(encoding="utf-8")) if OUTPUT.exists() else {}
    pending = [
        {"id": row["id"], "name": row["name"]}
        for row in rows
        if not valid_translation(translations.get(row["id"], ""))
    ]

    total = len(pending)
    for start in range(0, total, args.batch_size):
        batch = pending[start : start + args.batch_size]
        remaining = list(batch)
        last_error: Exception | None = None
        for attempt in range(4):
            try:
                result = call_ollama(args.model, remaining)
                valid = {
                    row["id"]: result[row["id"]]
                    for row in remaining
                    if valid_translation(result.get(row["id"], ""))
                }
                if valid:
                    translations.update(valid)
                    save(translations)
                remaining = [row for row in remaining if row["id"] not in valid]
                if remaining:
                    raise ValueError(f"missing or invalid ids: {[row['id'] for row in remaining[:8]]}")
                print(f"translated {min(start + len(batch), total)}/{total}", flush=True)
                last_error = None
                break
            except Exception as error:  # retry local model formatting/timeouts
                last_error = error
                time.sleep(attempt + 1)
        if last_error is not None:
            raise last_error

    missing = [row["id"] for row in rows if not valid_translation(translations.get(row["id"], ""))]
    if missing:
        raise SystemExit(f"Missing translations: {missing[:10]}")
    print(f"wrote {len(rows)} Chinese names to {OUTPUT}")


if __name__ == "__main__":
    main()
