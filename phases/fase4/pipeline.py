from __future__ import annotations

import json
import pickle
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import cross_val_score, train_test_split


FEATURES = ["temperatura", "umidade_solo", "ph_solo"]


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

    for col in FEATURES:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["irrigation_needed"] = (
        (df["umidade_solo"] < 25)
        | (df["temperatura"] > 32)
        | (df["ph_solo"] < 5.5)
        | (df["ph_solo"] > 7.5)
    ).astype(int)
    return df.dropna(subset=FEATURES).copy()


def _expand_samples(df: pd.DataFrame, target_size: int = 120) -> pd.DataFrame:
    if df.empty or len(df) >= target_size:
        return df
    expanded = [df]
    idx = 0
    while sum(len(chunk) for chunk in expanded) < target_size:
        base = df.iloc[[idx % len(df)]].copy()
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


def _dataset_summary(df: pd.DataFrame) -> dict[str, Any]:
    desc = df[FEATURES].describe().round(3).to_dict()
    counts = df["irrigation_needed"].value_counts().to_dict()
    total = int(len(df))
    pos = int(counts.get(1, 0))
    neg = int(counts.get(0, 0))
    return {
        "total": total,
        "positives": pos,
        "negatives": neg,
        "positive_ratio": round(pos / total, 4) if total else 0.0,
        "describe": desc,
        "preview": df.head(8).round(3).to_dict(orient="records"),
    }


def _feature_importance(model: Any, name: str) -> list[dict[str, Any]]:
    if hasattr(model, "feature_importances_"):
        values = model.feature_importances_
    elif hasattr(model, "coef_"):
        values = np.abs(model.coef_).flatten()
    else:
        return []
    total = float(np.sum(values)) or 1.0
    return [
        {"feature": feat, "importance": round(float(val) / total, 4)}
        for feat, val in zip(FEATURES, values)
    ]


def _roc_payload(y_true: pd.Series, y_score: np.ndarray | None) -> dict[str, Any] | None:
    if y_score is None or len(np.unique(y_true)) < 2:
        return None
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auc = float(roc_auc_score(y_true, y_score))
    return {
        "auc": round(auc, 4),
        "fpr": [round(float(x), 4) for x in fpr],
        "tpr": [round(float(x), 4) for x in tpr],
    }


def train_models(rows: list[dict[str, Any]]) -> dict[str, Any]:
    df = _to_frame(rows)
    if df.empty:
        raise ValueError("Sem dados validos para treino da Fase 4")
    df = _expand_samples(df)

    x = df[FEATURES]
    y = df["irrigation_needed"]

    stratify = y if y.nunique() > 1 else None
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=stratify
    )

    candidates = {
        "logistic": LogisticRegression(max_iter=300),
        "random_forest": RandomForestClassifier(n_estimators=120, random_state=42),
        "gradient_boosting": GradientBoostingClassifier(random_state=42),
    }

    metrics: dict[str, Any] = {}
    trained: dict[str, Any] = {}

    for name, model in candidates.items():
        t0 = time.perf_counter()
        model.fit(x_train, y_train)
        train_ms = round((time.perf_counter() - t0) * 1000.0, 2)

        pred = model.predict(x_test)
        proba = None
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(x_test)[:, 1]

        cm = confusion_matrix(y_test, pred, labels=[0, 1]).tolist()

        cv_scores: list[float] = []
        if stratify is not None:
            try:
                cv_scores = [
                    round(float(s), 4)
                    for s in cross_val_score(model, x, y, cv=5, scoring="f1")
                ]
            except Exception:
                cv_scores = []

        metrics[name] = {
            "accuracy": round(float(accuracy_score(y_test, pred)), 4),
            "precision": round(float(precision_score(y_test, pred, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, pred, zero_division=0)), 4),
            "f1": round(float(f1_score(y_test, pred, zero_division=0)), 4),
            "train_ms": train_ms,
            "confusion_matrix": cm,
            "feature_importance": _feature_importance(model, name),
            "roc": _roc_payload(y_test, proba),
            "cv_f1_scores": cv_scores,
            "cv_f1_mean": round(float(np.mean(cv_scores)), 4) if cv_scores else None,
            "cv_f1_std": round(float(np.std(cv_scores)), 4) if cv_scores else None,
        }
        trained[name] = model

    best_model = max(
        metrics.items(),
        key=lambda item: (item[1]["f1"], item[1]["accuracy"], -item[1]["train_ms"]),
    )[0]

    payload = {
        "best_model": best_model,
        "models": trained,
        "features": FEATURES,
    }
    with _models_file().open("wb") as fp:
        pickle.dump(payload, fp)

    report: dict[str, Any] = {
        "total_samples": int(len(df)),
        "train_samples": int(len(x_train)),
        "test_samples": int(len(x_test)),
        "best_model": best_model,
        "metrics": metrics,
        "dataset": _dataset_summary(df),
        "labels": ["nao_irrigar", "irrigar"],
        "features": FEATURES,
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
