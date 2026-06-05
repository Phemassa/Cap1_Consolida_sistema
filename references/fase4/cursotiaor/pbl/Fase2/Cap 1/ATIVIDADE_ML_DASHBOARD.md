# Atividade: Assistente Agrícola Inteligente com ML e Dashboard

## 📋 Objetivo Geral

Construir um protótipo de **Assistente Agrícola Inteligente** que:

1. **Modelar banco de dados** para armazenar dados dos sensores (reais ou simulados Wokwi)
2. **Implementar modelos de Machine Learning** (regressão supervisionada - Scikit-Learn)
3. **Prever variáveis críticas**: umidade do solo, pH e rendimento esperado
4. **Sugerir ações de irrigação** e manejo agrícola (C++ ou Python)
5. **Dashboard interativo** com Streamlit para gestores agrícolas
6. **Demonstrar domínio técnico** em IA, ciência de dados e automação no agronegócio

---

## 🎯 PARTE 1 - Dashboard ML com Streamlit

### Objetivo
Desenvolver pipeline completo de Machine Learning usando **Scikit-Learn**, conectado a interface interativa em **Streamlit**.

### Requisitos
- ✅ Pipeline ML completo com Scikit-Learn
- ✅ Modelo de regressão treinado
- ✅ Dashboard interativo para gestores
- ✅ Métricas de desempenho em tempo real
- ✅ Gráficos de correlação
- ✅ Previsões em tempo real

### Entregáveis
**📹 Vídeo (máximo 5 minutos)** apresentando:

1. **Integração do modelo** com dashboard Streamlit
2. **Bibliotecas utilizadas** e explicação do pipeline ML
3. **Demonstração do dashboard** funcionando:
   - Métricas exibidas
   - Previsões geradas
   - Gráficos e visualizações

### Tecnologias
- **Python 3.x**
- **Scikit-Learn** - Modelos ML
- **Streamlit** - Dashboard interativo
- **Pandas** - Manipulação de dados
- **Matplotlib/Plotly** - Visualizações
- **NumPy** - Operações numéricas

### Estrutura do Projeto
```
Cap 1/
├── data/
│   ├── sensor_data.csv          # Dados dos sensores ESP32
│   └── preprocessed_data.csv    # Dados tratados
├── models/
│   ├── train_model.py           # Treinamento ML
│   ├── irrigation_model.pkl     # Modelo salvo
│   └── model_evaluation.py      # Métricas
├── dashboard/
│   ├── app.py                   # App Streamlit principal
│   ├── pages/
│   │   ├── predictions.py       # Página previsões
│   │   ├── metrics.py           # Página métricas
│   │   └── visualizations.py    # Gráficos
│   └── requirements.txt         # Dependências
└── utils/
    ├── data_collection.py       # Coleta dados ESP32
    └── preprocessing.py         # Limpeza de dados
```

### Checklist - Parte 1
- [ ] Coletar dados dos sensores Wokwi/ESP32
- [ ] Criar base de dados (CSV/SQLite)
- [ ] Implementar pré-processamento de dados
- [ ] Treinar modelo de regressão (Scikit-Learn)
- [ ] Desenvolver dashboard Streamlit
- [ ] Adicionar métricas de performance
- [ ] Criar gráficos de correlação
- [ ] Implementar previsões em tempo real
- [ ] Testar integração completa
- [ ] Gravar vídeo demonstrativo (5 min)

---

## 🎯 PARTE 2 - Algoritmos Preditivos para Ações Futuras

### Objetivo
Criar e treinar modelos de regressão para **sugerir ações de irrigação** e manejo agrícola baseadas em previsões.

### Requisitos
- ✅ Modelos de regressão (linear, múltipla ou não linear)
- ✅ Previsões sobre:
  - Volume de irrigação necessário
  - Necessidade de fertilização (NPK)
  - Estimativa de rendimento
- ✅ Avaliação com métricas: **MAE, MSE, RMSE, R²**
- ✅ Recomendações baseadas nos resultados
- ✅ Documentação completa do processo
- ✅ Visualizações justificando decisões

### Entregáveis
**📹 Vídeo (máximo 5 minutos)** apresentando:

1. **Pipeline ML completo**:
   - Tratamento de dados
   - Treinamento do modelo
   - Validação e testes
2. **Demonstração do Streamlit**:
   - Funcionalidades principais
   - Interface do usuário
3. **Métricas e previsões**:
   - MAE, MSE, RMSE, R²
   - Interpretação dos resultados
   - Recomendações geradas

