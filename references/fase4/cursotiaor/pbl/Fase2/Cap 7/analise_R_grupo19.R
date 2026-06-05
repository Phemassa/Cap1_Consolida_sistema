# ============================================================================
# GRUPO 19 FIAP - 1º ano • 2025/2
# Projeto: FarmTech Solutions - Análise Estatística do Agronegócio Brasileiro
# 
# Integrantes:
#   - RM566826: Phellype Matheus Giacoia Flaibam Massarente
#   - RM567005: Carlos Alberto Florindo Costato
#   - RM568140: Cesar Martinho de Azeredo
# 
# Período: 18/09/2025 a 15/10/2025
# Data: 12/10/2025
# 
# Dados: Produção de Banana e Milho por Região (Fonte: CONAB/IBGE 2024)
# ============================================================================

# ============================================================================
# 1. CONFIGURAÇÃO INICIAL E CARREGAMENTO DE DADOS
# ============================================================================

# Limpar ambiente
rm(list = ls())

# Definir diretório de trabalho (ajuste conforme necessário)
# setwd("C:/Fiap Projeto/Fase2/cursotiaor/pbl/Fase2/Cap 7")

# Carregar dados - Grupo 19 (RM566826, RM567005, RM568140)
dados <- read.csv("dados_agronegocio_grupo19.csv", 
                  header = TRUE, 
                  sep = ",",
                  stringsAsFactors = TRUE)

# Exibir estrutura dos dados
cat("\n========== ESTRUTURA DOS DADOS ==========\n")
str(dados)

cat("\n========== PRIMEIRAS 10 LINHAS ==========\n")
print(head(dados, 10))

cat("\n========== RESUMO ESTATÍSTICO GERAL ==========\n")
summary(dados)

# ============================================================================
# 2. ANÁLISE DE VARIÁVEL QUANTITATIVA CONTÍNUA: ÁREA PLANTADA (ha)
# ============================================================================

cat("\n\n")
cat("############################################################\n")
cat("##  ANÁLISE QUANTITATIVA: ÁREA PLANTADA (HECTARES)      ##\n")
cat("############################################################\n\n")

# Extrair variável
area_plantada <- dados$area_plantada_ha

# ----------------------------------------------------------------------------
# 2.1 MEDIDAS DE TENDÊNCIA CENTRAL
# ----------------------------------------------------------------------------
cat("========== MEDIDAS DE TENDÊNCIA CENTRAL ==========\n")

# Média aritmética
media_area <- mean(area_plantada)
cat(sprintf("Média Aritmética: %.2f ha\n", media_area))

# Mediana
mediana_area <- median(area_plantada)
cat(sprintf("Mediana: %.2f ha\n", mediana_area))

# Moda (função personalizada)
calcular_moda <- function(x) {
  tabela_freq <- table(x)
  valor_moda <- as.numeric(names(tabela_freq)[which.max(tabela_freq)])
  frequencia_moda <- max(tabela_freq)
  return(list(valor = valor_moda, freq = frequencia_moda))
}

moda_area <- calcular_moda(area_plantada)
cat(sprintf("Moda: %.2f ha (frequência: %d)\n", moda_area$valor, moda_area$freq))

# ----------------------------------------------------------------------------
# 2.2 MEDIDAS DE DISPERSÃO
# ----------------------------------------------------------------------------
cat("\n========== MEDIDAS DE DISPERSÃO ==========\n")

# Variância
variancia_area <- var(area_plantada)
cat(sprintf("Variância: %.2f ha²\n", variancia_area))

# Desvio padrão
desvio_padrao_area <- sd(area_plantada)
cat(sprintf("Desvio Padrão: %.2f ha\n", desvio_padrao_area))

# Amplitude
amplitude_area <- diff(range(area_plantada))
min_area <- min(area_plantada)
max_area <- max(area_plantada)
cat(sprintf("Amplitude: %.2f ha (Min: %.2f | Max: %.2f)\n", 
            amplitude_area, min_area, max_area))

# Coeficiente de variação
cv_area <- (desvio_padrao_area / media_area) * 100
cat(sprintf("Coeficiente de Variação (CV): %.2f%%\n", cv_area))

# Interpretação do CV
cat("\nInterpretação do CV:\n")
if (cv_area < 15) {
  cat("  → Baixa dispersão (dados homogêneos)\n")
} else if (cv_area < 30) {
  cat("  → Média dispersão (dados moderadamente heterogêneos)\n")
} else {
  cat("  → Alta dispersão (dados heterogêneos)\n")
}

# ----------------------------------------------------------------------------
# 2.3 MEDIDAS SEPARATRIZES
# ----------------------------------------------------------------------------
cat("\n========== MEDIDAS SEPARATRIZES ==========\n")

