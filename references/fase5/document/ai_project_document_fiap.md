<img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=30% height=30%>

# AI Project Document - Módulo 1 - FIAP

**_Os trechos em itálico servem apenas como guia para o preenchimento da seção. Por esse motivo, não devem fazer parte da documentação final_**

## Grupo FarmTech Solutions

#### Integrantes do grupo

| Nome | RM | LinkedIn |
|------|-----|----------|
| Phellype Matheus Giacoia Flaibam Massarente | RM566826 | [LinkedIn](https://www.linkedin.com/in/phellype-massarente-13739810a/) |
| Carlos Alberto Florindo Costato | RM567005 | [LinkedIn](https://www.linkedin.com/in/carlos-costato/) |
| Cesar Martinho de Azeredo | RM568140 | [LinkedIn](https://www.linkedin.com/in/cesar-azeredo) |

**Tutor:** Andre Godoy  
**Coordenador(a):** Ana Cristina dos Santos

## Sumário

[1. Introdução](#c1)

[2. Visão Geral do Projeto](#c2)

[3. Desenvolvimento do Projeto](#c3)

[4. Resultados e Avaliações](#c4)

[5. Conclusões e Trabalhos Futuros](#c5)

[6. Referências](#c6)

[Anexos](#c7)

<br>

# <a name="c1"></a>1. Introdução

## 1.1. Escopo do Projeto

### 1.1.1. Contexto da Inteligência Artificial

*A FarmTech Solutions atua no segmento de Inteligência Artificial aplicada ao agronegócio, prestando serviços para fazendas de médio porte. O projeto faz uso de técnicas de Machine Learning supervisionado e não supervisionado para analisar dados de condições climáticas e de solo, prevendo o rendimento de safras agrícolas. A aplicação tem abrangência nacional, podendo ser adaptada a diferentes culturas e regiões do Brasil.*

### 1.1.2. Descrição da Solução Desenvolvida

*A solução consiste em um pipeline de Machine Learning que recebe dados de sensores (precipitação, umidade, temperatura) e gera previsões de rendimento de safra em toneladas por hectare. O sistema inclui:*
- *Análise exploratória dos dados agrícolas*
- *Segmentação de tendências por clusterização*
- *5 modelos preditivos de regressão para estimativa de rendimento*
- *Estimativa de custos para hospedagem em nuvem AWS*

## 1.2. Objetivos do Projeto

*Definir os objetivos:*
- *Realizar análise exploratória do dataset crop_yield.csv*
- *Identificar tendências de rendimento via clusterização (ML não supervisionado)*
- *Construir e comparar 5 modelos preditivos de regressão (ML supervisionado)*
- *Estimar custos de hospedagem na AWS (SP vs Virgínia do Norte)*

<br>

# <a name="c2"></a>2. Visão Geral do Projeto

## 2.1. Objetivos do Projeto

*O projeto pretende:*
1. *Analisar a base de dados de rendimento agrícola com variáveis climáticas*
2. *Descobrir padrões e tendências de produtividade usando clusterização*
3. *Prever rendimento de safra com 5 algoritmos distintos de regressão*
4. *Fornecer uma estimativa de custo para implantação em nuvem AWS*

## 2.2. Público-Alvo

*Produtores rurais de médio porte (~200 hectares) que produzem múltiplas culturas e desejam otimizar suas operações com auxílio de IA. Equipe técnica da FarmTech Solutions. Avaliadores e professores da FIAP.*

## 2.3. Metodologia

*O desenvolvimento seguiu as etapas clássicas de um projeto de Data Science:*

1. *Entendimento do negócio e definição do problema*
2. *Coleta e compreensão dos dados (EDA)*
3. *Preparação dos dados (limpeza, encoding, normalização)*
4. *Modelagem — Clusterização (não supervisionado) e Regressão (supervisionado)*
5. *Avaliação dos modelos com métricas quantitativas*
6. *Apresentação dos resultados e conclusões*
7. *Estimativa de infraestrutura em nuvem*

<br>

# <a name="c3"></a>3. Desenvolvimento do Projeto

## 3.1. Tecnologias Utilizadas

| Tecnologia | Uso |
|-----------|-----|
| Python 3.x | Linguagem principal |
| Jupyter Notebook | Ambiente de desenvolvimento interativo |
| pandas | Manipulação e análise de dados |
| numpy | Computação numérica |
| matplotlib / seaborn | Visualização de dados |
| scikit-learn | Modelos de ML (regressão e clusterização) |
| xgboost (opcional) | Gradient Boosting otimizado |
| AWS Calculator | Estimativa de custos em nuvem |

## 3.2. Modelagem e Algoritmos

### 3.2.1. Machine Learning Não Supervisionado (Clusterização)

*Descrever os algoritmos de clusterização utilizados (K-Means, DBSCAN, etc.), o método de escolha do número de clusters (Elbow Method, Silhouette Score) e como foram interpretados os agrupamentos para identificar tendências de rendimento e outliers.*

### 3.2.2. Machine Learning Supervisionado (Regressão)

*5 modelos preditivos foram implementados:*

| # | Algoritmo | Justificativa da Escolha |
|---|-----------|-------------------------|
| 1 | Regressão Linear | *Baseline — modelo simples para comparação* |
| 2 | Decision Tree Regressor | *Captura não-linearidades, interpretável* |
| 3 | Random Forest Regressor | *Ensemble de árvores, reduz overfitting* |
| 4 | Gradient Boosting / XGBoost | *Alta performance em dados tabulares* |
| 5 | KNN Regressor / SVR / Ridge | *Abordagem diferente para diversificar* |

*Descrever para cada modelo: hiperparâmetros utilizados, processo de tunagem e decisões tomadas.*

## 3.3. Treinamento e Teste

*Descrever:*
- *Split treino/teste utilizado (ex.: 80/20)*
- *Random state para reprodutibilidade*
- *Cross-validation (se aplicada)*
- *Estratégia de encoding das variáveis categóricas*
- *Normalização/padronização aplicada*

### Variáveis do Dataset

| Variável | Descrição | Tipo |
|----------|-----------|------|
| Cultura | Nome da safra | Categórica |
| Precipitação (mm/dia) | Quantidade de chuva em mm por dia | Numérica |
| Umidade específica 2m (g/kg) | Vapor de água no ar por kg de ar seco a 2m | Numérica |
| Umidade relativa 2m (%) | Percentual de umidade relativa a 2m | Numérica |
| Temperatura 2m (ºC) | Temperatura a 2 metros do solo | Numérica |
| Rendimento (ton/ha) | Variável-alvo — rendimento da safra | Numérica |

<br>

# <a name="c4"></a>4. Resultados e Avaliações

## 4.1. Análise dos Resultados

### 4.1.1. Resultados da Clusterização

*Descrever os clusters encontrados, as tendências identificadas e os outliers detectados. Incluir visualizações.*

### 4.1.2. Resultados dos Modelos Preditivos

*Comparação dos 5 modelos:*

| Modelo | MAE | MSE | RMSE | R² Score |
|--------|-----|-----|------|----------|
| Regressão Linear | — | — | — | — |
| Decision Tree | — | — | — | — |
| Random Forest | — | — | — | — |
| Gradient Boosting | — | — | — | — |
| KNN / SVR / Ridge | — | — | — | — |

*Análise: qual modelo performou melhor e por quê? Gráficos de valores reais vs. preditos e análise de resíduos estão detalhados no notebook Jupyter.*

## 4.2. Feedback dos Usuários

*Incluir feedback recebido de colegas, tutores ou usuários finais durante o processo de avaliação do projeto, se aplicável.*

<br>

# <a name="c5"></a>5. Conclusões e Trabalhos Futuros

*Descrever:*
- *De que formas a solução atingiu os objetivos propostos*
- *Pontos fortes do trabalho*
- *Limitações encontradas*
- *Melhorias futuras possíveis (mais dados, novos features, deploy real, etc.)*

<br>

# <a name="c6"></a>6. Referências

- FIAP. Material didático: Fases 4 e 5 — Machine Learning Supervisionado e Não Supervisionado.
- Scikit-learn Documentation. Disponível em: https://scikit-learn.org/stable/
- AWS Pricing Calculator. Disponível em: https://calculator.aws/
- BRASIL. Lei nº 13.709/2018 (LGPD). Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm

<br>

# <a name="c7"></a>Anexos

*Inclua aqui quaisquer complementos para seu projeto, como diagramas, imagens, tabelas etc.*

## Anexo A — Screenshots da Calculadora AWS

*Inserir capturas de tela da Calculadora AWS para São Paulo e Virgínia do Norte.*

## Anexo B — Arquitetura do Projeto (Ir Além)

*Se aplicável, inserir diagrama da arquitetura IoT com ESP32.*
