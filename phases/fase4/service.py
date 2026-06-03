from datetime import datetime

from phases.fase3.repository import load_latest_readings
from phases.fase4.pipeline import load_metrics, predict as run_predict
from phases.fase4.pipeline import train_models


def run(limit: int = 120, force_train: bool = True) -> dict:
    rows, source = load_latest_readings(limit=limit)

    metrics = load_metrics()
    if force_train or metrics is None:
        metrics = train_models(rows)

    return {
        "phase": "fase4",
        "status": "ok",
        "message": "Pipeline ML executado",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "data_source": source,
        "report": metrics,
    }


def predict(temperatura: float, umidade_solo: float, ph_solo: float) -> dict:
    prediction = run_predict(
        {
            "temperatura": float(temperatura),
            "umidade_solo": float(umidade_solo),
            "ph_solo": float(ph_solo),
        }
    )
    return {
        "phase": "fase4",
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "prediction": prediction,
    }
