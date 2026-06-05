# 📋 Product Backlog — FarmTech Solutions | Fase 5

> **Projeto:** Previsão de Rendimento de Safra + Computação em Nuvem  
> **Time:** Phellype Massarente · Carlos Costato · Cesar Azeredo  
> **Início:** Março 2026  
> **Metodologia:** Sprints semanais (Quinta 1h30 + FDS)

---

## 🗂️ Índice de Épicos

| ID | Épico | Prioridade | Status |
|----|-------|------------|--------|
| EP-01 | Análise Exploratória de Dados (EDA) | 🔴 Alta | ✅ Concluído |
| EP-02 | Machine Learning Não Supervisionado | 🔴 Alta | ✅ Concluído |
| EP-03 | Machine Learning Supervisionado | 🔴 Alta | ✅ Concluído |
| EP-04 | Computação em Nuvem (AWS) | 🔴 Alta | ✅ Concluído |
| EP-05 | Entrega Final (Vídeos + Documentação) | 🔴 Alta | 🔄 Em progresso |
| EP-06 | Ir Além — ESP32 + IoT (Opcional) | 🟡 Média | 🔄 Em progresso |

---

## 🟦 EP-01 — Análise Exploratória de Dados (EDA)

> **Objetivo:** Compreender o dataset `crop_yield.csv`, identificar padrões, distribuições e correlações entre variáveis climáticas e rendimento agrícola.  
> **Sprint:** 1  
> **Responsáveis:** A definir

### 📖 Histórias de Usuário

#### US-01.1 — Setup do Ambiente e Repositório
> *Como* desenvolvedor do time FarmTech,  
> *Quero* ter o ambiente de desenvolvimento configurado e o repositório organizado,  
> *Para que* possamos colaborar e versionar o projeto desde o início.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-01.1.1 | Criar repositório GitHub público | — | 15 min | ✅ Feito |
| T-01.1.2 | Criar estrutura de pastas (template FIAP) | — | 15 min | ✅ Feito |
| T-01.1.3 | Criar README.md com dados do grupo | — | 30 min | ✅ Feito |
| T-01.1.4 | Criar `.gitignore` e arquivos auxiliares | — | 10 min | ✅ Feito |
| T-01.1.5 | Criar notebook `.ipynb` com nomenclatura correta | — | 10 min | ✅ Feito |
| T-01.1.6 | Instalar dependências (pandas, numpy, matplotlib, seaborn, scikit-learn) | — | 15 min | ✅ Feito |

---

#### US-01.2 — Carregamento e Inspeção Inicial dos Dados
> *Como* cientista de dados da FarmTech,  
> *Quero* carregar e inspecionar o dataset `crop_yield.csv`,  
> *Para que* eu compreenda a estrutura, tipos de dados e qualidade do dataset antes de analisá-lo.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-01.2.1 | Importar bibliotecas e carregar o CSV com `pd.read_csv()` | — | 10 min | ✅ Feito |
| T-01.2.2 | Verificar shape, dtypes e primeiras linhas (`.head()`, `.info()`) | — | 10 min | ✅ Feito |
| T-01.2.3 | Estatísticas descritivas com `.describe()` | — | 10 min | ✅ Feito |
| T-01.2.4 | Verificar valores nulos (`.isnull().sum()`) | — | 10 min | ✅ Feito |
| T-01.2.5 | Verificar duplicatas (`.duplicated().sum()`) | — | 5 min | ✅ Feito |
| T-01.2.6 | Identificar culturas únicas e suas frequências | — | 10 min | ✅ Feito |
| T-01.2.7 | Documentar achados em célula Markdown | — | 15 min | ✅ Feito |

---

#### US-01.3 — Análise Univariada
> *Como* cientista de dados da FarmTech,  
> *Quero* analisar a distribuição individual de cada variável,  
> *Para que* eu identifique assimetrias, outliers e características de cada feature.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-01.3.1 | Histogramas de todas as variáveis numéricas | — | 20 min | ✅ Feito |
| T-01.3.2 | Boxplots por variável numérica | — | 20 min | ✅ Feito |
| T-01.3.3 | Countplot das culturas (distribuição categórica) | — | 15 min | ✅ Feito |
| T-01.3.4 | Análise de assimetria e curtose | — | 15 min | ✅ Feito |
| T-01.3.5 | Documentar distribuições observadas em Markdown | — | 20 min | ✅ Feito |

