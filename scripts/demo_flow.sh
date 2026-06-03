#!/usr/bin/env bash
set -euo pipefail

echo "[1/8] Health"
python3 cli.py health

echo "[2/8] Fase 1-2"
python3 cli.py run fase1_2

echo "[3/8] Fase 3"
python3 cli.py monitor-fase3 --limit 20

echo "[4/8] Fase 4 train"
python3 cli.py train-fase4 --limit 120

echo "[5/8] Fase 4 predict"
python3 cli.py predict-fase4 --temperatura 30 --umidade-solo 22 --ph-solo 6

echo "[6/8] Fase 6"
python3 cli.py run-fase6 --images-dir data/images --limit 20

echo "[7/8] Monitor now"
python3 cli.py monitor-now --limit 20

echo "[8/8] Alerts history"
python3 cli.py alerts-history --limit 20
