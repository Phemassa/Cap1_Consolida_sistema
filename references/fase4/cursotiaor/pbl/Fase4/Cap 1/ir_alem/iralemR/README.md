# 📊 FarmTech Solutions - IR ALÉM 2: Análise Estatística com R

## 🌱 Visão Geral

Este é o **IR ALÉM 2** do projeto FarmTech Solutions - um sistema avançado de análise estatística em R para otimização de irrigação agrícola usando **Data Science** e **Machine Learning**.

### 🎯 Objetivos

- **Análise Exploratória**: Investigar padrões nos dados de sensores agrícolas
- **Modelagem Preditiva**: Desenvolver modelos de ML para decisão de irrigação
- **Visualizações Interativas**: Criar dashboards para monitoramento agrícola  
- **Relatórios Automatizados**: Gerar insights estatísticos para tomada de decisão

## 🏗️ Arquitetura do Sistema

```
iralemR/
├── analise_estatistica.R          # 📊 Análise exploratória e geração de dados
├── modelos_preditivos_corrigido.R # 🤖 ML models (GLM, Random Forest, SVM)
├── visualizacoes.R                # 📈 Dashboards e gráficos interativos
├── teste_sistema_completo.R       # 🧪 Testes automatizados do sistema
├── README.md                      # 📚 Esta documentação
└── dados_teste_ir_alem2.csv      # 💾 Dataset de exemplo (gerado)
```

## 🚀 Como Executar

### 1️⃣ **Instalação de Dependências**

```r
# Instala pacotes necessários
install.packages(c(
  "dplyr", "tidyr", "readr", "lubridate",    # Manipulação de dados
  "ggplot2", "plotly", "corrplot",           # Visualizações
  "randomForest", "e1071", "caret", "pROC", # Machine Learning
  "DT", "knitr"                              # Relatórios
))
```

### 2️⃣ **Teste do Sistema**

```r
# Executa teste completo (recomendado primeiro)
source("teste_sistema_completo.R")
```

### 3️⃣ **Análise Completa**

```r
# Carrega sistema principal
source("analise_estatistica.R")

# Executa análise para banana ou milho
resultados <- main_analise_estatistica("banana", dias_historico = 180)

# Visualiza resultados
print(resultados$analise_exploratoria$estatisticas)
```

### 4️⃣ **Modelos Preditivos**

```r
# Carrega módulo de modelos
source("modelos_preditivos_corrigido.R")

# Treina modelos de Machine Learning
modelos <- treinar_modelos_irrigacao(resultados$dados)

# Faz predições
novos_dados <- data.frame(temperatura = 28, umidade_solo = 35, ph_solo = 6.5)
predicao <- prever_irrigacao(modelos, novos_dados)
```

### 5️⃣ **Visualizações**

```r
# Carrega módulo de visualizações
source("visualizacoes.R")

# Cria todas as visualizações
viz <- criar_todas_visualizacoes(resultados$dados, modelos)

# Exibe dashboard
mostrar_dashboard(viz)
```

## 📊 Funcionalidades Principais

### 🔍 **Análise Exploratória de Dados (EDA)**

- **Estatísticas Descritivas**: Média, mediana, quartis de todas as variáveis
- **Análise de Correlação**: Matriz de correlação entre variáveis ambientais
- **Padrões Sazonais**: Identificação de ciclos anuais e mensais
- **Distribuições**: Histogramas e densidade das principais métricas
- **Outliers Detection**: Identificação de valores anômalos

### 🤖 **Modelos Preditivos**

#### **1. Regressão Logística**
```r
# Prediz necessidade de irrigação binária (Sim/Não)
modelo_glm <- glm(irrigacao_realizada ~ temperatura + umidade_solo + ph_solo, 
                  family = binomial)
```

#### **2. Random Forest** 
```r
# Classificação robusta com feature importance
modelo_rf <- randomForest(irrigacao_realizada ~ ., 
                         ntree = 300, importance = TRUE)
```

#### **3. Support Vector Machine (SVM)**
```r
# Classificação não-linear com kernel radial
modelo_svm <- svm(irrigacao_realizada ~ ., 
                  kernel = "radial", probability = TRUE)
```

### 📈 **Visualizações e Dashboards**

#### **Dashboard Principal**
- Status atual dos sensores com alertas visuais
- Histórico de irrigação dos últimos 30 dias
- Padrões de irrigação por condição climática
- KPIs principais (irrigações, umidade média, produtividade)

#### **Análises de Correlação**
- Heatmap de correlação entre variáveis
- Impacto do NPK na produtividade
- Mapas de calor sazonais de irrigação

#### **Séries Temporais**
- Evolução temporal de temperatura, umidade, pH
- Tendências com médias móveis
- Gráficos interativos com plotly

## 🧪 Dados Simulados vs Reais

### **Dados Sintéticos (para testes)**

O sistema gera dados realistas baseados em:

```r
# Padrões sazonais de temperatura
temperatura <- 25 + 5 * sin(2 * pi * tempo_normalizado) + ruído

# Umidade correlacionada inversamente com temperatura  
umidade_solo <- 50 - 0.8 * (temperatura - 25) + ruído

# pH com drift temporal
ph_solo <- 6.5 + 0.3 * sin(2 * pi * tempo_normalizado) + ruído

# NPK baseado em probabilidades condicionais
npk_adequado <- função_do_ph_e_clima()
```

### **Integração com Dados Reais do ESP32**

```r
# Para dados reais do ESP32, substitua:
dados_reais <- read.csv("dados_esp32.csv")
dados_reais$data <- as.Date(dados_reais$timestamp)

# Execute a análise normalmente
resultados_reais <- main_analise_estatistica_dados_reais(dados_reais)
```

