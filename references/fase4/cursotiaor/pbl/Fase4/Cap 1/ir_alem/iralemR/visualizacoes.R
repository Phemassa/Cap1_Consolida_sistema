# ═══════════════════════════════════════════════════════════════════════════
# FarmTech Solutions - Visualizações de Dados Agrícolas (IR ALÉM 2)
# ═══════════════════════════════════════════════════════════════════════════
#
# OBJETIVO: Criar visualizações interativas para análise agrícola
#
# VISUALIZAÇÕES INCLUÍDAS:
# - Dashboard principal de irrigação
# - Análise de correlação NPK
# - Séries temporais de sensores
# - Mapas de calor sazonais
# - Gráficos de performance dos modelos
# - Relatórios de produtividade
#
# TECNOLOGIAS:
# - ggplot2 para gráficos estáticos
# - plotly para interatividade
# - corrplot para correlações
# - DT para tabelas interativas
#
# ═══════════════════════════════════════════════════════════════════════════

# Carrega bibliotecas necessárias
library(ggplot2)
library(plotly)
library(gridExtra)
library(corrplot)
library(DT)
library(dplyr)
library(tidyr)
library(lubridate)

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÕES DE TEMA E CORES
# ═══════════════════════════════════════════════════════════════════════════

# Paleta de cores FarmTech
cores_farmtech <- list(
  primary = "#2E7D32",      # Verde principal
  secondary = "#4CAF50",    # Verde secundário
  accent = "#FF9800",       # Laranja de alerta
  danger = "#F44336",       # Vermelho de perigo
  info = "#2196F3",         # Azul informativo
  warning = "#FFC107",      # Amarelo de aviso
  success = "#4CAF50",      # Verde de sucesso
  background = "#F5F5F5"    # Cinza claro de fundo
)

# Tema customizado ggplot
theme_farmtech <- theme_minimal() +
  theme(
    plot.title = element_text(size = 16, face = "bold", color = cores_farmtech$primary),
    plot.subtitle = element_text(size = 12, color = "gray60"),
    axis.title = element_text(size = 12, face = "bold"),
    axis.text = element_text(size = 10),
    legend.title = element_text(size = 12, face = "bold"),
    legend.text = element_text(size = 10),
    panel.grid.minor = element_blank(),
    plot.background = element_rect(fill = "white", color = NA),
    panel.background = element_rect(fill = "white", color = NA)
  )

# Define tema padrão
theme_set(theme_farmtech)

# ═══════════════════════════════════════════════════════════════════════════
# 1. DASHBOARD PRINCIPAL DE IRRIGAÇÃO
# ═══════════════════════════════════════════════════════════════════════════

