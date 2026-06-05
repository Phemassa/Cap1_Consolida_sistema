# Cap 7 - Análise Estatística do Agronegócio Brasileiro

## 📊 Atividade: Ciência de Dados com R

**Curso:** Tecnologia em Inteligência Artificial e Robótica  
**Disciplina:** Ciência de Dados  
**Instituição:** FIAP  
**Data:** 12/10/2025  

**Grupo 19 - Integrantes:**
- **RM566826:** Phellype Matheus Giacoia Flaibam Massarente
- **RM567005:** Carlos Alberto Florindo Costato
- **RM568140:** Cesar Martinho de Azeredo

---

## 🎯 Objetivo

Realizar análise estatística descritiva completa de dados reais do agronegócio brasileiro, utilizando técnicas de estatística aplicada e visualização de dados em R.

---

## 📁 Estrutura do Projeto

```
Cap 7/
├── analise_R_grupo19.R            # Script R com análise completa (Grupo 19)
├── dados_agronegocio_grupo19.csv  # Base de dados (35 linhas)
├── README.md                      # Este arquivo
├── graficos/                      # Gráficos gerados (automático)
└── docs/                          # Documentação adicional
```

---

## 📊 Base de Dados

### Estrutura das Colunas

| Coluna | Tipo | Descrição | Exemplos |
|--------|------|-----------|----------|
| **num_propriedades** | Quantitativa Discreta | Número de propriedades agrícolas | 45, 123, 234 |
| **area_plantada_ha** | Quantitativa Contínua | Área plantada em hectares | 1234.50, 2547.80 |
| **regiao** | Qualitativa Nominal | Região geográfica do Brasil | Norte, Sul, Centro-Oeste |
| **porte_propriedade** | Qualitativa Ordinal | Classificação por tamanho | Pequena, Media, Grande |

### Dimensões
- **Linhas:** 35 registros
- **Colunas:** 4 variáveis
- **Fonte:** Dados simulados baseados em padrões CONAB/IBGE 2024

### Critérios de Classificação

**Porte da Propriedade:**
- **Pequena:** < 500 hectares
- **Média:** 500 - 2.500 hectares  
- **Grande:** > 2.500 hectares

---

## 🔬 Análises Realizadas

### 1. Variável Quantitativa Contínua: Área Plantada (ha)

#### Medidas de Tendência Central
- ✅ **Média aritmética** - Valor médio das áreas
- ✅ **Mediana** - Valor central (50º percentil)
- ✅ **Moda** - Valor mais frequente

#### Medidas de Dispersão
- ✅ **Variância** - Variabilidade dos dados
- ✅ **Desvio padrão** - Dispersão em relação à média
- ✅ **Amplitude** - Diferença entre máximo e mínimo
- ✅ **Coeficiente de Variação (CV)** - Dispersão relativa (%)

#### Medidas Separatrizes
- ✅ **Quartis** (Q1, Q2, Q3) - Divisão em 4 partes
- ✅ **Decis** - Divisão em 10 partes (percentis)
- ✅ **Amplitude Interquartil (IQR)** - Q3 - Q1
- ✅ **Análise de Outliers** - Método IQR

#### Gráficos Gerados
- 📊 **Histograma** - Distribuição de frequências
- 📦 **Boxplot** - Medidas resumidas e outliers
- 📈 **Curva de Densidade** - Distribuição contínua
- 📉 **Q-Q Plot** - Teste visual de normalidade

### 2. Variável Qualitativa Nominal: Região

#### Análises
- ✅ **Tabela de frequências** (absoluta, relativa, percentual)
- ✅ **Região predominante** e menos frequente
- ✅ **Distribuição percentual**

#### Gráficos
- 📊 **Gráfico de Barras** - Comparação entre regiões
- 🥧 **Gráfico de Pizza** - Proporções relativas

### 3. Variável Qualitativa Ordinal: Porte da Propriedade

#### Análises
- ✅ **Tabela de frequências ordenada**
- ✅ **Análise cruzada** - Área média por porte
- ✅ **Distribuição por categoria**

#### Gráfico
- 📊 **Gráfico de Barras** - Frequência por porte