# Quartis
quartis <- quantile(area_plantada, probs = c(0.25, 0.50, 0.75))
cat("Quartis:\n")
cat(sprintf("  Q1 (25%%): %.2f ha\n", quartis[1]))
cat(sprintf("  Q2 (50%% - Mediana): %.2f ha\n", quartis[2]))
cat(sprintf("  Q3 (75%%): %.2f ha\n", quartis[3]))

# Amplitude interquartil (IQR)
iqr_area <- IQR(area_plantada)
cat(sprintf("\nAmplitude Interquartil (IQR): %.2f ha\n", iqr_area))

# Percentis (decis)
percentis <- quantile(area_plantada, probs = seq(0, 1, 0.1))
cat("\nDecis (Percentis de 10% em 10%):\n")
print(round(percentis, 2))

# Análise de outliers (Método IQR)
cat("\n========== ANÁLISE DE OUTLIERS ==========\n")
limite_inferior <- quartis[1] - 1.5 * iqr_area
limite_superior <- quartis[3] + 1.5 * iqr_area
outliers <- area_plantada[area_plantada < limite_inferior | area_plantada > limite_superior]

cat(sprintf("Limite Inferior: %.2f ha\n", limite_inferior))
cat(sprintf("Limite Superior: %.2f ha\n", limite_superior))
cat(sprintf("Número de Outliers: %d\n", length(outliers)))

if (length(outliers) > 0) {
  cat("Valores outliers identificados:\n")
  print(round(sort(outliers), 2))
} else {
  cat("Nenhum outlier identificado.\n")
}

# ----------------------------------------------------------------------------
# 2.4 ANÁLISE GRÁFICA DA VARIÁVEL QUANTITATIVA
# ----------------------------------------------------------------------------
cat("\n========== GERANDO GRÁFICOS ==========\n")

# Configurar layout para 4 gráficos
par(mfrow = c(2, 2), mar = c(4, 4, 3, 2))

# GRÁFICO 1: Histograma
hist(area_plantada,
     main = "Histograma: Área Plantada",
     xlab = "Área Plantada (hectares)",
     ylab = "Frequência",
     col = "#2E7D32",
     border = "white",
     breaks = 10,
     las = 1)
abline(v = media_area, col = "red", lwd = 2, lty = 2)
abline(v = mediana_area, col = "blue", lwd = 2, lty = 2)
legend("topright", 
       legend = c("Média", "Mediana"), 
       col = c("red", "blue"), 
       lty = 2, 
       lwd = 2,
       cex = 0.8)

# GRÁFICO 2: Boxplot
boxplot(area_plantada,
        main = "Boxplot: Área Plantada",
        ylab = "Área Plantada (hectares)",
        col = "#43A047",
        border = "#1B5E20",
        outcol = "red",
        outpch = 19,
        las = 1,
        horizontal = FALSE)
abline(h = media_area, col = "red", lwd = 2, lty = 2)
text(1.3, media_area, sprintf("Média: %.1f", media_area), col = "red", cex = 0.8)

# GRÁFICO 3: Gráfico de Densidade
plot(density(area_plantada),
     main = "Curva de Densidade: Área Plantada",
     xlab = "Área Plantada (hectares)",
     ylab = "Densidade",
     col = "#2E7D32",
     lwd = 2,
     las = 1)
polygon(density(area_plantada), col = rgb(46/255, 125/255, 50/255, 0.3), border = NA)
abline(v = media_area, col = "red", lwd = 2, lty = 2)
abline(v = mediana_area, col = "blue", lwd = 2, lty = 2)
legend("topright", 
       legend = c("Média", "Mediana"), 
       col = c("red", "blue"), 
       lty = 2, 
       lwd = 2,
       cex = 0.7)

# GRÁFICO 4: Q-Q Plot (teste de normalidade visual)
qqnorm(area_plantada,
       main = "Q-Q Plot: Normalidade",
       xlab = "Quantis Teóricos",
       ylab = "Quantis Amostrais",
       col = "#2E7D32",
       pch = 19,
       las = 1)
qqline(area_plantada, col = "red", lwd = 2, lty = 2)

cat("✅ Gráficos da variável quantitativa gerados com sucesso!\n")

# ============================================================================
# 3. ANÁLISE DE VARIÁVEL QUALITATIVA NOMINAL: REGIÃO
# ============================================================================

cat("\n\n")
cat("############################################################\n")
cat("##  ANÁLISE QUALITATIVA: REGIÃO GEOGRÁFICA              ##\n")
cat("############################################################\n\n")

