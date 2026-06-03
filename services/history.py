from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _runtime_dir() -> Path:
    path = _repo_root() / "data" / "runtime"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _history_file() -> Path:
    return _runtime_dir() / "alerts_history.jsonl"


def append_history(event: dict[str, Any]) -> None:
    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        **event,
    }
    with _history_file().open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(record, ensure_ascii=True) + "\n")


def read_history(limit: int = 50) -> list[dict[str, Any]]:
    path = _history_file()
    if not path.exists():
        return []

    lines = path.read_text(encoding="utf-8").splitlines()
    selected = lines[-limit:]
    result = []
    for line in selected:
        try:
            result.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return result