### 4. Variável Quantitativa Discreta: Número de Propriedades

#### Análises
- ✅ **Medidas de tendência central**
- ✅ **Medidas de dispersão**
- ✅ **Amplitude e valores extremos**

#### Gráfico
- 📊 **Histograma** - Distribuição de frequências

---

## 🚀 Como Executar

### Pré-requisitos

1. **R instalado** (versão 4.0+)
   - Download: https://cran.r-project.org/

2. **RStudio (opcional, mas recomendado)**
   - Download: https://posit.co/download/rstudio-desktop/

### Execução no RStudio

1. **Abrir o projeto:**
   ```r
   setwd("C:/Fiap Projeto/Fase2/cursotiaor/pbl/Fase2/Cap 7")
   ```

2. **Abrir o script:**
   - File → Open File → `analise_R_grupo19.R`

3. **Executar o script completo:**
   - Pressione `Ctrl + Shift + Enter` (Windows/Linux)
   - Ou `Cmd + Shift + Enter` (Mac)
   - Ou clique em "Source" no painel superior

### Execução via Terminal R

```bash
cd "C:\Fiap Projeto\Fase2\cursotiaor\pbl\Fase2\Cap 7"
Rscript analise_R_grupo19.R
```

### Execução Passo a Passo

Para executar linha por linha no RStudio:
- Posicione o cursor na linha desejada
- Pressione `Ctrl + Enter` (Windows/Linux) ou `Cmd + Enter` (Mac)

---

## 📈 Resultados Esperados

### Console (Output)

O script exibirá no console:

1. **Estrutura dos dados** - Tipos e dimensões
2. **Resumo estatístico geral** - summary()
3. **Análise quantitativa detalhada** - Todas as medidas
4. **Tabelas de frequências** - Variáveis qualitativas
5. **Análise de outliers** - Valores extremos identificados
6. **Relatório final** - Conclusões e recomendações

### Gráficos (Plots)

O script gerará automaticamente:

- ✅ 4 gráficos para variável quantitativa contínua
- ✅ 2 gráficos para variável qualitativa nominal
- ✅ 1 gráfico para variável qualitativa ordinal
- ✅ 1 gráfico para variável quantitativa discreta

**Total:** 8 visualizações estatísticas

---

## 📊 Interpretação dos Resultados

### Coeficiente de Variação (CV)

| CV | Interpretação |
|----|---------------|
| **< 15%** | Baixa dispersão - Dados homogêneos |
| **15-30%** | Média dispersão - Dados moderadamente heterogêneos |
| **> 30%** | Alta dispersão - Dados heterogêneos |

### Outliers (Método IQR)

- **Limite Inferior:** Q1 - 1.5 × IQR
- **Limite Superior:** Q3 + 1.5 × IQR
- **Outliers:** Valores fora desses limites

### Q-Q Plot

- **Pontos alinhados à reta:** Dados seguem distribuição normal
- **Pontos afastados da reta:** Desvio da normalidade

---

## 🔍 Fontes de Dados

### Dados Utilizados

Esta análise baseia-se em dados simulados seguindo padrões reais de:

1. **CONAB** - Companhia Nacional de Abastecimento
   - Website: https://www.conab.gov.br/
   - Dados: Safras, produção agrícola

2. **IBGE** - Instituto Brasileiro de Geografia e Estatística
   - Website: https://www.ibge.gov.br/
   - Dados: Censo agropecuário, produção municipal

3. **EMBRAPA** - Empresa Brasileira de Pesquisa Agropecuária
   - Website: https://www.embrapa.br/
   - Dados: Requisitos nutricionais (NPK) por cultura

### Padrões de Referência

Os valores simulados refletem:
- Distribuição regional de produção de **Banana** e **Milho**
- Classificação de propriedades segundo critérios do INCRA
- Área plantada conforme médias nacionais 2024

---

## 🎓 Requisitos Atendidos - Cap 7 FIAP