# Tabela de frequências
cat("========== TABELA DE FREQUÊNCIAS ==========\n")
tabela_regiao <- table(dados$regiao)
freq_absoluta <- as.vector(tabela_regiao)
freq_relativa <- prop.table(tabela_regiao)
freq_percentual <- freq_relativa * 100

df_regiao <- data.frame(
  Região = names(tabela_regiao),
  `Freq. Absoluta` = freq_absoluta,
  `Freq. Relativa` = round(freq_relativa, 4),
  `Freq. Percentual` = sprintf("%.2f%%", freq_percentual),
  check.names = FALSE
)

print(df_regiao)

# Estatísticas adicionais
cat("\n========== ESTATÍSTICAS RESUMIDAS ==========\n")
cat(sprintf("Total de observações: %d\n", sum(freq_absoluta)))
cat(sprintf("Região mais frequente: %s (%d propriedades)\n", 
            names(which.max(tabela_regiao)), max(tabela_regiao)))
cat(sprintf("Região menos frequente: %s (%d propriedades)\n", 
            names(which.min(tabela_regiao)), min(tabela_regiao)))

# ----------------------------------------------------------------------------
# 3.1 ANÁLISE GRÁFICA DA VARIÁVEL QUALITATIVA
# ----------------------------------------------------------------------------
cat("\n========== GERANDO GRÁFICOS QUALITATIVOS ==========\n")

# Configurar layout para 2 gráficos
par(mfrow = c(1, 2), mar = c(5, 4, 4, 2))

# GRÁFICO 1: Gráfico de Barras
cores_regioes <- c("#1B5E20", "#2E7D32", "#43A047", "#66BB6A", "#81C784")

barplot(tabela_regiao,
        main = "Distribuição de Propriedades por Região",
        xlab = "Região",
        ylab = "Número de Propriedades",
        col = cores_regioes,
        border = "white",
        las = 1,
        ylim = c(0, max(tabela_regiao) * 1.2))

# Adicionar valores sobre as barras
text(x = barplot(tabela_regiao, plot = FALSE),
     y = tabela_regiao + max(tabela_regiao) * 0.05,
     labels = tabela_regiao,
     cex = 1.2,
     font = 2)

# GRÁFICO 2: Gráfico de Pizza
pie(tabela_regiao,
    main = "Proporção de Propriedades por Região",
    col = cores_regioes,
    border = "white",
    labels = sprintf("%s\n(%d - %.1f%%)", 
                     names(tabela_regiao), 
                     tabela_regiao, 
                     freq_percentual),
    cex = 0.9)

cat("✅ Gráficos da variável qualitativa gerados com sucesso!\n")

# ============================================================================
# 4. ANÁLISE DE VARIÁVEL QUALITATIVA ORDINAL: PORTE DA PROPRIEDADE
# ============================================================================

cat("\n\n")
cat("############################################################\n")
cat("##  ANÁLISE QUALITATIVA ORDINAL: PORTE DA PROPRIEDADE   ##\n")
cat("############################################################\n\n")

# Ordenar níveis corretamente
dados$porte_propriedade <- factor(dados$porte_propriedade, 
                                   levels = c("Pequena", "Media", "Grande"),
                                   ordered = TRUE)

# Tabela de frequências
cat("========== TABELA DE FREQUÊNCIAS (PORTE) ==========\n")
tabela_porte <- table(dados$porte_propriedade)
freq_absoluta_porte <- as.vector(tabela_porte)
freq_relativa_porte <- prop.table(tabela_porte)
freq_percentual_porte <- freq_relativa_porte * 100

df_porte <- data.frame(
  Porte = names(tabela_porte),
  `Freq. Absoluta` = freq_absoluta_porte,
  `Freq. Relativa` = round(freq_relativa_porte, 4),
  `Freq. Percentual` = sprintf("%.2f%%", freq_percentual_porte),
  check.names = FALSE
)

print(df_porte)

# Análise cruzada: Área média por porte
cat("\n========== ANÁLISE CRUZADA: ÁREA MÉDIA POR PORTE ==========\n")
area_media_por_porte <- aggregate(area_plantada_ha ~ porte_propriedade, 
                                   data = dados, 
                                   FUN = mean)
names(area_media_por_porte) <- c("Porte", "Área Média (ha)")
area_media_por_porte$`Área Média (ha)` <- round(area_media_por_porte$`Área Média (ha)`, 2)
print(area_media_por_porte)

# Gráfico de barras para porte
par(mfrow = c(1, 1), mar = c(5, 4, 4, 2))

cores_porte <- c("#81C784", "#43A047", "#1B5E20")
barplot(tabela_porte,
        main = "Distribuição de Propriedades por Porte",
        xlab = "Porte da Propriedade",
        ylab = "Número de Propriedades",
        col = cores_porte,
        border = "white",
        las = 1,
        ylim = c(0, max(tabela_porte) * 1.2))