---

#### US-01.4 — Análise Bivariada e Correlações
> *Como* cientista de dados da FarmTech,  
> *Quero* analisar relações entre variáveis e a variável-alvo (Rendimento),  
> *Para que* eu identifique quais features mais influenciam o rendimento da safra.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-01.4.1 | Matriz de correlação + heatmap (seaborn) | — | 20 min | ✅ Feito |
| T-01.4.2 | Scatter plots: cada variável vs. Rendimento | — | 30 min | ✅ Feito |
| T-01.4.3 | Boxplots de Rendimento por Cultura | — | 15 min | ✅ Feito |
| T-01.4.4 | Pairplot das variáveis numéricas | — | 15 min | ✅ Feito |
| T-01.4.5 | Análise groupby: estatísticas de rendimento por cultura | — | 20 min | ✅ Feito |
| T-01.4.6 | Documentar correlações e insights em Markdown | — | 30 min | ✅ Feito |

---

## 🟩 EP-02 — Machine Learning Não Supervisionado (Clusterização)

> **Objetivo:** Encontrar tendências de rendimento das plantações por meio de clusterização e identificar cenários discrepantes (outliers).  
> **Sprint:** 2  
> **Responsáveis:** A definir

### 📖 Histórias de Usuário

#### US-02.1 — Preparação dos Dados para Clusterização
> *Como* cientista de dados da FarmTech,  
> *Quero* preparar os dados (normalização, seleção de features),  
> *Para que* os algoritmos de clusterização funcionem corretamente sem viés de escala.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-02.1.1 | Selecionar features relevantes para clusterização | — | 15 min | ✅ Feito |
| T-02.1.2 | Aplicar StandardScaler ou MinMaxScaler | — | 15 min | ✅ Feito |
| T-02.1.3 | Tratar variáveis categóricas (encoding se necessário) | — | 15 min | ✅ Feito |
| T-02.1.4 | Documentar decisões de pré-processamento | — | 10 min | ✅ Feito |

---

#### US-02.2 — Clusterização com K-Means
> *Como* cientista de dados da FarmTech,  
> *Quero* aplicar K-Means e determinar o número ideal de clusters,  
> *Para que* eu segmente as plantações em grupos com padrões similares de rendimento.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-02.2.1 | Implementar Método do Cotovelo (Elbow) para K de 2 a 10 | — | 20 min | ✅ Feito |
| T-02.2.2 | Calcular Silhouette Score para cada K | — | 15 min | ✅ Feito |
| T-02.2.3 | Treinar K-Means com K ideal | — | 15 min | ✅ Feito |
| T-02.2.4 | Visualizar clusters em 2D (PCA ou features principais) | — | 30 min | ✅ Feito |
| T-02.2.5 | Analisar centróides e características de cada cluster | — | 20 min | ✅ Feito |

---

#### US-02.3 — Exploração de Outros Algoritmos de Clusterização
> *Como* cientista de dados da FarmTech,  
> *Quero* testar algoritmos alternativos (DBSCAN, Hierarchical),  
> *Para que* eu compare abordagens e escolha a mais adequada aos dados agrícolas.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-02.3.1 | Implementar DBSCAN e ajustar eps/min_samples | — | 30 min | ✅ Feito |
| T-02.3.2 | Implementar Agglomerative Clustering + dendrograma | — | 30 min | ✅ Feito |
| T-02.3.3 | Comparar resultados entre K-Means, DBSCAN e Hierarchical | — | 20 min | ✅ Feito |
| T-02.3.4 | Documentar qual algoritmo melhor segmentou os dados | — | 20 min | ✅ Feito |

---

