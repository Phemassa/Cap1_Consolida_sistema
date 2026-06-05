# ═══════════════════════════════════════════════════════════════════════════
# FarmTech Solutions - Análise Estatística de Irrigação (IR ALÉM 2)
# ═══════════════════════════════════════════════════════════════════════════
#
# OBJETIVO: Implementar análise estatística em R para decisão de irrigação
#
# FUNCIONALIDADES:
# - Análise exploratória de dados agrícolas
# - Modelos preditivos para irrigação
# - Visualizações interativas
# - Relatórios estatísticos automatizados
# - Integração com dados do ESP32
#
# AUTORES: Grupo 59 FIAP
# DATA: Outubro 2025
# ═══════════════════════════════════════════════════════════════════════════

# Carrega bibliotecas necessárias
if (!require("pacman")) install.packages("pacman")

pacman::p_load(
  # Manipulação de dados
  dplyr,
  tidyr, 
  readr,
  lubridate,
  
  # Visualizações
  ggplot2,
  plotly,
  corrplot,
  gridExtra,
  
  # Análise estatística
  broom,
  caret,
  randomForest,
  e1071,
  
  # Séries temporais
  forecast,
  tseries,
  
  # Comunicação serial (se necessário)
  serial,
  
  # Relatórios
  knitr,
  DT
)

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÕES GLOBAIS
# ═══════════════════════════════════════════════════════════════════════════

# Configurações de cultura (Banana vs Milho)
CULTURA_CONFIG <- list(
  banana = list(
    nome = "Banana",
    emoji = "🍌",
    umidade_min = 40,
    umidade_ideal = 60,
    umidade_max = 80,
    ph_min = 5.5,
    ph_max = 7.5,
    temp_otima = 27,
    npk_prioridade = c("K", "N", "P"),
    estacao_plantio = "Outubro-Março"
  ),
  milho = list(
    nome = "Milho", 
    emoji = "🌽",
    umidade_min = 35,
    umidade_ideal = 50,
    umidade_max = 70,
    ph_min = 5.5,
    ph_max = 7.5,
    temp_otima = 25,
    npk_prioridade = c("N", "P", "K"),
    estacao_plantio = "Setembro-Dezembro"
  )
)

# Configurações globais
set.seed(42)  # Para reprodutibilidade
options(digits = 3)
theme_set(theme_minimal())

# ═══════════════════════════════════════════════════════════════════════════
# FUNÇÕES DE GERAÇÃO DE DADOS SINTÉTICOS
# ═══════════════════════════════════════════════════════════════════════════

