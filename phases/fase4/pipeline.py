from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _runtime_dir() -> Path:
    path = _repo_root() / "data" / "runtime"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _models_file() -> Path:
    return _runtime_dir() / "fase4_models.pkl"


def _metrics_file() -> Path:
    return _runtime_dir() / "fase4_metrics.json"


def _to_frame(rows: list[dict[str, Any]]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    if df.empty:
        return df

    for col in ["temperatura", "umidade_solo", "ph_solo"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Label operacional inicial para treino supervisionado.
    df["irrigation_needed"] = (
        (df["umidade_solo"] < 25) | (df["temperatura"] > 32) | (df["ph_solo"] < 5.5) | (df["ph_solo"] > 7.5)
    ).astype(int)

    df = df.dropna(subset=["temperatura", "umidade_solo", "ph_solo"]).copy()
    return df


def _expand_samples(df: pd.DataFrame, target_size: int = 120) -> pd.DataFrame:
    if df.empty:
        return df

    if len(df) >= target_size:
        return df

    expanded = [df]
    idx = 0
    while sum(len(chunk) for chunk in expanded) < target_size:
        base = df.iloc[[idx % len(df)]].copy()
        # Pequeno jitter para permitir treino de forma robusta em datasets curtos.
        base["temperatura"] = (base["temperatura"] + ((idx % 5) - 2) * 0.15).clip(lower=-5, upper=60)
        base["umidade_solo"] = (base["umidade_solo"] + ((idx % 7) - 3) * 0.5).clip(lower=0, upper=100)
        base["ph_solo"] = (base["ph_solo"] + ((idx % 3) - 1) * 0.03).clip(lower=0, upper=14)
        base["irrigation_needed"] = (
            (base["umidade_solo"] < 25)
            | (base["temperatura"] > 32)
            | (base["ph_solo"] < 5.5)
            | (base["ph_solo"] > 7.5)
        ).astype(int)
        expanded.append(base)
        idx += 1

    return pd.concat(expanded, ignore_index=True)


def train_models(rows: list[dict[str, Any]]) -> dict[str, Any]:
    df = _to_frame(rows)
    if df.empty:
        raise ValueError("Sem dados validos para treino da Fase 4")

    df = _expand_samples(df)
    x = df[["temperatura", "umidade_solo", "ph_solo"]]
    y = df["irrigation_needed"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y if y.nunique() > 1 else None
    )

    models = {
        "logistic": LogisticRegression(max_iter=300),
        "random_forest": RandomForestClassifier(n_estimators=120, random_state=42),
        "gradient_boosting": GradientBoostingClassifier(random_state=42),
    }

    metrics: dict[str, Any] = {}
    trained: dict[str, Any] = {}

    for name, model in models.items():
        model.fit(x_train, y_train)
        pred = model.predict(x_test)
        metrics[name] = {
            "accuracy": round(float(accuracy_score(y_test, pred)), 4),
            "precision": round(float(precision_score(y_test, pred, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, pred, zero_division=0)), 4),
            "f1": round(float(f1_score(y_test, pred, zero_division=0)), 4),
        }
        trained[name] = model

    best_model = max(metrics.items(), key=lambda item: item[1]["f1"])[0]

    payload = {
        "best_model": best_model,
        "models": trained,
        "features": ["temperatura", "umidade_solo", "ph_solo"],
    }
    with _models_file().open("wb") as fp:
        pickle.dump(payload, fp)

    report = {
        "total_samples": int(len(df)),
        "train_samples": int(len(x_train)),
        "test_samples": int(len(x_test)),
        "best_model": best_model,
        "metrics": metrics,
    }
    _metrics_file().write_text(json.dumps(report, indent=2, ensure_ascii=True), encoding="utf-8")
    return report


def load_metrics() -> dict[str, Any] | None:
    path = _metrics_file()
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def predict(data: dict[str, float]) -> dict[str, Any]:
    model_path = _models_file()
    if not model_path.exists():
        raise FileNotFoundError("Modelos nao treinados. Execute o treino da Fase 4 primeiro.")

    with model_path.open("rb") as fp:
        payload = pickle.load(fp)

    best_name = payload["best_model"]
    model = payload["models"][best_name]
    features = payload["features"]

    x = pd.DataFrame([data])[features]
    pred = int(model.predict(x)[0])

    probability = None
    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(x)[0][1])

    return {
        "model": best_name,
        "prediction": pred,
        "needs_irrigation": bool(pred == 1),
        "probability": round(probability, 4) if probability is not None else None,
        "input": data,
    }
