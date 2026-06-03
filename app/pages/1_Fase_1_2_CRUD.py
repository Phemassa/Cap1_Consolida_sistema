import streamlit as st

from services.orchestrator import create_area, delete_area, run_phase, update_area


st.set_page_config(page_title="Fase 1-2 CRUD", layout="wide")
st.title("Fase 1-2 - CRUD de Areas")
st.caption("Base consolidada de areas em CSV")

st.subheader("Areas atuais")
st.json(run_phase("fase1_2"))

st.subheader("Criar area")
c1, c2, c3 = st.columns(3)
with c1:
    add_nome = st.text_input("Nome", value="Talhao X")
with c2:
    add_cultura = st.text_input("Cultura", value="milho")
with c3:
    add_hectares = st.number_input("Hectares", min_value=0.1, value=5.0)

if st.button("Adicionar area"):
    st.json(create_area(nome=add_nome, cultura=add_cultura, hectares=add_hectares))

st.subheader("Atualizar area")
u1, u2, u3, u4 = st.columns(4)
with u1:
    upd_id = st.number_input("ID area", min_value=1, value=1, step=1)
with u2:
    upd_nome = st.text_input("Novo nome (opcional)", value="")
with u3:
    upd_cultura = st.text_input("Nova cultura (opcional)", value="")
with u4:
    upd_hectares = st.number_input("Novo hectares (0 ignora)", min_value=0.0, value=0.0)

if st.button("Atualizar area"):
    st.json(
        update_area(
            area_id=int(upd_id),
            nome=upd_nome or None,
            cultura=upd_cultura or None,
            hectares=None if upd_hectares == 0 else float(upd_hectares),
        )
    )

st.subheader("Remover area")
del_id = st.number_input("ID para remover", min_value=1, value=2, step=1)
if st.button("Remover area"):
    st.json(delete_area(area_id=int(del_id)))
