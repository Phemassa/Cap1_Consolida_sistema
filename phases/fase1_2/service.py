from datetime import datetime

from phases.fase1_2.repository import create_area, delete_area, list_areas, update_area


def run() -> dict:
    areas = list_areas()
    return {
        "phase": "fase1_2",
        "status": "ok",
        "message": "Modulo Fase 1-2 com CRUD CSV ativo",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "total_areas": len(areas),
        "areas": areas,
    }


def add(nome: str, cultura: str, hectares: float) -> dict:
    area = create_area(nome=nome, cultura=cultura, hectares=hectares)
    return {
        "phase": "fase1_2",
        "status": "ok",
        "action": "create",
        "area": area,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def edit(area_id: int, nome: str | None, cultura: str | None, hectares: float | None) -> dict:
    area = update_area(area_id=area_id, nome=nome, cultura=cultura, hectares=hectares)
    if area is None:
        return {
            "phase": "fase1_2",
            "status": "error",
            "message": f"Area {area_id} nao encontrada",
        }
    return {
        "phase": "fase1_2",
        "status": "ok",
        "action": "update",
        "area": area,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def remove(area_id: int) -> dict:
    deleted = delete_area(area_id=area_id)
    if not deleted:
        return {
            "phase": "fase1_2",
            "status": "error",
            "message": f"Area {area_id} nao encontrada",
        }
    return {
        "phase": "fase1_2",
        "status": "ok",
        "action": "delete",
        "area_id": area_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
