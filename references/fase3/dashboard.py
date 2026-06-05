import os
import streamlit as st
import oracledb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="FarmTech Solutions - Dashboard de Irrigação",
    page_icon="🌱",
    layout="wide"
)

# Título
st.title("🌱 FarmTech Solutions - Dashboard de Monitoramento Agrícola")
st.markdown("**Sistema IoT de Irrigação Inteligente para Cultivo de Banana**")

# Configurações de conexão Oracle
# NOTA: por segurança, prefira definir a senha via variável de ambiente ORACLE_PASSWORD
ORACLE_CONFIG = {
    'user': 'RM566826',
    # IMPORTANT: do NOT commit real passwords. Use environment variables instead.
    # Replace the value below with a placeholder or leave empty before committing.
    'password': 'SUA_DATA_NASCIMENTO_AQUI',  # fallback - preferir usar env var ORACLE_PASSWORD
    'host': 'oracle.fiap.com.br',
    'port': 1521,
    'sid': 'ORCL'
}

# Runtime password: prefer ORACLE_PASSWORD env var, otherwise allow user to type it in the sidebar
ORACLE_PASSWORD_RUNTIME = os.environ.get('ORACLE_PASSWORD')
if not ORACLE_PASSWORD_RUNTIME:
    st.sidebar.subheader("🔐 Conexão Oracle")
    st.sidebar.write("A senha não foi definida via variável de ambiente. Você pode digitá-la abaixo (formato DDMMAA).")
    ORACLE_PASSWORD_RUNTIME = st.sidebar.text_input("Senha Oracle (DDMMAA)", type="password", key="oracle_pwd_input")
    
# Runtime user: prefer ORACLE_USER env var, otherwise allow user to type it in the sidebar
ORACLE_USER_RUNTIME = os.environ.get('ORACLE_USER')
if not ORACLE_USER_RUNTIME:
    ORACLE_USER_RUNTIME = st.sidebar.text_input("Usuário Oracle (ex: RM566826)", value=ORACLE_CONFIG.get('user'), key="oracle_user_input")

def conectar_oracle():
    """Estabelece conexão com o banco Oracle"""
    # Prefer runtime password (env var or sidebar input) then fallback to config
    password = os.environ.get('ORACLE_PASSWORD') or ORACLE_PASSWORD_RUNTIME or ORACLE_CONFIG.get('password')

    # Se o password ainda for o placeholder ou vazio, interromper e orientar o usuário
    if not password or password == 'SUA_DATA_NASCIMENTO_AQUI':
        st.error("A senha do Oracle não foi fornecida. Defina a variável de ambiente ORACLE_PASSWORD ou digite a senha na barra lateral.")
        st.info("No PowerShell (temporário): $env:ORACLE_PASSWORD=\"161083\"  # substitua pela sua data DDMMAA")
        return None

    try:
        # Escolher usuário em runtime (env var > sidebar > config)
        user = os.environ.get('ORACLE_USER') or ORACLE_USER_RUNTIME or ORACLE_CONFIG.get('user')

        connection = oracledb.connect(
            user=user,
            password=password,
            host=ORACLE_CONFIG['host'],
            port=ORACLE_CONFIG['port'],
            service_name=ORACLE_CONFIG['sid']
        )
        return connection
    except oracledb.Error as error:
        msg = str(error)
        # Detectar erro de autenticação e fornecer instruções específicas
        if 'ORA-01017' in msg or 'invalid username/password' in msg:
            st.error("Erro de autenticação: credenciais inválidas (ORA-01017). Verifique seu usuário/senha.")
            st.info("Soluções:\n - Confirme a senha (data de nascimento DDMMAA)\n - Defina a variável de ambiente ORACLE_PASSWORD no PowerShell: $env:ORACLE_PASSWORD=\"161083\"\n - Ou atualize 'ORACLE_CONFIG' em dashboard.py e reinicie o app")
        else:
            st.error(f"Erro ao conectar ao Oracle: {error}")
        return None