criar_dashboard_irrigacao <- function(dados) {
  # Cria dashboard principal com métricas de irrigação
  
  cat("📊 Criando Dashboard Principal de Irrigação...\n")
  
  # 1.1 Gráfico de Status Atual dos Sensores
  dados_recentes <- tail(dados, 1)
  
  status_sensores <- data.frame(
    Sensor = c("Temperatura", "Umidade Solo", "pH", "NPK"),
    Valor = c(
      dados_recentes$temperatura,
      dados_recentes$umidade_solo,
      dados_recentes$ph_solo * 10,  # Escala pH para visualização
      mean(c(dados_recentes$nitrogenio_ok, dados_recentes$fosforo_ok, dados_recentes$potassio_ok)) * 100
    ),
    Ideal_Min = c(20, 40, 55, 70),
    Ideal_Max = c(30, 70, 75, 100),
    Unidade = c("°C", "%", "pH*10", "%"),
    Status = c(
      ifelse(dados_recentes$temperatura >= 20 & dados_recentes$temperatura <= 30, "OK", "Alerta"),
      ifelse(dados_recentes$umidade_solo >= 40 & dados_recentes$umidade_solo <= 70, "OK", "Alerta"),
      ifelse(dados_recentes$ph_solo >= 5.5 & dados_recentes$ph_solo <= 7.5, "OK", "Alerta"),
      ifelse(mean(c(dados_recentes$nitrogenio_ok, dados_recentes$fosforo_ok, dados_recentes$potassio_ok)) > 0.7, "OK", "Alerta")
    )
  )
  
  p1 <- ggplot(status_sensores, aes(x = Sensor, y = Valor, fill = Status)) +
    geom_col(alpha = 0.8) +
    geom_errorbar(aes(ymin = Ideal_Min, ymax = Ideal_Max), width = 0.2, color = "black", size = 1) +
    scale_fill_manual(values = c("OK" = cores_farmtech$success, "Alerta" = cores_farmtech$warning)) +
    labs(
      title = "🌡️ Status Atual dos Sensores",
      subtitle = paste("Última leitura:", format(dados_recentes$data, "%d/%m/%Y")),
      x = "Sensores",
      y = "Valores",
      caption = "Barras pretas indicam faixas ideais"
    ) +
    coord_flip()
  
  # 1.2 Gráfico de Histórico de Irrigação (últimos 30 dias)
  dados_30d <- dados %>%
    filter(data >= (max(data) - 30)) %>%
    mutate(
      irrigacao_num = as.numeric(irrigacao_realizada),
      dia_nome = format(data, "%d/%m")
    )
  
  p2 <- ggplot(dados_30d, aes(x = data)) +
    geom_line(aes(y = umidade_solo), color = cores_farmtech$info, size = 1, alpha = 0.7) +
    geom_point(aes(y = umidade_solo * irrigacao_num), 
               color = cores_farmtech$primary, size = 2, alpha = 0.8) +
    geom_hline(yintercept = 40, linetype = "dashed", color = cores_farmtech$danger, alpha = 0.6) +
    geom_hline(yintercept = 70, linetype = "dashed", color = cores_farmtech$success, alpha = 0.6) +
    labs(
      title = "💧 Histórico de Irrigação (30 dias)",
      subtitle = "Linha azul: Umidade do solo | Pontos verdes: Irrigação realizada",
      x = "Data",
      y = "Umidade do Solo (%)",
      caption = "Linhas tracejadas: Limites ideais de umidade"
    ) +
    scale_x_date(date_labels = "%d/%m", date_breaks = "5 days") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  # 1.3 Distribuição de Irrigações por Condição
  condicoes_irrigacao <- dados %>%
    mutate(
      condicao_clima = case_when(
        precipitacao > 10 ~ "Chuva",
        temperatura > 30 ~ "Muito Quente",
        temperatura < 18 ~ "Frio", 
        TRUE ~ "Normal"
      )
    ) %>%
    group_by(condicao_clima, irrigacao_realizada) %>%
    summarise(count = n(), .groups = "drop") %>%
    mutate(
      irrigacao_label = ifelse(irrigacao_realizada, "Irrigou", "Não Irrigou")
    )
  
  p3 <- ggplot(condicoes_irrigacao, aes(x = condicao_clima, y = count, fill = irrigacao_label)) +
    geom_col(position = "fill", alpha = 0.8) +
    scale_fill_manual(values = c("Irrigou" = cores_farmtech$primary, "Não Irrigou" = cores_farmtech$background)) +
    labs(
      title = "🌤️ Padrões de Irrigação por Condição Climática",
      x = "Condição Climática",
      y = "Proporção",
      fill = "Ação"
    ) +
    scale_y_continuous(labels = scales::percent) +
    coord_flip()
  
  # 1.4 Indicadores KPI
  kpis <- dados %>%
    summarise(
      irrigacoes_mes = sum(irrigacao_realizada[data >= (max(data) - 30)]),
      umidade_media = mean(umidade_solo),
      produtividade_media = mean(produtividade, na.rm = TRUE),
      eficiencia_npk = mean(nitrogenio_ok & fosforo_ok & potassio_ok) * 100,
      .groups = "drop"
    )
  
  # Tabela de KPIs
  kpis_table <- data.frame(
    Métrica = c("Irrigações (30 dias)", "Umidade Média", "Produtividade", "Eficiência NPK"),
    Valor = c(
      paste(kpis$irrigacoes_mes, "vezes"),
      paste(round(kpis$umidade_media, 1), "%"),
      paste(round(kpis$produtividade_media, 1), "%"),
      paste(round(kpis$eficiencia_npk, 1), "%")
    ),
    Status = c("📊", "💧", "📈", "🧪")
  )
  
  # Combina gráficos
  dashboard <- list(
    status_sensores = p1,
    historico_irrigacao = p2,
    padroes_clima = p3,
    kpis = kpis_table
  )
  
  cat("✅ Dashboard criado com sucesso!\n\n")
  
  return(dashboard)
}

