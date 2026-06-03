import streamlit as st

from services.orchestrator import run_fase6_vision


st.set_page_config(page_title="Fase 6 Visao", layout="wide")
st.title("Fase 6 - Visao Computacional")
st.caption("Inferencia baseline por pasta de imagens")

images_dir = st.text_input("Pasta de imagens (opcional)", value="")
limit = st.slider("Qtd. max imagens", min_value=1, max_value=200, value=50, step=1)

if st.button("Executar inferencia"):
    st.json(run_fase6_vision(images_dir=images_dir or None, limit=limit))
