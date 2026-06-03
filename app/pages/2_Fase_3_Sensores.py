import streamlit as st

from services.orchestrator import monitor_fase3


st.set_page_config(page_title="Fase 3 Sensores", layout="wide")
st.title("Fase 3 - Sensores Oracle/CSV")
st.caption("Coleta consolidada com fallback local")

limit = st.slider("Quantidade de leituras", min_value=5, max_value=200, value=20, step=5)
send_alerts = st.checkbox("Enviar alertas durante monitoramento", value=False)

if st.button("Coletar snapshot"):
    st.json(monitor_fase3(limit=limit, send_alerts=send_alerts))