gerar_dados_historicos <- function(cultura = "banana", dias = 180) {
  # Gera dataset histórico sintético baseado em padrões reais agrícolas
  #
  # Args:
  #   cultura: 'banana' ou 'milho'
  #   dias: número de dias de histórico
  #
  # Returns:
  #   data.frame com dados históricos
  
  config <- CULTURA_CONFIG[[cultura]]
  
  # Sequência temporal
  datas <- seq.Date(
    from = Sys.Date() - dias,
    to = Sys.Date() - 1,
    by = "day"
  )
  
  n <- length(datas)
  
  # Padrões sazonais e ciclos
  tempo_normalizado <- as.numeric(datas - min(datas)) / max(as.numeric(datas - min(datas)))
  
  # Temperatura com variação sazonal
  temperatura <- config$temp_otima + 
    8 * sin(2 * pi * tempo_normalizado) +  # Variação anual
    3 * sin(2 * pi * tempo_normalizado * 365 / 7) +  # Variação semanal
    rnorm(n, 0, 2)  # Ruído aleatório
  
  # Umidade correlacionada com temperatura (inversa)
  umidade_base <- config$umidade_ideal - 0.8 * (temperatura - config$temp_otima)
  umidade_solo <- pmax(10, pmin(90, umidade_base + rnorm(n, 0, 5)))
  
  # pH com drift temporal e correlação com NPK
  ph_solo <- config$ph_min + (config$ph_max - config$ph_min) * 
    (0.5 + 0.3 * sin(2 * pi * tempo_normalizado) + rnorm(n, 0, 0.2))
  ph_solo <- pmax(4, pmin(9, ph_solo))
  
  # NPK correlacionados entre si e com pH
  npk_prob_base <- plogis((ph_solo - 6.5) * 2)  # Probabilidade baseada em pH
  
  nitrogenio_ok <- rbinom(n, 1, pmax(0.2, pmin(0.9, npk_prob_base + rnorm(n, 0, 0.1))))
  fosforo_ok <- rbinom(n, 1, pmax(0.2, pmin(0.9, npk_prob_base * 0.9 + rnorm(n, 0, 0.1))))
  potassio_ok <- rbinom(n, 1, pmax(0.2, pmin(0.9, npk_prob_base * 1.1 + rnorm(n, 0, 0.1))))
  
  # Irrigação histórica baseada em lógica realista
  irrigacao_necessaria <- ifelse(
    umidade_solo < config$umidade_min |
    (temperatura > config$temp_otima + 5 & umidade_solo < config$umidade_ideal) |
    (ph_solo < config$ph_min | ph_solo > config$ph_max) & umidade_solo < config$umidade_ideal,
    1, 0
  )
  
  # Produtividade simulada baseada em múltiplos fatores
  score_umidade <- pmax(0, 1 - abs(umidade_solo - config$umidade_ideal) / 30)
  score_temperatura <- pmax(0, 1 - abs(temperatura - config$temp_otima) / 15)
  score_ph <- pmax(0, 1 - abs(ph_solo - 6.5) / 2)
  score_npk <- (nitrogenio_ok + fosforo_ok + potassio_ok) / 3
  
  produtividade <- (score_umidade * 0.3 + score_temperatura * 0.25 + 
                   score_ph * 0.2 + score_npk * 0.25) * 100 + rnorm(n, 0, 5)
  produtividade <- pmax(20, pmin(100, produtividade))
  
  # Precipitação com padrão sazonal
  precipitacao <- pmax(0, 
    20 * sin(2 * pi * tempo_normalizado + pi/4) +  # Padrão sazonal
    rexp(n, 0.1)  # Eventos extremos de chuva
  )
  
  # Variáveis meteorológicas adicionais
  pressao_atmosferica <- 1013 + 15 * sin(2 * pi * tempo_normalizado) + rnorm(n, 0, 5)
  umidade_ar <- pmax(30, pmin(95, 65 + 20 * sin(2 * pi * tempo_normalizado) + rnorm(n, 0, 8)))
  vento <- pmax(0, rgamma(n, 2, 1))
  
  # Criação do dataset
  data.frame(
    data = datas,
    dia_ano = yday(datas),
    mes = month(datas),
    estacao = case_when(
      month(datas) %in% c(12, 1, 2) ~ "Verão",
      month(datas) %in% c(3, 4, 5) ~ "Outono", 
      month(datas) %in% c(6, 7, 8) ~ "Inverno",
      TRUE ~ "Primavera"
    ),
    temperatura = round(temperatura, 1),
    umidade_solo = round(umidade_solo, 1),
    ph_solo = round(ph_solo, 2),
    nitrogenio_ok = as.logical(nitrogenio_ok),
    fosforo_ok = as.logical(fosforo_ok),
    potassio_ok = as.logical(potassio_ok),
    irrigacao_realizada = as.logical(irrigacao_necessaria),
    precipitacao = round(precipitacao, 1),
    pressao_atmosferica = round(pressao_atmosferica, 1),
    umidade_ar = round(umidade_ar, 1),
    vento_kmh = round(vento, 1),
    produtividade = round(produtividade, 1),
    cultura = config$nome,
    stringsAsFactors = FALSE
  )
}

