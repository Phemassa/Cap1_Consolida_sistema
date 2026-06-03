from __future__ import annotations

from typing import Any


def summarize_latest(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "total_readings": 0,
            "latest": None,
        }

    latest = rows[-1]
    return {
        "total_readings": len(rows),
        "latest": latest,
        "avg_umidade_solo": _avg(rows, "umidade_solo"),
        "avg_temperatura": _avg(rows, "temperatura"),
        "avg_ph_solo": _avg(rows, "ph_solo"),
    }


def _avg(rows: list[dict[str, Any]], key: str) -> float | None:
    values = [r.get(key) for r in rows if isinstance(r.get(key), (int, float))]
    if not values:
        return None
    return round(sum(values) / len(values), 2)


def build_alert_payloads(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not rows:
        return []

    latest = rows[-1]
    alerts: list[dict[str, Any]] = []

    umidade = latest.get("umidade_solo")
    if isinstance(umidade, (int, float)) and umidade < 20:
        alerts.append(
            {
                "source": "fase3",
                "metric": "umidade_solo",
                "value": umidade,
                "threshold": 20,
                "action": "Iniciar irrigacao corretiva e revisar disponibilidade hidrica",
            }
        )

    ph = latest.get("ph_solo")
    if isinstance(ph, (int, float)) and (ph < 5.5 or ph > 7.5):
        alerts.append(
            {
                "source": "fase3",
                "metric": "ph_solo",
                "value": ph,
                "threshold": "5.5-7.5",
                "action": "Ajustar manejo de solo e revisar adubacao para estabilizar pH",
            }
        )

    temp = latest.get("temperatura")
    if isinstance(temp, (int, float)) and temp > 35:
        alerts.append(
            {
                "source": "fase3",
                "metric": "temperatura",
                "value": temp,
                "threshold": 35,
                "action": "Reforcar monitoramento e avaliar estrategia de resfriamento/irrigacao",
            }
        )

    return alerts
