# 🚀 Roadmap — Fase 5 | FarmTech Solutions (FIAP)

> **Objetivo:** Desenvolver as entregas obrigatórias (Machine Learning + Computação em Nuvem) e, opcionalmente, os desafios "Ir Além" (ESP32 + IoT).
>
> **Agenda de trabalho:** Quintas-feiras (1h30) + Finais de semana

---

## 📋 Visão Geral das Entregas

| # | Entrega | Tipo | Peso | Status |
|---|---------|------|------|--------|
| 1 | Machine Learning — Previsão de Rendimento de Safra | Obrigatória | 10 pts | ✅ Concluído |
| 2 | Computação em Nuvem — Estimativa de Custos AWS | Obrigatória | 10 pts | ✅ Concluído |
| 3 | **ESP32 + Wi-Fi + Sensores (Opção 1) — ESCOLHIDA** | Ir Além | Troféu | 🔄 Em progresso |
| 4 | ML + ESP32 — Classificação de Saúde (Opção 2) | Ir Além | Troféu | ⚪ Não escolhido |

---

## 📅 Cronograma por Sprints

### 🔵 SPRINT 1 — Fundação e Análise Exploratória
**Foco:** Entrega 1 — Parte 1/3  
**Tempo estimado:** 1 quinta (1h30) + 1 FDS (~4-6h)

| Dia | Tarefa | Duração | Detalhes |
|-----|--------|---------|----------|
| **Quinta** | Setup do repositório GitHub + estrutura do projeto | 30 min | Criar repo, README inicial, estrutura de pastas |
| **Quinta** | Download e leitura do dataset `crop_yield.csv` | 15 min | Entender as variáveis |
| **Quinta** | Início da Análise Exploratória (EDA) | 45 min | Importar libs, verificar shape, tipos, nulos |
| **Sábado** | EDA completa | 3-4h | Estatísticas descritivas, distribuições, correlações, visualizações |
| **Domingo** | Documentação em Markdown no Jupyter | 1-2h | Narrar achados, inserir gráficos, conclusões parciais |

#### ✅ Checklist Sprint 1
- [ ] Repositório GitHub criado e público
- [ ] Arquivo `.ipynb` criado com nomenclatura correta: `PhellypeMatheusGiacoiaFlaibamMassarente_rm566826_pbl_fase4.ipynb`
- [ ] Dataset carregado e inspecionado (`.head()`, `.info()`, `.describe()`)
- [ ] Verificação de valores nulos e duplicados
- [ ] Análise univariada (histogramas, boxplots por variável)
- [ ] Análise bivariada (correlações, scatter plots, heatmap)
- [ ] Análise por cultura (groupby Cultura)
- [ ] Células Markdown documentando os achados

---

### 🟢 SPRINT 2 — Clusterização e Detecção de Outliers
**Foco:** Entrega 1 — Parte 2/3 (ML Não Supervisionado)  
**Tempo estimado:** 1 quinta (1h30) + 1 FDS (~4-6h)

| Dia | Tarefa | Duração | Detalhes |
|-----|--------|---------|----------|
| **Quinta** | Preparação dos dados para clusterização | 30 min | Normalização/padronização, seleção de features |
| **Quinta** | Implementar K-Means + Método do Cotovelo | 60 min | Testar diferentes K, plotar inércias |
| **Sábado** | Explorar outros algoritmos de clusterização | 2-3h | DBSCAN, Hierarchical, etc. |
| **Sábado** | Detecção de outliers | 1-2h | IQR, Z-Score, Isolation Forest, análise visual |
| **Domingo** | Análise e documentação das tendências | 2-3h | Interpretar clusters, narrar insights em Markdown |

#### ✅ Checklist Sprint 2
- [ ] Dados normalizados/padronizados (StandardScaler / MinMaxScaler)
- [ ] Método do Cotovelo (Elbow Method) aplicado
- [ ] Silhouette Score calculado
- [ ] Clusters visualizados (2D com PCA ou scatter)
- [ ] Tendências de rendimento por cluster identificadas
- [ ] Outliers detectados e documentados
- [ ] Relação dos clusters com as culturas explicada
- [ ] Markdown com conclusões sobre padrões e discrepâncias

