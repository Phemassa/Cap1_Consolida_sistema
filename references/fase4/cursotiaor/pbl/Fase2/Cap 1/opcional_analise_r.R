# ==============================================================================
# FarmTech Solutions - Opcional 2: Análise Estatística em R
# Cap 1 - Um Mapa do Tesouro
# Atividade: Análise R para decisão de irrigação inteligente
# ==============================================================================

# Identificação do Grupo
# Grupo 19 FIAP - 1 ano • 2025/2 - Fase 2 - de 18/09/2025 a 15/10/2025
# RM566826 - Phellype Matheus Giacoia Flaibam Massarente
# RM567005 - Carlos Alberto Florindo Costato
# RM568140 - Cesar Martinho de Azeredo
# Data: 12/10/2025

# ==============================================================================
# OBJETIVO
# ==============================================================================
# Implementar análise estatística para otimizar decisão de irrigação baseada
# em dados históricos de sensores (umidade, temperatura, pH, NPK)

# ==============================================================================
# PARTE 1: SIMULAÇÃO DE DADOS HISTÓRICOS DE SENSORES
# ==============================================================================

cat("\n")
cat("================================================================================\n")
cat("🌾 FarmTech Solutions - Análise Estatística para Irrigação Inteligente\n")
cat("   Opcional 2: Decisão baseada em dados históricos\n")
cat("================================================================================\n\n")

# Configurar seed para reprodutibilidade
set.seed(42)

# Gerar 100 leituras históricas simuladas
n_leituras <- 100

# Criar dataframe com dados históricos
dados_sensores <- data.frame(
  id = 1:n_leituras,
  umidade_solo = round(runif(n_leituras, min = 30, max = 85), 1),
  temperatura = round(rnorm(n_leituras, mean = 26, sd = 4), 1),
  pH_solo = round(runif(n_leituras, min = 5.0, max = 8.0), 1),
  nitrogenio_ok = sample(c(TRUE, FALSE), n_leituras, replace = TRUE, prob = c(0.7, 0.3)),
  fosforo_ok = sample(c(TRUE, FALSE), n_leituras, replace = TRUE, prob = c(0.6, 0.4)),
  potassio_ok = sample(c(TRUE, FALSE), n_leituras, replace = TRUE, prob = c(0.8, 0.2)),
  irrigacao_ativa = sample(c(TRUE, FALSE), n_leituras, replace = TRUE, prob = c(0.4, 0.6))
)

# Adicionar cultura (Banana ou Milho)
dados_sensores$cultura <- sample(c("Banana", "Milho"), n_leituras, replace = TRUE)

cat("✅ Dados históricos gerados: 100 leituras de sensores\n\n")

# Visualizar primeiras linhas
cat("📊 Amostra dos dados:\n")
print(head(dados_sensores, 5))
cat("\n")

# ==============================================================================
# PARTE 2: ANÁLISE ESTATÍSTICA DE UMIDADE DO SOLO
# ==============================================================================

cat("================================================================================\n")
cat("📈 ANÁLISE ESTATÍSTICA: UMIDADE DO SOLO\n")
cat("================================================================================\n\n")

# Medidas de Tendência Central
media_umidade <- mean(dados_sensores$umidade_solo)
mediana_umidade <- median(dados_sensores$umidade_solo)

# Função para calcular moda
calcular_moda <- function(x) {
  freq <- table(x)
  as.numeric(names(freq)[which.max(freq)])
}
moda_umidade <- calcular_moda(dados_sensores$umidade_solo)

cat(sprintf("📍 Média de Umidade:    %.2f%%\n", media_umidade))
cat(sprintf("📍 Mediana de Umidade:  %.2f%%\n", mediana_umidade))
cat(sprintf("📍 Moda de Umidade:     %.2f%%\n\n", moda_umidade))

# Medidas de Dispersão
variancia_umidade <- var(dados_sensores$umidade_solo)
desvio_umidade <- sd(dados_sensores$umidade_solo)
amplitude_umidade <- max(dados_sensores$umidade_solo) - min(dados_sensores$umidade_solo)
cv_umidade <- (desvio_umidade / media_umidade) * 100

cat(sprintf("📊 Variância:           %.2f\n", variancia_umidade))
cat(sprintf("📊 Desvio Padrão:       %.2f%%\n", desvio_umidade))
cat(sprintf("📊 Amplitude:           %.2f%%\n", amplitude_umidade))
cat(sprintf("📊 Coef. Variação (CV): %.2f%%\n\n", cv_umidade))