def carregar_dados():
    """Carrega dados do banco Oracle"""
    conn = conectar_oracle()
    if conn is None:
        return None

    try:
        query = "SELECT * FROM SENSORES ORDER BY DATA, HORA"
        df = pd.read_sql(query, conn)

        # --- Normalizações e limpeza de dados ---------------------------------
        def _auto_scale(series, low, high, max_iter=15):
            """Normalize numeric series by dividing by 10 repeatedly until the median
            falls into the expected [low, high] range or until max_iter is reached.

            This is more robust for integers that were stored as scaled values
            (e.g. 172102137871826 representing 17.21...).
            """
            s = pd.to_numeric(series, errors='coerce')
            if s.dropna().empty:
                return s

            scaled = s.copy()
            for _ in range(max_iter):
                med = scaled.median()
                if pd.isna(med):
                    break
                if low <= med <= high:
                    return scaled.round(3)
                # If median is too large, divide by 10 and retry
                if med > high:
                    scaled = scaled / 10.0
                    continue
                # If median is too small, try multiplying by 10 (handles some odd cases)
                if med < low:
                    scaled = scaled * 10.0
                    continue

            # fallback: return original coercion (no scaling applied)
            return s

        # Normalize numeric-like columns that may be scaled in the Oracle table
        scale_targets = {
            'TEMPERATURA': (-50, 60),
            'UMIDADE_SOLO': (0, 100),
            'PH_SOLO': (0, 14),
            'UMIDADE_AR': (0, 100),
            'PRESSAO_ATMOSFERICA': (800, 1100),
            'VENTO_KMH': (0, 200),
            'PRECIPITACAO': (0, 500),
            'PRODUTIVIDADE': (0, 100)
        }

        for col, (low, high) in scale_targets.items():
            if col in df.columns:
                df[col] = _auto_scale(df[col], low, high)

        # Convert precipitation and wind to numeric
        if 'PRECIPITACAO' in df.columns:
            df['PRECIPITACAO'] = pd.to_numeric(df['PRECIPITACAO'], errors='coerce')
        if 'VENTO_KMH' in df.columns:
            df['VENTO_KMH'] = pd.to_numeric(df['VENTO_KMH'], errors='coerce')

        # Convert nutrient and irrigation flags to booleans
        for col in ['NITROGENIO_OK', 'FOSFORO_OK', 'POTASSIO_OK', 'IRRIGACAO_REALIZADA']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: True if str(x).strip().upper().startswith('T') else False)

        # Round common numeric columns
        for col in ['TEMPERATURA', 'UMIDADE_SOLO', 'PH_SOLO']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col] = df[col].round(3)
        # ----------------------------------------------------------------------

        # Converter colunas de data/hora
        # Handle possible types: DATA may be datetime already or string; HORA may be numeric
        if 'DATA' in df.columns and 'HORA' in df.columns:
            # prepare date part
            if pd.api.types.is_datetime64_any_dtype(df['DATA']):
                date_part = df['DATA'].dt.strftime('%Y-%m-%d')
            else:
                date_part = df['DATA'].astype(str)

            # prepare hour part
            # some sources use integers, some strings; normalize to two-digit hour
            hora_part = df['HORA'].astype(str).str.zfill(2)

            # build datetime and coerce errors to NaT
            df['DATA_HORA'] = pd.to_datetime(date_part + ' ' + hora_part + ':00:00', errors='coerce')
            df = df.sort_values('DATA_HORA')
        else:
            # fallback: try to parse any datetime-like column
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    df['DATA_HORA'] = df[col]
                    break
            if 'DATA_HORA' not in df.columns:
                # last resort: create index-based datetime
                df['DATA_HORA'] = pd.RangeIndex(start=0, stop=len(df))

        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None
    finally:
        if conn:
            conn.close()

def calcular_sugestoes_irrigacao(df):
    """Calcula sugestões de irrigação baseadas em condições climáticas"""
    if df is None or df.empty:
        return "Dados insuficientes para análise"

    # Última leitura
    ultima = df.iloc[-1]

    sugestoes = []

    # Condições para irrigação
    if ultima['UMIDADE_SOLO'] < 40:
        sugestoes.append("⚠️ Umidade do solo baixa - Irrigação recomendada")

    if ultima['TEMPERATURA'] > 30:
        sugestoes.append("🌡️ Temperatura elevada - Verificar necessidade de irrigação")

    if ultima['PRECIPITACAO'] == 0 and ultima['UMIDADE_AR'] < 60:
        sugestoes.append("🌧️ Sem precipitação recente e ar seco - Irrigação necessária")

    if ultima['PRESSAO_ATMOSFERICA'] < 1000:
        sugestoes.append("📊 Pressão atmosférica baixa - Possível mudança climática")

    if not ultima['NITROGENIO_OK']:
        sugestoes.append("🧪 Nitrogênio baixo - Considerar fertilização")

    if not ultima['FOSFORO_OK']:
        sugestoes.append("🧪 Fósforo baixo - Considerar fertilização")

    if not ultima['POTASSIO_OK']:
        sugestoes.append("🧪 Potássio baixo - Considerar fertilização")

    if ultima['PH_SOLO'] < 6.0 or ultima['PH_SOLO'] > 7.0:
        sugestoes.append("🧪 pH do solo fora do ideal (6.0-7.0) - Correção necessária")

    if not sugestoes:
        sugestoes.append("✅ Condições ideais - Manter monitoramento")

    return "\n".join(sugestoes)

