from phases.fase1_2.service import add as add_fase1_2
from phases.fase1_2.service import edit as edit_fase1_2
from phases.fase1_2.service import remove as remove_fase1_2
from phases.fase1_2.service import run as run_fase1_2
from phases.fase3.service import run as run_fase3
from phases.fase4.service import predict as predict_fase4
from phases.fase4.service import run as run_fase4
from phases.fase6.service import run as run_fase6
from services.monitoring import monitor_and_alert_once, read_history


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


def create_area(nome: str, cultura: str, hectares: float) -> dict:
    return add_fase1_2(nome=nome, cultura=cultura, hectares=hectares)


def update_area(area_id: int, nome: str | None, cultura: str | None, hectares: float | None) -> dict:
    return edit_fase1_2(area_id=area_id, nome=nome, cultura=cultura, hectares=hectares)


def delete_area(area_id: int) -> dict:
    return remove_fase1_2(area_id=area_id)


def monitor_now(limit: int = 20) -> dict:
    return monitor_and_alert_once(limit=limit)


def alerts_history(limit: int = 50) -> dict:
    return {
        "status": "ok",
        "total": limit,
        "items": read_history(limit=limit),
    }