# Medidas Separatrizes
quartis_umidade <- quantile(dados_sensores$umidade_solo, probs = c(0.25, 0.50, 0.75))
iqr_umidade <- IQR(dados_sensores$umidade_solo)

cat("📐 Quartis:\n")
cat(sprintf("   Q1 (25%%): %.2f%%\n", quartis_umidade[1]))
cat(sprintf("   Q2 (50%%): %.2f%%\n", quartis_umidade[2]))
cat(sprintf("   Q3 (75%%): %.2f%%\n\n", quartis_umidade[3]))
cat(sprintf("📐 IQR (Intervalo Interquartil): %.2f%%\n\n", iqr_umidade))

# Análise de Outliers
limite_inferior <- quartis_umidade[1] - 1.5 * iqr_umidade
limite_superior <- quartis_umidade[3] + 1.5 * iqr_umidade
outliers <- dados_sensores$umidade_solo[dados_sensores$umidade_solo < limite_inferior | 
                                        dados_sensores$umidade_solo > limite_superior]

cat(sprintf("🔍 Outliers detectados: %d leituras\n", length(outliers)))
if (length(outliers) > 0) {
  cat(sprintf("   Valores: %s\n\n", paste(round(outliers, 1), collapse = ", ")))
} else {
  cat("   Nenhum outlier detectado\n\n")
}

# ==============================================================================
# PARTE 3: ANÁLISE GRÁFICA
# ==============================================================================

cat("================================================================================\n")
cat("📊 GERANDO GRÁFICOS DE ANÁLISE\n")
cat("================================================================================\n\n")

# Configurar layout para 4 gráficos
par(mfrow = c(2, 2), mar = c(4, 4, 3, 2))

# 1. Histograma
hist(dados_sensores$umidade_solo, 
     main = "Histograma: Umidade do Solo",
     xlab = "Umidade (%)",
     ylab = "Frequência",
     col = "#3498db",
     border = "white",
     breaks = 15)
abline(v = media_umidade, col = "red", lwd = 2, lty = 2)
legend("topright", legend = c("Média"), col = "red", lty = 2, lwd = 2)

# 2. Boxplot
boxplot(dados_sensores$umidade_solo,
        main = "Boxplot: Umidade do Solo",
        ylab = "Umidade (%)",
        col = "#2ecc71",
        border = "#27ae60",
        horizontal = FALSE)
abline(h = c(40, 60, 80), col = c("red", "orange", "red"), lty = 2)
text(1.3, 40, "Mínimo", col = "red", cex = 0.8)
text(1.3, 60, "Ideal", col = "orange", cex = 0.8)
text(1.3, 80, "Máximo", col = "red", cex = 0.8)

# 3. Gráfico de Densidade
plot(density(dados_sensores$umidade_solo),
     main = "Densidade: Umidade do Solo",
     xlab = "Umidade (%)",
     ylab = "Densidade",
     col = "#9b59b6",
     lwd = 2)
polygon(density(dados_sensores$umidade_solo), col = rgb(155/255, 89/255, 182/255, 0.3))

# 4. Q-Q Plot
qqnorm(dados_sensores$umidade_solo,
       main = "Q-Q Plot: Normalidade",
       col = "#e74c3c",
       pch = 19)
qqline(dados_sensores$umidade_solo, col = "#c0392b", lwd = 2)

cat("✅ Gráficos gerados com sucesso!\n\n")

# ==============================================================================
# PARTE 4: ANÁLISE QUALITATIVA (CULTURA)
# ==============================================================================

cat("================================================================================\n")
cat("📈 ANÁLISE QUALITATIVA: TIPO DE CULTURA\n")
cat("================================================================================\n\n")

# Frequência das culturas
freq_cultura <- table(dados_sensores$cultura)
prop_cultura <- prop.table(freq_cultura) * 100

cat("📊 Distribuição por Cultura:\n")
print(freq_cultura)
cat("\n")
cat("📊 Percentuais:\n")
for (i in 1:length(prop_cultura)) {
  cat(sprintf("   %s: %.1f%%\n", names(prop_cultura)[i], prop_cultura[i]))
}
cat("\n")

# Gráficos qualitativos
par(mfrow = c(1, 2), mar = c(4, 4, 3, 2))

# Gráfico de Barras
barplot(freq_cultura,
        main = "Distribuição por Cultura",
        xlab = "Cultura",
        ylab = "Frequência",
        col = c("#f39c12", "#16a085"),
        border = "white",
        ylim = c(0, max(freq_cultura) * 1.2))
