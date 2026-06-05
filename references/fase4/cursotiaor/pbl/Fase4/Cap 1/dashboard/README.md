# FarmTech Solutions - Dashboard Avançado
## 🎓 FIAP - Fase 2 - Cap 1 - IR ALÉM 2

### 📋 Visão Geral

Dashboard interativo desenvolvido com **Streamlit** para monitoramento em tempo real do sistema de irrigação inteligente FarmTech. Integrado com banco de dados SQLite e sistema de auto-ingestão de dados.

---

## 🚀 Instalação e Configuração

### 1. Pré-requisitos
- Python 3.8 ou superior
- Sistema de auto-ingestão rodando (`database_manager.py`)
- Dados históricos gerados (`generate_sensor_data.py`)

### 2. Instalar Dependências
```bash
pip install -r dashboard/requirements.txt
```

### 3. Executar Dashboard
```bash
streamlit run dashboard/app.py
```

O dashboard estará disponível em: `http://localhost:8501`

---

## 📊 Estrutura do Dashboard

### **Página Principal** (`app.py`)
- **KPIs em Tempo Real**: Temperatura, Umidade, pH, Status Irrigação, NPK
- **Gráficos Interativos**: Evolução temporal de parâmetros
- **Sistema de Alertas**: Recomendações contextuais
- **Auto-refresh**: Atualização a cada 5 segundos

### **1. Correlações** (`pages/1_📊_Correlacoes.py`)
- Matriz de correlação entre variáveis
- Scatter plots interativos
- Pairplot multivariável
- Análises específicas:
  - Temperatura vs Umidade
  - pH vs NPK
  - Irrigação vs Condições Ambientais

### **2. Previsões** (`pages/2_🔮_Previsoes.py`)
- Interface de entrada de parâmetros
- Previsão de volume de irrigação
- Estimativa de rendimento por cultura
- Recomendações de dosagem NPK
- Histórico de previsões
- Métricas do modelo ML

### **3. Tendências** (`pages/3_📈_Tendencias.py`)
- Séries temporais de múltiplos parâmetros
- Médias móveis e detecção de tendências
- Análise de padrões de irrigação
- Estatísticas diárias/semanais/mensais
- Comparação entre culturas

### **4. Análise Inteligente** (`pages/4_💡_Analise.py`)
- **Insights Automáticos**: Detecção de anomalias
- **Performance do Sistema**: Eficiência, qualidade NPK, estabilidade pH
- **Comparação entre Culturas**: Volume de água, qualidade nutricional
- **Plano de Ação**: Prioridades imediatas, curto e médio prazo
- **Análise Econômica**: Custos de água e fertilizantes
- **Health Score**: Índice de saúde geral (0-100)
- **Relatórios Exportáveis**: CSV, estatísticas

---

## 🔧 Configuração Técnica

### Conexão com Banco de Dados
```python
from database.database_manager import FarmTechDatabase

db = FarmTechDatabase('database/farmtech.db')
```

### Cache de Dados
O dashboard utiliza cache do Streamlit para otimizar performance:
```python
@st.cache_data(ttl=10)  # Cache de 10 segundos
def load_sensor_data():
    return pd.read_sql_query(query, db.conn)
```

### Auto-Refresh
Script JavaScript para recarregar página automaticamente:
```python
st.markdown("""
<script>
setTimeout(function(){ window.location.reload(); }, 5000);
</script>
""", unsafe_allow_html=True)
```

---

## 📈 Visualizações Disponíveis

### Gráficos Plotly
1. **Line Charts**: Evolução temporal de temperatura, umidade, pH
2. **Gauges**: Indicadores visuais de NPK
3. **Bar Charts**: Volume de irrigação, comparação entre culturas
4. **Scatter Plots**: Correlações entre variáveis
5. **Heatmaps**: Matriz de correlação
6. **Box Plots**: Distribuição de pH por status NPK
7. **Histogramas**: Distribuição de duração de irrigação
8. **Pie Charts**: Volume por cultura
9. **Subplots**: Múltiplas séries temporais combinadas
10. **Indicator Gauges**: Health score do sistema

### Elementos Interativos
- Sliders para entrada de parâmetros
- Selectboxes para filtros (período, cultura)
- Checkboxes para ativação de nutrientes
- Forms para submissão de previsões
- Download buttons para relatórios

---

## 🎯 Casos de Uso

### 1. Monitoramento em Tempo Real
```python
# Acesse a página principal para visualizar:
- Temperatura atual
- Umidade do solo
- Status de irrigação
- Alertas automáticos
```

### 2. Análise de Correlações
```python
# Navegue para "Correlações" e explore:
- Como temperatura afeta umidade
- Relação entre pH e NPK
- Impacto das variáveis na irrigação
```

### 3. Fazer Previsões
```python
# Acesse "Previsões" e:
1. Ajuste os sliders de temperatura, umidade, pH
2. Marque os checkboxes de NPK
3. Selecione a cultura
4. Clique em "Fazer Previsão"
5. Analise volume recomendado e dosagens NPK
```

### 4. Identificar Tendências
```python
# Em "Tendências":
- Selecione período de análise
- Filtre por cultura
- Observe médias móveis
- Identifique padrões sazonais
```

