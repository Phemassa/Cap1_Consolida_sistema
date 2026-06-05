# 📊 Fontes de Dados Reais - Agronegócio Brasileiro

## 🎯 Como Obter Dados Reais

Este documento explica onde e como baixar dados reais do agronegócio brasileiro para usar na análise estatística.

---

## 1. CONAB - Companhia Nacional de Abastecimento

### 🌐 Website Principal
**URL:** https://www.conab.gov.br/

### 📊 Dados Disponíveis

#### Séries Históricas de Safras
**Link:** https://www.conab.gov.br/info-agro/safras/serie-historica-das-safras

**Dados:**
- Área plantada (mil hectares)
- Produtividade (kg/ha)
- Produção (mil toneladas)
- Por cultura e região

**Culturas principais:**
- Soja, Milho, Algodão, Arroz, Feijão
- Café, Cana-de-açúcar, Trigo
- Banana, Laranja, Uva

#### Como Baixar:
1. Acesse o link acima
2. Escolha a **cultura** (ex: Milho)
3. Clique em **"Planilha Excel"** ou **"CSV"**
4. Salve o arquivo

#### Exemplo de Estrutura:
```
UF, Região, Área (mil ha), Produção (mil t), Produtividade (kg/ha)
SP, Sudeste, 1234.5, 5678.9, 4602
PR, Sul, 2345.6, 8901.2, 3795
```

---

## 2. IBGE - Instituto Brasileiro de Geografia e Estatística

### 🌐 Website Principal
**URL:** https://www.ibge.gov.br/

### 📊 SIDRA - Sistema de Recuperação Automática

**Link:** https://sidra.ibge.gov.br/

#### Tabelas Úteis:

**Tabela 1612 - Produção Agrícola Municipal**
- **URL:** https://sidra.ibge.gov.br/tabela/1612
- **Dados:** Área plantada, quantidade produzida, valor da produção
- **Granularidade:** Por município, produto, ano

**Tabela 5457 - Censo Agropecuário 2017**
- **URL:** https://sidra.ibge.gov.br/tabela/5457
- **Dados:** Estabelecimentos agropecuários por características
- **Variáveis:** Tamanho, região, tipo de exploração

#### Como Baixar:
1. Acesse a tabela desejada
2. Escolha as **variáveis** (linhas e colunas)
3. Defina o **período** (anos)
4. Clique em **"Download"** → CSV ou Excel

---

## 3. EMBRAPA - Empresa Brasileira de Pesquisa Agropecuária

### 🌐 Website Principal
**URL:** https://www.embrapa.br/

### 📊 Dados Técnicos

#### Requisitos Nutricionais (NPK)
**Link:** https://www.embrapa.br/busca-de-solucoes-tecnologicas

**Dados disponíveis:**
- Necessidades de Nitrogênio (N), Fósforo (P), Potássio (K)
- Por cultura e região
- Recomendações técnicas

#### Como Acessar:
1. Acesse o link
2. Busque por: "nutrição" + "[nome da cultura]"
3. Baixe publicações técnicas (PDF)
4. Extraia dados das tabelas

---

## 4. MAPA - Ministério da Agricultura

### 🌐 Website Principal
**URL:** https://www.gov.br/agricultura/pt-br

### 📊 Dados Regulatórios

**Link:** https://www.gov.br/agricultura/pt-br/assuntos/politica-agricola

**Dados:**
- Registro de defensivos agrícolas
- Registro de fertilizantes
- Certificações orgânicas

---

## 5. CEPEA - Centro de Estudos Avançados em Economia Aplicada

### 🌐 Website Principal
**URL:** https://www.cepea.esalq.usp.br/br

### 📊 Indicadores de Preços

**Link:** https://www.cepea.esalq.usp.br/br/indicador

**Dados:**
- Preços agrícolas diários
- Índices econômicos do setor
- Séries históricas

**Culturas cobertas:**
- Soja, Milho, Café, Açúcar
- Boi, Leite, Suínos, Aves

---

## 📋 Exemplo Prático: Baixando Dados de Banana

### Passo 1: CONAB - Área Plantada

1. Acesse: https://www.conab.gov.br/info-agro/safras/serie-historica-das-safras
2. Procure por **"Banana"** ou **"Fruticultura"**
3. Baixe a planilha Excel/CSV
4. Extraia colunas:
   - Estado/Região
   - Área plantada (ha)
   - Produção (toneladas)

### Passo 2: IBGE - Produção Municipal

