from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image, ImageStat


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _default_images_dir() -> Path:
    path = _repo_root() / "data" / "images"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _classify_brightness(img: Image.Image) -> tuple[str, float]:
    # Heuristica baseline para MVP local sem modelo pesado.
    stat = ImageStat.Stat(img.convert("RGB"))
    brightness = sum(stat.mean) / 3.0
    if brightness < 90:
        return "possivel_estresse", brightness
    if brightness > 180:
        return "alta_reflectancia", brightness
    return "normal", brightness


def infer_folder(folder: str | None = None, limit: int = 50) -> dict[str, Any]:
    base = Path(folder) if folder else _default_images_dir()
    if not base.exists():
        raise FileNotFoundError(f"Pasta de imagens nao encontrada: {base}")

    files = [
        p
        for p in sorted(base.iterdir())
        if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    ][:limit]

    results = []
    counts = {"normal": 0, "possivel_estresse": 0, "alta_reflectancia": 0}

    for file_path in files:
        with Image.open(file_path) as img:
            label, brightness = _classify_brightness(img)
            counts[label] = counts.get(label, 0) + 1
            results.append(
                {
                    "file": file_path.name,
                    "label": label,
                    "brightness": round(float(brightness), 2),
                    "size": {"w": img.width, "h": img.height},
                }
            )

    return {
        "images_dir": str(base),
        "total_images": len(files),
        "counts": counts,
        "results": results,
    }