### ✅ Base de Dados
- [x] Mínimo 30 linhas (✅ 35 linhas)
- [x] 4 colunas com tipos específicos:
  - [x] Quantitativa Discreta (num_propriedades)
  - [x] Quantitativa Contínua (area_plantada_ha)
  - [x] Qualitativa Nominal (regiao)
  - [x] Qualitativa Ordinal (porte_propriedade)

### ✅ Análise Quantitativa
- [x] Medidas de Tendência Central (média, mediana, moda)
- [x] Medidas de Dispersão (variância, desvio padrão, amplitude, CV)
- [x] Medidas Separatrizes (quartis, percentis)
- [x] Análise de Outliers (método IQR)
- [x] 4 Gráficos (histograma, boxplot, densidade, Q-Q plot)

### ✅ Análise Qualitativa
- [x] Tabela de frequências (absoluta, relativa, percentual)
- [x] Gráfico de Barras
- [x] Gráfico de Pizza

### ✅ Identificação
- [x] Primeira linha com identificação completa
- [x] Formato: `NomeCompleto_RMXXXXX_fase2_cap7`

---

## 🔧 Personalização

### Alterar para seus dados

1. **Identificação do Grupo:**
   - ✅ Arquivos já nomeados como `grupo19` (RM566826, RM567005, RM568140)
   - ✅ Cabeçalho do script R contém os 3 integrantes do Grupo 19

2. **Usar seus próprios dados:**
   - Substituir `dados_agronegocio_grupo19.csv`
   - Manter estrutura de 4 colunas com mesmos tipos
   - Ajustar nomes das colunas no script se necessário

3. **Adicionar análises:**
   - Testes de normalidade (Shapiro-Wilk)
   - Análise de correlação entre variáveis
   - Gráficos adicionais (scatter plots, etc.)

---

## 📚 Conceitos Estatísticos

### Medidas de Tendência Central
- **Média (μ):** Soma dos valores / Número de observações
- **Mediana:** Valor central quando dados ordenados
- **Moda:** Valor mais frequente

### Medidas de Dispersão
- **Variância (σ²):** Média dos quadrados dos desvios
- **Desvio Padrão (σ):** Raiz quadrada da variância
- **Amplitude:** Diferença entre máximo e mínimo
- **CV (%):** (σ / μ) × 100 - Dispersão relativa

### Quartis
- **Q1 (25%):** 25% dos dados abaixo deste valor
- **Q2 (50%):** Mediana - 50% dos dados abaixo e 50% acima
- **Q3 (75%):** 75% dos dados abaixo deste valor

---

## 🐛 Solução de Problemas

### Erro: "cannot open file 'dados_agronegocio_grupo19.csv'"

**Solução:**
```r
# Verificar diretório atual
getwd()

# Definir diretório correto
setwd("C:/Fiap Projeto/Fase2/cursotiaor/pbl/Fase2/Cap 7")
```

### Erro: "object 'dados' not found"

**Solução:** Execute a seção de carregamento de dados primeiro (linhas 1-20)

### Gráficos não aparecem

**Solução:**
- RStudio: Aba "Plots" no painel inferior direito
- R Console: Gráficos abrem em janela separada

---

## 📝 Referências

### Livros
- **BUSSAB, W. O.; MORETTIN, P. A.** Estatística Básica. 9ª ed. Saraiva, 2017.
- **MONTGOMERY, D. C.; RUNGER, G. C.** Applied Statistics and Probability for Engineers. Wiley, 2018.

### Online
- **R Documentation:** https://www.rdocumentation.org/
- **Quick-R:** https://www.statmethods.net/
- **R Graph Gallery:** https://r-graph-gallery.com/

### Fontes de Dados Oficiais
- **CONAB:** https://www.conab.gov.br/
- **IBGE:** https://www.ibge.gov.br/
- **EMBRAPA:** https://www.embrapa.br/
- **MAPA:** https://www.gov.br/agricultura/pt-br

---

## 📧 Contato

**Projeto:** FarmTech Solutions - Sistema de Irrigação Inteligente  
**Grupo:** 59  
**Instituição:** FIAP  
**Curso:** Tecnologia em Inteligência Artificial e Robótica

---

**Data de Atualização:** 12/10/2025  
**Versão:** 1.0  
**Status:** ✅ Completo e funcional
