# Origem: https://github.com/Phemassa/Cap_1_Rede_Neural (Fase 6) | artefatos em references/fase6/
from datetime import datetime

from phases.fase6.pipeline import infer_folder


def run(images_dir: str | None = None, limit: int = 50) -> dict:
    report = infer_folder(folder=images_dir, limit=limit)
    return {
        "phase": "fase6",
        "status": "ok",
        "message": "Inferencia de visao executada",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "input_mode": "images_folder",
        "report": report,
    }
