"""Pipeline end-to-end que interliga todas as fases do FarmTech (Fase 7).

Fluxo real de decisao:
  Fase 1-2 (areas) -> Fase 3 (telemetria) -> Fase 4 (ML) -> regras -> Fase 5 (alertas) -> Fase 6 (visao)

Cada etapa consome a saida da anterior e contribui para uma decisao final
de irrigacao, com rastro completo (decision trace) para auditoria e apresentacao.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from phases.fase1_2.repository import list_areas
from phases.fase3.repository import load_latest_readings
from phases.fase3.rules import build_alert_payloads, summarize_latest
from phases.fase4.pipeline import load_metrics, train_models
from phases.fase4.pipeline import predict as ml_predict
from phases.fase6.service import run as run_fase6
from services.alert_service import AlertService
from services.history import append_history


def _now() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _decision_from_signals(rule_alerts: list[dict[str, Any]], ml: dict[str, Any]) -> dict[str, Any]:
    """Combina regras determinísticas (Fase 3) e ML (Fase 4) numa decisão única."""
    rule_says_irrigate = len(rule_alerts) > 0
    ml_says_irrigate = bool(ml.get("needs_irrigation"))
    probability = ml.get("probability")

    if rule_says_irrigate and ml_says_irrigate:
        verdict = "IRRIGAR"
        confidence = "alta"
        rationale = "Regras de sensor e modelo de ML concordam: irrigacao recomendada."
    elif rule_says_irrigate and not ml_says_irrigate:
        verdict = "IRRIGAR"
        confidence = "media"
        rationale = "Regras de sensor acionaram alerta mesmo com ML neutro. Prioriza seguranca operacional."
    elif not rule_says_irrigate and ml_says_irrigate:
        verdict = "MONITORAR"
        confidence = "media"
        rationale = "ML sugere tendencia de irrigacao, mas nenhuma regra critica foi violada."
    else:
        verdict = "MANTER"
        confidence = "alta"
        rationale = "Sensores dentro dos limites e ML negativo: nenhuma acao necessaria."

    return {
        "verdict": verdict,
        "confidence": confidence,
        "rationale": rationale,
        "rule_signal": rule_says_irrigate,
        "ml_signal": ml_says_irrigate,
        "ml_probability": probability,
        "agreement": rule_says_irrigate == ml_says_irrigate,
    }


def run_end_to_end(
    limit: int = 20,
    send_alerts: bool = True,
    include_vision: bool = True,
    images_dir: str | None = None,
) -> dict[str, Any]:
    """Executa o fluxo completo interligando as 6 fases e retorna trace + decisão."""
    trace: list[dict[str, Any]] = []
    started = _now()

    # ---------- Fase 1-2: contexto de areas ----------
    areas = list_areas()
    total_hectares = round(sum(float(a.get("hectares", 0) or 0) for a in areas), 2)
    trace.append({
        "step": 1,
        "phase": "fase1_2",
        "title": "Contexto de areas",
        "status": "ok",
        "detail": f"{len(areas)} areas monitoradas, {total_hectares} hectares no total.",
        "output": {"total_areas": len(areas), "total_hectares": total_hectares},
    })

    # ---------- Fase 3: telemetria ----------
    rows, source = load_latest_readings(limit=limit)
    summary = summarize_latest(rows)
    latest = summary.get("latest") or {}
    rule_alerts = build_alert_payloads(rows)
    trace.append({
        "step": 2,
        "phase": "fase3",
        "title": "Telemetria de sensores",
        "status": "ok",
        "detail": (
            f"Fonte: {source}. {summary.get('total_readings', 0)} leituras. "
            f"Ultima: temp {latest.get('temperatura')}C, "
            f"umidade {latest.get('umidade_solo')}%, pH {latest.get('ph_solo')}."
        ),
        "output": {"data_source": source, "summary": summary, "rule_alerts": rule_alerts},
    })

    # ---------- Fase 4: ML sobre a leitura real ----------
    ml_result: dict[str, Any] = {}
    ml_status = "ok"
    ml_detail = ""
    try:
        if load_metrics() is None:
            train_models(rows)
        if latest and latest.get("temperatura") is not None:
            ml_result = ml_predict({
                "temperatura": float(latest.get("temperatura")),
                "umidade_solo": float(latest.get("umidade_solo")),
                "ph_solo": float(latest.get("ph_solo")),
            })
            prob = ml_result.get("probability")
            prob_txt = f"{prob:.0%}" if isinstance(prob, (int, float)) else "n/d"
            ml_detail = (
                f"Modelo {ml_result.get('model')} preve "
                f"{'IRRIGAR' if ml_result.get('needs_irrigation') else 'MANTER'} "
                f"(probabilidade {prob_txt})."
            )
        else:
            ml_status = "skip"
            ml_detail = "Sem leitura valida para inferencia."
    except Exception as exc:  # noqa: BLE001 - registrar e seguir o fluxo
        ml_status = "error"
        ml_detail = f"Falha no ML: {exc}"

    trace.append({
        "step": 3,
        "phase": "fase4",
        "title": "Inteligencia / predicao",
        "status": ml_status,
        "detail": ml_detail,
        "output": ml_result,
    })

    # ---------- Decisao combinada ----------
    decision = _decision_from_signals(rule_alerts, ml_result)
    trace.append({
        "step": 4,
        "phase": "decisao",
        "title": "Motor de decisao",
        "status": "ok",
        "detail": f"Veredito: {decision['verdict']} (confianca {decision['confidence']}). {decision['rationale']}",
        "output": decision,
    })

    # ---------- Fase 5: alertas ----------
    dispatch_results: list[dict[str, Any]] = []
    should_dispatch = send_alerts and decision["verdict"] in {"IRRIGAR", "MONITORAR"} and rule_alerts
    if should_dispatch:
        service = AlertService()
        for payload in rule_alerts:
            enriched = {
                **payload,
                "decision": decision["verdict"],
                "ml_probability": decision.get("ml_probability"),
            }
            dispatch_results.append(service.send_alert(enriched))
    alert_detail = (
        f"{len(dispatch_results)} alerta(s) despachado(s)."
        if dispatch_results else "Nenhum alerta necessario neste ciclo."
    )
    trace.append({
        "step": 5,
        "phase": "fase5",
        "title": "Mensageria / alertas",
        "status": "ok",
        "detail": alert_detail,
        "output": {"dispatched": dispatch_results, "count": len(dispatch_results)},
    })

    # ---------- Fase 6: visao (opcional) ----------
    vision_report: dict[str, Any] = {}
    if include_vision:
        try:
            vision = run_fase6(images_dir=images_dir, limit=20)
            vision_report = vision.get("report", {})
            counts = vision_report.get("counts", {})
            trace.append({
                "step": 6,
                "phase": "fase6",
                "title": "Visao computacional",
                "status": "ok",
                "detail": (
                    f"{vision_report.get('total_images', 0)} imagens analisadas: "
                    f"{counts.get('possivel_estresse', 0)} com possivel estresse."
                ),
                "output": vision_report,
            })
        except Exception as exc:  # noqa: BLE001
            trace.append({
                "step": 6,
                "phase": "fase6",
                "title": "Visao computacional",
                "status": "error",
                "detail": f"Falha na visao: {exc}",
                "output": {},
            })

    finished = _now()
    result = {
        "status": "ok",
        "started_at": started,
        "finished_at": finished,
        "decision": decision,
        "trace": trace,
        "context": {
            "areas": len(areas),
            "total_hectares": total_hectares,
            "data_source": source,
        },
        "telemetry": summary,
        "ml": ml_result,
        "rule_alerts": rule_alerts,
        "dispatched_alerts": dispatch_results,
        "vision": vision_report,
    }

    append_history({
        "type": "pipeline_e2e",
        "verdict": decision["verdict"],
        "confidence": decision["confidence"],
        "agreement": decision["agreement"],
        "alerts_count": len(dispatch_results),
        "data_source": source,
    })

    return result
