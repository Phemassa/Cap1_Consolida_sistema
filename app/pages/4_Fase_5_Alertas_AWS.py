import streamlit as st

from services.alert_service import AlertService
from services.orchestrator import alerts_history, monitor_now


st.set_page_config(page_title="Fase 5 Alertas", layout="wide")
st.title("Fase 5 - Mensageria AWS")
st.caption("Monitoramento e historico de eventos de alerta")

st.subheader("Teste manual de alerta")
value = st.number_input("Umidade do solo", min_value=0.0, max_value=100.0, value=15.0)
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

st.subheader("Monitoramento com disparo")
monitor_limit = st.slider("Janela de monitoramento", min_value=5, max_value=200, value=20, step=5)
if st.button("Monitorar agora"):
    st.json(monitor_now(limit=monitor_limit))

st.subheader("Historico")
history_limit = st.slider("Registros", min_value=5, max_value=200, value=20, step=5)
if st.button("Atualizar historico"):
    st.json(alerts_history(limit=history_limit))