---

### 🟡 SPRINT 3 — Modelos Preditivos de Regressão
**Foco:** Entrega 1 — Parte 3/3 (ML Supervisionado)  
**Tempo estimado:** 1 quinta (1h30) + 1 FDS (~6-8h)

| Dia | Tarefa | Duração | Detalhes |
|-----|--------|---------|----------|
| **Quinta** | Preparação dos dados para regressão | 30 min | Encoding categórico, split treino/teste, feature engineering |
| **Quinta** | Modelo 1 — Regressão Linear | 30 min | Treinar, avaliar, documentar |
| **Quinta** | Modelo 2 — Decision Tree Regressor | 30 min | Treinar, avaliar, documentar |
| **Sábado** | Modelo 3 — Random Forest Regressor | 1-2h | Treinar, tunar hiperparâmetros, avaliar |
| **Sábado** | Modelo 4 — Gradient Boosting / XGBoost | 1-2h | Treinar, tunar hiperparâmetros, avaliar |
| **Sábado** | Modelo 5 — KNN / SVR / outro | 1-2h | Treinar, avaliar, documentar |
| **Domingo** | Comparação dos modelos + Métricas | 2-3h | Tabela comparativa, gráficos residuais, conclusões |
| **Domingo** | Finalização do Jupyter + revisão geral | 1-2h | Revisão do notebook inteiro, MD final |

#### ✅ Checklist Sprint 3
- [ ] Variáveis categóricas tratadas (Label Encoding / One-Hot)
- [ ] Split treino/teste (ex.: 80/20 com `random_state`)
- [ ] **5 modelos implementados**, cada um com algoritmo diferente:
  - [ ] Modelo 1: Regressão Linear
  - [ ] Modelo 2: Decision Tree Regressor
  - [ ] Modelo 3: Random Forest Regressor
  - [ ] Modelo 4: Gradient Boosting (ou XGBoost)
  - [ ] Modelo 5: KNN Regressor (ou SVR / Ridge / Lasso)
- [ ] Métricas calculadas para cada modelo:
  - [ ] MAE (Mean Absolute Error)
  - [ ] MSE (Mean Squared Error)
  - [ ] RMSE (Root Mean Squared Error)
  - [ ] R² Score
- [ ] Tabela comparativa entre os 5 modelos
- [ ] Gráficos de valores reais vs. preditos
- [ ] Análise de resíduos
- [ ] Cross-validation aplicada
- [ ] Conclusões sobre o melhor modelo e limitações
- [ ] Notebook 100% executável de ponta a ponta

---

### 🟠 SPRINT 4 — Computação em Nuvem (AWS)
**Foco:** Entrega 2  
**Tempo estimado:** 1 quinta (1h30) + 1 FDS (~3-4h)

| Dia | Tarefa | Duração | Detalhes |
|-----|--------|---------|----------|
| **Quinta** | Acessar a Calculadora AWS | 30 min | https://calculator.aws/ — entender a interface |
| **Quinta** | Cotar máquina em São Paulo (sa-east-1) | 30 min | EC2: 2 vCPUs, 1 GiB RAM, até 5 Gbps, 50 GB HDD |
| **Quinta** | Cotar máquina na Virgínia do Norte (us-east-1) | 30 min | Mesmas configurações, On-Demand 100% |
| **Sábado** | Comparação de custos + prints/screenshots | 1-2h | Capturar telas, montar tabela comparativa |
| **Sábado** | Justificativa técnica e legal | 1-2h | LGPD, latência, soberania de dados, performance |
| **Domingo** | Documentar no README | 1-2h | Imagens, gráficos, textos organizados |

#### ✅ Checklist Sprint 4
- [ ] Cotação São Paulo (sa-east-1):
  - [ ] Instância EC2 identificada (ex.: t3.micro ou similar)
  - [ ] Custo On-Demand mensal e anual
  - [ ] Screenshot da calculadora
- [ ] Cotação Virgínia do Norte (us-east-1):
  - [ ] Mesma instância EC2
  - [ ] Custo On-Demand mensal e anual
  - [ ] Screenshot da calculadora
