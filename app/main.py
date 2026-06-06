import streamlit as st
import sys
from pathlib import Path

# Garante imports absolutos a partir da raiz do projeto.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.healthcheck import collect_health
from services.orchestrator import run_phase


st.set_page_config(page_title="FarmTech Fase 7", layout="wide")
st.title("FarmTech - Consolidacao Fase 7")
st.caption("Home da plataforma consolidada (use o menu lateral para acessar cada fase)")

st.success(
    "✨ **Cockpit Operacional** (Mission Control) na barra lateral: executa o pipeline real "
    "Fase 1-2 → 3 → 4 → decisao → 5 → 6 ao vivo, com veredito de irrigacao, rastro das fases e telemetria."
)

col_a, col_b, col_c = st.columns(3)

with col_a:
    if st.button("Executar Fase 1 e 2"):
        st.json(run_phase("fase1_2"))

with col_b:
    if st.button("Executar Fase 3"):
        st.json(run_phase("fase3"))

with col_c:
    if st.button("Executar Fase 4"):
        st.json(run_phase("fase4"))

if st.button("Executar Fase 6"):
    st.json(run_phase("fase6"))

st.subheader("Health Check")
if st.button("Atualizar status"):
    st.json(collect_health())

st.subheader("Exemplo CLI")
st.code(
    "python cli.py health\n"
    "python cli.py run fase1_2\n"
    "python cli.py run fase3\n"
    "python cli.py monitor-fase3 --limit 20\n"
    "python cli.py monitor-fase3 --limit 20 --send-alerts\n"
    "python cli.py train-fase4 --limit 120\n"
    "python cli.py predict-fase4 --temperatura 30 --umidade-solo 22 --ph-solo 6\n"
    "python cli.py run-fase6 --limit 50\n"
    "python cli.py run-fase6 --images-dir data/images --limit 20\n"
    "python cli.py area-add --nome Talhao_C --cultura soja --hectares 12\n"
    "python cli.py area-update --id 1 --hectares 11\n"
    "python cli.py area-delete --id 2\n"
    "python cli.py monitor-now --limit 20\n"
    "python cli.py alerts-history --limit 20\n"
    "python cli.py alert-test --value 15 --threshold 20\n"
    "python cli.py pipeline --limit 22",
    language="bash",
)

st.subheader("Navegacao")
st.markdown("Use as paginas no menu lateral para operacoes detalhadas por fase.")

