# 💡 Exemplos Práticos - Scripts R

**Casos de Uso Reais e Exemplos Avançados**

Esta documentação fornece exemplos práticos detalhados de como usar e estender os scripts R do FarmTech Solutions para diferentes cenários agrícolas.

## 📋 Índice
1. [Cenários Básicos](#cenários-básicos)
2. [Casos de Uso Avançados](#casos-de-uso-avançados)
3. [Integrações](#integrações)
4. [Personalizações](#personalizações)
5. [Troubleshooting com Exemplos](#troubleshooting-com-exemplos)

## 🌱 Cenários Básicos

### Cenário 1: Primeira Análise de Dados

#### Situação
Você acabou de coletar dados de 10 plantações de banana e quer entender as características básicas.

#### Dados de Exemplo (banana.csv)
```csv
comprimento,largura,nome_insumo,qtd_insumo,unidade,area,figura
120.5,80.2,"Fosfato",965.61,"kg",9656.1,"Retângulo"
95.0,60.5,"Nitrogênio",574.75,"kg",5747.5,"Retângulo"
150.3,90.7,"Potássio",1363.21,"kg",13632.1,"Retângulo"
110.0,75.0,"Herbicida",825.0,"L",8250.0,"Retângulo"
88.5,55.2,"Inseticida",488.52,"mL",4885.2,"Retângulo"
```

#### Execução
```bash
cd FarmTechSolutions/r_app
Rscript analise.R
```

#### Saída Esperada
```
--- Estatísticas Banana ---
Média comprimento: 112.86
Desvio padrão comprimento: 24.73
Média largura: 72.32
Desvio padrão largura: 14.91
Média qtd_insumo: 843.42
Desvio padrão qtd_insumo: 371.84
```

#### Interpretação
- **Comprimento médio**: 112.86m indica terrenos de tamanho médio
- **Alto desvio padrão**: Variabilidade significativa entre plantações
- **Quantidade de insumo**: Proporcional à área (boa correlação)

### Cenário 2: Monitoramento Climático Regional

#### Situação
Precisa verificar condições climáticas para decidir sobre aplicação de defensivos.

#### Execução para Banana
```bash
Rscript clima.R banana
```

#### Saída Esperada
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

#### Tomada de Decisão
- **Temperatura 23.5°C**: Ideal para aplicações
- **Vento 12.3km/h**: Moderado, adequado
- **Condição 2**: Parcialmente nublado, seguro para pulverização

## 🚀 Casos de Uso Avançados

### Caso 1: Análise Comparativa Sazonal

#### Criando Script Personalizado (analise_sazonal.R)
```r
library(readr)

# Carregar dados históricos
banana_q1 <- read_csv("../python_app/historico/banana_q1_2025.csv", show_col_types = FALSE)
banana_q2 <- read_csv("../python_app/historico/banana_q2_2025.csv", show_col_types = FALSE)

# Função para calcular estatísticas
calcular_stats <- function(dados, periodo) {
  cat(sprintf("\n--- Estatísticas %s ---\n", periodo))
  cat('Média área:', mean(dados$area), '\n')
  cat('Média insumo:', mean(dados$qtd_insumo), '\n')
  
  # Retornar para comparação
  return(list(
    area_media = mean(dados$area),
    insumo_medio = mean(dados$qtd_insumo)
  ))
}

# Análise comparativa
stats_q1 <- calcular_stats(banana_q1, "Q1 2025")
stats_q2 <- calcular_stats(banana_q2, "Q2 2025")

# Comparação
diferenca_area <- stats_q2$area_media - stats_q1$area_media
diferenca_insumo <- stats_q2$insumo_medio - stats_q1$insumo_medio

cat("\n--- Comparação Sazonal ---\n")
cat('Variação área Q1→Q2:', diferenca_area, 'm²\n')
cat('Variação insumo Q1→Q2:', diferenca_insumo, 'unidades\n')

if (diferenca_area > 0) {
  cat('📈 Expansão da área plantada\n')
} else {
  cat('📉 Redução da área plantada\n')
}
```

### Caso 2: Alerta Meteorológico Automatizado

#### Script de Monitoramento (alerta_clima.R)
```r
library(httr)

# Configuração de limites
TEMP_MAX <- 35  # °C
VENTO_MAX <- 25 # km/h
CODES_PERIGOSOS <- c(51:67, 71:86, 95:99)  # Chuva, neve, tempestade

# Função de verificação
verificar_condicoes <- function(lat, lon, nome_local) {
  url <- paste0('https://api.open-meteo.com/v1/forecast?latitude=', lat,
                '&longitude=', lon, '&current_weather=true')
  
  res <- GET(url)
  if (status_code(res) != 200) {
    cat("❌ Erro ao acessar dados para", nome_local, "\n")
    return(FALSE)
  }
  
  dados <- content(res, as='parsed')
  temp <- dados$current_weather$temperature
  vento <- dados$current_weather$windspeed
  codigo <- dados$current_weather$weathercode
  
  # Verificar alertas
  alertas <- c()
  
  if (temp > TEMP_MAX) {
    alertas <- c(alertas, paste("🌡️ Temperatura alta:", temp, "°C"))
  }
  
  if (vento > VENTO_MAX) {
    alertas <- c(alertas, paste("💨 Vento forte:", vento, "km/h"))
  }
  
  if (codigo %in% CODES_PERIGOSOS) {
    alertas <- c(alertas, paste("⛈️ Condição adversa:", codigo))
  }
  
  # Relatório
  if (length(alertas) > 0) {
    cat("🚨 ALERTAS PARA", nome_local, ":\n")
    for (alerta in alertas) {
      cat("  ", alerta, "\n")
    }
    return(TRUE)
  } else {
    cat("✅", nome_local, "- Condições normais\n")
    return(FALSE)
  }
}

# Coordenadas das fazendas
fazendas <- data.frame(
  nome = c("Fazenda Norte", "Fazenda Sul", "Fazenda Central"),
  lat = c(-23.55, -25.43, -21.78),
  lon = c(-46.63, -49.27, -43.91)
)

# Verificar todas as fazendas
cat("=== RELATÓRIO METEOROLÓGICO ===\n")
cat("Data/Hora:", format(Sys.time(), "%Y-%m-%d %H:%M"), "\n\n")

alertas_ativos <- 0
for (i in 1:nrow(fazendas)) {
  if (verificar_condicoes(fazendas$lat[i], fazendas$lon[i], fazendas$nome[i])) {
    alertas_ativos <- alertas_ativos + 1
  }
}

cat("\n📊 RESUMO:", alertas_ativos, "de", nrow(fazendas), "fazendas com alertas\n")
```

### Caso 3: Relatório Automatizado de Produtividade

#### Script de Relatório (relatorio_produtividade.R)
```r
library(readr)

# Função para calcular métricas de produtividade
calcular_produtividade <- function(cultura) {
  arquivo <- paste0("../python_app/", cultura, ".csv")
  
  if (!file.exists(arquivo)) {
    cat("❌ Arquivo não encontrado:", arquivo, "\n")
    return(NULL)
  }
  
  dados <- read_csv(arquivo, show_col_types = FALSE)
  
  # Métricas calculadas
  area_total <- sum(dados$area)
  insumo_total <- sum(dados$qtd_insumo)
  area_media <- mean(dados$area)
  eficiencia <- insumo_total / area_total  # insumo por m²
  
  # Análise por tipo de insumo
  tipos_insumo <- table(dados$nome_insumo)
  insumo_predominante <- names(tipos_insumo)[which.max(tipos_insumo)]
  
  return(list(
    cultura = cultura,
    registros = nrow(dados),
    area_total = area_total,
    area_media = area_media,
    insumo_total = insumo_total,
    eficiencia = eficiencia,
    insumo_predominante = insumo_predominante
  ))
}

# Gerar relatório completo
gerar_relatorio <- function() {
  cat("=== RELATÓRIO DE PRODUTIVIDADE FARMTECH ===\n")
  cat("Gerado em:", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n\n")
  
  culturas <- c("banana", "milho")
  
  for (cultura in culturas) {
    cat("🌱", toupper(cultura), "\n")
    cat(rep("-", 40), "\n", sep="")
    
    prod <- calcular_produtividade(cultura)
    
    if (!is.null(prod)) {
      cat(sprintf("📊 Registros: %d\n", prod$registros))
      cat(sprintf("📐 Área total: %.2f m²\n", prod$area_total))
      cat(sprintf("📏 Área média: %.2f m²\n", prod$area_media))
      cat(sprintf("🧪 Insumo total: %.2f unidades\n", prod$insumo_total))
      cat(sprintf("⚡ Eficiência: %.4f insumo/m²\n", prod$eficiencia))
      cat(sprintf("🥇 Insumo predominante: %s\n", prod$insumo_predominante))
      
      # Classificação de eficiência
      if (prod$eficiencia < 0.1) {
        cat("🟢 Eficiência: ALTA\n")
      } else if (prod$eficiencia < 0.2) {
        cat("🟡 Eficiência: MÉDIA\n")
      } else {
        cat("🔴 Eficiência: BAIXA\n")
      }
    }
    cat("\n")
  }
  
  cat("📈 Recomendações baseadas nos dados disponíveis em TECHNICAL_DOCS_R.md\n")
}

# Executar relatório
gerar_relatorio()
```

## 🔗 Integrações

### Integração 1: Python + R Pipeline

#### Script Python (executar_analise_completa.py)
```python
import subprocess
import os
import json
from datetime import datetime

def executar_pipeline_completo():
    """Pipeline completo: Python → CSV → R → Relatório"""
    
    print("🚀 Iniciando pipeline FarmTech Solutions")
    
    # 1. Gerar dados Python
    print("📊 Gerando dados com Python...")
    resultado_python = subprocess.run(
        ["python", "python_app/main.py"], 
        capture_output=True, text=True, input="5\n"  # Sair automaticamente
    )
    
    # 2. Executar análise R
    print("📈 Executando análise estatística...")
    resultado_r = subprocess.run(
        ["Rscript", "r_app/analise.R"], 
        capture_output=True, text=True, cwd="."
    )
    
    # 3. Coletar dados meteorológicos
    print("🌤️ Coletando dados meteorológicos...")
    resultado_clima = subprocess.run(
        ["Rscript", "r_app/clima.R", "banana"], 
        capture_output=True, text=True, cwd="."
    )
    
    # 4. Compilar relatório
    relatorio = {
        "timestamp": datetime.now().isoformat(),
        "analise_estatistica": resultado_r.stdout,
        "dados_clima": resultado_clima.stdout,
        "status": "completo"
    }
    
    # 5. Salvar relatório JSON
    with open("relatorio_completo.json", "w") as f:
        json.dump(relatorio, f, indent=2)
    
    print("✅ Pipeline concluído! Relatório salvo em relatorio_completo.json")
    
    return relatorio

if __name__ == "__main__":
    executar_pipeline_completo()
```

### Integração 2: Dashboard Web Simples

#### Script R para Web (dashboard_simples.R)
```r
# Instalar se necessário: install.packages("httpuv")
library(httpuv)

# Função para gerar HTML com dados
gerar_html_dashboard <- function() {
  # Executar análises
  source("analise.R")
  
  # Capturar saída (simplificado)
  banana <- read_csv("../python_app/banana.csv", show_col_types = FALSE)
  
  html <- paste0(
    "<!DOCTYPE html>",
    "<html><head><title>FarmTech Dashboard</title></head>",
    "<body style='font-family: Arial, sans-serif; margin: 40px;'>",
    "<h1>🚜 FarmTech Solutions Dashboard</h1>",
    "<h2>📊 Estatísticas Banana</h2>",
    "<ul>",
    "<li>Registros: ", nrow(banana), "</li>",
    "<li>Área média: ", round(mean(banana$area), 2), " m²</li>",
    "<li>Insumo médio: ", round(mean(banana$qtd_insumo), 2), "</li>",
    "</ul>",
    "<p><em>Atualizado em: ", Sys.time(), "</em></p>",
    "</body></html>"
  )
  
  return(html)
}

# Servidor HTTP simples
servidor <- startServer("127.0.0.1", 8080, list(
  call = function(req) {
    list(
      status = 200L,
      headers = list('Content-Type' = 'text/html'),
      body = gerar_html_dashboard()
    )
  }
))

cat("🌐 Dashboard disponível em: http://localhost:8080\n")
cat("Pressione Ctrl+C para parar\n")

# Manter servidor ativo
while (TRUE) {
  service()
  Sys.sleep(1)
}
```

## 🎨 Personalizações

### Personalização 1: Novas Culturas

#### Adicionando Cultura de Soja
```r
# Modificar clima.R - adicionar na lista de cidades
cidades_plantio <- list(
  banana = c("Registro", "Juquiá", "Sete Barras", "Miracatu", "Iguape"),
  milho = c("Sorriso", "Lucas do Rio Verde", "Primavera do Leste", "Unaí", "Rio Verde"),
  soja = c("Campo Grande", "Dourados", "Chapadão do Sul", "Maracaju", "Sidrolândia")
)

# Modificar analise.R - adicionar leitura de soja.csv
if (file.exists('../python_app/soja.csv')) {
  soja <- read_csv('../python_app/soja.csv', show_col_types = FALSE)
  
  cat('\n--- Estatísticas Soja ---\n')
  cat('Média área:', mean(soja$area), '\n')
  cat('Desvio padrão área:', sd(soja$area), '\n')
  cat('Média qtd_insumo:', mean(soja$qtd_insumo), '\n')
  cat('Desvio padrão qtd_insumo:', sd(soja$qtd_insumo), '\n')
}
```

### Personalização 2: Métricas Customizadas

#### Script de Métricas Avançadas (metricas_custom.R)
```r
library(readr)

# Função para análise de eficiência por hectare
analisar_eficiencia_hectare <- function(dados) {
  dados$area_hectare <- dados$area / 10000  # Converter m² para hectare
  dados$insumo_por_hectare <- dados$qtd_insumo / dados$area_hectare
  
  # Classificar eficiência
  dados$classe_eficiencia <- cut(
    dados$insumo_por_hectare,
    breaks = c(0, 100, 200, 300, Inf),
    labels = c("Muito Eficiente", "Eficiente", "Moderado", "Ineficiente")
  )
  
  # Estatísticas por classe
  table(dados$classe_eficiencia)
}

# Função para análise de outliers
detectar_outliers <- function(dados, coluna) {
  Q1 <- quantile(dados[[coluna]], 0.25, na.rm = TRUE)
  Q3 <- quantile(dados[[coluna]], 0.75, na.rm = TRUE)
  IQR <- Q3 - Q1
  
  limite_inferior <- Q1 - 1.5 * IQR
  limite_superior <- Q3 + 1.5 * IQR
  
  outliers <- dados[[coluna]] < limite_inferior | dados[[coluna]] > limite_superior
  
  cat("Outliers em", coluna, ":\n")
  cat("Detectados:", sum(outliers, na.rm = TRUE), "de", length(dados[[coluna]]), "\n")
  
  if (sum(outliers, na.rm = TRUE) > 0) {
    cat("Valores:", dados[[coluna]][outliers], "\n")
  }
  
  return(outliers)
}

# Executar análises customizadas
banana <- read_csv("../python_app/banana.csv", show_col_types = FALSE)

cat("=== ANÁLISE DE EFICIÊNCIA ===\n")
print(analisar_eficiencia_hectare(banana))

cat("\n=== DETECÇÃO DE OUTLIERS ===\n")
detectar_outliers(banana, "area")
detectar_outliers(banana, "qtd_insumo")
```

## 🔧 Troubleshooting com Exemplos

### Problema 1: Dados Inconsistentes

#### Situação
CSV com valores negativos ou nulos.

#### Script de Limpeza (limpar_dados.R)
```r
library(readr)

limpar_csv <- function(arquivo) {
  cat("Limpando arquivo:", arquivo, "\n")
  
  dados <- read_csv(arquivo, show_col_types = FALSE)
  dados_originais <- nrow(dados)
  
  # Remover linhas com valores negativos
  dados <- dados[dados$area > 0, ]
  dados <- dados[dados$qtd_insumo > 0, ]
  
  # Remover valores nulos
  dados <- dados[complete.cases(dados), ]
  
  dados_finais <- nrow(dados)
  removidos <- dados_originais - dados_finais
  
  cat("Registros originais:", dados_originais, "\n")
  cat("Registros limpos:", dados_finais, "\n")
  cat("Removidos:", removidos, "\n")
  
  # Salvar arquivo limpo
  arquivo_limpo <- sub("\\.csv$", "_limpo.csv", arquivo)
  write_csv(dados, arquivo_limpo)
  
  cat("Arquivo limpo salvo:", arquivo_limpo, "\n")
}

# Usar: limpar_csv("../python_app/banana.csv")
```

### Problema 2: API Indisponível

#### Script com Fallback (clima_robusto.R)
```r
library(httr)

obter_clima_com_fallback <- function(lat, lon) {
  # Tentar API principal
  url_principal <- paste0('https://api.open-meteo.com/v1/forecast?latitude=', lat,
                         '&longitude=', lon, '&current_weather=true')
  
  tryCatch({
    res <- GET(url_principal, timeout(10))
    if (status_code(res) == 200) {
      return(content(res, as='parsed'))
    }
  }, error = function(e) {
    cat("Erro na API principal:", e$message, "\n")
  })
  
  # Fallback: dados simulados baseados em médias históricas
  cat("⚠️ Usando dados de fallback (médias históricas)\n")
  
  fallback_data <- list(
    current_weather = list(
      temperature = 23.5,  # Média para São Paulo
      windspeed = 12.0,
      weathercode = 1
    )
  )
  
  return(fallback_data)
}

# Testar função
dados <- obter_clima_com_fallback(-23.55, -46.63)
cat("Temperatura:", dados$current_weather$temperature, "°C\n")
```

### Problema 3: Performance com Datasets Grandes

#### Script Otimizado (analise_otimizada.R)
```r
library(readr)

# Para datasets > 100MB
analisar_dataset_grande <- function(arquivo) {
  cat("Analisando dataset grande:", arquivo, "\n")
  
  # Ler apenas colunas necessárias
  dados <- read_csv(arquivo, 
                   col_select = c("area", "qtd_insumo", "nome_insumo"),
                   show_col_types = FALSE)
  
  # Usar funções vetorizadas
  stats <- list(
    registros = nrow(dados),
    area_total = sum(dados$area),
    area_media = mean(dados$area),
    insumo_total = sum(dados$qtd_insumo),
    insumo_medio = mean(dados$qtd_insumo)
  )
  
  # Processamento em chunks para economia de memória
  chunk_size <- 10000
  n_chunks <- ceiling(nrow(dados) / chunk_size)
  
  cat("Processando em", n_chunks, "chunks de", chunk_size, "registros\n")
  
  for (i in 1:n_chunks) {
    inicio <- (i-1) * chunk_size + 1
    fim <- min(i * chunk_size, nrow(dados))
    chunk <- dados[inicio:fim, ]
    
    # Processamento do chunk
    cat("Chunk", i, ":", fim - inicio + 1, "registros\n")
  }
  
  return(stats)
}
```

---

## 📊 Resultados Esperados por Cenário

### Análise Básica (10-50 registros)
- **Tempo de execução**: < 1 segundo
- **Estatísticas**: Médias e desvios padrão básicos
- **Uso de memória**: < 50MB

### Análise Avançada (100-1000 registros)  
- **Tempo de execução**: 1-5 segundos
- **Estatísticas**: Incluindo outliers e correlações
- **Uso de memória**: 50-200MB

### Análise de Produção (1000+ registros)
- **Tempo de execução**: 5-30 segundos
- **Estatísticas**: Análise completa com chunks
- **Uso de memória**: Otimizada para < 500MB

---

**Exemplos Práticos R v1.0.0**
*Casos reais para agricultura de precisão* 📊🌱

**Próximos passos**: Consulte [TECHNICAL_DOCS_R.md](./TECHNICAL_DOCS_R.md) para detalhes avançados