### 5. Obter Insights
```python
# Página "Análise":
- Visualize alertas automáticos
- Confira health score
- Baixe relatórios CSV
- Siga plano de ação recomendado
```

---

## 🔒 Segurança e Performance

### Boas Práticas Implementadas
- ✅ Cache de dados para reduzir consultas ao banco
- ✅ Validação de inputs do usuário
- ✅ Tratamento de exceções com mensagens claras
- ✅ TTL configurável para cache dinâmico
- ✅ Lazy loading de conexões com banco
- ✅ Uso de `@st.cache_resource` para objetos persistentes

### Limites de Performance
- **TTL Cache**: 10-60 segundos dependendo da página
- **Auto-refresh**: 5 segundos (página principal)
- **Máximo de Leituras**: Últimas 1000 por query
- **Tamanho de CSV**: Limitado a 100 registros por download

---

## 🌐 Deploy em Produção

### Streamlit Cloud (Recomendado)
1. Crie conta em https://streamlit.io/cloud
2. Conecte seu repositório GitHub
3. Configure:
   - **Main file**: `dashboard/app.py`
   - **Python version**: 3.9
   - **Requirements**: `dashboard/requirements.txt`
4. Deploy automático a cada commit

### Variáveis de Ambiente
```bash
# .streamlit/config.toml
[server]
port = 8501
headless = true

[browser]
gatherUsageStats = false
```

### URL de Produção
Após deploy, o dashboard estará disponível em:
```
https://[seu-usuario]-farmtech-dashboard.streamlit.app
```

---

## 🐛 Troubleshooting

### Erro: "Nenhum dado disponível"
**Solução**: Execute o sistema de auto-ingestão
```bash
python database/database_manager.py
```

### Erro: "Import streamlit could not be resolved"
**Solução**: Instale as dependências
```bash
pip install -r dashboard/requirements.txt
```

### Dashboard não atualiza automaticamente
**Solução**: Limpe o cache
```python
# No dashboard, pressione 'C' ou clique em "Clear Cache"
```

### Performance lenta
**Solução**: Ajuste o TTL do cache
```python
@st.cache_data(ttl=60)  # Aumentar para 60 segundos
```

### Gráficos não aparecem
**Solução**: Verifique instalação do Plotly
```bash
pip install plotly==5.18.0
```

---

## 📦 Dependências

### Core
- `streamlit==1.29.0` - Framework do dashboard
- `pandas==2.1.4` - Manipulação de dados
- `plotly==5.18.0` - Visualizações interativas

### Machine Learning
- `scikit-learn==1.3.2` - Modelos preditivos
- `joblib==1.3.2` - Persistência de modelos

### Database
- `sqlite3` (built-in) - Banco de dados

### Utilities
- `numpy==1.26.2` - Computação numérica
- `seaborn==0.13.0` - Visualizações estatísticas

---

## 🎓 Pontuação FIAP

### IR ALÉM 2: Dashboard Avançado (+20 pontos)
✅ Dashboard online interativo com Streamlit  
✅ Múltiplas páginas (Principal + 4 páginas temáticas)  
✅ Correlações entre variáveis com heatmaps  
✅ Previsões com modelo ML integrado  
✅ Tendências e séries temporais  
✅ Insights automáticos e alertas inteligentes  
✅ Auto-refresh em tempo real  
✅ Exportação de relatórios  
✅ Health score do sistema  
✅ Análise econômica de custos  

**Total**: 20 pontos de 20 possíveis ✅

---

## 📹 Demonstração em Vídeo

### Roteiro Sugerido (3 minutos)
1. **Introdução** (15s)
   - Apresentar o dashboard e objetivo

2. **Página Principal** (45s)
   - Mostrar KPIs em tempo real
   - Demonstrar auto-refresh
   - Exibir alertas

3. **Correlações** (30s)
   - Navegar para página de correlações
   - Mostrar heatmap
   - Explorar scatter plot interativo

4. **Previsões** (45s)
   - Ajustar parâmetros no formulário
   - Fazer previsão
   - Explicar resultados e recomendações

5. **Análise Inteligente** (30s)
   - Mostrar insights automáticos
   - Exibir health score
   - Demonstrar exportação de relatório

6. **Conclusão** (15s)
   - Resumir funcionalidades
   - Destacar diferenciais

---

## 🤝 Contribuição

Este é um projeto acadêmico da FIAP. Para melhorias:
1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/melhoria`)
3. Commit suas mudanças (`git commit -m 'Add melhoria'`)
4. Push para a branch (`git push origin feature/melhoria`)
5. Abra um Pull Request

---

## 📄 Licença

Projeto acadêmico - FIAP 2025  
Uso educacional apenas

---

## 👥 Autores

**FarmTech Solutions - Grupo 19**  
FIAP - Pós-Tech: Agronegócio e IA  
Fase 2 - Cap 1 - Outubro 2025

---

## 📞 Suporte

Para dúvidas sobre o dashboard:
- Consulte a documentação principal em `/docs`
- Verifique os logs em `farmtech.log`
- Execute testes com dados simulados

**Última atualização**: Janeiro 2025