### Modelos Implementados

#### 1. Modelo de Irrigação
```python
# Entrada: umidade_solo, temperatura, pH, NPK
# Saída: volume_irrigacao_recomendado (litros/m²)
```

#### 2. Modelo de Fertilização
```python
# Entrada: pH, N, P, K, histórico_crescimento
# Saída: dosagem_NPK_recomendada (g/m²)
```

#### 3. Modelo de Rendimento
```python
# Entrada: umidade, temperatura, NPK, dias_cultivo
# Saída: rendimento_estimado (kg/hectare)
```

### Métricas de Avaliação
- **MAE** (Mean Absolute Error) - Erro médio absoluto
- **MSE** (Mean Squared Error) - Erro quadrático médio
- **RMSE** (Root Mean Squared Error) - Raiz do erro quadrático médio
- **R²** (Coeficiente de Determinação) - Qualidade do ajuste

### Checklist - Parte 2
- [ ] Definir variáveis target (irrigação, fertilização, rendimento)
- [ ] Coletar/gerar dados históricos
- [ ] Implementar feature engineering
- [ ] Treinar modelo de regressão linear
- [ ] Treinar modelo de regressão múltipla
- [ ] Testar modelo de regressão não linear (opcional)
- [ ] Calcular métricas (MAE, MSE, RMSE, R²)
- [ ] Criar visualizações (scatter plots, residuals)
- [ ] Implementar sistema de recomendações
- [ ] Integrar com dashboard Streamlit
- [ ] Documentar processo completo
- [ ] Gravar vídeo demonstrativo (5 min)

---

## 🚀 IR ALÉM 1 - Integração IoT com Banco de Dados SQL

### Objetivo
Modelar banco de dados SQL para armazenar dados dos sensores IoT com **ingestão e atualização automática**.

### Requisitos
- ✅ Banco de dados SQL (SQLite, PostgreSQL ou MySQL)
- ✅ Schema baseado nos princípios de Cognitive Data Science
- ✅ Ingestão automática de dados dos sensores
- ✅ Processo de atualização em tempo real
- ✅ Índices e otimizações para consultas analíticas

### Entregáveis
**📹 Vídeo (máximo 3 minutos)** demonstrando:

1. **Funcionamento da ingestão/população** de dados IoT no banco SQL
2. **Processo de atualização automática** dos dados
3. **Consultas SQL** demonstrando dados armazenados

### Tecnologias
- **SQLite** - Banco local (desenvolvimento)
- **PostgreSQL** - Banco robusto (produção)
- **SQLAlchemy** - ORM Python
- **Pandas** - ETL e transformações
- **Schedule/APScheduler** - Automação

### Schema do Banco de Dados

#### Tabela: sensor_readings (Leituras dos Sensores)
```sql
CREATE TABLE sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    temperatura FLOAT NOT NULL,
    umidade_solo FLOAT NOT NULL,
    ph_solo FLOAT NOT NULL,
    nitrogenio BOOLEAN NOT NULL,
    fosforo BOOLEAN NOT NULL,
    potassio BOOLEAN NOT NULL,
    irrigacao_ativa BOOLEAN NOT NULL,
    cultura VARCHAR(50) NOT NULL,
    INDEX idx_timestamp (timestamp),
    INDEX idx_cultura (cultura)
);
```

#### Tabela: predictions (Previsões do Modelo)
```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reading_id INTEGER NOT NULL,
    volume_irrigacao FLOAT,
    dosagem_n FLOAT,
    dosagem_p FLOAT,
    dosagem_k FLOAT,
    rendimento_estimado FLOAT,
    confianca FLOAT,
    modelo_versao VARCHAR(20),
    FOREIGN KEY (reading_id) REFERENCES sensor_readings(id),
    INDEX idx_timestamp (timestamp)
);
```

#### Tabela: irrigation_actions (Ações de Irrigação)
```sql
CREATE TABLE irrigation_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reading_id INTEGER NOT NULL,
    acao VARCHAR(20) NOT NULL, -- 'LIGAR' ou 'DESLIGAR'
    motivo TEXT,
    volume_aplicado FLOAT,
    duracao_minutos INTEGER,
    FOREIGN KEY (reading_id) REFERENCES sensor_readings(id),
    INDEX idx_timestamp (timestamp)
);
```

