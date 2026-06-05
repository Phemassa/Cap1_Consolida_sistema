"""
FarmTech Solutions - Página de Correlações
==========================================
Análise de correlações entre variáveis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from database.database_manager import FarmTechDatabase

st.set_page_config(page_title="Correlações - FarmTech", page_icon="📊", layout="wide")

# Inicializar banco
@st.cache_resource
def init_database():
    return FarmTechDatabase('database/farmtech.db')

db = init_database()

st.title("📊 Análise de Correlações")
st.markdown("### Relações entre variáveis agrícolas")
st.markdown("---")

# Carregar dados
@st.cache_data(ttl=10)
def load_data():
    return db.get_recent_readings(limit=1000)

df = load_data()

if df.empty:
    st.warning("⚠️ Nenhum dado disponível")
    st.stop()

# Preparar dados numéricos
df_numeric = df[['temperatura', 'umidade_solo', 'ph_solo', 
                 'nitrogenio', 'fosforo', 'potassio', 'irrigacao_ativa']].copy()

# Matriz de Correlação
st.subheader("🔢 Matriz de Correlação")

# Calcular correlação
corr_matrix = df_numeric.corr()

# Heatmap com Plotly
fig_corr = px.imshow(
    corr_matrix,
    text_auto='.2f',
    aspect="auto",
    color_continuous_scale='RdBu_r',
    title="Correlação entre Variáveis"
)
fig_corr.update_layout(
    width=800,
    height=600
)
st.plotly_chart(fig_corr, use_container_width=True)

# Interpretação
st.markdown("#### 💡 Interpretação:")
st.info("""
- **Valores próximos de +1**: Correlação positiva forte (crescem juntas)
- **Valores próximos de -1**: Correlação negativa forte (uma cresce, outra diminui)  
- **Valores próximos de 0**: Sem correlação
""")

# Scatter Plots Interativos
st.markdown("---")
st.subheader("📈 Análise de Relações (Scatter Plots)")

col1, col2 = st.columns(2)

with col1:
    x_var = st.selectbox("Variável X", df_numeric.columns, index=0)

with col2:
    y_var = st.selectbox("Variável Y", df_numeric.columns, index=1)

# Criar scatter plot
fig_scatter = px.scatter(
    df,
    x=x_var,
    y=y_var,
    color='cultura' if 'cultura' in df.columns else None,
    trendline="ols",
    title=f"Relação entre {x_var} e {y_var}"
)
fig_scatter.update_layout(hovermode='closest')
st.plotly_chart(fig_scatter, use_container_width=True)

# Pairplot (grid de correlações)
st.markdown("---")
st.subheader("📊 Grid de Correlações (Pairplot)")

if st.checkbox("Gerar Pairplot (pode demorar)"):
    with st.spinner("Gerando gráficos..."):
        # Seleciona subset de variáveis
        vars_selected = st.multiselect(
            "Selecione variáveis",
            df_numeric.columns.tolist(),
            default=['temperatura', 'umidade_solo', 'ph_solo']
        )
        
        if len(vars_selected) >= 2:
            fig, axes = plt.subplots(len(vars_selected), len(vars_selected), 
                                    figsize=(15, 15))
            
            for i, var1 in enumerate(vars_selected):
                for j, var2 in enumerate(vars_selected):
                    ax = axes[i, j]
                    if i == j:
                        # Diagonal: histograma
                        ax.hist(df[var1], bins=20, edgecolor='black')
                        ax.set_ylabel('Frequência')
                    else:
                        # Off-diagonal: scatter
                        ax.scatter(df[var2], df[var1], alpha=0.5)
                    
                    if i == len(vars_selected) - 1:
                        ax.set_xlabel(var2)
                    if j == 0:
                        ax.set_ylabel(var1)
            
            plt.tight_layout()
            st.pyplot(fig)

# Análises Específicas
st.markdown("---")
st.subheader("🎯 Análises Específicas")

tab1, tab2, tab3 = st.tabs(["Umidade vs Irrigação", "pH vs NPK", "Temperatura vs Umidade"])

with tab1:
    st.markdown("#### 💧 Relação Umidade x Irrigação")
    
    fig1 = px.box(
        df,
        x='irrigacao_ativa',
        y='umidade_solo',
        color='irrigacao_ativa',
        title="Distribuição de Umidade por Status de Irrigação"
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Estatísticas
    irrig_on = df[df['irrigacao_ativa'] == 1]['umidade_solo'].mean()
    irrig_off = df[df['irrigacao_ativa'] == 0]['umidade_solo'].mean()
    
    col1, col2 = st.columns(2)
    col1.metric("Umidade Média (Irrigação ON)", f"{irrig_on:.1f}%")
    col2.metric("Umidade Média (Irrigação OFF)", f"{irrig_off:.1f}%")

with tab2:
    st.markdown("#### 🧪 Relação pH x NPK")
    
    # Criar variável NPK combinada
    df['npk_status'] = (df['nitrogenio'].astype(bool) & 
                        df['fosforo'].astype(bool) & 
                        df['potassio'].astype(bool)).astype(int)
    
    fig2 = px.violin(
        df,
        x='npk_status',
        y='ph_solo',
        color='npk_status',
        box=True,
        title="Distribuição de pH por Status NPK"
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    npk_ok = df[df['npk_status'] == 1]['ph_solo'].mean()
    npk_low = df[df['npk_status'] == 0]['ph_solo'].mean()
    
    col1, col2 = st.columns(2)
    col1.metric("pH Médio (NPK OK)", f"{npk_ok:.2f}")
    col2.metric("pH Médio (NPK Baixo)", f"{npk_low:.2f}")

with tab3:
    st.markdown("#### 🌡️ Relação Temperatura x Umidade")
    
    fig3 = px.density_contour(
        df,
        x='temperatura',
        y='umidade_solo',
        marginal_x="histogram",
        marginal_y="histogram",
        title="Densidade: Temperatura vs Umidade"
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    # Correlação específica
    corr_temp_umid = df['temperatura'].corr(df['umidade_solo'])
    st.metric(
        "Correlação Temperatura-Umidade", 
        f"{corr_temp_umid:.3f}",
        help="Valores próximos de -1 indicam que umidade diminui quando temperatura aumenta"
    )

# Insights Automáticos
st.markdown("---")
st.subheader("💡 Insights Descobertos")

insights = []

# Análise de correlações fortes
for i in range(len(corr_matrix)):
    for j in range(i+1, len(corr_matrix)):
        corr_value = corr_matrix.iloc[i, j]
        if abs(corr_value) > 0.5:
            var1 = corr_matrix.index[i]
            var2 = corr_matrix.columns[j]
            tipo = "positiva" if corr_value > 0 else "negativa"
            insights.append(f"📊 Correlação **{tipo}** forte entre `{var1}` e `{var2}` (r={corr_value:.2f})")

if insights:
    for insight in insights:
        st.markdown(insight)
else:
    st.info("Nenhuma correlação forte detectada nos dados atuais.")

# Footer
st.markdown("---")
st.caption("🌾 FarmTech Solutions - Análise de Correlações | Atualizado automaticamente")