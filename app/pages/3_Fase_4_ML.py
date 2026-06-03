import streamlit as st

from services.orchestrator import infer_fase4, train_fase4


st.set_page_config(page_title="Fase 4 ML", layout="wide")
st.title("Fase 4 - Pipeline ML")
st.caption("Treino, metricas e predicao de necessidade de irrigacao")

train_limit = st.slider("Amostras para treino", min_value=20, max_value=300, value=120, step=10)
if st.button("Treinar modelos"):
    st.json(train_fase4(limit=train_limit, force_train=True))

st.subheader("Predicao")
p1, p2, p3 = st.columns(3)
with p1:
    temperatura = st.number_input("Temperatura", value=30.0)
with p2:
    umidade_solo = st.number_input("Umidade do solo", value=22.0)
with p3:
    ph_solo = st.number_input("pH do solo", value=6.0)

if st.button("Prever"):
    st.json(infer_fase4(temperatura=temperatura, umidade_solo=umidade_solo, ph_solo=ph_solo))
