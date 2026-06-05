# Cap 7 - Decolando com ciências de dados - Atividade Avaliativa

## Sumário

- [1. Informações da Atividade](#1-informações-da-atividade)
- [2. Introdução](#2-introdução)
- [3. Contextualização: Agronegócio](#3-contextualização-agronegócio)
  - [3.1 Componentes do Agronegócio](#31-componentes-do-agronegócio)
  - [3.2 Importância do Agronegócio](#32-importância-do-agronegócio)
  - [3.3 Desafios e Tendências](#33-desafios-e-tendências)
- [4. Fontes de Dados Públicos](#4-fontes-de-dados-públicos)
- [5. Metodologia da Atividade](#5-metodologia-da-atividade)
  - [5.1 Pesquisa de Dados](#51-pesquisa-de-dados)
  - [5.2 Criação da Base de Dados](#52-criação-da-base-de-dados)
  - [5.3 Análise Estatística em R](#53-análise-estatística-em-r)
- [6. Entregáveis](#6-entregáveis)
- [7. Observações Importantes](#7-observações-importantes)

---

## 1. Informações da Atividade

**Atividade:** ANÁLISE ESTATÍSTICA DE DADOS DO AGRO  
**Período:** 18/09/2025 a 15/10/2025  
**Status:** Entrega pendente  

> **⚠️ Atenção:** Atividades entregues até 3 dias após o prazo receberão até 70% da nota. O cálculo é feito automaticamente pelo sistema, o professor não tem controle sobre o percentual da nota atribuída.

---

## 2. Introdução

A análise estatística de dados do agronegócio representa uma competência fundamental para profissionais que atuam no setor agrícola moderno. Esta atividade integra conhecimentos de ciência de dados com a realidade do agronegócio brasileiro, utilizando fontes oficiais de dados públicos.

O objetivo é desenvolver habilidades práticas em **coleta**, **tratamento** e **análise estatística** de dados reais do setor agrícola, aplicando técnicas de estatística descritiva e visualização de dados usando a linguagem R.

---

## 3. Contextualização: Agronegócio

### 3.1 Definição

O **agronegócio** é um setor econômico que engloba todas as atividades relacionadas à **produção**, **comercialização** e **distribuição** de produtos agrícolas. É uma área vital para a economia global, especialmente em países onde a agricultura desempenha um papel significativo na geração de riqueza e alimentação da população.

### 3.2 Componentes do Agronegócio

#### 3.2.1 Produção Agrícola
- **Cultivo de plantas:** Agrícolas, frutíferas, hortaliças
- **Criação de animais:** Produção de alimentos, fibras e outros produtos
- **Sistemas produtivos:** Integração de técnicas modernas e tradicionais

#### 3.2.2 Agroindústria
- **Processamento:** Transformação de produtos agrícolas
- **Industrialização:** Alimentos processados, rações, bioenergia
- **Agregação de valor:** Beneficiamento e qualificação de produtos

#### 3.2.3 Distribuição e Logística
- **Transporte:** Movimentação eficiente de produtos
- **Armazenamento:** Conservação e estocagem adequada
- **Distribuição:** Chegada aos mercados consumidores

#### 3.2.4 Comercialização
- **Mercado interno:** Vendas no território nacional
- **Mercado internacional:** Operações de importação e exportação
- **Negociação:** Formação de preços e contratos

### 3.3 Importância do Agronegócio

#### 3.3.1 Segurança Alimentar
O agronegócio é **fundamental** para garantir o abastecimento de alimentos para a população mundial, desempenhando papel crucial na **segurança alimentar global**.

#### 3.3.2 Geração de Empregos
- **Maior empregador** em muitas regiões
- **Oportunidades no campo** e na agroindústria
- **Serviços relacionados** e apoio técnico

#### 3.3.3 Contribuição Econômica
- **Contribuição significativa** para o PIB nacional
- **Motor econômico** em países agrícolas
- **Geração de divisas** via exportações

#### 3.3.4 Desenvolvimento Regional
- **Motor do desenvolvimento rural**
- **Melhoria da infraestrutura** em áreas agrícolas
- **Elevação do padrão de vida** regional

#### 3.3.5 Inovação e Tecnologia
- **Agricultura de precisão**
- **Biotecnologia** aplicada
- **Novas técnicas de manejo**
- **Eficiência e sustentabilidade**

### 3.4 Desafios e Tendências

#### 3.4.1 Sustentabilidade
- **Práticas agrícolas sustentáveis**
- **Conservação de recursos naturais**
- **Mitigação das mudanças climáticas**

#### 3.4.2 Globalização
- **Comércio internacional** crescente
- **Padrões globais** de qualidade
- **Segurança alimentar** internacional

#### 3.4.3 Digitalização
- **Tecnologias digitais** para monitoramento
- **Gestão de culturas** automatizada
- **Análise de dados** avançada
- **Transformação digital** do setor

---

## 4. Fontes de Dados Públicos

### 4.1 Fontes Oficiais Obrigatórias

Para esta atividade, você deve pesquisar dados nas seguintes fontes oficiais:

#### 4.1.1 CONAB - Companhia Nacional de Abastecimento
**Website:** https://www.conab.gov.br/
- **Especialidade:** Dados de safras, preços, estoques
- **Tipos de dados:** Produção agrícola, comercialização, armazenagem

#### 4.1.2 IBGE - Instituto Brasileiro de Geografia e Estatística
**Website:** https://www.ibge.gov.br/
- **Especialidade:** Estatísticas oficiais do Brasil
- **Tipos de dados:** Censos agropecuários, produção municipal

#### 4.1.3 MAPA - Ministério da Agricultura, Pecuária e Abastecimento
**Website:** https://www.gov.br/agricultura/pt-br
- **Especialidade:** Políticas e regulamentações do setor
- **Tipos de dados:** Registro de defensivos, sementes, fertilizantes

#### 4.1.4 EMBRAPA - Empresa Brasileira de Pesquisa Agropecuária
**Website:** https://www.embrapa.br/
- **Especialidade:** Pesquisa e desenvolvimento tecnológico
- **Tipos de dados:** Estudos técnicos, inovações, resultados de pesquisa

#### 4.1.5 INPE - Instituto Nacional de Pesquisas Espaciais
**Website:** https://www.gov.br/inpe/pt-br
- **Especialidade:** Monitoramento por satélite
- **Tipos de dados:** Imagens, desmatamento, queimadas, clima

#### 4.1.6 CNA BRASIL - Confederação da Agricultura e Pecuária do Brasil
**Website:** https://www.cnabrasil.org.br/
- **Especialidade:** Representação do setor privado
- **Tipos de dados:** Indicadores econômicos, estudos setoriais

---

## 5. Metodologia da Atividade

### 5.1 Pesquisa de Dados

#### 5.1.1 Etapa 1: Exploração das Fontes
1. **Acesse cada fonte** listada na seção 4
2. **Explore os dados disponíveis** em cada plataforma
3. **Identifique datasets** relevantes para análise
4. **Documente as fontes** utilizadas

#### 5.1.2 Critérios de Seleção
- **Relevância:** Dados relacionados ao agronegócio
- **Atualidade:** Preferencialmente dados recentes
- **Completude:** Informações suficientes para análise
- **Qualidade:** Dados confiáveis e bem estruturados

### 5.2 Criação da Base de Dados

#### 5.2.1 Especificações Técnicas

**Formato:** Arquivo Excel (.xlsx)  
**Dimensões mínimas:** 30 linhas × 4 colunas  

#### 5.2.2 Estrutura Obrigatória das Colunas

| Coluna | Tipo de Variável | Descrição | Exemplos |
|--------|------------------|-----------|----------|
| **Coluna 1** | **Quantitativa Discreta** | Números inteiros contáveis | Número de propriedades, quantidade de animais, número de funcionários |
| **Coluna 2** | **Quantitativa Contínua** | Números reais com decimais | Área plantada (ha), produção (toneladas), preço (R$/kg) |
| **Coluna 3** | **Qualitativa Nominal** | Categorias sem ordem | Região (Norte, Sul), Tipo de cultura (Soja, Milho), Estado |
| **Coluna 4** | **Qualitativa Ordinal** | Categorias com ordem | Porte da propriedade (Pequena, Média, Grande), Classificação (A, B, C) |

#### 5.2.3 Exemplo de Estrutura

```
| Nº Propriedades | Área Plantada (ha) | Região    | Porte        |
|-----------------|-------------------|-----------|--------------|
| 150             | 2,547.80          | Centro-Oeste | Grande    |
| 89              | 1,234.50          | Sul       | Média        |
| 234             | 3,891.20          | Sudeste   | Grande       |
```

### 5.3 Análise Estatística em R

#### 5.3.1 Análise de Variável Quantitativa

**Escolha UMA variável quantitativa** (discreta ou contínua) e realize:

##### A) Medidas de Tendência Central
- **Média aritmética** (`mean()`)
- **Mediana** (`median()`)
- **Moda** (função personalizada ou `Mode()`)

##### B) Medidas de Dispersão
- **Variância** (`var()`)
- **Desvio padrão** (`sd()`)
- **Amplitude** (`range()`)
- **Coeficiente de variação** (CV = σ/μ × 100)

##### C) Medidas Separatrizes
- **Quartis** (`quantile()`)
- **Percentis** (`quantile(probs = c(...))`)
- **Análise de outliers**

##### D) Análise Gráfica
- **Histograma** (`hist()`)
- **Boxplot** (`boxplot()`)
- **Gráfico de densidade** (`density()` + `plot()`)
- **Gráfico Q-Q** (`qqnorm()` + `qqline()`)

#### 5.3.2 Análise de Variável Qualitativa

**Escolha UMA variável qualitativa** (nominal ou ordinal) e realize:

##### Análise Gráfica Obrigatória
- **Gráfico de barras** (`barplot()`)
- **Gráfico de pizza** (`pie()`)
- **Análise de frequências** (`table()`)

#### 5.3.3 Estrutura do Código R

```r
# NomeCompleto_RMXXXXX_fase2_cap7
# Exemplo: JoaoSantos_RM76332_fase2_cap7

# Carregamento dos dados
dados <- read.xlsx("caminho/para/arquivo.xlsx")

# Análise Quantitativa
# [SEU CÓDIGO AQUI]

# Análise Qualitativa  
# [SEU CÓDIGO AQUI]
```

---

## 6. Entregáveis

### 6.1 Arquivo Excel
- **Nome:** `dados_agronegocio_[RMXXXXX].xlsx`
- **Conteúdo:** Base de dados com 30+ linhas e 4 colunas específicas
- **Qualidade:** Dados reais extraídos das fontes oficiais

### 6.2 Arquivo R
- **Nome:** `analise_[RMXXXXX].R`
- **Primeira linha:** Comentário com identificação completa
- **Conteúdo:** Códigos de análise estatística completa
- **Documentação:** Comentários explicativos no código

### 6.3 Estrutura de Entrega

```
📁 Atividade_Cap7_[RMXXXXX]/
├── 📊 dados_agronegocio_[RMXXXXX].xlsx
├── 📈 analise_[RMXXXXX].R
└── 📝 README.md (opcional, mas recomendado)
```

### 6.4 Formato da Identificação

**Primeira linha obrigatória do arquivo R:**
```r
# NomeCompleto_RMXXXXX_fase2_cap7
```

**Exemplo:**
```r
# JoaoSantos_RM76332_fase2_cap7
```

---

## 7. Observações Importantes

### 7.1 Diretrizes de Entrega

> **⚠️ Verificação de Upload:** Verifique se o arquivo do upload está correto. Não é possível enviar outro arquivo após fechamento da entrega na plataforma ou correção do professor.

> **⏰ Prazo Final:** Não deixe para realizar a entrega nos últimos minutos do prazo. Você pode ter algum problema e perder a entrega. As entregas são realizadas apenas pela plataforma.

> **🚫 Colaboração Externa:** Não disponibilize a resposta da sua atividade em grupos de WhatsApp, Discord, Microsoft Teams, pois pode gerar plágio e zerar a atividade para todos.

### 7.2 Revisão e Correção

> **📅 Período de Revisão:** Você tem um período máximo de **15 dias** após a publicação da nota para solicitar a revisão da correção.

### 7.3 Critérios de Qualidade

#### 7.3.1 Base de Dados Excel
- ✅ **Mínimo 30 linhas** de dados reais
- ✅ **4 colunas** com tipos corretos de variáveis
- ✅ **Dados consistentes** e sem valores faltantes críticos
- ✅ **Fonte identificada** e confiável

#### 7.3.2 Análise em R
- ✅ **Identificação completa** na primeira linha
- ✅ **Código funcional** e bem estruturado
- ✅ **Análises completas** conforme especificado
- ✅ **Comentários explicativos** adequados
- ✅ **Gráficos bem formatados** e legíveis

#### 7.3.3 Aspectos Técnicos
- ✅ **Uso correto** das funções estatísticas
- ✅ **Interpretação adequada** dos resultados
- ✅ **Visualizações informativas** e claras
- ✅ **Código reproduzível** e organizado

---

## Conclusão

Esta atividade proporciona experiência prática com **dados reais do agronegócio brasileiro**, desenvolvendo competências essenciais em:

- **Coleta de dados** de fontes oficiais
- **Estruturação de datasets** para análise
- **Aplicação de técnicas** estatísticas descritivas
- **Visualização de dados** com R
- **Interpretação de resultados** estatísticos

O domínio dessas habilidades é fundamental para profissionais que pretendem atuar na interseção entre **tecnologia** e **agronegócio**, área em crescente expansão no mercado brasileiro.

---

**Data:** 28/09/2025  
**Curso:** Tecnologia em Inteligência Artificial e Robótica  
**Disciplina:** Ciência de Dados com R  
**Instituição:** FIAP