# ═══════════════════════════════════════════════════════════════════════════
# ANÁLISE EXPLORATÓRIA DE DADOS (EDA)
# ═══════════════════════════════════════════════════════════════════════════

analise_exploratoria <- function(dados) {
  # Realiza análise exploratória completa dos dados agrícolas
  #
  # Args:
  #   dados: data.frame com dados históricos
  #
  # Returns:
  #   list com estatísticas e gráficos
  
  cat("🔍 ANÁLISE EXPLORATÓRIA DE DADOS AGRÍCOLAS\n")
  cat("=" , rep("=", 50), "\n")
  
  # Estatísticas descritivas
  cat("\n📊 ESTATÍSTICAS DESCRITIVAS:\n")
  print(summary(dados))
  
  # Correlações entre variáveis numéricas
  vars_numericas <- dados %>% 
    select_if(is.numeric) %>%
    select(-dia_ano, -mes)
  
  cor_matrix <- cor(vars_numericas, use = "complete.obs")
  
  # Gráfico de correlação
  p_cor <- corrplot::corrplot(
    cor_matrix, 
    method = "color",
    type = "upper",
    order = "hclust",
    title = "Matriz de Correlação - Variáveis Agrícolas",
    mar = c(0,0,2,0)
  )
  
  # Distribuições das variáveis principais
  p1 <- ggplot(dados, aes(x = temperatura)) +
    geom_histogram(bins = 30, fill = "orange", alpha = 0.7) +
    geom_vline(aes(xintercept = mean(temperatura)), color = "red", linetype = "dashed") +
    labs(title = "🌡️ Distribuição da Temperatura", x = "Temperatura (°C)", y = "Frequência")
  
  p2 <- ggplot(dados, aes(x = umidade_solo)) +
    geom_histogram(bins = 30, fill = "blue", alpha = 0.7) +
    geom_vline(aes(xintercept = mean(umidade_solo)), color = "red", linetype = "dashed") +
    labs(title = "💧 Distribuição da Umidade do Solo", x = "Umidade (%)", y = "Frequência")
  
  p3 <- ggplot(dados, aes(x = ph_solo)) +
    geom_histogram(bins = 30, fill = "green", alpha = 0.7) +
    geom_vline(aes(xintercept = mean(ph_solo)), color = "red", linetype = "dashed") +
    labs(title = "🧪 Distribuição do pH do Solo", x = "pH", y = "Frequência")
  
  p4 <- ggplot(dados, aes(x = produtividade)) +
    geom_histogram(bins = 30, fill = "purple", alpha = 0.7) +
    geom_vline(aes(xintercept = mean(produtividade)), color = "red", linetype = "dashed") +
    labs(title = "📈 Distribuição da Produtividade", x = "Produtividade (%)", y = "Frequência")
  
  # Séries temporais
  p5 <- dados %>%
    select(data, temperatura, umidade_solo, produtividade) %>%
    pivot_longer(-data, names_to = "variavel", values_to = "valor") %>%
    ggplot(aes(x = data, y = valor, color = variavel)) +
    geom_line(alpha = 0.8) +
    facet_wrap(~ variavel, scales = "free_y", nrow = 3) +
    labs(title = "📈 Séries Temporais - Variáveis Principais", x = "Data", y = "Valor") +
    theme(legend.position = "none")
  
  # Análise sazonal
  p6 <- dados %>%
    group_by(estacao) %>%
    summarise(
      temp_media = mean(temperatura),
      umidade_media = mean(umidade_solo),
      prod_media = mean(produtividade),
      .groups = "drop"
    ) %>%
    pivot_longer(-estacao, names_to = "metrica", values_to = "valor") %>%
    ggplot(aes(x = estacao, y = valor, fill = estacao)) +
    geom_col(alpha = 0.8) +
    facet_wrap(~ metrica, scales = "free_y") +
    labs(title = "🌱 Análise Sazonal", x = "Estação", y = "Valor Médio") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  # Padrões de irrigação
  irrigacao_stats <- dados %>%
    group_by(irrigacao_realizada) %>%
    summarise(
      count = n(),
      temp_media = mean(temperatura),
      umidade_media = mean(umidade_solo),
      prod_media = mean(produtividade),
      .groups = "drop"
    )
  
  cat("\n💧 ESTATÍSTICAS DE IRRIGAÇÃO:\n")
  print(irrigacao_stats)
  
  # NPK Analysis
  npk_stats <- dados %>%
    summarise(
      nitrogenio_adequado = mean(nitrogenio_ok) * 100,
      fosforo_adequado = mean(fosforo_ok) * 100,
      potassio_adequado = mean(potassio_ok) * 100
    )
  
  cat("\n🧪 ADEQUAÇÃO NPK (%):\n")
  print(npk_stats)
  
  # Retorna resultados
  list(
    estatisticas = summary(dados),
    correlacoes = cor_matrix,
    graficos = list(p1, p2, p3, p4, p5, p6),
    irrigacao_stats = irrigacao_stats,
    npk_stats = npk_stats
  )
}

