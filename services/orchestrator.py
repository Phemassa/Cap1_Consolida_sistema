from phases.fase1_2.service import run as run_fase1_2
from phases.fase3.service import run as run_fase3
from phases.fase4.service import predict as predict_fase4
from phases.fase4.service import run as run_fase4
from phases.fase6.service import run as run_fase6


def run_phase(phase: str) -> dict:
    dispatch = {
        "fase1_2": run_fase1_2,
        "fase3": run_fase3,
        "fase4": run_fase4,
        "fase6": run_fase6,
    }
    if phase not in dispatch:
        return {"status": "error", "message": f"Fase invalida: {phase}"}
    return dispatch[phase]()


def monitor_fase3(limit: int = 20, send_alerts: bool = False) -> dict:
    return run_fase3(limit=limit, send_alerts=send_alerts)


def train_fase4(limit: int = 120, force_train: bool = True) -> dict:
    return run_fase4(limit=limit, force_train=force_train)


def infer_fase4(temperatura: float, umidade_solo: float, ph_solo: float) -> dict:
    return predict_fase4(temperatura=temperatura, umidade_solo=umidade_solo, ph_solo=ph_solo)


def run_fase6_vision(images_dir: str | None = None, limit: int = 50) -> dict:
    return run_fase6(images_dir=images_dir, limit=limit)
