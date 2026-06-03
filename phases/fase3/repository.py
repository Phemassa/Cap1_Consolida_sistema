from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from app.config import settings

try:
    import oracledb
except ImportError:
    oracledb = None


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _csv_candidates() -> list[Path]:
    root = _repo_root()
    return [
        root / "data" / "sensor_readings.csv",
        root / "data" / "sensor_readings_sample.csv",
    ]


def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "TEMPERATURA": "temperatura",
        "UMIDADE_SOLO": "umidade_solo",
        "PH_SOLO": "ph_solo",
        "CULTURA": "cultura",
        "IRRIGACAO_REALIZADA": "irrigacao_ativa",
        "DATA_HORA": "timestamp",
    }
    df = df.rename(columns=rename_map)

    if "timestamp" not in df.columns:
        if "DATA" in df.columns and "HORA" in df.columns:
            df["timestamp"] = df["DATA"].astype(str) + " " + df["HORA"].astype(str)
        else:
            df["timestamp"] = pd.Timestamp.utcnow().isoformat()

    expected = ["timestamp", "temperatura", "umidade_solo", "ph_solo", "cultura", "irrigacao_ativa"]
    for col in expected:
        if col not in df.columns:
            df[col] = None

    for col in ["temperatura", "umidade_solo", "ph_solo"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["cultura"] = df["cultura"].fillna("indefinida").astype(str)
    df["irrigacao_ativa"] = df["irrigacao_ativa"].fillna(False)

    return df[expected]


def _from_oracle(limit: int) -> pd.DataFrame | None:
    if oracledb is None:
        return None

    if not (settings.oracle_user and settings.oracle_password and settings.oracle_host):
        return None

    dsn = f"{settings.oracle_host}:{settings.oracle_port}/{settings.oracle_service_name}"
    query = f"""
        SELECT *
        FROM SENSORES
        ORDER BY DATA DESC, HORA DESC
        FETCH FIRST {int(limit)} ROWS ONLY
    """

    try:
        with oracledb.connect(
            user=settings.oracle_user,
            password=settings.oracle_password,
            dsn=dsn,
        ) as conn:
            return pd.read_sql(query, con=conn)
    except Exception:
        return None


def _from_csv(limit: int) -> pd.DataFrame:
    for path in _csv_candidates():
        if path.exists():
            df = pd.read_csv(path)
            return df.tail(limit).copy()
    raise FileNotFoundError("Nenhum CSV de fallback encontrado em data/")


def load_latest_readings(limit: int = 20) -> tuple[list[dict[str, Any]], str]:
    oracle_df = _from_oracle(limit)
    if oracle_df is not None and not oracle_df.empty:
        norm = _normalize(oracle_df)
        return norm.to_dict(orient="records"), "oracle"

    csv_df = _from_csv(limit)
    norm = _normalize(csv_df)
    return norm.to_dict(orient="records"), "csv_fallback"
