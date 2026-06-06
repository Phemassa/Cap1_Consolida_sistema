"""Captura screenshots reais das paginas do dashboard Streamlit via Playwright.

Uso:
    python scripts/capture_evidencias.py [--base-url http://localhost:8502]

Requer o dashboard rodando (PYTHONPATH=$PWD streamlit run app/main.py).
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT_DIR = Path(__file__).resolve().parents[1] / "assets" / "evidencias"


def _shot(page, filename: str) -> None:
    target = OUT_DIR / filename
    page.screenshot(path=str(target), full_page=True)
    print(f"   salvo: {target}")


def _goto(page, base_url: str, route: str, settle: float = 3.0) -> None:
    url = f"{base_url}{route}"
    print(f"-> {url}")
    page.goto(url, wait_until="networkidle", timeout=60000)
    try:
        page.wait_for_selector("[data-testid='stAppViewContainer']", timeout=30000)
    except Exception:
        pass
    time.sleep(settle)


def _click_text(page, role: str, name: str, settle: float = 4.0) -> None:
    try:
        page.get_by_role(role, name=name).first.click(timeout=15000)
        time.sleep(settle)
    except Exception as exc:  # pragma: no cover - best effort
        print(f"   aviso: nao clicou em {name!r}: {exc}")


def capture(base_url: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)

        # 1. Cockpit Operacional (hero: pipeline real + veredito + gauges)
        _goto(page, base_url, "/Cockpit_Operacional", settle=6)
        _shot(page, "dashboard_home.png")

        # 2. Portal de apresentacao (visao geral) + aba Fase 4 com graficos ricos
        _goto(page, base_url, "/Portal_Apresentacao", settle=5)
        _shot(page, "portal_apresentacao.png")
        _click_text(page, "tab", "Fase 4", settle=5)
        _shot(page, "fase4_treino_metricas.png")

        # 3. Fase 1-2 CRUD
        _goto(page, base_url, "/Fase_1_2_CRUD", settle=3)
        _shot(page, "fase1_2_crud.png")

        # 4. Fase 3 sensores
        _goto(page, base_url, "/Fase_3_Sensores", settle=4)
        _shot(page, "fase3_snapshot.png")

        # 5. Fase 4 ML - executa predicao real e captura resultado
        _goto(page, base_url, "/Fase_4_ML", settle=3)
        _click_text(page, "button", "Prever", settle=4)
        _shot(page, "fase4_predicao.png")

        # 6. Fase 5 alertas
        _goto(page, base_url, "/Fase_5_Alertas_AWS", settle=4)
        _shot(page, "fase5_alertas.png")

        # 7. Fase 6 visao
        _goto(page, base_url, "/Fase_6_Visao", settle=4)
        _shot(page, "fase6_inferencia.png")

        browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Captura evidencias do dashboard")
    parser.add_argument("--base-url", default="http://localhost:8502")
    args = parser.parse_args()
    capture(args.base_url)
    print("Concluido.")


if __name__ == "__main__":
    main()