#### Tabela: culturas (Informações das Culturas)
```sql
CREATE TABLE culturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL UNIQUE,
    n_ideal FLOAT NOT NULL,
    p_ideal FLOAT NOT NULL,
    k_ideal FLOAT NOT NULL,
    ph_minimo FLOAT NOT NULL,
    ph_maximo FLOAT NOT NULL,
    umidade_minima FLOAT NOT NULL,
    umidade_ideal FLOAT NOT NULL,
    rendimento_esperado FLOAT,
    INDEX idx_nome (nome)
);
```

### Pipeline de Ingestão Automática

#### Código Python (database_ingestion.py)
```python
import sqlite3
from datetime import datetime
import schedule
import time

class DatabaseIngestor:
    def __init__(self, db_path='farmtech.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        """Cria tabelas se não existirem"""
        cursor = self.conn.cursor()
        
        # Criar tabelas (SQL acima)
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS sensor_readings (...);
            CREATE TABLE IF NOT EXISTS predictions (...);
            CREATE TABLE IF NOT EXISTS irrigation_actions (...);
            CREATE TABLE IF NOT EXISTS culturas (...);
        ''')
        
        self.conn.commit()
    
    def ingest_sensor_data(self, data):
        """Insere dados dos sensores"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO sensor_readings 
            (temperatura, umidade_solo, ph_solo, nitrogenio, 
             fosforo, potassio, irrigacao_ativa, cultura)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['temperatura'], data['umidade_solo'], 
              data['ph_solo'], data['nitrogenio'],
              data['fosforo'], data['potassio'],
              data['irrigacao_ativa'], data['cultura']))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def ingest_prediction(self, reading_id, prediction_data):
        """Insere previsão do modelo"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO predictions 
            (reading_id, volume_irrigacao, dosagem_n, dosagem_p, 
             dosagem_k, rendimento_estimado, confianca, modelo_versao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (reading_id, prediction_data['volume_irrigacao'],
              prediction_data['dosagem_n'], prediction_data['dosagem_p'],
              prediction_data['dosagem_k'], prediction_data['rendimento'],
              prediction_data['confianca'], 'v1.0'))
        
        self.conn.commit()
    
    def auto_update_job(self):
        """Job executado periodicamente para atualizar dados"""
        # Lê dados do ESP32/Wokwi (via serial ou simulação)
        sensor_data = self.read_sensor_data()
        
        # Insere no banco
        reading_id = self.ingest_sensor_data(sensor_data)
        
        # Faz previsão com modelo ML
        prediction = self.predict_with_model(sensor_data)
        
        # Salva previsão
        self.ingest_prediction(reading_id, prediction)
        
        print(f"✅ Dados atualizados: ID {reading_id}")
    
    def start_auto_update(self, interval_seconds=5):
        """Inicia atualização automática"""
        schedule.every(interval_seconds).seconds.do(self.auto_update_job)
        
        print(f"🔄 Atualização automática a cada {interval_seconds}s")
        while True:
            schedule.run_pending()
            time.sleep(1)
```

### Checklist - IR ALÉM 1
- [ ] Criar schema SQL otimizado
- [ ] Implementar DatabaseIngestor class
- [ ] Conectar com dados ESP32/Wokwi
- [ ] Configurar atualização automática (5s)
- [ ] Criar índices para performance
- [ ] Implementar logging de operações
- [ ] Adicionar tratamento de erros
- [ ] Testar com 1000+ registros
- [ ] Otimizar queries analíticas
- [ ] Gravar vídeo demonstrativo (3 min)

---

## 🎨 IR ALÉM 2 - Dashboard Analítico Interativo Online

### Objetivo
Criar dashboard visual **interativo e online** com gráficos avançados, correlações e tendências de produtividade.

### Requisitos
- ✅ Dashboard online (Streamlit Cloud ou similar)
- ✅ Gráficos de correlação entre variáveis
- ✅ Resultados de previsão em tempo real
- ✅ Tendências de produtividade (série temporal)
- ✅ Filtros interativos por cultura/período
- ✅ Mapas de calor (heatmaps)
- ✅ Indicadores KPI destacados

### Entregáveis
**Dashboard online acessível** com:

1. **Página Principal**: KPIs e resumo executivo
2. **Página Correlações**: Matriz de correlação e scatter plots
3. **Página Previsões**: Resultados do modelo ML
4. **Página Tendências**: Gráficos de série temporal
5. **Página Análise**: Insights e recomendações

### Tecnologias
- **Streamlit** - Framework web Python
- **Plotly** - Gráficos interativos
- **Seaborn** - Visualizações estatísticas
- **Pandas** - Análise de dados
- **Streamlit Cloud** - Deploy gratuito