# ═══════════════════════════════════════════════════════════════════════════
# 2. ANÁLISE DE CORRELAÇÃO E HEATMAPS
# ═══════════════════════════════════════════════════════════════════════════

criar_analise_correlacao <- function(dados) {
  # Cria análises de correlação entre variáveis
  
  cat("🔗 Criando Análises de Correlação...\n")
  
  # 2.1 Matriz de correlação das variáveis principais
  vars_numericas <- dados %>%
    select(temperatura, umidade_solo, ph_solo, precipitacao, 
           pressao_atmosferica, umidade_ar, vento_kmh, produtividade) %>%
    na.omit()
  
  cor_matrix <- cor(vars_numericas)
  
  # 2.2 Heatmap de correlação
  p1 <- corrplot(cor_matrix, 
                 method = "color",
                 type = "upper", 
                 order = "hclust",
                 title = "Matriz de Correlação - Variáveis Ambientais",
                 mar = c(0,0,2,0),
                 tl.cex = 0.8,
                 tl.col = "black")
  
  # 2.3 Correlação NPK vs Produtividade
  npk_prod <- dados %>%
    mutate(
      npk_adequado = nitrogenio_ok & fosforo_ok & potassio_ok,
      npk_score = (as.numeric(nitrogenio_ok) + as.numeric(fosforo_ok) + as.numeric(potassio_ok)) / 3
    ) %>%
    group_by(npk_adequado) %>%
    summarise(
      prod_media = mean(produtividade, na.rm = TRUE),
      prod_sd = sd(produtividade, na.rm = TRUE),
      count = n(),
      .groups = "drop"
    ) %>%
    mutate(npk_label = ifelse(npk_adequado, "NPK Adequado", "NPK Deficiente"))
  
  p2 <- ggplot(npk_prod, aes(x = npk_label, y = prod_media, fill = npk_label)) +
    geom_col(alpha = 0.8) +
    geom_errorbar(aes(ymin = prod_media - prod_sd, ymax = prod_media + prod_sd), 
                  width = 0.2) +
    scale_fill_manual(values = c("NPK Adequado" = cores_farmtech$success, 
                                "NPK Deficiente" = cores_farmtech$danger)) +
    labs(
      title = "🧪 Impacto do NPK na Produtividade",
      x = "Status NPK",
      y = "Produtividade Média (%)",
      fill = "Status"
    ) +
    theme(legend.position = "none")
  
  # 2.3 Heatmap sazonal
  heatmap_sazonal <- dados %>%
    mutate(
      mes = month(data),
      semana = week(data)
    ) %>%
    group_by(mes, semana) %>%
    summarise(
      irrigacao_freq = mean(as.numeric(irrigacao_realizada)),
      temp_media = mean(temperatura),
      umidade_media = mean(umidade_solo),
      .groups = "drop"
    )
  
  p3 <- ggplot(heatmap_sazonal, aes(x = semana, y = factor(mes), fill = irrigacao_freq)) +
    geom_tile(alpha = 0.8) +
    scale_fill_gradient(low = "white", high = cores_farmtech$primary, 
                       name = "Freq.\nIrrigação") +
    labs(
      title = "🗓️ Heatmap Sazonal de Irrigação",
      x = "Semana do Ano",
      y = "Mês",
      subtitle = "Frequência de irrigação ao longo do ano"
    )
  
  correlacao_results <- list(
    matriz_correlacao = cor_matrix,
    grafico_correlacao = p1,
    npk_produtividade = p2,
    heatmap_sazonal = p3
  )
  
  cat("✅ Análises de correlação criadas!\n\n")
  
  return(correlacao_results)
}

# ═══════════════════════════════════════════════════════════════════════════
# 3. SÉRIES TEMPORAIS INTERATIVAS
# ═══════════════════════════════════════════════════════════════════════════

