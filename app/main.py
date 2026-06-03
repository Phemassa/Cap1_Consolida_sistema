import json

import streamlit as st

from services.alert_service import AlertService
from services.healthcheck import collect_health
from services.orchestrator import monitor_fase3, run_phase


st.set_page_config(page_title="FarmTech Fase 7", layout="wide")
st.title("FarmTech - Consolidacao Fase 7")
st.caption("Orquestracao hibrida: dashboard + CLI")

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

st.subheader("Monitoramento Fase 3 (Oracle/CSV)")
limit = st.slider("Qtd. de leituras", min_value=5, max_value=200, value=20, step=5)
send_alerts = st.checkbox("Enviar alertas AWS ao monitorar", value=False)

if st.button("Coletar snapshot Fase 3"):
    st.json(monitor_fase3(limit=limit, send_alerts=send_alerts))

st.subheader("Health Check")
if st.button("Atualizar status"):
    st.json(collect_health())

st.subheader("Teste de Alerta AWS por E-mail")
value = st.number_input("Umidade do solo (teste)", min_value=0.0, max_value=100.0, value=15.0)
threshold = st.number_input("Limiar", min_value=0.0, max_value=100.0, value=20.0)

if st.button("Disparar alerta de teste"):
    service = AlertService()
    payload = {
        "source": "fase3",
        "metric": "umidade_solo",
        "value": value,
        "threshold": threshold,
        "action": "Verificar irrigacao e iniciar ajuste corretivo",
    }
    st.json(service.send_alert(payload))

st.subheader("Exemplo CLI")
st.code(
    "python cli.py health\n"
    "python cli.py run fase3\n"
    "python cli.py monitor-fase3 --limit 20\n"
    "python cli.py monitor-fase3 --limit 20 --send-alerts\n"
    "python cli.py alert-test --value 15 --threshold 20",
    language="bash",
)

st.subheader("Payload padrao de alerta")
st.code(json.dumps({"source": "fase3", "metric": "umidade_solo"}, indent=2), language="json")