# Carregar dados (principal) — ainda exibiremos a aba de Diagnóstico mesmo se falhar
with st.spinner('Conectando ao banco de dados...'):
    df = carregar_dados()

# Cria abas: Visão Geral (dashboard) e Diagnóstico
tab1, tab2 = st.tabs(["Visão Geral", "Diagnóstico"])

with tab1:
    if df is None:
        st.error("Não foi possível carregar os dados. Verifique a conexão com o banco Oracle.")
        st.info("Abra a aba 'Diagnóstico' para mais detalhes e logs de conexão.")
    else:
        # Sidebar com informações
        st.sidebar.header("📊 Informações do Sistema")
        st.sidebar.metric("Total de Registros", len(df))
        st.sidebar.metric("Última Atualização", df['DATA_HORA'].max().strftime('%d/%m/%Y %H:%M'))

        # Status dos sensores NPK
        st.sidebar.subheader("🧪 Status NPK")
        ultima = df.iloc[-1]
        st.sidebar.write(f"**Nitrogênio:** {'✅ OK' if ultima['NITROGENIO_OK'] else '❌ Baixo'}")
        st.sidebar.write(f"**Fósforo:** {'✅ OK' if ultima['FOSFORO_OK'] else '❌ Baixo'}")
        st.sidebar.write(f"**Potássio:** {'✅ OK' if ultima['POTASSIO_OK'] else '❌ Baixo'}")

        # Status da irrigação
        st.sidebar.subheader("💧 Status Irrigação")
        st.sidebar.write(f"**Irrigação Realizada:** {'✅ Sim' if ultima['IRRIGACAO_REALIZADA'] else '❌ Não'}")

        # Layout principal
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📈 Níveis de Umidade, pH, P, K ao Longo do Tempo")

            # Gráfico de umidade do solo
            fig_umidade = px.line(df, x='DATA_HORA', y='UMIDADE_SOLO',
                                 title='Umidade do Solo (%)',
                                 labels={'UMIDADE_SOLO': 'Umidade (%)', 'DATA_HORA': 'Data/Hora'})
            fig_umidade.update_traces(line_color='#1f77b4')
            st.plotly_chart(fig_umidade, use_container_width=True)

            # Gráfico de pH
            fig_ph = px.line(df, x='DATA_HORA', y='PH_SOLO',
                             title='pH do Solo',
                             labels={'PH_SOLO': 'pH', 'DATA_HORA': 'Data/Hora'})
            fig_ph.add_hline(y=6.0, line_dash="dash", line_color="red", annotation_text="pH Mínimo Ideal")
            fig_ph.add_hline(y=7.0, line_dash="dash", line_color="red", annotation_text="pH Máximo Ideal")
            st.plotly_chart(fig_ph, use_container_width=True)

        with col2:
            st.subheader("🌡️ Condições Climáticas Atuais")

            # Métricas atuais
            st.metric("Temperatura", f"{ultima['TEMPERATURA']:.1f}°C")
            st.metric("Umidade do Ar", f"{ultima['UMIDADE_AR']:.1f}%")
            st.metric("Precipitação", f"{ultima['PRECIPITACAO']:.1f}mm")
            st.metric("Vento", f"{ultima['VENTO_KMH']:.1f}km/h")
            st.metric("Pressão", f"{ultima['PRESSAO_ATMOSFERICA']:.1f}hPa")

            # Status NPK detalhado
            st.subheader("🧪 Níveis de Nutrientes")
            npk_data = pd.DataFrame({
                'Nutriente': ['Nitrogênio (N)', 'Fósforo (P)', 'Potássio (K)'],
                'Status': ['OK' if ultima['NITROGENIO_OK'] else 'Baixo',
                          'OK' if ultima['FOSFORO_OK'] else 'Baixo',
                          'OK' if ultima['POTASSIO_OK'] else 'Baixo']
            })

            # Cores para status
            colors = ['green' if status == 'OK' else 'red' for status in npk_data['Status']]
            fig_npk = go.Figure(data=[go.Table(
                header=dict(values=list(npk_data.columns),
                           fill_color='paleturquoise',
                           align='left'),
                cells=dict(values=[npk_data.Nutriente, npk_data.Status],
                          fill_color=[['white']*len(npk_data), colors],
                          align='left'))
            ])
            st.plotly_chart(fig_npk, use_container_width=True)

        # Sugestões de irrigação
        st.subheader("💡 Sugestões de Irrigação Baseadas no Clima")
        sugestoes = calcular_sugestoes_irrigacao(df)
        st.info(sugestoes)

        # Gráfico de produtividade
        st.subheader("📊 Produtividade ao Longo do Tempo")
        fig_prod = px.line(df, x='DATA_HORA', y='PRODUTIVIDADE',
                          title='Produtividade Estimada (%)',
                          labels={'PRODUTIVIDADE': 'Produtividade (%)', 'DATA_HORA': 'Data/Hora'})
        fig_prod.update_traces(line_color='#2ca02c')
        st.plotly_chart(fig_prod, use_container_width=True)

        # Footer
        st.markdown("---")
        st.markdown("**FarmTech Solutions** - Sistema IoT para Agricultura Inteligente")
        st.markdown("*Dados em tempo real do ESP32 integrado com Python*")