text(x = barplot(tabela_porte, plot = FALSE),
     y = tabela_porte + max(tabela_porte) * 0.05,
     labels = tabela_porte,
     cex = 1.2,
     font = 2)

cat("✅ Análise de variável ordinal concluída!\n")

# ============================================================================
# 5. ANÁLISE DE VARIÁVEL QUANTITATIVA DISCRETA: NÚMERO DE PROPRIEDADES
# ============================================================================

cat("\n\n")
cat("############################################################\n")
cat("##  ANÁLISE QUANTITATIVA DISCRETA: Nº PROPRIEDADES      ##\n")
cat("############################################################\n\n")

num_prop <- dados$num_propriedades

cat("========== MEDIDAS DE TENDÊNCIA CENTRAL ==========\n")
cat(sprintf("Média: %.2f propriedades\n", mean(num_prop)))
cat(sprintf("Mediana: %.0f propriedades\n", median(num_prop)))

cat("\n========== MEDIDAS DE DISPERSÃO ==========\n")
cat(sprintf("Desvio Padrão: %.2f\n", sd(num_prop)))
cat(sprintf("Amplitude: %.0f (Min: %d | Max: %d)\n", 
            diff(range(num_prop)), min(num_prop), max(num_prop)))

# Gráfico
par(mfrow = c(1, 1))
hist(num_prop,
     main = "Histograma: Número de Propriedades",
     xlab = "Número de Propriedades",
     ylab = "Frequência",
     col = "#43A047",
     border = "white",
     breaks = 15)

cat("✅ Análise de variável discreta concluída!\n")

# ============================================================================
# 6. RELATÓRIO FINAL E INTERPRETAÇÕES
# ============================================================================

cat("\n\n")
cat("############################################################\n")
cat("##  RELATÓRIO FINAL - INTERPRETAÇÕES                    ##\n")
cat("############################################################\n\n")

cat("========== CONCLUSÕES DA ANÁLISE ==========\n\n")

cat("1. ÁREA PLANTADA (Quantitativa Contínua):\n")
cat(sprintf("   • A área média plantada é de %.2f hectares\n", media_area))
cat(sprintf("   • 50%% das propriedades têm área entre %.2f e %.2f ha (IQR)\n", 
            quartis[1], quartis[3]))
cat(sprintf("   • Coeficiente de Variação de %.2f%% indica ", cv_area))
if (cv_area < 15) {
  cat("dados homogêneos\n")
} else if (cv_area < 30) {
  cat("heterogeneidade moderada\n")
} else {
  cat("alta heterogeneidade\n")
}

cat("\n2. REGIÃO GEOGRÁFICA (Qualitativa Nominal):\n")
regiao_predominante <- names(which.max(tabela_regiao))
cat(sprintf("   • Região predominante: %s (%.1f%% das propriedades)\n", 
            regiao_predominante, 
            max(freq_percentual)))
cat("   • Distribuição indica concentração no ", regiao_predominante, "\n")

cat("\n3. PORTE DA PROPRIEDADE (Qualitativa Ordinal):\n")
porte_predominante <- names(which.max(tabela_porte))
cat(sprintf("   • Porte predominante: %s (%.1f%% das propriedades)\n", 
            porte_predominante, 
            max(freq_percentual_porte)))
cat(sprintf("   • Propriedades grandes têm área média de %.2f ha\n", 
            area_media_por_porte[area_media_por_porte$Porte == "Grande", 2]))

cat("\n4. NÚMERO DE PROPRIEDADES (Quantitativa Discreta):\n")
cat(sprintf("   • Média de %.0f propriedades por registro\n", mean(num_prop)))
cat(sprintf("   • Variação entre %d e %d propriedades\n", min(num_prop), max(num_prop)))

cat("\n========== RECOMENDAÇÕES AGRONÔMICAS ==========\n")
cat("• Propriedades grandes (>2.500 ha) devem investir em agricultura de precisão\n")
cat("• Propriedades médias (1.000-2.500 ha) podem otimizar uso de insumos\n")
cat("• Propriedades pequenas (<1.000 ha) devem focar em culturas de alto valor\n")
cat("• Monitoramento de NPK crítico para regiões Sul e Centro-Oeste\n")

cat("\n\n")
cat("############################################################\n")
cat("##  ANÁLISE ESTATÍSTICA CONCLUÍDA COM SUCESSO!          ##\n")
cat("##  FarmTech Solutions - Grupo 59 FIAP                  ##\n")
cat("##  Data: 12/10/2025                                    ##\n")
cat("############################################################\n")

# Resetar configurações gráficas
par(mfrow = c(1, 1))

# Fim do script