#### US-02.4 — Detecção de Outliers
> *Como* cientista de dados da FarmTech,  
> *Quero* identificar outliers no dataset,  
> *Para que* eu saiba quais registros são discrepantes e avalie seu impacto na modelagem.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-02.4.1 | Detecção de outliers por IQR (Interquartile Range) | — | 20 min | ✅ Feito |
| T-02.4.2 | Detecção de outliers por Z-Score | — | 15 min | ✅ Feito |
| T-02.4.3 | Isolation Forest para detecção multivariada | — | 20 min | ✅ Feito |
| T-02.4.4 | Visualizações dos outliers identificados | — | 20 min | ✅ Feito |
| T-02.4.5 | Documentar outliers: quantos, quais culturas, impacto | — | 20 min | ✅ Feito |

---

#### US-02.5 — Análise de Tendências e Insights dos Clusters
> *Como* analista da FarmTech,  
> *Quero* interpretar os clusters e tendências encontradas,  
> *Para que* o cliente entenda os padrões de rendimento e tome decisões baseadas em dados.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-02.5.1 | Mapear clusters vs. culturas (crosstab / heatmap) | — | 20 min | ✅ Feito |
| T-02.5.2 | Analisar média de rendimento por cluster | — | 15 min | ✅ Feito |
| T-02.5.3 | Identificar perfis de alto/baixo rendimento | — | 20 min | ✅ Feito |
| T-02.5.4 | Escrever conclusões e tendências em Markdown | — | 30 min | ✅ Feito |

---

## 🟨 EP-03 — Machine Learning Supervisionado (Regressão)

> **Objetivo:** Construir 5 modelos preditivos de regressão para prever o rendimento da safra, avaliar com métricas e selecionar o melhor.  
> **Sprint:** 3  
> **Responsáveis:** A definir

### 📖 Histórias de Usuário

#### US-03.1 — Preparação dos Dados para Regressão
> *Como* cientista de dados da FarmTech,  
> *Quero* preparar os dados para modelagem supervisionada,  
> *Para que* os modelos recebam inputs corretos e comparáveis.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-03.1.1 | Encoding da variável categórica "Cultura" (LabelEncoder ou OneHot) | — | 15 min | ✅ Feito |
| T-03.1.2 | Definir X (features) e y (Rendimento) | — | 10 min | ✅ Feito |
| T-03.1.3 | Split treino/teste (80/20, random_state fixo) | — | 10 min | ✅ Feito |
| T-03.1.4 | Normalizar/padronizar features se necessário | — | 15 min | ✅ Feito |
| T-03.1.5 | Documentar pipeline de pré-processamento | — | 10 min | ✅ Feito |

---

#### US-03.2 — Modelo 1: Regressão Linear
> *Como* cientista de dados,  
> *Quero* treinar uma Regressão Linear como baseline,  
> *Para que* eu tenha um ponto de referência para comparar modelos mais complexos.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-03.2.1 | Instanciar e treinar LinearRegression | — | 10 min | ✅ Feito |
| T-03.2.2 | Predizer no conjunto de teste | — | 5 min | ✅ Feito |
| T-03.2.3 | Calcular MAE, MSE, RMSE, R² | — | 10 min | ✅ Feito |
| T-03.2.4 | Gráfico real vs. predito | — | 10 min | ✅ Feito |
| T-03.2.5 | Documentar resultados | — | 10 min | ✅ Feito |

---

#### US-03.3 — Modelo 2: Decision Tree Regressor
> *Como* cientista de dados,  
> *Quero* treinar um Decision Tree Regressor,  
> *Para que* eu capture relações não-lineares e tenha um modelo interpretável.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-03.3.1 | Instanciar e treinar DecisionTreeRegressor | — | 10 min | ✅ Feito |
| T-03.3.2 | Predizer e calcular métricas (MAE, MSE, RMSE, R²) | — | 10 min | ✅ Feito |
| T-03.3.3 | Analisar feature importance | — | 10 min | ✅ Feito |
| T-03.3.4 | Gráfico real vs. predito | — | 10 min | ✅ Feito |
| T-03.3.5 | Documentar resultados | — | 10 min | ✅ Feito |

---