## 🎯 Métricas de Performance

### **Avaliação dos Modelos**

- **Acurácia**: Percentual de predições corretas
- **AUC-ROC**: Área sob a curva ROC (0.5-1.0)
- **Sensibilidade**: Taxa de verdadeiros positivos
- **Especificidade**: Taxa de verdadeiros negativos
- **Feature Importance**: Importância de cada variável

### **Exemplo de Resultados**

```
📈 COMPARAÇÃO DE MODELOS:
                    Acurácia    AUC
Regressão Logística   0.847   0.901
Random Forest         0.865   0.923
SVM                   0.852   0.908

🏆 Melhor modelo: Random Forest
```

## 🌾 Configurações de Cultura

### **Banana** 🍌
```r
banana = list(
  umidade_ideal = 60,
  temp_otima = 27,
  ph_range = c(5.5, 7.5),
  npk_prioridade = c("K", "N", "P")
)
```

### **Milho** 🌽
```r
milho = list(
  umidade_ideal = 50,
  temp_otima = 25, 
  ph_range = c(5.5, 7.5),
  npk_prioridade = c("N", "P", "K")
)
```

## 🔧 Personalização

### **Adicionando Nova Cultura**

```r
CULTURA_CONFIG$nova_cultura <- list(
  nome = "Nova Cultura",
  emoji = "🌱",
  umidade_min = 30,
  umidade_ideal = 55,
  temp_otima = 24,
  ph_min = 6.0,
  ph_max = 7.0
)
```

### **Novos Modelos**

```r
# Adicione seu próprio modelo
treinar_modelo_customizado <- function(dados) {
  # Seu código aqui
  modelo <- seu_algoritmo(dados)
  return(modelo)
}
```

## 📋 Outputs e Relatórios

### **Arquivos Gerados**

- `dados_historicos_irrigacao.csv` - Dataset completo processado
- `dados_teste_ir_alem2.csv` - Dados sintéticos para testes
- Gráficos salvos em alta resolução (PNG/PDF)
- Relatórios HTML interativos

### **Relatório Exemplo**

```
🌱 RELATÓRIO FINAL - FARMTECH SOLUTIONS
---------------------------------------------
📅 Período: 2024-07-01 a 2024-12-27
📊 Observações: 180

🌡️ MÉTRICAS AMBIENTAIS:
   Temperatura média: 25.2°C
   Umidade média solo: 52.3%
   pH médio: 6.51

💧 MÉTRICAS DE IRRIGAÇÃO:
   Total irrigações: 67
   Frequência: 37.2%

📈 MÉTRICAS DE PRODUÇÃO:
   Produtividade média: 78.5%
```

## 🚨 Troubleshooting

### **Problemas Comuns**

1. **Erro de pacotes**: Execute `install.packages()` para dependências
2. **Erro de dados**: Verifique se `data` está no formato Date
3. **Erro de memória**: Reduza `dias_historico` para datasets menores
4. **Gráficos não aparecem**: Verifique se está usando RStudio ou R console

### **Performance**

- **Dados pequenos** (<1000 obs): Todos os modelos funcionam bem
- **Dados médios** (1000-10000 obs): Random Forest recomendado  
- **Dados grandes** (>10000 obs): Use sampling ou SVM

## 🤝 Integração com IR ALÉM 1 (Python)

### **Workflow Completo**

1. **ESP32** → Coleta dados dos sensores
2. **Python (IR ALÉM 1)** → Processa clima e comunica com ESP32
3. **R (IR ALÉM 2)** → Análise estatística e modelos preditivos
4. **Dashboard** → Visualização integrada dos resultados

### **Troca de Dados**

```r
# R lê dados processados pelo Python
dados_python <- read.csv("dados_processados_python.csv")

# R processa e salva resultados para Python
write.csv(resultados_r, "analise_estatistica_para_python.csv")
```

## 🎓 Conceitos de Data Science Aplicados

### **Feature Engineering**
- Variáveis lag (valores anteriores)
- Médias móveis  
- Índices compostos (déficit hídrico, stress térmico)
- Variáveis categóricas (condições climáticas)

### **Cross-Validation**
```r
# K-fold cross validation
cv_results <- trainControl(method = "cv", number = 5)
modelo_cv <- train(irrigacao_realizada ~ ., 
                   data = dados, 
                   method = "rf",
                   trControl = cv_results)
```

### **Ensemble Learning**
```r
# Combina predições de múltiplos modelos
pred_ensemble <- (pred_glm + pred_rf + pred_svm) / 3
```

## 📚 Referências Técnicas

- **Agricultura de Precisão**: Conceitos aplicados de IoT agrícola
- **Machine Learning**: Algoritmos supervisionados para classificação
- **Análise de Séries Temporais**: Padrões sazonais e tendências
- **Estatística Descritiva**: Medidas de tendência e dispersão
- **Visualização de Dados**: Princípios de dashboard design

---

## 🏆 Status do Projeto

✅ **IR ALÉM 1 (Python)** - Integração com API climática - **CONCLUÍDO**  
✅ **IR ALÉM 2 (R)** - Análise estatística e ML - **CONCLUÍDO**  
🎯 **Sistema Integrado** - ESP32 + Python + R - **PRONTO PARA PRODUÇÃO**

---

**Desenvolvido por:** Grupo 59 FIAP  
**Disciplina:** Fase 2 - Cap 1  
**Data:** Outubro 2024  
**Versão:** 2.0.0

🌱 **FarmTech Solutions - O futuro da agricultura é data-driven!** 📊