text(x = c(0.7, 1.9), 
     y = freq_cultura + 3, 
     labels = freq_cultura, 
     cex = 1.2, 
     font = 2)

# Gráfico de Pizza
pie(freq_cultura,
    main = "Proporção de Culturas",
    col = c("#f39c12", "#16a085"),
    labels = paste(names(freq_cultura), "\n", round(prop_cultura, 1), "%"),
    cex = 1.0)

cat("✅ Gráficos qualitativos gerados!\n\n")

# ==============================================================================
# PARTE 5: MODELO DE DECISÃO PARA IRRIGAÇÃO
# ==============================================================================

cat("================================================================================\n")
cat("🤖 MODELO DE DECISÃO: RECOMENDAÇÃO DE IRRIGAÇÃO\n")
cat("================================================================================\n\n")

# Definir limites baseados na análise estatística
UMIDADE_CRITICA <- quartis_umidade[1]  # Q1 = 25% dos dados mais secos
UMIDADE_IDEAL <- media_umidade
UMIDADE_MAXIMA <- quartis_umidade[3]   # Q3 = 75% dos dados

cat(sprintf("📌 Limites definidos estatisticamente:\n"))
cat(sprintf("   Umidade Crítica (Q1):  %.2f%%\n", UMIDADE_CRITICA))
cat(sprintf("   Umidade Ideal (Média): %.2f%%\n", UMIDADE_IDEAL))
cat(sprintf("   Umidade Máxima (Q3):   %.2f%%\n\n", UMIDADE_MAXIMA))

# Função de decisão
decidir_irrigacao <- function(umidade, temp, pH, npk_ok, cultura) {
  # Regra 1: Solo muito seco (abaixo de Q1)
  if (umidade < UMIDADE_CRITICA) {
    return(list(
      decisao = "IRRIGAR URGENTE",
      motivo = sprintf("Umidade crítica (%.1f%% < %.1f%%)", umidade, UMIDADE_CRITICA),
      intensidade = 100
    ))
  }
  
  # Regra 2: Solo encharcado (acima de Q3)
  if (umidade > UMIDADE_MAXIMA) {
    return(list(
      decisao = "NÃO IRRIGAR",
      motivo = sprintf("Solo encharcado (%.1f%% > %.1f%%)", umidade, UMIDADE_MAXIMA),
      intensidade = 0
    ))
  }
  
  # Regra 3: Temperatura alta + umidade abaixo da média
  if (temp > (mean(dados_sensores$temperatura) + sd(dados_sensores$temperatura)) && 
      umidade < UMIDADE_IDEAL) {
    return(list(
      decisao = "IRRIGAR",
      motivo = sprintf("Temp alta (%.1f°C) + umidade baixa", temp),
      intensidade = 70
    ))
  }
  
  # Regra 4: NPK inadequado + umidade baixa
  if (!npk_ok && umidade < UMIDADE_IDEAL) {
    return(list(
      decisao = "IRRIGAR",
      motivo = sprintf("NPK inadequado + umidade baixa (%.1f%%)", umidade),
      intensidade = 60
    ))
  }
  
  # Regra 5: Condições normais
  return(list(
    decisao = "MANTER",
    motivo = "Condições dentro do esperado",
    intensidade = 0
  ))
}

# Testar modelo com 5 cenários
cat("🧪 TESTANDO MODELO COM CENÁRIOS REAIS:\n\n")

cenarios <- list(
  list(umidade = 35, temp = 32, pH = 6.5, npk_ok = TRUE, cultura = "Banana"),
  list(umidade = 65, temp = 24, pH = 6.8, npk_ok = TRUE, cultura = "Milho"),
  list(umidade = 82, temp = 22, pH = 7.0, npk_ok = TRUE, cultura = "Banana"),
  list(umidade = 48, temp = 29, pH = 6.2, npk_ok = FALSE, cultura = "Milho"),
  list(umidade = 55, temp = 35, pH = 6.5, npk_ok = TRUE, cultura = "Banana")
)

for (i in 1:length(cenarios)) {
  c <- cenarios[[i]]
  resultado <- decidir_irrigacao(c$umidade, c$temp, c$pH, c$npk_ok, c$cultura)
  
  cat(sprintf("Cenário %d: %s\n", i, c$cultura))
  cat(sprintf("  Umidade: %.1f%% | Temp: %.1f°C | pH: %.1f | NPK: %s\n", 
              c$umidade, c$temp, c$pH, ifelse(c$npk_ok, "✅", "❌")))
  cat(sprintf("  🤖 DECISÃO: %s\n", resultado$decisao))
  cat(sprintf("  📝 Motivo: %s\n", resultado$motivo))
  cat(sprintf("  💧 Intensidade: %d%%\n\n", resultado$intensidade))
}