#### US-03.4 — Modelo 3: Random Forest Regressor
> *Como* cientista de dados,  
> *Quero* treinar um Random Forest Regressor,  
> *Para que* eu reduza overfitting com ensemble de árvores e obtenha melhor generalização.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-03.4.1 | Instanciar e treinar RandomForestRegressor | — | 10 min | ✅ Feito |
| T-03.4.2 | Tunar hiperparâmetros (n_estimators, max_depth, etc.) | — | 30 min | ✅ Feito |
| T-03.4.3 | Predizer e calcular métricas (MAE, MSE, RMSE, R²) | — | 10 min | ✅ Feito |
| T-03.4.4 | Analisar feature importance | — | 10 min | ✅ Feito |
| T-03.4.5 | Gráfico real vs. predito | — | 10 min | ✅ Feito |
| T-03.4.6 | Documentar resultados | — | 10 min | ✅ Feito |

---

#### US-03.5 — Modelo 4: Gradient Boosting / XGBoost
> *Como* cientista de dados,  
> *Quero* treinar um Gradient Boosting Regressor (ou XGBoost),  
> *Para que* eu obtenha alta performance em dados tabulares com boosting iterativo.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-03.5.1 | Instanciar e treinar GradientBoostingRegressor (ou XGBRegressor) | — | 10 min | ✅ Feito |
| T-03.5.2 | Tunar hiperparâmetros (learning_rate, n_estimators, max_depth) | — | 30 min | ✅ Feito |
| T-03.5.3 | Predizer e calcular métricas (MAE, MSE, RMSE, R²) | — | 10 min | ✅ Feito |
| T-03.5.4 | Gráfico real vs. predito | — | 10 min | ✅ Feito |
| T-03.5.5 | Documentar resultados | — | 10 min | ✅ Feito |

---

#### US-03.6 — Modelo 5: KNN Regressor (ou SVR / Ridge / Lasso)
> *Como* cientista de dados,  
> *Quero* treinar um quinto modelo com abordagem diferente,  
> *Para que* eu diversifique os algoritmos e tenha uma comparação mais robusta.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-03.6.1 | Instanciar e treinar KNeighborsRegressor (ou SVR/Ridge/Lasso) | — | 10 min | ✅ Feito |
| T-03.6.2 | Tunar hiperparâmetros (n_neighbors / C / alpha) | — | 20 min | ✅ Feito |
| T-03.6.3 | Predizer e calcular métricas (MAE, MSE, RMSE, R²) | — | 10 min | ✅ Feito |
| T-03.6.4 | Gráfico real vs. predito | — | 10 min | ✅ Feito |
| T-03.6.5 | Documentar resultados | — | 10 min | ✅ Feito |

---

#### US-03.7 — Comparação e Seleção do Melhor Modelo
> *Como* analista da FarmTech,  
> *Quero* comparar os 5 modelos lado a lado com métricas e visualizações,  
> *Para que* eu recomende o modelo mais adequado para prever rendimento de safra.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-03.7.1 | Montar tabela comparativa (DataFrame com métricas dos 5 modelos) | — | 20 min | ✅ Feito |
| T-03.7.2 | Gráfico de barras comparando R² dos 5 modelos | — | 15 min | ✅ Feito |
| T-03.7.3 | Gráfico de barras comparando RMSE dos 5 modelos | — | 15 min | ✅ Feito |
| T-03.7.4 | Análise de resíduos do melhor modelo | — | 20 min | ✅ Feito |
| T-03.7.5 | Cross-validation (cv=5) no melhor modelo | — | 20 min | ✅ Feito |
| T-03.7.6 | Escrever conclusão final: melhor modelo, pontos fortes, limitações | — | 30 min | ✅ Feito |

---

## 🟧 EP-04 — Computação em Nuvem (AWS)

> **Objetivo:** Estimar custos na AWS para hospedar a ML, comparar regiões SP vs Virgínia e justificar a escolha considerando LGPD e latência.  
> **Sprint:** 4  
> **Responsáveis:** A definir

### 📖 Histórias de Usuário

