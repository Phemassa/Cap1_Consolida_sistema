"""
FarmTech Solutions - Dashboard Principal
=========================================
Dashboard interativo para análise de dados agrícolas
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Adiciona path do projeto
sys.path.append(str(Path(__file__).parent.parent))

from database.database_manager import FarmTechDatabase

# Configuração da página
st.set_page_config(
    page_title="FarmTech Solutions",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E7D32;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E7D32;
    }
    .stAlert {
        background-color: #E8F5E9;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar conexão com banco de dados
@st.cache_resource
def init_database():
    """Inicializa conexão com banco de dados"""
    return FarmTechDatabase('database/farmtech.db')

db = init_database()

# Sidebar
st.sidebar.image("https://via.placeholder.com/200x80/2E7D32/FFFFFF?text=FarmTech", use_container_width=True)
st.sidebar.title("🌾 FarmTech Solutions")
st.sidebar.markdown("### Sistema de Irrigação Inteligente")

# Filtros
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Filtros")

cultura_filter = st.sidebar.selectbox(
    "Cultura",
    ["Todas", "banana", "milho"]
)

periodo_filter = st.sidebar.selectbox(
    "Período",
    ["Últimas 24h", "Última semana", "Último mês", "Tudo"]
)

limit_map = {
    "Últimas 24h": 288,  # 24h * 60min / 5min
    "Última semana": 2016,
    "Último mês": 8640,
    "Tudo": 10000
}

# Header
st.markdown('<h1 class="main-header">🌾 FarmTech Solutions Dashboard</h1>', unsafe_allow_html=True)
st.markdown("### 📊 Análise em Tempo Real - Sistema de Irrigação Inteligente")
st.markdown("---")

# Carregar dados
@st.cache_data(ttl=5)  # Cache por 5 segundos
def load_data(limit, cultura):
    """Carrega dados do banco"""
    if cultura == "Todas":
        return db.get_recent_readings(limit=limit)
    else:
        return db.get_recent_readings(limit=limit, cultura=cultura)

df = load_data(limit_map[periodo_filter], 
               None if cultura_filter == "Todas" else cultura_filter)

if df.empty:
    st.warning("⚠️ Nenhum dado encontrado. Execute o sistema de ingestão primeiro!")
    st.info("💡 Execute: `python database/database_manager.py`")
    st.stop()

# KPIs Principais
st.subheader("📈 Indicadores Principais")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    temp_media = df['temperatura'].mean()
    temp_delta = df['temperatura'].iloc[0] - df['temperatura'].iloc[-1] if len(df) > 1 else 0
    st.metric(
        "🌡️ Temperatura Média",
        f"{temp_media:.1f}°C",
        f"{temp_delta:+.1f}°C"
    )

with col2:
    umid_media = df['umidade_solo'].mean()
    umid_delta = df['umidade_solo'].iloc[0] - df['umidade_solo'].iloc[-1] if len(df) > 1 else 0
    st.metric(
        "💧 Umidade Média",
        f"{umid_media:.1f}%",
        f"{umid_delta:+.1f}%"
    )

with col3:
    ph_media = df['ph_solo'].mean()
    ph_status = "✅" if 6.0 <= ph_media <= 7.0 else "⚠️"
    st.metric(
        f"{ph_status} pH Médio",
        f"{ph_media:.2f}",
        ""
    )

with col4:
    irrigacoes = df['irrigacao_ativa'].sum()
    perc_irrigacao = (irrigacoes / len(df) * 100) if len(df) > 0 else 0
    st.metric(
        "🚰 Irrigações Ativas",
        f"{irrigacoes}",
        f"{perc_irrigacao:.1f}%"
    )

with col5:
    npk_ok = ((df['nitrogenio'] == 1) & (df['fosforo'] == 1) & (df['potassio'] == 1)).sum()
    perc_npk = (npk_ok / len(df) * 100) if len(df) > 0 else 0
    st.metric(
        "🧪 NPK Adequado",
        f"{npk_ok}",
        f"{perc_npk:.1f}%"
    )

st.markdown("---")

# Gráficos principais
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌡️ Evolução da Temperatura")
    fig_temp = px.line(
        df.tail(100),
        x='timestamp',
        y='temperatura',
        color='cultura' if 'cultura' in df.columns else None,
        title="Temperatura ao longo do tempo"
    )
    fig_temp.update_layout(
        xaxis_title="Data/Hora",
        yaxis_title="Temperatura (°C)",
        hovermode='x unified'
    )
    st.plotly_chart(fig_temp, use_container_width=True)

with col2:
    st.subheader("💧 Evolução da Umidade do Solo")
    fig_umid = px.line(
        df.tail(100),
        x='timestamp',
        y='umidade_solo',
        color='cultura' if 'cultura' in df.columns else None,
        title="Umidade do solo ao longo do tempo"
    )
    fig_umid.add_hline(y=40, line_dash="dash", line_color="red", 
                       annotation_text="Mínimo (40%)")
    fig_umid.add_hline(y=60, line_dash="dash", line_color="green", 
                       annotation_text="Ideal (60%)")
    fig_umid.update_layout(
        xaxis_title="Data/Hora",
        yaxis_title="Umidade (%)",
        hovermode='x unified'
    )
    st.plotly_chart(fig_umid, use_container_width=True)

# Gráfico de pH
st.subheader("🧪 Evolução do pH do Solo")
fig_ph = px.line(
    df.tail(100),
    x='timestamp',
    y='ph_solo',
    color='cultura' if 'cultura' in df.columns else None,
    title="pH do solo ao longo do tempo"
)
fig_ph.add_hrect(y0=6.0, y1=7.0, fillcolor="green", opacity=0.1, 
                 annotation_text="Faixa Ideal", annotation_position="top left")
fig_ph.update_layout(
    xaxis_title="Data/Hora",
    yaxis_title="pH",
    hovermode='x unified'
)
st.plotly_chart(fig_ph, use_container_width=True)

# Status NPK
st.markdown("---")
st.subheader("🧪 Status dos Nutrientes (NPK)")

col1, col2, col3 = st.columns(3)

with col1:
    n_ok = (df['nitrogenio'] == 1).sum()
    n_perc = (n_ok / len(df) * 100) if len(df) > 0 else 0
    
    fig_n = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=n_perc,
        title={'text': "Nitrogênio (N)"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "lightyellow"},
                {'range': [80, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    st.plotly_chart(fig_n, use_container_width=True)

with col2:
    p_ok = (df['fosforo'] == 1).sum()
    p_perc = (p_ok / len(df) * 100) if len(df) > 0 else 0
    
    fig_p = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=p_perc,
        title={'text': "Fósforo (P)"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkorange"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "lightyellow"},
                {'range': [80, 100], 'color': "lightgreen"}
            ]
        }
    ))
    st.plotly_chart(fig_p, use_container_width=True)

with col3:
    k_ok = (df['potassio'] == 1).sum()
    k_perc = (k_ok / len(df) * 100) if len(df) > 0 else 0
    
    fig_k = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=k_perc,
        title={'text': "Potássio (K)"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkgreen"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "lightyellow"},
                {'range': [80, 100], 'color': "lightgreen"}
            ]
        }
    ))
    st.plotly_chart(fig_k, use_container_width=True)

# Alertas e Recomendações
st.markdown("---")
st.subheader("💡 Alertas e Recomendações")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ⚠️ Alertas Ativos")
    
    # Verificar condições críticas
    if umid_media < 40:
        st.error("🚨 **CRÍTICO**: Umidade do solo muito baixa! Irrigação urgente necessária.")
    elif umid_media < 50:
        st.warning("⚠️ **ATENÇÃO**: Umidade do solo abaixo do ideal. Considere irrigar.")
    else:
        st.success("✅ Umidade do solo em níveis adequados.")
    
    if ph_media < 5.5:
        st.warning("⚠️ Solo muito ácido. Recomenda-se aplicação de calcário.")
    elif ph_media > 7.5:
        st.warning("⚠️ Solo muito alcalino. Ajuste o pH.")
    else:
        st.success("✅ pH do solo em níveis adequados.")
    
    if perc_npk < 50:
        st.error("🚨 **CRÍTICO**: Níveis de NPK insuficientes. Aplicar fertilizantes urgentemente.")
    elif perc_npk < 70:
        st.warning("⚠️ **ATENÇÃO**: Considere fertilização em breve.")
    else:
        st.success("✅ Níveis de NPK adequados.")

with col2:
    st.markdown("#### 📋 Recomendações")
    
    recomendacoes = []
    
    if umid_media < 50:
        recomendacoes.append("💧 Aumentar frequência de irrigação")
    
    if ph_media < 6.0:
        recomendacoes.append("🧪 Aplicar calcário para elevar pH")
    elif ph_media > 7.0:
        recomendacoes.append("🧪 Aplicar enxofre para reduzir pH")
    
    if n_perc < 70:
        recomendacoes.append("🔵 Aplicar fertilizante nitrogenado (ureia)")
    
    if p_perc < 70:
        recomendacoes.append("🟡 Aplicar superfosfato simples")
    
    if k_perc < 70:
        recomendacoes.append("🟢 Aplicar cloreto de potássio")
    
    if temp_media > 30:
        recomendacoes.append("🌡️ Considerar irrigação noturna (reduz evaporação)")
    
    if recomendacoes:
        for rec in recomendacoes:
            st.info(rec)
    else:
        st.success("✅ Nenhuma ação necessária no momento. Condições ideais!")

# Dados recentes
st.markdown("---")
st.subheader("📊 Dados Recentes")

# Mostra últimas 10 leituras
st.dataframe(
    df.head(10)[['timestamp', 'temperatura', 'umidade_solo', 'ph_solo', 
                 'nitrogenio', 'fosforo', 'potassio', 'irrigacao_ativa', 'cultura']],
    use_container_width=True
)

# Estatísticas do banco
stats = db.get_statistics()

st.markdown("---")
st.subheader("📈 Estatísticas Gerais do Sistema")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de Leituras", f"{stats['total_leituras']:,}")

with col2:
    st.metric("Total de Previsões", f"{stats['total_previsoes']:,}")

with col3:
    st.metric("Total de Ações", f"{stats['total_acoes']:,}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌾 <strong>FarmTech Solutions</strong> - Sistema de Irrigação Inteligente</p>
    <p>FIAP - Projeto Fase 2 | Outubro 2025</p>
    <p>Atualização automática a cada 5 segundos</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh (recarrega página a cada 5 segundos)
st.markdown("""
<script>
    setTimeout(function() {
        window.location.reload();
    }, 5000);
</script>
""", unsafe_allow_html=True)