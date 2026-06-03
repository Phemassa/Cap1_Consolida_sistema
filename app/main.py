import json

import streamlit as st

from services.alert_service import AlertService
from services.healthcheck import collect_health
from services.orchestrator import alerts_history, infer_fase4, monitor_fase3, monitor_now, run_fase6_vision, run_phase, train_fase4


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

st.subheader("Fase 4 - Pipeline ML")
train_limit = st.slider("Amostras para treino Fase 4", min_value=20, max_value=300, value=120, step=10)
if st.button("Treinar Fase 4"):
    st.json(train_fase4(limit=train_limit, force_train=True))

col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    p_temp = st.number_input("Temperatura", value=30.0)
with col_p2:
    p_umidade = st.number_input("Umidade do solo", value=22.0)
with col_p3:
    p_ph = st.number_input("pH do solo", value=6.0)

if st.button("Prever necessidade de irrigacao"):
    st.json(infer_fase4(temperatura=p_temp, umidade_solo=p_umidade, ph_solo=p_ph))

st.subheader("Fase 6 - Visao Computacional (baseline)")
images_dir = st.text_input("Pasta de imagens (opcional)", value="")
vision_limit = st.slider("Qtd. max de imagens", min_value=1, max_value=200, value=50, step=1)
if st.button("Executar inferencia Fase 6"):
    st.json(run_fase6_vision(images_dir=images_dir or None, limit=vision_limit))

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

st.subheader("Fase 5 - Monitoramento e Mensageria AWS")
monitor_limit = st.slider("Janela de monitoramento", min_value=5, max_value=200, value=20, step=5)
if st.button("Monitorar agora e disparar alertas"):
    st.json(monitor_now(limit=monitor_limit))

history_limit = st.slider("Historico de alertas", min_value=5, max_value=200, value=20, step=5)
if st.button("Atualizar historico"):
    st.json(alerts_history(limit=history_limit))

st.subheader("Exemplo CLI")
st.code(
    "python cli.py health\n"
    "python cli.py run fase3\n"
    "python cli.py monitor-fase3 --limit 20\n"
    "python cli.py monitor-fase3 --limit 20 --send-alerts\n"
    "python cli.py train-fase4 --limit 120\n"
    "python cli.py predict-fase4 --temperatura 30 --umidade-solo 22 --ph-solo 6\n"
    "python cli.py run-fase6 --limit 50\n"
    "python cli.py run-fase6 --images-dir data/images --limit 20\n"
    "python cli.py monitor-now --limit 20\n"
    "python cli.py alerts-history --limit 20\n"
    "python cli.py alert-test --value 15 --threshold 20",
    language="bash",
)

st.subheader("Payload padrao de alerta")
st.code(json.dumps({"source": "fase3", "metric": "umidade_solo"}, indent=2), language="json")