- [ ] Tabela comparativa de custos (SP vs Virgínia)
- [ ] Gráfico comparativo de custos
- [ ] Justificativa técnica considerando:
  - [ ] LGPD e restrições legais de dados no exterior
  - [ ] Latência e acesso rápido aos dados dos sensores
  - [ ] Diferença de custo vs. compliance
  - [ ] Escolha final bem fundamentada
- [ ] README atualizado com toda a documentação da Entrega 2

---

### 🔴 SPRINT 5 — Vídeos, README Final e Entrega
**Foco:** Finalização e polimento  
**Tempo estimado:** 1 quinta (1h30) + 1 FDS (~4-5h)

| Dia | Tarefa | Duração | Detalhes |
|-----|--------|---------|----------|
| **Quinta** | Revisão final do Notebook Jupyter | 1h | Verificar execução completa, ortografia |
| **Quinta** | Revisão final do README | 30 min | Links, imagens, estrutura |
| **Sábado** | Gravar Vídeo 1 — Machine Learning | 1-2h | Roteiro, gravação, upload YouTube (não listado) |
| **Sábado** | Gravar Vídeo 2 — AWS Cloud | 1-2h | Roteiro, gravação, upload YouTube (não listado) |
| **Domingo** | Finalizar README com links dos vídeos | 30 min | Inserir links do YouTube |
| **Domingo** | Commit final + verificação do repositório | 30 min | Testar todos os links, repo público |
| **Domingo** | Submissão no portal FIAP | 30 min | Enviar link do GitHub |

#### ✅ Checklist Sprint 5
- [ ] Notebook re-executado do zero (Kernel → Restart & Run All)
- [ ] README final com:
  - [ ] Introdução do projeto
  - [ ] Link para o Jupyter Notebook
  - [ ] Seção da Entrega 1 (ML) com link do vídeo
  - [ ] Seção da Entrega 2 (AWS) com imagens e link do vídeo
  - [ ] (Opcional) Seção "Ir Além"
- [ ] Vídeo 1 gravado e no YouTube (≤ 5 min, não listado)
- [ ] Vídeo 2 gravado e no YouTube (≤ 5 min, não listado)
- [ ] Repositório público e acessível
- [ ] **NENHUM commit após a data de entrega**
- [ ] Link do repositório postado no portal FIAP

---

### 🟣 SPRINT 6 (OPCIONAL) — "Ir Além" — ESP32 + IoT
**Foco:** Ir Além — Opção 1 e/ou 2  
**Tempo estimado:** 2-3 finais de semana extras (~10-15h)

#### Opção 1: Sistema de Coleta com ESP32 + Wi-Fi

| Etapa | Tarefa | Duração |
|-------|--------|---------|
| 1 | Escolher 2 sensores (ex.: DHT22 temp/umidade + sensor de umidade do solo) | 1h |
| 2 | Montar circuito no Wokwi.com (simulação) | 2h |
| 3 | Programar ESP32 (C/C++ ou MicroPython) — coleta + Wi-Fi | 3-4h |
| 4 | Configurar destino dos dados (MQTT/Banco/HTML) | 2-3h |
| 5 | Testar integração completa | 1-2h |
| 6 | Documentar no GitHub (seção "Ir Além") + vídeo | 2h |

#### Opção 2: Classificação de Saúde com ML + ESP32

| Etapa | Tarefa | Duração |
|-------|--------|---------|
| 1 | Escolher sensor e cultura agrícola | 1h |
| 2 | Integrar sensor ao ESP32, coletar dados | 3-4h |
| 3 | Treinar modelo ML (Scikit-learn / TensorFlow) | 3-4h |
| 4 | Pipeline: ESP32 → dados → modelo → classificação | 2-3h |
| 5 | Validar com dados em tempo real | 1-2h |
| 6 | Documentar + vídeo (≤ 5 min) | 2h |

#### ✅ Checklist "Ir Além"
- [x] Seção "Ir Além" no README do GitHub
- [ ] Código-fonte comentado no repositório
- [ ] Figura da arquitetura do circuito (Wokwi.com ou similar)
- [x] Justificativa dos sensores escolhidos
- [ ] Demonstração funcional (vídeo ≤ 5 min, YouTube não listado)

---

## 📁 Estrutura do Repositório (Template Oficial FIAP)

