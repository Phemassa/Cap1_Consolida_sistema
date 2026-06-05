"""
FarmTech Solutions - Página de Previsões
========================================
Modelo de Machine Learning para previsões
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from database.database_manager import FarmTechDatabase

st.set_page_config(page_title="Previsões - FarmTech", page_icon="🔮", layout="wide")

@st.cache_resource
def init_database():
    return FarmTechDatabase('database/farmtech.db')

db = init_database()

st.title("🔮 Previsões e Recomendações")
st.markdown("### Modelo de Machine Learning para Irrigação Inteligente")
st.markdown("---")

# Formulário de Input
st.subheader("📝 Dados de Entrada")

with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        temperatura = st.slider("🌡️ Temperatura (°C)", 15.0, 40.0, 25.0, 0.5)
        umidade = st.slider("💧 Umidade Solo (%)", 20.0, 90.0, 60.0, 1.0)
        ph = st.slider("🧪 pH", 5.0, 8.0, 6.5, 0.1)
    
    with col2:
        nitrogenio = st.checkbox("🔵 Nitrogênio Adequado", value=True)
        fosforo = st.checkbox("🟡 Fósforo Adequado", value=True)
        potassio = st.checkbox("🟢 Potássio Adequado", value=False)
    
    with col3:
        cultura = st.selectbox("🌾 Cultura", ["banana", "milho"])
    
    submitted = st.form_submit_button("🔮 Fazer Previsão", type="primary")

if submitted:
    # Lógica de previsão (placeholder - será substituída por modelo real)
    st.markdown("---")
    st.subheader("📊 Resultados da Previsão")
    
    # Calcular volume de irrigação
    volume_irrigacao = 0.0
    if umidade < 50:
        volume_irrigacao = 10 - (umidade * 0.15)
    
    # Calcular dosagens NPK
    dosagem_n = 0 if nitrogenio else (12 if cultura == "milho" else 15)
    dosagem_p = 0 if fosforo else (8 if cultura == "milho" else 10)
    dosagem_k = 0 if potassio else (10 if cultura == "milho" else 20)
    
    # Estimar rendimento
    rendimento_base = 25000 if cultura == "banana" else 8000
    fator = 1.0
    
    if 50 <= umidade <= 70:
        fator *= 1.0
    else:
        fator *= 0.85
    
    if 6.0 <= ph <= 7.0:
        fator *= 1.0
    else:
        fator *= 0.9
    
    if 20 <= temperatura <= 30:
        fator *= 1.0
    else:
        fator *= 0.9
    
    rendimento = rendimento_base * fator
    
    # Exibir resultados
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💧 Volume de Irrigação",
            f"{max(0, volume_irrigacao):.1f} L/m²",
            help="Volume recomendado de água"
        )
    
    with col2:
        st.metric(
            "🌾 Rendimento Estimado",
            f"{rendimento:,.0f} kg/ha",
            f"{((rendimento/rendimento_base - 1) * 100):+.1f}%",
            help="Produção esperada"
        )
    
    with col3:
        dosagem_total = dosagem_n + dosagem_p + dosagem_k
        st.metric(
            "🧪 Fertilizante Total",
            f"{dosagem_total:.0f} g/m²",
            help="Soma de NPK necessário"
        )
    
    with col4:
        confianca = 85  # Placeholder
        st.metric(
            "🎯 Confiança",
            f"{confianca}%",
            help="Confiança do modelo"
        )
    
    # Detalhamento NPK
    st.markdown("---")
    st.subheader("🧪 Dosagens NPK Recomendadas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🔵 Nitrogênio (N)")
        if dosagem_n > 0:
            st.error(f"**{dosagem_n} g/m²** - Aplicação necessária")
            st.info("💡 Usar ureia ou nitrato de amônio")
        else:
            st.success("✅ Níveis adequados")
    
    with col2:
        st.markdown("#### 🟡 Fósforo (P)")
        if dosagem_p > 0:
            st.warning(f"**{dosagem_p} g/m²** - Aplicação necessária")
            st.info("💡 Usar superfosfato simples")
        else:
            st.success("✅ Níveis adequados")
    
    with col3:
        st.markdown("#### 🟢 Potássio (K)")
        if dosagem_k > 0:
            st.error(f"**{dosagem_k} g/m²** - Aplicação necessária")
            st.info("💡 Usar cloreto de potássio")
        else:
            st.success("✅ Níveis adequados")
    
    # Gráfico de comparação
    st.markdown("---")
    st.subheader("📊 Comparação com Ideal")
    
    fig = go.Figure()
    
    categorias = ['Nitrogênio', 'Fósforo', 'Potássio']
    ideal = [15 if cultura == "banana" else 12, 
             10 if cultura == "banana" else 8,
             20 if cultura == "banana" else 10]
    atual = [0 if nitrogenio else ideal[0],
             0 if fosforo else ideal[1],
             0 if potassio else ideal[2]]
    
    fig.add_trace(go.Bar(
        name='Ideal',
        x=categorias,
        y=ideal,
        marker_color='lightgreen'
    ))
    
    fig.add_trace(go.Bar(
        name='Deficit (a aplicar)',
        x=categorias,
        y=[dosagem_n, dosagem_p, dosagem_k],
        marker_color='lightcoral'
    ))
    
    fig.update_layout(
        title="Comparação NPK: Ideal vs Déficit",
        yaxis_title="Dosagem (g/m²)",
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Recomendações
    st.markdown("---")
    st.subheader("💡 Recomendações Personalizadas")
    
    if volume_irrigacao > 5:
        st.warning(f"🚰 **Irrigação urgente**: Aplicar {volume_irrigacao:.1f} L/m² imediatamente")
    elif volume_irrigacao > 2:
        st.info(f"💧 **Irrigação moderada**: Aplicar {volume_irrigacao:.1f} L/m² nas próximas horas")
    else:
        st.success("✅ **Sem necessidade de irrigação** no momento")
    
    if temperatura > 30:
        st.info("🌡️ Temperatura alta detectada. Considere irrigação noturna para reduzir evaporação.")
    
    if ph < 6.0:
        st.warning("🧪 pH baixo. Aplicar calcário para correção.")
    elif ph > 7.0:
        st.warning("🧪 pH alto. Aplicar enxofre para correção.")
    
    if cultura == "banana" and not potassio:
        st.error("🍌 **CRÍTICO para BANANA**: Potássio insuficiente! Prioridade máxima.")
    
    if cultura == "milho" and not nitrogenio:
        st.error("🌽 **CRÍTICO para MILHO**: Nitrogênio insuficiente! Prioridade máxima.")

# Histórico de Previsões
st.markdown("---")
st.subheader("📈 Histórico de Previsões")

@st.cache_data(ttl=10)
def load_predictions():
    query = """
    SELECT p.*, s.temperatura, s.umidade_solo, s.ph_solo
    FROM predictions p
    JOIN sensor_readings s ON p.reading_id = s.id
    ORDER BY p.timestamp DESC
    LIMIT 50
    """
    return pd.read_sql_query(query, db.conn)

try:
    df_pred = load_predictions()
    if not df_pred.empty:
        st.dataframe(df_pred, use_container_width=True)
    else:
        st.info("Nenhuma previsão registrada ainda. Execute o sistema de ingestão.")
except Exception as e:
    st.warning(f"Erro ao carregar previsões: {e}")

# Métricas do Modelo
st.markdown("---")
st.subheader("🎯 Métricas do Modelo ML")

col1, col2, col3, col4 = st.columns(4)

# Placeholder - será atualizado com modelo real
col1.metric("MAE", "2.3 L/m²", help="Mean Absolute Error")
col2.metric("RMSE", "3.1 L/m²", help="Root Mean Squared Error")
col3.metric("R²", "0.87", help="Coeficiente de Determinação")
col4.metric("Acurácia", "89%", help="Acurácia geral")

st.info("💡 **Nota**: Métricas serão atualizadas após treinamento do modelo real com dados históricos.")

st.markdown("---")
st.caption("🌾 FarmTech Solutions - Previsões ML | Modelo v1.0")