#### US-04.1 — Cotação AWS — Região São Paulo (sa-east-1)
> *Como* engenheiro de infraestrutura da FarmTech,  
> *Quero* cotar uma máquina Linux na região São Paulo usando a Calculadora AWS,  
> *Para que* eu saiba o custo On-Demand de hospedar a API/ML no Brasil.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-04.1.1 | Acessar https://calculator.aws/ e selecionar EC2 | — | 10 min | ✅ Feito |
| T-04.1.2 | Configurar: Linux, 2 vCPUs, 1 GiB RAM, sa-east-1 | — | 15 min | ✅ Feito |
| T-04.1.3 | Adicionar 50 GB de armazenamento HDD (EBS) | — | 10 min | ✅ Feito |
| T-04.1.4 | Selecionar On-Demand 100% | — | 5 min | ✅ Feito |
| T-04.1.5 | Capturar screenshot da cotação completa | — | 5 min | ⬜ A fazer |
| T-04.1.6 | Anotar custo mensal e anual | — | 5 min | ✅ Feito |

---

#### US-04.2 — Cotação AWS — Região Virgínia do Norte (us-east-1)
> *Como* engenheiro de infraestrutura da FarmTech,  
> *Quero* cotar a mesma máquina na região Virgínia do Norte,  
> *Para que* eu compare os custos com São Paulo.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-04.2.1 | Configurar: Linux, 2 vCPUs, 1 GiB RAM, us-east-1 | — | 15 min | ✅ Feito |
| T-04.2.2 | Adicionar 50 GB de armazenamento HDD (EBS) | — | 10 min | ✅ Feito |
| T-04.2.3 | Selecionar On-Demand 100% | — | 5 min | ✅ Feito |
| T-04.2.4 | Capturar screenshot da cotação completa | — | 5 min | ⬜ A fazer |
| T-04.2.5 | Anotar custo mensal e anual | — | 5 min | ✅ Feito |

---

#### US-04.3 — Comparação de Custos e Justificativa
> *Como* analista da FarmTech,  
> *Quero* comparar os custos das duas regiões e justificar tecnicamente a melhor escolha,  
> *Para que* o cliente entenda a recomendação e os trade-offs envolvidos.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-04.3.1 | Montar tabela comparativa SP vs Virgínia (custo mensal/anual) | — | 20 min | ✅ Feito |
| T-04.3.2 | Criar gráfico comparativo de custos | — | 20 min | ✅ Feito |
| T-04.3.3 | Pesquisar e documentar implicações da LGPD | — | 30 min | ✅ Feito |
| T-04.3.4 | Analisar latência SP vs Virgínia para acesso aos sensores | — | 20 min | ✅ Feito |
| T-04.3.5 | Escrever justificativa final (custo vs compliance vs latência) | — | 30 min | ✅ Feito |
| T-04.3.6 | Inserir tudo no README.md (imagens + texto) | — | 30 min | ✅ Feito |

---

## 🟥 EP-05 — Entrega Final (Vídeos + Documentação)

> **Objetivo:** Gravar vídeos demonstrativos, finalizar README e garantir que tudo esteja pronto para entrega.  
> **Sprint:** 5  
> **Responsáveis:** A definir

### 📖 Histórias de Usuário

#### US-05.1 — Revisão e Polimento do Notebook Jupyter
> *Como* time FarmTech,  
> *Queremos* revisar e garantir que o notebook seja 100% executável,  
> *Para que* a equipe da FIAP consiga rodar sem erros na correção.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-05.1.1 | Restart Kernel & Run All — verificar se roda sem erros | — | 15 min | ✅ Feito |
| T-05.1.2 | Revisar ortografia e formatação das células Markdown | — | 20 min | ✅ Feito |
| T-05.1.3 | Garantir que gráficos estão renderizando corretamente | — | 10 min | ✅ Feito |
| T-05.1.4 | Verificar que comentários inline estão no código | — | 15 min | ✅ Feito |
| T-05.1.5 | Conferir nomenclatura do arquivo `.ipynb` | — | 5 min | ✅ Feito |

---