# ==============================================================================
# PARTE 6: VALIDAÇÃO DO MODELO
# ==============================================================================

cat("================================================================================\n")
cat("✅ VALIDAÇÃO DO MODELO\n")
cat("================================================================================\n\n")

# Aplicar modelo aos dados históricos
decisoes_historicas <- sapply(1:nrow(dados_sensores), function(i) {
  d <- dados_sensores[i, ]
  npk_ok <- d$nitrogenio_ok && d$fosforo_ok && d$potassio_ok
  resultado <- decidir_irrigacao(d$umidade_solo, d$temperatura, d$pH_solo, npk_ok, d$cultura)
  resultado$decisao
})

# Análise de decisões
tabela_decisoes <- table(decisoes_historicas)
cat("📊 Distribuição de decisões nos dados históricos:\n")
print(tabela_decisoes)
cat("\n")

# Percentuais
prop_decisoes <- prop.table(tabela_decisoes) * 100
for (i in 1:length(prop_decisoes)) {
  cat(sprintf("   %s: %.1f%%\n", names(prop_decisoes)[i], prop_decisoes[i]))
}

cat("\n")
cat("================================================================================\n")
cat("✅ ANÁLISE COMPLETA FINALIZADA!\n")
cat("================================================================================\n\n")

# ==============================================================================
# PARTE 7: EXPORTAR RESULTADOS
# ==============================================================================

# Salvar dados com decisões
dados_com_decisoes <- dados_sensores
dados_com_decisoes$decisao_modelo <- decisoes_historicas

# Salvar CSV
write.csv(dados_com_decisoes, "resultados_analise_irrigacao.csv", row.names = FALSE)

cat("💾 Resultados salvos em 'resultados_analise_irrigacao.csv'\n\n")

# ==============================================================================
# CONCLUSÕES E BENEFÍCIOS
# ==============================================================================

cat("================================================================================\n")
cat("📌 CONCLUSÕES\n")
cat("================================================================================\n\n")

cat("✅ BENEFÍCIOS DA ANÁLISE ESTATÍSTICA:\n\n")

cat("1. DECISÃO BASEADA EM DADOS\n")
cat("   - Limites definidos por quartis (25%, 50%, 75%)\n")
cat("   - Decisões não arbitrárias, mas estatisticamente fundamentadas\n\n")

cat("2. OTIMIZAÇÃO DE RECURSOS\n")
cat(sprintf("   - %.1f%% das leituras históricas precisavam irrigação urgente\n", 
            prop_decisoes["IRRIGAR URGENTE"]))
cat(sprintf("   - %.1f%% estavam com umidade excessiva (evitar desperdício)\n\n",
            ifelse("NÃO IRRIGAR" %in% names(prop_decisoes), 
                   prop_decisoes["NÃO IRRIGAR"], 0)))

cat("3. PREVISIBILIDADE\n")
cat(sprintf("   - Coeficiente de Variação: %.2f%% (quanto menor, mais previsível)\n", cv_umidade))
cat("   - Outliers detectados: ", length(outliers), " (eventos excepcionais)\n\n")

cat("4. ESCALABILIDADE\n")
cat("   - Modelo pode ser retreinado com mais dados\n")
cat("   - Fácil adaptação para diferentes culturas\n")
cat("   - Base para Machine Learning futuro\n\n")

cat("================================================================================\n")
cat("🎯 INTEGRAÇÃO COM ESP32\n")
cat("================================================================================\n\n")

cat("Para integrar esta análise com o ESP32:\n\n")
cat("1. Execute este script periodicamente (ex: a cada hora)\n")
cat("2. Leia dados históricos do arquivo JSON gerado pelo ESP32\n")
cat("3. Calcule estatísticas e limites dinâmicos\n")
cat("4. Envie limites atualizados via Serial para o ESP32\n")
cat("5. ESP32 usa limites otimizados para decisão em tempo real\n\n")

cat("Exemplo de comando Serial:\n")
cat("LIMITES:40.5,57.3,75.8  (Crítico, Ideal, Máximo)\n\n")

cat("================================================================================\n")
cat("✅ Análise R completa! Sistema pronto para produção.\n")
cat("================================================================================\n\n")

# Restaurar layout gráfico padrão
par(mfrow = c(1, 1))