# ═══════════════════════════════════════════════════════════════════════════
# FUNÇÃO PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

main_analise_estatistica <- function(cultura = "banana", dias_historico = 180) {
  # Função principal que executa análise estatística completa
  #
  # Args:
  #   cultura: 'banana' ou 'milho'  
  #   dias_historico: número de dias de dados históricos
  #
  # Returns:
  #   list com todos os resultados
  
  cat("🚀 FARMTECH SOLUTIONS - ANÁLISE ESTATÍSTICA DE IRRIGAÇÃO\n")
  cat("=" , rep("=", 60), "\n")
  cat("🌱 Cultura:", CULTURA_CONFIG[[cultura]]$emoji, CULTURA_CONFIG[[cultura]]$nome, "\n")
  cat("📅 Período de análise:", dias_historico, "dias\n")
  cat("🕐 Executado em:", format(Sys.time(), "%d/%m/%Y %H:%M:%S"), "\n")
  cat("=" , rep("=", 60), "\n\n")
  
  # 1. Geração de dados históricos
  cat("📊 Gerando dados históricos sintéticos...\n")
  dados <- gerar_dados_historicos(cultura, dias_historico)
  cat("✅ Dataset criado:", nrow(dados), "observações\n\n")
  
  # 2. Análise exploratória 
  cat("🔍 Realizando análise exploratória...\n")
  eda_results <- analise_exploratoria(dados)
  cat("✅ Análise exploratória concluída\n\n")
  
  # 3. Salva dados para uso posterior
  write_csv(dados, "dados_historicos_irrigacao.csv")
  cat("💾 Dados salvos em: dados_historicos_irrigacao.csv\n\n")
  
  # 4. Retorna resultados
  cat("🎉 ANÁLISE ESTATÍSTICA CONCLUÍDA COM SUCESSO!\n")
  cat("=" , rep("=", 60), "\n")
  
  list(
    dados = dados,
    configuracao = CULTURA_CONFIG[[cultura]],
    analise_exploratoria = eda_results,
    arquivo_dados = "dados_historicos_irrigacao.csv"
  )
}

# ═══════════════════════════════════════════════════════════════════════════
# EXECUÇÃO PRINCIPAL (descomente para testar)
# ═══════════════════════════════════════════════════════════════════════════

# Executa análise para cultura de banana
# resultados_banana <- main_analise_estatistica("banana", 180)

# Executa análise para cultura de milho  
# resultados_milho <- main_analise_estatistica("milho", 180)

cat("📚 Script R carregado com sucesso!\n")
cat("💡 Execute: main_analise_estatistica('banana') ou main_analise_estatistica('milho')\n")
cat("🔧 Bibliotecas carregadas e funções prontas para uso.\n")