"""
FarmTech Solutions - Página de Tendências
=========================================
Análise de séries temporais e padrões
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from database.database_manager import FarmTechDatabase

st.set_page_config(page_title="Tendências - FarmTech", page_icon="📈", layout="wide")

@st.cache_resource
def init_database():
    return FarmTechDatabase('database/farmtech.db')

db = init_database()

st.title("📈 Análise de Tendências")
st.markdown("### Séries Temporais e Padrões de Comportamento")
st.markdown("---")

# Filtros de período
col1, col2 = st.columns(2)

with col1:
    periodo = st.selectbox(
        "⏰ Período de Análise",
        ["Últimas 24 horas", "Últimos 7 dias", "Últimos 30 dias", "Todos"]
    )

with col2:
    cultura_filtro = st.selectbox(
        "🌾 Filtrar por Cultura",
        ["Todas", "banana", "milho"]
    )

@st.cache_data(ttl=30)
def load_time_series_data(periodo_sel, cultura_sel):
    query = """
    SELECT 
        s.id,
        s.timestamp,
        s.temperatura,
        s.umidade_solo,
        s.ph_solo,
        s.nitrogenio as nitrogenio_ok,
        s.fosforo as fosforo_ok,
        s.potassio as potassio_ok,
        s.irrigacao_ativa,
        s.cultura,
        i.duracao_minutos,
        i.volume_aplicado as volume_litros
    FROM sensor_readings s
    LEFT JOIN irrigation_actions i ON s.id = i.reading_id
    ORDER BY s.timestamp
    """
    df = pd.read_sql_query(query, db.conn)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Filtrar por período
    if periodo_sel == "Últimas 24 horas":
        df = df[df['timestamp'] >= df['timestamp'].max() - pd.Timedelta(hours=24)]
    elif periodo_sel == "Últimos 7 dias":
        df = df[df['timestamp'] >= df['timestamp'].max() - pd.Timedelta(days=7)]
    elif periodo_sel == "Últimos 30 dias":
        df = df[df['timestamp'] >= df['timestamp'].max() - pd.Timedelta(days=30)]
    
    # Filtrar por cultura
    if cultura_sel != "Todas":
        df = df[df['cultura'] == cultura_sel]
    
    return df

try:
    df = load_time_series_data(periodo, cultura_filtro)
    
    if df.empty:
        st.warning("⚠️ Nenhum dado disponível para o período selecionado.")
    else:
        # Estatísticas do período
        st.subheader("📊 Estatísticas do Período")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        col1.metric(
            "📝 Total de Leituras",
            f"{len(df):,}",
            help="Número de medições realizadas"
        )
        
        col2.metric(
            "🌡️ Temp. Média",
            f"{df['temperatura'].mean():.1f}°C",
            help="Temperatura média do período"
        )
        
        col3.metric(
            "💧 Umidade Média",
            f"{df['umidade_solo'].mean():.1f}%",
            help="Umidade média do solo"
        )
        
        irrigacoes = df['duracao_minutos'].notna().sum()
        col4.metric(
            "🚰 Irrigações",
            f"{irrigacoes}",
            help="Eventos de irrigação"
        )
        
        volume_total = df['volume_litros'].sum() if 'volume_litros' in df else 0
        col5.metric(
            "💦 Volume Total",
            f"{volume_total:.0f} L",
            help="Volume total irrigado"
        )
        
        # Gráfico de múltiplas séries temporais
        st.markdown("---")
        st.subheader("📈 Evolução Temporal de Parâmetros")
        
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            subplot_titles=(
                '🌡️ Temperatura', 
                '💧 Umidade do Solo',
                '🧪 pH do Solo',
                '🚰 Volume de Irrigação'
            ),
            vertical_spacing=0.08
        )
        
        # Temperatura
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['temperatura'],
                mode='lines',
                name='Temperatura',
                line=dict(color='red', width=2)
            ),
            row=1, col=1
        )
        
        # Umidade
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['umidade_solo'],
                mode='lines',
                name='Umidade',
                line=dict(color='blue', width=2),
                fill='tozeroy'
            ),
            row=2, col=1
        )
        
        # pH
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['ph_solo'],
                mode='lines',
                name='pH',
                line=dict(color='green', width=2)
            ),
            row=3, col=1
        )
        
        # Volume de irrigação
        df_irrigacao = df[df['volume_litros'].notna()]
        fig.add_trace(
            go.Bar(
                x=df_irrigacao['timestamp'],
                y=df_irrigacao['volume_litros'],
                name='Volume',
                marker_color='lightblue'
            ),
            row=4, col=1
        )
        
        fig.update_xaxes(title_text="Tempo", row=4, col=1)
        fig.update_yaxes(title_text="°C", row=1, col=1)
        fig.update_yaxes(title_text="%", row=2, col=1)
        fig.update_yaxes(title_text="pH", row=3, col=1)
        fig.update_yaxes(title_text="Litros", row=4, col=1)
        
        fig.update_layout(height=1000, showlegend=False)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Análise de Correlação Temporal
        st.markdown("---")
        st.subheader("🔄 Correlação Temporal entre Variáveis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Temperatura vs Umidade
            fig1 = px.scatter(
                df, 
                x='temperatura', 
                y='umidade_solo',
                color='ph_solo',
                title='🌡️ Temperatura vs 💧 Umidade (colorido por pH)',
                labels={'temperatura': 'Temperatura (°C)', 'umidade_solo': 'Umidade (%)', 'ph_solo': 'pH'},
                trendline='ols'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # pH vs NPK
            df['npk_adequado'] = (df['nitrogenio_ok'] & df['fosforo_ok'] & df['potassio_ok']).astype(int)
            fig2 = px.box(
                df,
                x='npk_adequado',
                y='ph_solo',
                title='🧪 pH vs Status NPK',
                labels={'npk_adequado': 'NPK Adequado (0=Não, 1=Sim)', 'ph_solo': 'pH'},
                color='npk_adequado'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Padrões de Irrigação
        st.markdown("---")
        st.subheader("🚰 Padrões de Irrigação")
        
        df_irrig = df[df['duracao_minutos'].notna()].copy()
        
        if not df_irrig.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Histograma de duração
                fig3 = px.histogram(
                    df_irrig,
                    x='duracao_minutos',
                    title='⏱️ Distribuição de Duração de Irrigação',
                    labels={'duracao_minutos': 'Duração (minutos)'},
                    nbins=20
                )
                st.plotly_chart(fig3, use_container_width=True)
            
            with col2:
                # Irrigação por cultura
                if 'cultura' in df_irrig.columns:
                    fig4 = px.pie(
                        df_irrig,
                        names='cultura',
                        values='volume_litros',
                        title='💦 Volume por Cultura'
                    )
                    st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Nenhuma irrigação registrada no período selecionado.")
        
        # Tendências e Previsões
        st.markdown("---")
        st.subheader("🔮 Identificação de Tendências")
        
        # Calcular médias móveis
        df['temp_ma7'] = df['temperatura'].rolling(window=min(7, len(df))).mean()
        df['umid_ma7'] = df['umidade_solo'].rolling(window=min(7, len(df))).mean()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌡️ Tendência de Temperatura")
            fig5 = go.Figure()
            fig5.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['temperatura'],
                mode='lines',
                name='Valor Real',
                line=dict(color='lightcoral', width=1)
            ))
            fig5.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['temp_ma7'],
                mode='lines',
                name='Média Móvel',
                line=dict(color='red', width=3)
            ))
            fig5.update_layout(xaxis_title="Tempo", yaxis_title="°C")
            st.plotly_chart(fig5, use_container_width=True)
            
            # Análise de tendência
            if len(df) > 1:
                tendencia_temp = df['temperatura'].iloc[-1] - df['temperatura'].iloc[0]
                if abs(tendencia_temp) > 1:
                    if tendencia_temp > 0:
                        st.warning(f"⚠️ Temperatura em **alta**: +{tendencia_temp:.1f}°C")
                    else:
                        st.info(f"📉 Temperatura em **queda**: {tendencia_temp:.1f}°C")
                else:
                    st.success("✅ Temperatura **estável**")
        
        with col2:
            st.markdown("#### 💧 Tendência de Umidade")
            fig6 = go.Figure()
            fig6.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['umidade_solo'],
                mode='lines',
                name='Valor Real',
                line=dict(color='lightblue', width=1)
            ))
            fig6.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['umid_ma7'],
                mode='lines',
                name='Média Móvel',
                line=dict(color='blue', width=3)
            ))
            fig6.update_layout(xaxis_title="Tempo", yaxis_title="%")
            st.plotly_chart(fig6, use_container_width=True)
            
            # Análise de tendência
            if len(df) > 1:
                tendencia_umid = df['umidade_solo'].iloc[-1] - df['umidade_solo'].iloc[0]
                if abs(tendencia_umid) > 5:
                    if tendencia_umid > 0:
                        st.info(f"📈 Umidade em **alta**: +{tendencia_umid:.1f}%")
                    else:
                        st.error(f"⚠️ Umidade em **queda**: {tendencia_umid:.1f}%")
                else:
                    st.success("✅ Umidade **estável**")
        
        # Tabela de dados resumidos
        st.markdown("---")
        st.subheader("📋 Dados Detalhados")
        
        # Agrupar por dia
        df['date'] = df['timestamp'].dt.date
        daily_stats = df.groupby('date').agg({
            'temperatura': ['mean', 'min', 'max'],
            'umidade_solo': ['mean', 'min', 'max'],
            'ph_solo': 'mean',
            'duracao_minutos': 'sum',
            'volume_litros': 'sum'
        }).round(2)
        
        daily_stats.columns = ['Temp Média', 'Temp Min', 'Temp Max', 
                               'Umid Média', 'Umid Min', 'Umid Max',
                               'pH Médio', 'Irrig (min)', 'Volume (L)']
        
        st.dataframe(daily_stats, use_container_width=True)
        
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.info("Execute o sistema de auto-ingestão para gerar dados: `python database/database_manager.py`")

st.markdown("---")
st.caption("🌾 FarmTech Solutions - Análise de Tendências | Atualização automática a cada 30s")