### Estrutura do Dashboard

#### 1. Página Principal (Home)
```python
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="FarmTech Dashboard", layout="wide")

# KPIs principais
col1, col2, col3, col4 = st.columns(4)
col1.metric("Umidade Média", "62.5%", "+2.3%")
col2.metric("pH Médio", "6.8", "-0.1")
col3.metric("Irrigações Hoje", "12", "+3")
col4.metric("Rendimento Est.", "23.5t/ha", "+5.2%")

# Gráfico de status atual
st.plotly_chart(fig_status_atual, use_container_width=True)
```

#### 2. Página de Correlações
```python
# Matriz de correlação
import seaborn as sns

st.header("📊 Análise de Correlações")

# Heatmap
fig_corr = px.imshow(
    df.corr(),
    text_auto=True,
    aspect="auto",
    title="Matriz de Correlação"
)
st.plotly_chart(fig_corr)

# Scatter plots interativos
st.subheader("Relações entre Variáveis")
x_var = st.selectbox("Eixo X", df.columns)
y_var = st.selectbox("Eixo Y", df.columns)

fig_scatter = px.scatter(
    df, x=x_var, y=y_var, 
    color='cultura',
    trendline="ols"
)
st.plotly_chart(fig_scatter)
```

#### 3. Página de Previsões
```python
st.header("🔮 Previsões do Modelo ML")

# Input interativo
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    temperatura = col1.slider("Temperatura (°C)", 15, 40, 25)
    umidade = col2.slider("Umidade Solo (%)", 20, 90, 60)
    ph = col1.slider("pH", 5.0, 8.0, 6.5)
    
    submitted = st.form_submit_button("Fazer Previsão")
    
    if submitted:
        # Previsão
        prediction = model.predict([[temperatura, umidade, ph, ...]])
        
        # Exibir resultado
        st.success(f"Volume de irrigação recomendado: {prediction[0]:.1f} L/m²")
        
        # Métricas do modelo
        col1, col2, col3 = st.columns(3)
        col1.metric("MAE", f"{mae:.2f}")
        col2.metric("RMSE", f"{rmse:.2f}")
        col3.metric("R²", f"{r2:.3f}")
```

#### 4. Página de Tendências
```python
st.header("📈 Tendências de Produtividade")

# Série temporal
fig_trend = px.line(
    df, 
    x='timestamp', 
    y='rendimento_estimado',
    color='cultura',
    title="Evolução do Rendimento Estimado"
)
st.plotly_chart(fig_trend, use_container_width=True)

# Decomposição sazonal
from statsmodels.tsa.seasonal import seasonal_decompose

decomposition = seasonal_decompose(df['rendimento_estimado'], period=24)

fig_seasonal = make_subplots(rows=4, cols=1)
# Adicionar trend, seasonal, resid...
st.plotly_chart(fig_seasonal)
```

#### 5. Página de Análise
```python
st.header("💡 Insights e Recomendações")

# Análise automática
if df['umidade_solo'].mean() < 50:
    st.warning("⚠️ Umidade média baixa. Aumentar frequência de irrigação.")

if df['ph_solo'].mean() < 6.0:
    st.info("ℹ️ Solo ácido. Recomenda-se aplicação de calcário.")

# Top insights
st.subheader("🎯 Principais Insights")
insights = [
    "Correlação forte entre umidade e rendimento (r=0.82)",
    "pH ideal para banana: 6.5-7.0",
    "Irrigação noturna reduz evaporação em 30%"
]

for insight in insights:
    st.markdown(f"- {insight}")

# Download de relatório
st.download_button(
    "📄 Baixar Relatório Completo",
    data=generate_pdf_report(),
    file_name="relatorio_farmtech.pdf"
)
```

### Deploy no Streamlit Cloud

1. **Criar requirements.txt**:
```txt
streamlit==1.28.0
plotly==5.17.0
pandas==2.0.0
scikit-learn==1.3.0
seaborn==0.12.0
```

2. **Push para GitHub**:
```bash
git add .
git commit -m "feat: Dashboard analítico completo"
git push origin main
```

3. **Deploy**:
- Acesse https://share.streamlit.io
- Conecte repositório GitHub
- Selecione arquivo `dashboard/app.py`
- Deploy automático!

