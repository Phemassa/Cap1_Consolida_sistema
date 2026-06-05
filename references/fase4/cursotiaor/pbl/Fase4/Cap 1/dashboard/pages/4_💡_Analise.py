"""
FarmTech Solutions - Página de Análise Inteligente
=================================================
Insights automáticos e recomendações baseadas em IA
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from database.database_manager import FarmTechDatabase

st.set_page_config(page_title="Análise - FarmTech", page_icon="💡", layout="wide")

@st.cache_resource
def init_database():
    return FarmTechDatabase('database/farmtech.db')

db = init_database()

st.title("💡 Análise Inteligente")
st.markdown("### Insights Automáticos e Recomendações Estratégicas")
st.markdown("---")

@st.cache_data(ttl=60)
def load_analysis_data():
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
        i.volume_aplicado as volume_litros,
        i.motivo as motivo_irrigacao
    FROM sensor_readings s
    LEFT JOIN irrigation_actions i ON s.id = i.reading_id
    ORDER BY s.timestamp DESC
    """
    df = pd.read_sql_query(query, db.conn)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

try:
    df = load_analysis_data()
    
    if df.empty:
        st.warning("⚠️ Nenhum dado disponível. Execute o sistema de auto-ingestão.")
    else:
        # Análise de Performance Geral
        st.subheader("🎯 Performance do Sistema")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Eficiência de irrigação
        total_leituras = len(df)
        leituras_irrigadas = df['duracao_minutos'].notna().sum()
        eficiencia = (1 - leituras_irrigadas / total_leituras) * 100 if total_leituras > 0 else 0
        
        col1.metric(
            "⚡ Eficiência Geral",
            f"{eficiencia:.1f}%",
            help="Percentual de tempo sem necessidade de irrigação"
        )
        
        # Qualidade NPK
        df['npk_completo'] = (df['nitrogenio_ok'] & df['fosforo_ok'] & df['potassio_ok']).astype(int)
        qualidade_npk = df['npk_completo'].mean() * 100
        
        col2.metric(
            "🧪 Qualidade NPK",
            f"{qualidade_npk:.1f}%",
            help="Percentual com todos nutrientes adequados"
        )
        
        # Estabilidade pH
        ph_dentro_range = ((df['ph_solo'] >= 5.5) & (df['ph_solo'] <= 7.5)).sum()
        estabilidade_ph = (ph_dentro_range / len(df)) * 100
        
        col3.metric(
            "⚖️ Estabilidade pH",
            f"{estabilidade_ph:.1f}%",
            help="Percentual com pH ideal (5.5-7.5)"
        )
        
        # Consumo de água
        consumo_agua = df['volume_litros'].sum()
        col4.metric(
            "💧 Consumo Total",
            f"{consumo_agua:.0f} L",
            help="Volume total de água utilizado"
        )
        
        # Insights Automáticos
        st.markdown("---")
        st.subheader("🔍 Insights Detectados Automaticamente")
        
        insights = []
        
        # Análise 1: Temperatura
        temp_media = df['temperatura'].mean()
        temp_atual = df['temperatura'].iloc[0]
        if temp_atual > 30:
            insights.append({
                'nivel': 'critical',
                'icone': '🌡️',
                'titulo': 'Temperatura Crítica',
                'descricao': f'Temperatura atual de {temp_atual:.1f}°C está acima do ideal (30°C).',
                'acao': 'Considere irrigação nas horas mais frescas (início da manhã ou final da tarde) para reduzir evaporação.'
            })
        elif temp_atual < 15:
            insights.append({
                'nivel': 'warning',
                'icone': '❄️',
                'titulo': 'Temperatura Baixa',
                'descricao': f'Temperatura de {temp_atual:.1f}°C pode retardar crescimento.',
                'acao': 'Monitore geadas. Considere cobertura do solo para manter temperatura.'
            })
        
        # Análise 2: Umidade
        umid_media = df['umidade_solo'].mean()
        umid_atual = df['umidade_solo'].iloc[0]
        if umid_atual < 40:
            insights.append({
                'nivel': 'critical',
                'icone': '🚨',
                'titulo': 'Solo Muito Seco',
                'descricao': f'Umidade de {umid_atual:.1f}% abaixo do mínimo (40%).',
                'acao': 'Irrigação urgente necessária! Aplicar água imediatamente.'
            })
        elif umid_atual > 80:
            insights.append({
                'nivel': 'warning',
                'icone': '💦',
                'titulo': 'Solo Saturado',
                'descricao': f'Umidade de {umid_atual:.1f}% acima do máximo (80%).',
                'acao': 'Suspender irrigação. Verificar drenagem do solo. Risco de doenças radiculares.'
            })
        
        # Análise 3: pH
        ph_atual = df['ph_solo'].iloc[0]
        if ph_atual < 5.5:
            insights.append({
                'nivel': 'warning',
                'icone': '🧪',
                'titulo': 'Solo Ácido',
                'descricao': f'pH de {ph_atual:.2f} abaixo do ideal (5.5-7.5).',
                'acao': 'Aplicar calcário dolomítico (200-300 kg/ha) para correção de acidez.'
            })
        elif ph_atual > 7.5:
            insights.append({
                'nivel': 'warning',
                'icone': '🧪',
                'titulo': 'Solo Alcalino',
                'descricao': f'pH de {ph_atual:.2f} acima do ideal (5.5-7.5).',
                'acao': 'Aplicar enxofre elementar (50-100 kg/ha) para acidificar o solo.'
            })
        
        # Análise 4: NPK
        n_ok = df['nitrogenio_ok'].iloc[0]
        p_ok = df['fosforo_ok'].iloc[0]
        k_ok = df['potassio_ok'].iloc[0]
        
        if not n_ok:
            insights.append({
                'nivel': 'critical',
                'icone': '🔵',
                'titulo': 'Deficiência de Nitrogênio',
                'descricao': 'Nitrogênio insuficiente detectado.',
                'acao': 'Aplicar ureia (45% N) ou nitrato de amônio (33% N). Dose: 100-150 kg/ha.'
            })
        
        if not p_ok:
            insights.append({
                'nivel': 'warning',
                'icone': '🟡',
                'titulo': 'Deficiência de Fósforo',
                'descricao': 'Fósforo abaixo do recomendado.',
                'acao': 'Aplicar superfosfato simples (18% P2O5). Dose: 80-120 kg/ha.'
            })
        
        if not k_ok:
            insights.append({
                'nivel': 'critical',
                'icone': '🟢',
                'titulo': 'Deficiência de Potássio',
                'descricao': 'Potássio insuficiente - crítico para banana.',
                'acao': 'Aplicar cloreto de potássio (60% K2O). Dose: 150-200 kg/ha. URGENTE!'
            })
        
        # Análise 5: Padrão de irrigação
        if leituras_irrigadas > total_leituras * 0.7:
            insights.append({
                'nivel': 'warning',
                'icone': '💧',
                'titulo': 'Alto Consumo de Água',
                'descricao': f'{(leituras_irrigadas/total_leituras*100):.0f}% das leituras necessitaram irrigação.',
                'acao': 'Verificar: 1) Vazamentos, 2) Eficiência do sistema, 3) Drenagem do solo.'
            })
        
        # Exibir insights
        if insights:
            for insight in insights:
                if insight['nivel'] == 'critical':
                    st.error(f"**{insight['icone']} {insight['titulo']}**\n\n{insight['descricao']}\n\n**🎯 Ação Recomendada:** {insight['acao']}")
                elif insight['nivel'] == 'warning':
                    st.warning(f"**{insight['icone']} {insight['titulo']}**\n\n{insight['descricao']}\n\n**💡 Recomendação:** {insight['acao']}")
                else:
                    st.info(f"**{insight['icone']} {insight['titulo']}**\n\n{insight['descricao']}\n\n**✅ Sugestão:** {insight['acao']}")
        else:
            st.success("✅ **Sistema operando perfeitamente!** Todas as condições estão dentro dos parâmetros ideais.")
        
        # Comparação entre Culturas
        st.markdown("---")
        st.subheader("🌾 Comparação entre Culturas")
        
        if 'cultura' in df.columns and df['cultura'].nunique() > 1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Volume por cultura
                vol_cultura = df.groupby('cultura')['volume_litros'].sum().reset_index()
                fig1 = px.bar(
                    vol_cultura,
                    x='cultura',
                    y='volume_litros',
                    title='💦 Volume de Água por Cultura',
                    labels={'cultura': 'Cultura', 'volume_litros': 'Volume (Litros)'},
                    color='cultura'
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Qualidade NPK por cultura
                npk_cultura = df.groupby('cultura')['npk_completo'].mean().reset_index()
                npk_cultura['npk_completo'] = npk_cultura['npk_completo'] * 100
                fig2 = px.bar(
                    npk_cultura,
                    x='cultura',
                    y='npk_completo',
                    title='🧪 Qualidade NPK por Cultura',
                    labels={'cultura': 'Cultura', 'npk_completo': 'NPK Adequado (%)'},
                    color='cultura'
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        # Recomendações Estratégicas
        st.markdown("---")
        st.subheader("📋 Plano de Ação Recomendado")
        
        st.markdown("""
        ### 🎯 Prioridades Imediatas (0-24h)
        1. **Irrigação**: Verificar condições de umidade e temperatura
        2. **NPK**: Aplicar nutrientes deficientes conforme análise
        3. **pH**: Corrigir solo se fora da faixa ideal
        
        ### 📅 Ações de Curto Prazo (1-7 dias)
        - Monitorar resposta das plantas aos ajustes
        - Coletar amostras de solo para análise laboratorial
        - Verificar sistema de irrigação quanto a vazamentos
        
        ### 🔮 Planejamento de Médio Prazo (1-4 semanas)
        - Implementar fertirrigação para otimizar aplicação de NPK
        - Considerar rotação de culturas se problemas persistirem
        - Avaliar sistema de drenagem
        
        ### 💰 Análise Econômica
        """)
        
        # Cálculo de custos (valores estimados)
        custo_agua = consumo_agua * 0.01  # R$ 0,01 por litro
        custo_npk = 0
        
        if not n_ok:
            custo_npk += 150  # Ureia
        if not p_ok:
            custo_npk += 120  # Superfosfato
        if not k_ok:
            custo_npk += 200  # Cloreto K
        
        col1, col2, col3 = st.columns(3)
        
        col1.metric("💧 Custo de Água", f"R$ {custo_agua:.2f}")
        col2.metric("🧪 Custo de Fertilizantes", f"R$ {custo_npk:.2f}")
        col3.metric("💰 Custo Total Estimado", f"R$ {custo_agua + custo_npk:.2f}")
        
        # Relatório Exportável
        st.markdown("---")
        st.subheader("📄 Exportar Relatório")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Gerar Relatório CSV", type="primary"):
                # Criar relatório resumido
                relatorio = df.head(100).to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=relatorio,
                    file_name=f"relatorio_farmtech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📈 Gerar Relatório Estatístico", type="secondary"):
                stats = df.describe().to_csv()
                st.download_button(
                    label="⬇️ Download Estatísticas",
                    data=stats,
                    file_name=f"estatisticas_farmtech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        # Diagnóstico do Sistema
        st.markdown("---")
        st.subheader("🔧 Diagnóstico do Sistema")
        
        # Calcular health score
        health_score = 0
        max_score = 100
        
        # Temperatura (20 pontos)
        if 20 <= temp_atual <= 30:
            health_score += 20
        elif 15 <= temp_atual <= 35:
            health_score += 10
        
        # Umidade (25 pontos)
        if 50 <= umid_atual <= 70:
            health_score += 25
        elif 40 <= umid_atual <= 80:
            health_score += 15
        
        # pH (20 pontos)
        if 5.5 <= ph_atual <= 7.5:
            health_score += 20
        elif 5.0 <= ph_atual <= 8.0:
            health_score += 10
        
        # NPK (35 pontos)
        if n_ok:
            health_score += 12
        if p_ok:
            health_score += 11
        if k_ok:
            health_score += 12
        
        # Exibir health score
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=health_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Índice de Saúde do Sistema"},
                delta={'reference': 80},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkgreen" if health_score > 80 else "orange" if health_score > 60 else "red"},
                    'steps': [
                        {'range': [0, 60], 'color': "lightcoral"},
                        {'range': [60, 80], 'color': "lightyellow"},
                        {'range': [80, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig_gauge.update_layout(height=300)
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            st.metric("🎯 Score", f"{health_score}/100")
            if health_score >= 80:
                st.success("✅ Excelente")
            elif health_score >= 60:
                st.warning("⚠️ Regular")
            else:
                st.error("❌ Crítico")
        
        with col3:
            st.metric("📈 Meta", "90/100")
            delta = health_score - 90
            st.metric("Gap", f"{delta:+d} pts")
        
except Exception as e:
    st.error(f"❌ Erro ao carregar análise: {e}")
    st.info("Execute o sistema de auto-ingestão: `python database/database_manager.py`")

st.markdown("---")
st.caption("🌾 FarmTech Solutions - Análise Inteligente | IA-Powered Insights")