#### US-05.2 — Gravação do Vídeo 1 — Machine Learning
> *Como* time FarmTech,  
> *Queremos* gravar um vídeo de até 5 minutos demonstrando a Entrega 1,  
> *Para que* os avaliadores vejam o ML funcionando sem precisar executar o código.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-05.2.1 | Montar roteiro do vídeo (EDA → Clusters → 5 modelos → conclusão) | — | 20 min | ✅ Feito |
| T-05.2.2 | Gravar tela + narração (≤ 5 min) | — | 45 min | ✅ Feito |
| T-05.2.3 | Editar vídeo se necessário | — | 20 min | ✅ Feito |
| T-05.2.4 | Upload no YouTube como "não listado" | — | 10 min | ✅ Feito |
| T-05.2.5 | Adicionar link do vídeo no README.md | — | 5 min | ✅ Feito |

**Atualização US-05.2 (17/03/2026):**
- Link do vídeo Entrega 1 (Machine Learning): https://youtu.be/Slx6_YHVWig

---

#### US-05.3 — Gravação do Vídeo 2 — AWS Cloud
> *Como* time FarmTech,  
> *Queremos* gravar um vídeo de até 5 minutos demonstrando a Entrega 2,  
> *Para que* os avaliadores vejam a comparação de custos na AWS.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-05.3.1 | Montar roteiro do vídeo (calculadora → SP vs Virgínia → justificativa) | — | 20 min | ✅ Feito |
| T-05.3.2 | Gravar tela + narração (≤ 5 min) | — | 45 min | ✅ Feito |
| T-05.3.3 | Editar vídeo se necessário | — | 20 min | ✅ Feito |
| T-05.3.4 | Upload no YouTube como "não listado" | — | 10 min | ✅ Feito |
| T-05.3.5 | Adicionar link do vídeo no README.md | — | 5 min | ✅ Feito |

**Atualização US-05.3 (17/03/2026):**
- Link do vídeo AWS Cloud: https://youtu.be/xAOtlSShT0I

---

#### US-05.4 — Commit Final e Submissão
> *Como* time FarmTech,  
> *Queremos* fazer o commit final e submeter o link no portal da FIAP,  
> *Para que* a entrega seja registrada dentro do prazo.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-05.4.1 | Revisão final do README completo (todos os links funcionando) | — | 15 min | ✅ Feito |
| T-05.4.2 | Verificar que repo está público | — | 5 min | ⬜ A fazer (verificar no GitHub) |
| T-05.4.3 | Commit final + push | — | 10 min | 🔄 Em progresso |
| T-05.4.4 | Postar link do repositório no portal FIAP | — | 10 min | ⬜ A fazer |
| T-05.4.5 | ⚠️ NÃO FAZER mais commits após entrega | — | — | ⬜ A fazer |

---

## 🟪 EP-06 — Ir Além: ESP32 + IoT (Opcional)

> **Objetivo:** Implementar sistema de coleta de dados com ESP32 real + sensores + comunicação Wi-Fi.  
> **Sprint:** 6 (pós-entrega obrigatória)  
> **Responsáveis:** A definir  
> **Opção Escolhida:** ✅ **Opção 1 — Sistema de Coleta com ESP32 + Wi-Fi**  
> (Não Opção 2 — Classificação de Saúde com ML + ESP32)

### 📖 Histórias de Usuário

#### US-06.1 — Design e Planejamento do Sistema IoT
> *Como* engenheiro IoT da FarmTech,  
> *Quero* definir sensores, arquitetura e destino dos dados,  
> *Para que* o sistema esteja bem planejado antes da implementação.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-06.1.1 | Escolher 2 sensores compatíveis com o contexto agrícola | — | 30 min | ✅ Feito |
| T-06.1.2 | Definir destino dos dados (MQTT / Banco / HTML / HTTP) | — | 20 min | ✅ Feito |
| T-06.1.3 | Desenhar arquitetura do circuito (Wokwi.com) | — | 1h | 🔄 Em progresso |
| T-06.1.4 | Escrever justificativa dos sensores escolhidos | — | 20 min | ✅ Feito |