> Baseado no template: [agodoi/templateFiapVfinal](https://github.com/agodoi/templateFiapVfinal)

```
📦 farmtech-solutions-fase5/
├── 📂 .github/                              ← Configurações do GitHub
├── 📂 assets/                               ← Imagens, logos, screenshots
│   ├── logo-fiap.png
│   ├── aws_sp_cotacao.png
│   ├── aws_virginia_cotacao.png
│   ├── comparativo_custos.png
│   └── arquitetura_iot.png                  ← (Ir Além)
├── 📂 config/                               ← Configurações do projeto
├── 📂 document/                             ← Documentação do projeto
│   ├── ai_project_document_fiap.md          ← Doc principal de IA
│   └── 📂 other/                            ← Docs complementares
├── 📂 scripts/                              ← Scripts auxiliares
├── 📂 src/                                  ← Código-fonte
│   ├── PhellypeMatheusGiacoiaFlaibamMassarente_rm566826_pbl_fase4.ipynb ← Notebook Jupyter
│   ├── crop_yield.csv                       ← Dataset
│   └── 📂 esp32/                            ← (Ir Além)
│       └── main.cpp
├── 📄 .gitignore
├── 📄 README.md                             ← Guia principal do projeto
└── 📄 ROADMAP_FASE5.md                      ← Este roteiro
```

---

## 🎯 Barema — Resumo dos Pesos

### Entrega 1 — Machine Learning (10 pts)

| Critério | Peso |
|----------|------|
| Repositório GitHub (prazo, nomenclatura, organização) | 1.5 |
| Notebook Jupyter (código + markdown + achados) | 3.0 |
| README (intro + link Jupyter + link vídeo) | 2.0 |
| Vídeo demonstrativo (≤ 5 min, YouTube não listado) | 2.0 |
| Organização e apresentação geral | 1.5 |

### Entrega 2 — AWS Cloud (10 pts)

| Critério | Peso |
|----------|------|
| Estimativa de custos AWS (SP vs Virgínia) | 2.5 |
| Justificativa técnica (LGPD, latência, custo) | 2.5 |
| Documentação no README (imagens + gráficos + texto) | 2.0 |
| Vídeo demonstrativo (≤ 5 min, YouTube não listado) | 2.0 |
| Organização e pontualidade | 1.0 |

---

## 📌 Lembretes Importantes

1. **Nomenclatura do arquivo Jupyter:** `NomeCompleto_rmXXXXX_pbl_fase4.ipynb`
2. **Repositório PÚBLICO** no GitHub
3. **Vídeos no YouTube como "não listado"** (máx. 5 min cada)
4. **NÃO fazer commits após a data de entrega**
5. **README não deve repetir o conteúdo do Jupyter** — serve como guia introdutório
6. **Notebook deve ser executável do zero** (Restart & Run All sem erros)
7. **5 modelos preditivos com algoritmos DIFERENTES**
8. **AWS On-Demand 100%** — não usar reserved ou spot

---

## 🛠️ Stack Tecnológico

| Componente | Tecnologia |
|------------|-----------|
| Linguagem ML | Python 3.x |
| Notebook | Jupyter Notebook |
| Libs principais | pandas, numpy, matplotlib, seaborn, scikit-learn |
| Libs extras | xgboost, plotly (opcional) |
| Clusterização | KMeans, DBSCAN, AgglomerativeClustering |
| Regressão | LinearRegression, DecisionTreeRegressor, RandomForestRegressor, GradientBoostingRegressor, KNeighborsRegressor |
| Cloud | AWS Calculator |
| IoT (Ir Além) | ESP32, C/C++ ou MicroPython, MQTT |
| Versionamento | Git + GitHub |

---

## 📊 Faixas de Nota

| Faixa | Descrição |
|-------|-----------|
| **9.0 – 10.0** | Excelência total: código funcional, organização impecável, vídeo claro |
| **7.0 – 8.9** | Completo com pequenas falhas de organização ou execução |
| **5.0 – 6.9** | Falhas significativas (código não funcional, documentação incompleta) |
| **0.0 – 4.9** | Não atende requisitos mínimos ou fora do prazo |

---

*Última atualização: Março 2026*
