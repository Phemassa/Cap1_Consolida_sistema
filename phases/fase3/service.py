from datetime import datetime

from phases.fase3.repository import load_latest_readings
from phases.fase3.rules import build_alert_payloads, summarize_latest
from services.alert_service import AlertService


def run(limit: int = 20, send_alerts: bool = False) -> dict:
    rows, source = load_latest_readings(limit=limit)
    summary = summarize_latest(rows)
    payloads = build_alert_payloads(rows)

    dispatch_results = []
    if send_alerts and payloads:
        alert_service = AlertService()
        for payload in payloads:
            dispatch_results.append(alert_service.send_alert(payload))

    return {
        "phase": "fase3",
        "status": "ok",
        "message": "Snapshot de sensores coletado",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "data_source": source,
        "summary": summary,
        "alerts": payloads,
        "alert_dispatch": dispatch_results,
    }