with tab2:
    st.header("🔎 Diagnóstico de Conexão e Dados")
    st.markdown("Use esta aba para verificar conexão, ver contagem e amostra da tabela `SENSORES`.")

    # Mostrar resumo da configuração de conexão (senha oculta)
    user_used = os.environ.get('ORACLE_USER') or ORACLE_USER_RUNTIME or ORACLE_CONFIG.get('user')
    host = ORACLE_CONFIG.get('host')
    port = ORACLE_CONFIG.get('port')
    sid = ORACLE_CONFIG.get('sid')
    user_mask = user_used
    if user_mask and len(user_mask) > 2:
        user_mask = user_mask[0] + '*' * (len(user_mask) - 2) + user_mask[-1]
    st.write(f"Conexão: `{user_mask}@{host}:{port}/{sid}`  — senha não exibida")

    conn = None
    last_error = None
    try:
        conn = conectar_oracle()
        if conn is None:
            st.warning("Não foi possível estabelecer conexão. Verifique credenciais na barra lateral ou variáveis de ambiente.")
            st.info("Dicas: verifique `$env:ORACLE_USER` e `$env:ORACLE_PASSWORD` no PowerShell; a senha é DDMMAA.")
        else:
            st.success("✅ Conexão estabelecida com o Oracle (para diagnóstico).")
            c = conn.cursor()

            # Count
            try:
                sql_count = "SELECT COUNT(*) FROM SENSORES"
                c.execute(sql_count)
                count = c.fetchone()[0]
                st.metric("Registros na tabela SENSORES", count)
            except Exception as e:
                last_error = e
                st.error("Erro ao contar registros na tabela `SENSORES`.")
                with st.expander("Detalhes do erro (contagem)"):
                    import traceback
                    st.text(traceback.format_exc())

            # Sample rows
            try:
                sql_sample = "SELECT * FROM SENSORES WHERE ROWNUM <= 5 ORDER BY DATA, HORA"
                sample = pd.read_sql(sql_sample, conn)
                st.subheader("Amostra (5 primeiros registros)")
                st.dataframe(sample)
                st.subheader("Tipos de colunas")
                st.write(sample.dtypes.astype(str))
                with st.expander("SQL executado (cópia rápida)"):
                    st.code(sql_sample, language='sql')
            except Exception as e:
                last_error = e
                st.error("Erro ao ler amostra da tabela `SENSORES`.")
                with st.expander("Detalhes do erro (amostra)"):
                    import traceback
                    st.text(traceback.format_exc())

            c.close()
    except Exception as e:
        last_error = e
        st.error("Erro geral de diagnóstico ao tentar conectar/ler o banco.")
        with st.expander("Detalhes do erro geral"):
            import traceback
            st.text(traceback.format_exc())
    finally:
        if conn:
            conn.close()

    if last_error:
        st.warning("Sugestões rápidas para resolver:")
        st.write("- Verifique se a tabela `SENSORES` existe no seu schema (execute SELECT table_name FROM user_tables;).")
        st.write("- Confirme o usuário e senha (senha = sua data de nascimento em DDMMAA).")
        st.write("- Se aparecer DPI-1047, instale Oracle Instant Client ou use oracledb em modo thin client.")
        with st.expander("Comandos úteis (PowerShell)"):
            st.code('$env:ORACLE_USER="RM566826"\n$env:ORACLE_PASSWORD="161083"\nstreamlit run dashboard.py', language='powershell')