### Checklist - IR ALÉM 2
- [ ] Criar estrutura multi-página
- [ ] Implementar KPIs principais
- [ ] Adicionar matriz de correlação
- [ ] Criar gráficos interativos
- [ ] Implementar previsão em tempo real
- [ ] Adicionar série temporal
- [ ] Criar sistema de insights
- [ ] Otimizar performance (cache)
- [ ] Adicionar filtros avançados
- [ ] Deploy no Streamlit Cloud
- [ ] Testar em diferentes dispositivos
- [ ] Documentar uso do dashboard

---

## 📊 Estrutura de Dados

### Tabela: sensor_readings
```sql
CREATE TABLE sensor_readings (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME,
    temperatura FLOAT,
    umidade_solo FLOAT,
    ph_solo FLOAT,
    nitrogenio BOOLEAN,
    fosforo BOOLEAN,
    potassio BOOLEAN,
    irrigacao_ativa BOOLEAN
);
```

### Tabela: predictions
```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME,
    volume_irrigacao FLOAT,
    dosagem_n FLOAT,
    dosagem_p FLOAT,
    dosagem_k FLOAT,
    rendimento_estimado FLOAT,
    confianca FLOAT
);
```

---

## 🚀 Passos de Implementação

### 1. Coleta de Dados
```python
# Conectar ao ESP32 via Serial ou usar dados Wokwi
# Salvar em CSV ou banco de dados
```

### 2. Pré-processamento
```python
# Limpeza, normalização, feature engineering
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
```

### 3. Treinamento
```python
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
```

### 4. Dashboard Streamlit
```python
import streamlit as st
import plotly.express as px

st.title("🌾 FarmTech Solutions - Assistente Agrícola")
st.metric("Umidade Solo", f"{umidade}%")
st.plotly_chart(fig_correlacao)
```

### 5. Deploy
```bash
streamlit run dashboard/app.py
# Hospedar em Streamlit Cloud (gratuito)
```

---

## 📦 Dependências

### requirements.txt
```txt
streamlit>=1.28.0
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
matplotlib>=3.7.0
seaborn>=0.12.0
joblib>=1.3.0
pyserial>=3.5  # Para comunicação ESP32
```

### Instalação
```bash
pip install -r requirements.txt
```

---

## 🎬 Roteiro dos Vídeos

### Vídeo Parte 1 (5 min)
1. **Introdução** (30s) - Apresentação do projeto
2. **Pipeline ML** (1m30s) - Código e bibliotecas
3. **Dashboard** (2m) - Demonstração funcionalidades
4. **Métricas** (1m) - Explicação dos resultados
5. **Conclusão** (30s) - Próximos passos

### Vídeo Parte 2 (5 min)
1. **Introdução** (30s) - Continuação do projeto
2. **Modelos** (1m30s) - Regressão e treinamento
3. **Avaliação** (1m) - MAE, MSE, RMSE, R²
4. **Recomendações** (1m30s) - Sistema de sugestões
5. **Demo Final** (30s) - Integração completa

---

## 📚 Referências