1. Acesse: https://sidra.ibge.gov.br/tabela/1613
2. Configure:
   - **Linha:** Município
   - **Coluna:** Variável (Área plantada)
   - **Produto:** Banana
   - **Período:** 2023
3. Download CSV
4. Importe no Excel

### Passo 3: Criar Base de Dados

Combine dados em uma tabela:

```csv
municipio,regiao,area_plantada_ha,producao_ton,porte
São Paulo,Sudeste,1234.5,5678.9,Grande
Curitiba,Sul,678.3,2345.6,Media
Salvador,Nordeste,234.8,890.1,Pequena
```

---

## 🔄 Convertendo Dados Reais para o Formato do Cap 7

### Estrutura Necessária

Seu CSV precisa ter **exatamente 4 colunas**:

| Coluna | Tipo | Exemplo |
|--------|------|---------|
| `num_propriedades` | Quantitativa Discreta | 145 |
| `area_plantada_ha` | Quantitativa Contínua | 2547.80 |
| `regiao` | Qualitativa Nominal | Centro-Oeste |
| `porte_propriedade` | Qualitativa Ordinal | Grande |

### Script de Conversão (R)

```r
# Ler dados originais da CONAB
dados_conab <- read.csv("dados_conab_original.csv")

# Transformar e adaptar
dados_cap7 <- data.frame(
  num_propriedades = dados_conab$num_estabelecimentos,
  area_plantada_ha = dados_conab$area_ha,
  regiao = dados_conab$regiao_geografica,
  porte_propriedade = ifelse(dados_conab$area_ha < 500, "Pequena",
                       ifelse(dados_conab$area_ha < 2500, "Media", "Grande"))
)

# Salvar no formato correto - Grupo 19
write.csv(dados_cap7, "dados_agronegocio_grupo19.csv", row.names = FALSE)
```

---

## 📊 Dados Simulados vs Dados Reais

### Dados Simulados (Fornecidos)
✅ **Vantagens:**
- Prontos para uso
- Estrutura perfeita
- Sem valores faltantes
- Atende requisitos FIAP

❌ **Desvantagens:**
- Não são reais
- Menos autênticos

### Dados Reais (CONAB/IBGE)
✅ **Vantagens:**
- Dados oficiais
- Mais autênticos
- Aprendizado real

❌ **Desvantagens:**
- Requer limpeza
- Pode ter valores faltantes
- Precisa transformação

---

## 🎯 Recomendação

**Para Cap 7 FIAP:**
1. **Use os dados simulados fornecidos** - Garante aprovação
2. **Cite fontes reais no README** - Demonstra conhecimento
3. **Opcional:** Inclua seção "Dados Reais" mostrando que pesquisou

**Para projetos futuros:**
- Use dados reais de CONAB/IBGE
- Desenvolva habilidades de coleta de dados
- Aprenda limpeza e transformação de dados

---

## 📚 Outras Fontes Úteis

### Dados Climáticos
**INMET:** https://portal.inmet.gov.br/
- Temperatura, precipitação, umidade
- Séries históricas por estação

### Dados de Solo
**EMBRAPA Solos:** https://www.embrapa.br/solos
- Mapas de solos
- Análises químicas

### Dados Econômicos
**IPEA:** http://www.ipeadata.gov.br/
- PIB Agropecuário
- Índices econômicos

---

## ✅ Checklist de Coleta de Dados

Ao buscar dados reais:

- [ ] Fonte é oficial/confiável?
- [ ] Dados têm pelo menos 30 linhas?
- [ ] Possui variável quantitativa discreta?
- [ ] Possui variável quantitativa contínua?
- [ ] Possui variável qualitativa nominal?
- [ ] Possui variável qualitativa ordinal?
- [ ] Dados estão completos (sem muitos NAs)?
- [ ] Consegue salvar em CSV/Excel?

---

## 🔗 Links Rápidos

| Fonte | URL | Tipo de Dados |
|-------|-----|---------------|
| **CONAB** | https://www.conab.gov.br/ | Safras, preços, estoques |
| **IBGE SIDRA** | https://sidra.ibge.gov.br/ | Produção municipal, censo |
| **EMBRAPA** | https://www.embrapa.br/ | Técnicos, pesquisa |
| **CEPEA** | https://www.cepea.esalq.usp.br/ | Preços, índices |
| **MAPA** | https://www.gov.br/agricultura/ | Regulatório, políticas |

---

**FarmTech Solutions - Grupo 59 FIAP**  
**Atualizado:** 12/10/2025  
**Versão:** 1.0
