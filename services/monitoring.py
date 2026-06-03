from __future__ import annotations

from datetime import datetime
from typing import Any

from phases.fase3.service import run as run_fase3
from services.history import append_history, read_history


def monitor_and_alert_once(limit: int = 20) -> dict[str, Any]:
    snapshot = run_fase3(limit=limit, send_alerts=True)
    event = {
        "type": "monitor_fase3",
        "data_source": snapshot.get("data_source"),
        "alerts_count": len(snapshot.get("alerts", [])),
        "dispatch_count": len(snapshot.get("alert_dispatch", [])),
    }
    append_history(event)
    return snapshot