- [Scikit-Learn Documentation](https://scikit-learn.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [EMBRAPA - Dados Agrícolas](https://www.embrapa.br/)
- [Kaggle - Agricultural Datasets](https://www.kaggle.com/datasets)

---

## ✅ Critérios de Avaliação

### Parte 1 - Dashboard ML com Streamlit (50 pontos)
- [ ] Pipeline ML funcional (15 pts)
- [ ] Dashboard Streamlit completo (15 pts)
- [ ] Visualizações e métricas (10 pts)
- [ ] Vídeo demonstrativo (10 pts)

### Parte 2 - Algoritmos Preditivos (50 pontos)
- [ ] Modelos de regressão implementados (15 pts)
- [ ] Métricas calculadas e interpretadas (10 pts)
- [ ] Sistema de recomendações (15 pts)
- [ ] Vídeo demonstrativo (10 pts)

### IR ALÉM 1 - Banco de Dados SQL (Bônus +20 pontos)
- [ ] Schema SQL otimizado (5 pts)
- [ ] Ingestão automática funcionando (8 pts)
- [ ] Consultas e índices eficientes (4 pts)
- [ ] Vídeo demonstrativo (3 pts)

### IR ALÉM 2 - Dashboard Avançado (Bônus +20 pontos)
- [ ] Dashboard online acessível (5 pts)
- [ ] Gráficos de correlação interativos (5 pts)
- [ ] Tendências e séries temporais (5 pts)
- [ ] Sistema de insights automáticos (5 pts)

**Total Base: 100 pontos**  
**Total com IR ALÉM: 140 pontos**

---

## 🗓️ Cronograma Sugerido

| Semana | Atividade | Entregáveis |
|--------|-----------|-------------|
| 1 | Coleta e preparação de dados | CSV com 1000+ registros |
| 2 | Implementação pipeline ML | Modelo treinado + métricas |
| 3 | Desenvolvimento dashboard Streamlit | Dashboard local funcionando |
| 4 | Treinamento modelos preditivos | MAE, MSE, RMSE, R² calculados |
| 5 | Sistema de recomendações | Algoritmo de sugestões |
| 6 | **IR ALÉM 1**: Banco de dados SQL | Ingestão automática |
| 7 | **IR ALÉM 2**: Dashboard online | Deploy Streamlit Cloud |
| 8 | Testes, documentação e vídeos | Vídeos finais (5+5+3 min) |

---

## 📹 Roteiro dos Vídeos Atualizado

### Vídeo Parte 1 (5 min)
1. **Introdução** (30s) - Apresentação do projeto
2. **Pipeline ML** (1m30s) - Código e bibliotecas
3. **Dashboard** (2m) - Demonstração funcionalidades
4. **Métricas** (1m) - Explicação dos resultados
5. **Conclusão** (30s) - Próximos passos

### Vídeo Parte 2 (5 min)
1. **Introdução** (30s) - Continuação do projeto
2. **Modelos** (1m30s) - Regressão e treinamento
3. **Avaliação** (1m) - MAE, MSE, RMSE, R²
4. **Recomendações** (1m30s) - Sistema de sugestões
5. **Demo Final** (30s) - Integração completa

### Vídeo IR ALÉM 1 (3 min) - OPCIONAL
1. **Schema SQL** (45s) - Estrutura das tabelas
2. **Ingestão Automática** (1m15s) - Demonstração funcionando
3. **Consultas** (1m) - Exemplos de queries

### Vídeo IR ALÉM 2 (Demo Online) - OPCIONAL
- **Link do dashboard** online no README
- **Screenshots** das funcionalidades principais
- **Vídeo curto** navegando pelo dashboard (opcional)

---

## 💡 Dicas Atualizadas

### Dicas Gerais
1. **Comece simples**: Modelo linear básico primeiro
2. **Dados sintéticos**: Use Wokwi para gerar dados consistentes
3. **Versionamento**: Use Git para cada etapa
4. **Documentação**: Comente o código enquanto desenvolve
5. **Teste incremental**: Valide cada componente separadamente
6. **Dashboard responsivo**: Teste em diferentes resoluções
7. **Métricas visuais**: Gráficos facilitam interpretação

### Dicas IR ALÉM 1 (Banco de Dados)
8. **SQLite primeiro**: Mais simples para desenvolvimento
9. **PostgreSQL depois**: Se precisar de mais robustez
10. **Índices críticos**: `timestamp` e `cultura` sempre indexados
11. **Backup regular**: Automatize backup do banco
12. **Logging**: Registre todas as operações de ingestão

### Dicas IR ALÉM 2 (Dashboard Avançado)
13. **Cache do Streamlit**: Use `@st.cache_data` para otimizar
14. **Lazy loading**: Carregue dados sob demanda
15. **Plotly sobre Matplotlib**: Mais interativo
16. **Mobile first**: Teste em tela pequena primeiro
17. **Deploy cedo**: Suba no Streamlit Cloud logo no início

---

## 🎓 Recursos Adicionais

### Tutoriais Recomendados
- [Streamlit Tutorial Completo](https://docs.streamlit.io/get-started)
- [SQLAlchemy ORM Basics](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
- [Plotly Dashboard Tutorial](https://plotly.com/python/dashboard/)
- [Scikit-Learn Regression](https://scikit-learn.org/stable/supervised_learning.html#supervised-learning)

### Datasets de Exemplo
- [Kaggle: Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)
- [UCI: Soil Dataset](https://archive.ics.uci.edu/ml/datasets/Soil)
- [EMBRAPA Open Data](https://www.embrapa.br/en/dados-abertos)

### Ferramentas Úteis
- **DB Browser for SQLite** - Visualizar banco SQLite
- **pgAdmin** - Gerenciar PostgreSQL
- **Postman** - Testar APIs REST (se criar)
- **Jupyter Notebook** - Prototipação rápida

---

**Status**: 📝 Planejamento  
**Última atualização**: Outubro 2025  
**Grupo**: FarmTech Solutions - FIAP