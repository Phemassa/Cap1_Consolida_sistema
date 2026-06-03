from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _data_file() -> Path:
    path = _repo_root() / "data" / "areas.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        pd.DataFrame(
            [
                {"id": 1, "nome": "Talhao A", "cultura": "milho", "hectares": 10.5},
                {"id": 2, "nome": "Talhao B", "cultura": "banana", "hectares": 8.0},
            ]
        ).to_csv(path, index=False)
    return path


def _read_df() -> pd.DataFrame:
    return pd.read_csv(_data_file())


def _write_df(df: pd.DataFrame) -> None:
    df.to_csv(_data_file(), index=False)


def list_areas() -> list[dict[str, Any]]:
    df = _read_df()
    return df.to_dict(orient="records")


def create_area(nome: str, cultura: str, hectares: float) -> dict[str, Any]:
    df = _read_df()
    next_id = 1 if df.empty else int(df["id"].max()) + 1
    row = {"id": next_id, "nome": nome, "cultura": cultura, "hectares": float(hectares)}
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    _write_df(df)
    return row


def update_area(area_id: int, nome: str | None, cultura: str | None, hectares: float | None) -> dict[str, Any] | None:
    df = _read_df()
    mask = df["id"] == int(area_id)
    if not mask.any():
        return None

    if nome is not None:
        df.loc[mask, "nome"] = nome
    if cultura is not None:
        df.loc[mask, "cultura"] = cultura
    if hectares is not None:
        df.loc[mask, "hectares"] = float(hectares)

    _write_df(df)
    row = df.loc[mask].iloc[0].to_dict()
    return row


def delete_area(area_id: int) -> bool:
    df = _read_df()
    before = len(df)
    df = df[df["id"] != int(area_id)].copy()
    _write_df(df)
    return len(df) < before