criar_series_temporais <- function(dados) {
  # Cria gráficos interativos de séries temporais
  
  cat("📈 Criando Séries Temporais Interativas...\n")
  
  # 3.1 Série temporal principal com múltiplas variáveis
  dados_serie <- dados %>%
    select(data, temperatura, umidade_solo, ph_solo, precipitacao) %>%
    pivot_longer(-data, names_to = "variavel", values_to = "valor") %>%
    mutate(
      variavel_label = case_when(
        variavel == "temperatura" ~ "🌡️ Temperatura (°C)",
        variavel == "umidade_solo" ~ "💧 Umidade Solo (%)",
        variavel == "ph_solo" ~ "🧪 pH do Solo",
        variavel == "precipitacao" ~ "🌧️ Precipitação (mm)"
      )
    )
  
  p1 <- ggplot(dados_serie, aes(x = data, y = valor, color = variavel_label)) +
    geom_line(alpha = 0.7, size = 0.8) +
    facet_wrap(~ variavel_label, scales = "free_y", ncol = 2) +
    labs(
      title = "📊 Séries Temporais - Monitoramento Agrícola",
      x = "Data",
      y = "Valores",
      subtitle = "Evolução temporal das principais variáveis de monitoramento"
    ) +
    theme(legend.position = "none")
  
  # Versão interativa com plotly
  p1_interactive <- ggplotly(p1, tooltip = c("x", "y"))
  
  # 3.2 Análise de tendências
  dados_tendencias <- dados %>%
    arrange(data) %>%
    mutate(
      temp_ma7 = zoo::rollmean(temperatura, k = 7, fill = NA, align = "right"),
      umidade_ma7 = zoo::rollmean(umidade_solo, k = 7, fill = NA, align = "right"),
      irrigacao_ma7 = zoo::rollmean(as.numeric(irrigacao_realizada), k = 7, fill = NA, align = "right")
    ) %>%
    filter(!is.na(temp_ma7))
  
  p2 <- ggplot(dados_tendencias, aes(x = data)) +
    geom_line(aes(y = temperatura), alpha = 0.3, color = "red") +
    geom_line(aes(y = temp_ma7), color = "red", size = 1) +
    geom_line(aes(y = umidade_solo), alpha = 0.3, color = "blue") +
    geom_line(aes(y = umidade_ma7), color = "blue", size = 1) +
    labs(
      title = "📈 Tendências com Médias Móveis (7 dias)",
      subtitle = "Linhas finas: valores diários | Linhas grossas: médias móveis",
      x = "Data",
      y = "Valores",
      caption = "Vermelho: Temperatura | Azul: Umidade do Solo"
    )
  
  p2_interactive <- ggplotly(p2, tooltip = c("x", "y"))
  
  series_results <- list(
    series_principais = p1,
    series_interativas = p1_interactive,
    tendencias = p2,
    tendencias_interativas = p2_interactive
  )
  
  cat("✅ Séries temporais criadas!\n\n")
  
  return(series_results)
}

# ═══════════════════════════════════════════════════════════════════════════
# 4. ANÁLISE DE PERFORMANCE DOS MODELOS
# ═══════════════════════════════════════════════════════════════════════════

