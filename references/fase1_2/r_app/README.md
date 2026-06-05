# 📊 R Scripts - FarmTech Solutions

**Análises Estatísticas e Meteorológicas para Agricultura**

Esta pasta contém scripts R especializados para análise de dados agrícolas, processamento estatístico e coleta de informações meteorológicas.

## 📁 Estrutura dos Scripts

```
r_app/
├── 📄 analise.R              # Análise estatística dos dados CSV
├── 📄 clima.R                # Coleta de dados meteorológicos
├── 📄 requirements_r.txt     # Dependências R necessárias
└── 📄 README.md              # Este arquivo

```

## 🚀 Início Rápido

### 1. Instalação de Dependências
```r
# Execute no console R
install.packages(c("readr", "httr"), dependencies=TRUE)
```

### 2. Execução dos Scripts
```bash
# Análise estatística
Rscript analise.R

# Dados meteorológicos (cultura padrão: banana)
Rscript clima.R

# Dados meteorológicos para milho
Rscript clima.R milho
```

## 📊 Scripts Disponíveis

### 📈 `analise.R` - Análise Estatística
**Propósito**: Processa dados CSV gerados pela aplicação Python e calcula estatísticas descritivas.

**Funcionalidades**:
- ✅ Leitura automática de `banana.csv` e `milho.csv`
- ✅ Cálculo de médias e desvios padrão
- ✅ Análise percentual por tipo de figura geométrica
- ✅ Análise de distribuição por unidades de medida
- ✅ Estatísticas de área e quantidade de insumos

**Dados Analisados**:
- **Banana**: comprimento, largura, quantidade de insumo
- **Milho**: área, quantidade de insumo, distribuição geométrica, unidades

### 🌤️ `clima.R` - Dados Meteorológicos
**Propósito**: Coleta informações meteorológicas para regiões de cultivo usando API pública.

**Funcionalidades**:
- ✅ Consulta à API Open-Meteo para dados atuais
- ✅ Informações de temperatura, vento e condições climáticas
- ✅ Lista de cidades especializadas por cultura
- ✅ Suporte a argumentos de linha de comando

**Cidades Monitoradas**:
- **Banana**: Registro, Juquiá, Sete Barras, Miracatu, Iguape
- **Milho**: Sorriso, Lucas do Rio Verde, Primavera do Leste, Unaí, Rio Verde

## 📋 Dependências

### Pacotes R Necessários
```r
readr    # Leitura eficiente de arquivos CSV
httr     # Requisições HTTP para APIs
```

### APIs Externas
- **Open-Meteo**: API gratuita para dados meteorológicos
  - URL: https://open-meteo.com/
  - Sem necessidade de chave de API
  - Dados atualizados em tempo real

## 🔧 Configuração Avançada

### Personalização de Localização
```r
# Edite as coordenadas no arquivo clima.R
latitude <- -23.55    # Latitude da sua fazenda
longitude <- -46.63   # Longitude da sua fazenda
```

### Adição de Novas Cidades
```r
# Edite a lista no arquivo clima.R
cidades_plantio <- list(
  banana = c("Sua_Cidade_1", "Sua_Cidade_2"),
  milho = c("Sua_Cidade_3", "Sua_Cidade_4"),
  nova_cultura = c("Cidade_A", "Cidade_B")
)
```

## 📊 Saídas dos Scripts

### Exemplo de Saída - `analise.R`
```
--- Estatísticas Banana ---
Média comprimento: 125.5
Desvio padrão comprimento: 23.4
Média largura: 67.8
Desvio padrão largura: 15.2
Média qtd_insumo: 245.6
Desvio padrão qtd_insumo: 67.3

--- Percentual por tipo de geométrica (Milho) ---
Círculo: 33.3%
Retângulo: 45.0%
Quadrado: 21.7%

--- Estatísticas Milho ---
Média área: 1567.8
Desvio padrão área: 456.2
```

### Exemplo de Saída - `clima.R`
```
Tempo atual em São Paulo:
Temperatura: 23.5°C
Vento: 12.3km/h
Condição: 2

Cidades com plantio de banana:
- Registro
- Juquiá
- Sete Barras
- Miracatu
- Iguape
```

## 🛠️ Uso em Produção

### Automação com Cron (Linux/Mac)
```bash
# Execute análise diária às 08:00
0 8 * * * cd /caminho/para/FarmTechSolutions/r_app && Rscript analise.R

# Colete dados meteorológicos a cada 6 horas
0 */6 * * * cd /caminho/para/FarmTechSolutions/r_app && Rscript clima.R
```

### Agendamento Windows (Task Scheduler)
```batch
# Crie um arquivo .bat
cd "C:\Caminho\Para\FarmTechSolutions\r_app"
Rscript analise.R
```

## 🔍 Resolução de Problemas

### Erro: Pacote não encontrado
```r
# Instale manualmente
install.packages("nome_do_pacote", repos="https://cran.r-project.org/")
```

### Erro: Arquivo CSV não encontrado
```r
# Verifique se os dados Python foram gerados
# Execute primeiro: python ../python_app/main.py
```

### Erro: API não responde
```r
# Verifique conexão com internet
# A API Open-Meteo pode ter limitações temporárias
```

## 📈 Extensões Futuras

### Melhorias Planejadas
- [ ] **Visualizações**: Gráficos com ggplot2
- [ ] **Relatórios**: Documentos PDF automáticos
- [ ] **Previsão**: Modelos preditivos com dados históricos
- [ ] **Dashboard**: Interface web com Shiny
- [ ] **Alertas**: Notificações baseadas em condições climáticas

### Novas Análises
- [ ] **Correlação**: Relacionar clima com produtividade
- [ ] **Sazonalidade**: Análise temporal dos dados
- [ ] **Benchmarking**: Comparação entre regiões
- [ ] **Otimização**: Recomendações de insumos

## 📝 Notas Técnicas

### Performance
- Scripts otimizados para datasets de até 10.000 registros
- Uso eficiente de memória com `readr`
- Processamento vetorizado para cálculos

### Compatibilidade
- **R Version**: 3.6.0 ou superior
- **Sistemas**: Windows, Linux, macOS
- **Encoding**: UTF-8 para caracteres especiais

---

**R Scripts v1.0.0** - Análises estatísticas para agricultura inteligente 📊🌱

*Documentação técnica completa disponível em [TECHNICAL_DOCS_R.md](../documentacao/TECHNICAL_DOCS_R.md)*