**Decisões US-06.1 (17/03/2026):**
- **Sensores escolhidos:** DHT22 (temperatura/umidade do ar) + sensor de umidade do solo (analógico).
- **Destino dos dados:** API HTTP (JSON) hospedada na AWS (região sa-east-1).
- **Arquitetura planejada:** ESP32 → Wi-Fi → API HTTP na AWS → armazenamento/consumo no backend.
- **Justificativa:** combinação cobre variáveis críticas para irrigação (clima + solo), com baixo custo e ampla disponibilidade em simulação Wokwi e prototipagem física.

---

#### US-06.2 — Implementação no ESP32
> *Como* engenheiro IoT da FarmTech,  
> *Quero* programar o ESP32 para coletar dados e enviar via Wi-Fi,  
> *Para que* os dados dos sensores sejam disponibilizados em tempo real.

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-06.2.1 | Integrar sensores ao ESP32 (circuito físico ou Wokwi) | — | 1h | 🔄 Em progresso |
| T-06.2.2 | Programar leitura dos sensores (C/C++ ou MicroPython) | — | 1.5h | ✅ Feito |
| T-06.2.3 | Configurar comunicação Wi-Fi no ESP32 | — | 1h | 🔄 Em progresso |
| T-06.2.4 | Programar envio dos dados ao serviço escolhido | — | 1.5h | ✅ Feito |
| T-06.2.5 | Testar integração completa (sensor → Wi-Fi → destino) | — | 1h | 🔄 Em progresso |

**Atualização US-06.2 (17/03/2026):**
- Implementado firmware base em `src/esp32/main.cpp` (leitura DHT22 + solo e envio HTTP em JSON).
- Implementado simulador em `src/esp32/simulator.py` para testes sem hardware físico.
- Teste local executado com sucesso para geração/envio; integração fim a fim depende de API ativa no endpoint.

---

#### US-06.3 — Documentação e Vídeo do Ir Além
> *Como* time FarmTech,  
> *Queremos* documentar o Ir Além e gravar vídeo demonstrativo,  
> *Para que* recebamos a gratificação (troféu de excelência).

| ID | Task | Responsável | Estimativa | Status |
|----|------|-------------|------------|--------|
| T-06.3.1 | Criar seção "Ir Além" no README do GitHub | — | 20 min | ✅ Feito |
| T-06.3.2 | Upload do código-fonte comentado no repo | — | 15 min | ⬜ A fazer |
| T-06.3.3 | Inserir figura da arquitetura do circuito | — | 10 min | ⬜ A fazer |
| T-06.3.4 | Gravar vídeo demonstrativo (≤ 5 min, YouTube não listado) | — | 1h | ⬜ A fazer |
| T-06.3.5 | Adicionar link do vídeo no README | — | 5 min | ⬜ A fazer |

---

## 📊 Resumo do Backlog

| Épico | User Stories | Tasks | Estimativa Total |
|-------|-------------|-------|-----------------|
| EP-01 — EDA | 4 | 23 | ~5h |
| EP-02 — Clusterização | 5 | 22 | ~6h |
| EP-03 — Regressão | 7 | 34 | ~8h |
| EP-04 — AWS Cloud | 3 | 17 | ~4h |
| EP-05 — Entrega Final | 4 | 20 | ~5h |
| EP-06 — Ir Além (Opção 1) | 3 | 14 | ~10h |
| **TOTAL** | **26** | **130** | **~38h** |

---

## 🏷️ Legenda de Status

| Símbolo | Significado |
|---------|-------------|
| ⬜ A fazer | Não iniciado |
| 🔄 Em progresso | Em andamento |
| ✅ Feito | Concluído |
| ⛔ Bloqueado | Impedimento externo |
| 🚫 Cancelado | Removido do escopo |

---

## 📝 Convenção de IDs

```
EP-XX       → Épico (ex.: EP-01)
US-XX.Y     → User Story do épico XX (ex.: US-01.2)
T-XX.Y.Z    → Task Z da story Y do épico XX (ex.: T-01.2.3)
```

---

*Última atualização: Março 2026*