visualizar_performance_modelos <- function(resultados_modelos) {
  # Cria visualizações da performance dos modelos preditivos
  
  cat("🎯 Criando Visualizações de Performance dos Modelos...\n")
  
  if (is.null(resultados_modelos) || is.null(resultados_modelos$comparacao)) {
    cat("❌ Resultados de modelos não disponíveis\n")
    return(NULL)
  }
  
  # 4.1 Comparação de métricas
  metricas <- resultados_modelos$comparacao$metricas
  
  metricas_long <- metricas %>%
    pivot_longer(-Modelo, names_to = "Metrica", values_to = "Valor") %>%
    filter(!is.na(Valor))
  
  p1 <- ggplot(metricas_long, aes(x = Modelo, y = Valor, fill = Modelo)) +
    geom_col(alpha = 0.8) +
    facet_wrap(~ Metrica, scales = "free_y") +
    scale_fill_manual(values = c(
      "Regressão Logística" = cores_farmtech$info,
      "Random Forest" = cores_farmtech$success,
      "SVM" = cores_farmtech$warning
    )) +
    labs(
      title = "📊 Comparação de Performance dos Modelos",
      x = "Modelos",
      y = "Valor da Métrica"
    ) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1),
          legend.position = "none")
  
  # 4.2 Feature Importance (se disponível)
  feature_plot <- NULL
  if (!is.null(resultados_modelos$random_forest) && 
      !is.null(resultados_modelos$random_forest$importance)) {
    
    importance_rf <- resultados_modelos$random_forest$importance
    
    if (!is.null(importance_rf)) {
      importance_df <- data.frame(
        Feature = rownames(importance_rf),
        MeanDecreaseGini = importance_rf[, "MeanDecreaseGini"]
      ) %>%
        arrange(desc(MeanDecreaseGini)) %>%
        head(10)
      
      feature_plot <- ggplot(importance_df, aes(x = reorder(Feature, MeanDecreaseGini), 
                                               y = MeanDecreaseGini)) +
        geom_col(fill = cores_farmtech$primary, alpha = 0.8) +
        coord_flip() +
        labs(
          title = "🌳 Feature Importance (Random Forest)",
          x = "Variáveis",
          y = "Importância (Mean Decrease Gini)",
          subtitle = "Top 10 variáveis mais importantes para predição"
        )
    }
  }
  
  performance_results <- list(
    comparacao_metricas = p1,
    feature_importance = feature_plot
  )
  
  cat("✅ Visualizações de performance criadas!\n\n")
  
  return(performance_results)
}

# ═══════════════════════════════════════════════════════════════════════════
# 5. FUNÇÃO PRINCIPAL PARA TODAS AS VISUALIZAÇÕES
# ═══════════════════════════════════════════════════════════════════════════

criar_todas_visualizacoes <- function(dados_historicos, resultados_modelos = NULL) {
  # Função principal que cria todas as visualizações
  
  cat("🎨 INICIANDO CRIAÇÃO DE TODAS AS VISUALIZAÇÕES\n")
  cat("=", rep("=", 55), "\n\n")
  
  # 1. Dashboard principal
  dashboard <- criar_dashboard_irrigacao(dados_historicos)
  
  # 2. Análises de correlação
  correlacao <- criar_analise_correlacao(dados_historicos)
  
  # 3. Séries temporais
  series <- criar_series_temporais(dados_historicos)
  
  # 4. Performance dos modelos (se disponível)
  performance <- NULL
  if (!is.null(resultados_modelos)) {
    performance <- visualizar_performance_modelos(resultados_modelos)
  }
  
  cat("🎉 TODAS AS VISUALIZAÇÕES CRIADAS COM SUCESSO!\n")
  cat("=", rep("=", 55), "\n")
  
  # Retorna todas as visualizações organizadas
  list(
    dashboard = dashboard,
    correlacao = correlacao,
    series_temporais = series,
    performance_modelos = performance,
    configuracao = list(
      cores = cores_farmtech,
      tema = "theme_farmtech"
    )
  )
}

# ═══════════════════════════════════════════════════════════════════════════
# FUNÇÕES DE EXIBIÇÃO RÁPIDA
# ═══════════════════════════════════════════════════════════════════════════

mostrar_dashboard <- function(visualizacoes) {
  # Mostra o dashboard principal
  if (!is.null(visualizacoes$dashboard)) {
    print(visualizacoes$dashboard$status_sensores)
    print(visualizacoes$dashboard$historico_irrigacao)
    print(visualizacoes$dashboard$padroes_clima)
    print(visualizacoes$dashboard$kpis)
  }
}

mostrar_correlacoes <- function(visualizacoes) {
  # Mostra as análises de correlação
  if (!is.null(visualizacoes$correlacao)) {
    print(visualizacoes$correlacao$npk_produtividade)
    print(visualizacoes$correlacao$heatmap_sazonal)
  }
}

mostrar_series <- function(visualizacoes) {
  # Mostra as séries temporais
  if (!is.null(visualizacoes$series_temporais)) {
    print(visualizacoes$series_temporais$series_principais)
    print(visualizacoes$series_temporais$tendencias)
  }
}

cat("🎨 Módulo de visualizações carregado!\n")
cat("💡 Execute: criar_todas_visualizacoes(dados_historicos)\n")
cat("📊 Funções rápidas: mostrar_dashboard(), mostrar_correlacoes(), mostrar_series()\n")