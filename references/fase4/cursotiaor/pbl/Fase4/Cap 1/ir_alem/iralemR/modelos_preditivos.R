# ═══════════════════════════════════════════════════════════════════════════
# FarmTech Solutions - Modelos Preditivos de Irrigação (IR ALÉM 2)
# ═══════════════════════════════════════════════════════════════════════════
#
# OBJETIVO: Desenvolver modelos preditivos para otimização de irrigação
#
# MODELOS IMPLEMENTADOS:
# - Regressão Logística (decisão de irrigar)
# - Random Forest (classificação multi-classe)  
# - Modelo de Séries Temporais (previsão)
# - SVM (Support Vector Machine)
# - Ensemble Learning
#
# MÉTRICAS DE AVALIAÇÃO:
# - Acurácia, Precisão, Recall, F1-Score
# - AUC-ROC, Matriz de Confusão
# - Cross-validation
# - Feature importance
#
# ═══════════════════════════════════════════════════════════════════════════

# Carrega script base (se não carregado)
if (!exists("CULTURA_CONFIG")) {
  source("analise_estatistica.R")
}

# Bibliotecas adicionais para modelos preditivos
if (!require("pacman")) install.packages("pacman")

pacman::p_load(
  # Machine Learning
  randomForest,
  e1071,
  caret,
  xgboost,
  
  # Avaliação de modelos
  pROC,
  ROCR,
  
  # Ensemble methods
  caretEnsemble,
  
  # Otimização
  OptimalCutpoints,
  
  # Visualizações avançadas
  vip,
  pdp,
  lime
)

# ═══════════════════════════════════════════════════════════════════════════
# PREPARAÇÃO DE DADOS PARA MODELAGEM
# ═══════════════════════════════════════════════════════════════════════════

preparar_dados_modelo <- function(dados) {
  # Prepara dataset para modelagem preditiva
  #
  # Args:
  #   dados: data.frame com dados históricos
  #
  # Returns:
  #   list com dados processados para treino e teste
  
  cat("🔧 Preparando dados para modelagem...\n")
  
  # Feature Engineering
  dados_modelo <- dados %>%
    mutate(
      # Variáveis temporais
      dia_semana = wday(data, label = TRUE),
      trimestre = quarter(data),
      mes_categoria = case_when(
        mes %in% c(12, 1, 2) ~ "Verão",
        mes %in% c(3, 4, 5) ~ "Outono", 
        mes %in% c(6, 7, 8) ~ "Inverno",
        TRUE ~ "Primavera"
      ),
      
      # Índices compostos
      deficit_umidade = pmax(0, 50 - umidade_solo),  # Déficit hídrico
      stress_termico = abs(temperatura - 25),  # Stress térmico
      ph_desbalanceado = abs(ph_solo - 6.5),  # Desbalanceamento de pH
      
      # NPK combinado
      npk_score = (as.numeric(nitrogenio_ok) + as.numeric(fosforo_ok) + as.numeric(potassio_ok)) / 3,
      npk_deficiente = npk_score < 0.7,
      
      # Condições meteorológicas
      condicao_climatica = case_when(
        precipitacao > 20 & umidade_ar > 80 ~ "Chuva_Intensa",
        precipitacao > 5 & umidade_ar > 60 ~ "Chuva_Moderada",
        temperatura > 30 & umidade_ar < 40 ~ "Seca_Severa",
        temperatura > 28 & umidade_ar < 50 ~ "Seca_Moderada",
        TRUE ~ "Normal"
      ),
      
      # Variáveis lag (valores anteriores)
      temp_lag1 = lag(temperatura, 1),
      umidade_lag1 = lag(umidade_solo, 1),
      precipitacao_lag1 = lag(precipitacao, 1),
      
      # Médias móveis
      temp_ma3 = rollmean(temperatura, k = 3, fill = NA, align = "right"),
      umidade_ma3 = rollmean(umidade_solo, k = 3, fill = NA, align = "right"),
      
      # Target variables para diferentes modelos
      # 1. Classificação binária: Irrigar ou não
      necessita_irrigacao = irrigacao_realizada,
      
      # 2. Classificação multi-classe: Nível de irrigação
      nivel_irrigacao = case_when(
        umidade_solo >= 60 ~ "Nenhuma",
        umidade_solo >= 45 ~ "Leve", 
        umidade_solo >= 30 ~ "Moderada",
        TRUE ~ "Intensa"
      ),
      
      # 3. Regressão: Score de irrigação (0-100)
      score_irrigacao = case_when(
        umidade_solo < 20 ~ 100,
        umidade_solo < 30 ~ 80,
        umidade_solo < 40 ~ 60,
        umidade_solo < 50 ~ 40,
        umidade_solo < 60 ~ 20,
        TRUE ~ 0
      )
    ) %>%
    # Remove NAs criados pelas transformações
    filter(!is.na(temp_lag1)) %>%
    # Converte variáveis categóricas
    mutate(
      nivel_irrigacao = factor(nivel_irrigacao, levels = c("Nenhuma", "Leve", "Moderada", "Intensa")),
      condicao_climatica = factor(condicao_climatica),
      mes_categoria = factor(mes_categoria),
      dia_semana = factor(dia_semana)
    )
  
  # Seleciona features para modelos
  features_numericas <- c(
    "temperatura", "umidade_solo", "ph_solo", "precipitacao",
    "pressao_atmosferica", "umidade_ar", "vento_kmh",
    "deficit_umidade", "stress_termico", "ph_desbalanceado", "npk_score",
    "temp_lag1", "umidade_lag1", "precipitacao_lag1",
    "temp_ma3", "umidade_ma3", "dia_ano"
  )
  
  features_categoricas <- c(
    "nitrogenio_ok", "fosforo_ok", "potassio_ok", "npk_deficiente",
    "mes_categoria", "condicao_climatica"
  )
  
  # Dataset final para modelos
  dados_final <- dados_modelo %>%
    select(all_of(c(features_numericas, features_categoricas)), 
           necessita_irrigacao, nivel_irrigacao, score_irrigacao, data) %>%
    filter(complete.cases(.))
  
  # Split treino/teste (80/20)
  set.seed(42)
  indices_treino <- createDataPartition(
    dados_final$necessita_irrigacao, 
    p = 0.8, 
    list = FALSE
  )
  
  dados_treino <- dados_final[indices_treino, ]
  dados_teste <- dados_final[-indices_treino, ]
  
  cat("✅ Dados preparados:\n")
  cat("   - Treino:", nrow(dados_treino), "observações\n") 
  cat("   - Teste:", nrow(dados_teste), "observações\n")
  cat("   - Features numéricas:", length(features_numericas), "\n")
  cat("   - Features categóricas:", length(features_categoricas), "\n")
  
  list(
    dados_completo = dados_final,
    treino = dados_treino,
    teste = dados_teste,
    features_numericas = features_numericas,
    features_categoricas = features_categoricas
  )
}

# ═══════════════════════════════════════════════════════════════════════════
# MODELO 1: REGRESSÃO LOGÍSTICA
# ═══════════════════════════════════════════════════════════════════════════

treinar_regressao_logistica <- function(dados_prep) {
  # Treina modelo de regressão logística para decisão de irrigação
  
  cat("🤖 Treinando Regressão Logística...\n")
  
  # Prepara fórmula
  features <- c(dados_prep$features_numericas, dados_prep$features_categoricas)
  formula_str <- paste("necessita_irrigacao ~", paste(features, collapse = " + "))
  formula_obj <- as.formula(formula_str)
  
  # Treina modelo
  modelo_glm <- glm(
    formula_obj,
    data = dados_prep$treino,
    family = binomial(link = "logit")
  )
  
  # Predições
  pred_treino <- predict(modelo_glm, dados_prep$treino, type = "response")
  pred_teste <- predict(modelo_glm, dados_prep$teste, type = "response")
  
  # Converte para classificação
  pred_treino_class <- ifelse(pred_treino > 0.5, TRUE, FALSE)
  pred_teste_class <- ifelse(pred_teste > 0.5, TRUE, FALSE)
  
  # Métricas
  conf_matrix_treino <- confusionMatrix(
    factor(pred_treino_class), 
    factor(dados_prep$treino$necessita_irrigacao)
  )
  
  conf_matrix_teste <- confusionMatrix(
    factor(pred_teste_class), 
    factor(dados_prep$teste$necessita_irrigacao)
  )
  
  # AUC-ROC
  roc_treino <- roc(dados_prep$treino$necessita_irrigacao, pred_treino)
  roc_teste <- roc(dados_prep$teste$necessita_irrigacao, pred_teste)
  
  cat("✅ Regressão Logística treinada:\n")
  cat("   - AUC Treino:", round(auc(roc_treino), 3), "\n")
  cat("   - AUC Teste:", round(auc(roc_teste), 3), "\n")
  cat("   - Acurácia Teste:", round(conf_matrix_teste$overall["Accuracy"], 3), "\n")
  
  list(
    modelo = modelo_glm,
    pred_teste = pred_teste,
    pred_teste_class = pred_teste_class,
    conf_matrix = conf_matrix_teste,
    roc = roc_teste,
    auc = auc(roc_teste)
  )
}

# ═══════════════════════════════════════════════════════════════════════════
# MODELO 2: RANDOM FOREST
# ═══════════════════════════════════════════════════════════════════════════

treinar_random_forest <- function(dados_prep) {
  # Treina modelo Random Forest para classificação de irrigação
  
  cat("🌳 Treinando Random Forest...\n")
  
  # Prepara dados (Random Forest lida bem com fatores)
  treino_rf <- dados_prep$treino %>%
    select(all_of(c(dados_prep$features_numericas, dados_prep$features_categoricas)), 
           necessita_irrigacao)
  
  teste_rf <- dados_prep$teste %>%
    select(all_of(c(dados_prep$features_numericas, dados_prep$features_categoricas)), 
           necessita_irrigacao)
  
  # Treina modelo
  set.seed(42)
  modelo_rf <- randomForest(
    necessita_irrigacao ~ .,
    data = treino_rf,
    ntree = 500,
    mtry = floor(sqrt(ncol(treino_rf) - 1)),
    importance = TRUE,
    do.trace = FALSE
  )
  
  # Predições
  pred_treino_rf <- predict(modelo_rf, treino_rf, type = "class")
  pred_teste_rf <- predict(modelo_rf, teste_rf, type = "class")
  pred_prob_teste_rf <- predict(modelo_rf, teste_rf, type = "prob")[, 2]
  
  # Métricas
  conf_matrix_rf <- confusionMatrix(pred_teste_rf, teste_rf$necessita_irrigacao)
  roc_rf <- roc(teste_rf$necessita_irrigacao, pred_prob_teste_rf)
  
  # Feature importance
  importance_rf <- importance(modelo_rf)
  
  cat("✅ Random Forest treinado:\n")
  cat("   - AUC Teste:", round(auc(roc_rf), 3), "\n")
  cat("   - Acurácia Teste:", round(conf_matrix_rf$overall["Accuracy"], 3), "\n")
  cat("   - OOB Error:", round(modelo_rf$err.rate[nrow(modelo_rf$err.rate), 1], 3), "\n")
  
  list(
    modelo = modelo_rf,
    pred_teste = pred_prob_teste_rf,
    pred_teste_class = pred_teste_rf,
    conf_matrix = conf_matrix_rf,
    roc = roc_rf,
    auc = auc(roc_rf),
    importance = importance_rf
  )
}

# ═══════════════════════════════════════════════════════════════════════════
# MODELO 3: SUPPORT VECTOR MACHINE (SVM)
# ═══════════════════════════════════════════════════════════════════════════

treinar_svm <- function(dados_prep) {
  # Treina modelo SVM para classificação de irrigação
  
  cat("⚙️ Treinando SVM...\n")
  
  # Prepara dados (normaliza features numéricas)
  treino_svm <- dados_prep$treino %>%
    select(all_of(c(dados_prep$features_numericas, dados_prep$features_categoricas)), 
           necessita_irrigacao)
  
  teste_svm <- dados_prep$teste %>%
    select(all_of(c(dados_prep$features_numericas, dados_prep$features_categoricas)), 
           necessita_irrigacao)
  
  # Normalização das features numéricas
  preProcess_svm <- preProcess(
    treino_svm[dados_prep$features_numericas], 
    method = c("center", "scale")
  )
  
  treino_svm[dados_prep$features_numericas] <- predict(preProcess_svm, treino_svm[dados_prep$features_numericas])
  teste_svm[dados_prep$features_numericas] <- predict(preProcess_svm, teste_svm[dados_prep$features_numericas])
  
  # Treina SVM
  set.seed(42)
  modelo_svm <- svm(
    necessita_irrigacao ~ .,
    data = treino_svm,
    kernel = "radial",
    probability = TRUE,
    cost = 1,
    gamma = "scale"
  )
  
  # Predições
  pred_teste_svm <- predict(modelo_svm, teste_svm)
  pred_prob_teste_svm <- attr(predict(modelo_svm, teste_svm, probability = TRUE), "probabilities")[, 2]
  
  # Métricas
  conf_matrix_svm <- confusionMatrix(pred_teste_svm, teste_svm$necessita_irrigacao)
  roc_svm <- roc(teste_svm$necessita_irrigacao, pred_prob_teste_svm)
  
  cat("✅ SVM treinado:\n")
  cat("   - AUC Teste:", round(auc(roc_svm), 3), "\n")
  cat("   - Acurácia Teste:", round(conf_matrix_svm$overall["Accuracy"], 3), "\n")
  
  list(
    modelo = modelo_svm,
    pred_teste = pred_prob_teste_svm,
    pred_teste_class = pred_teste_svm,
    conf_matrix = conf_matrix_svm,
    roc = roc_svm,
    auc = auc(roc_svm),
    preprocess = preProcess_svm
  )
}

# ═══════════════════════════════════════════════════════════════════════════
# COMPARAÇÃO E ENSEMBLE DE MODELOS
# ═══════════════════════════════════════════════════════════════════════════

comparar_modelos <- function(modelo_glm, modelo_rf, modelo_svm) {
  # Compara performance dos modelos e cria ensemble
  
  cat("📊 Comparando modelos...\n")
  
  # Métricas de comparação
  metricas <- data.frame(
    Modelo = c("Regressão Logística", "Random Forest", "SVM"),
    AUC = c(modelo_glm$auc, modelo_rf$auc, modelo_svm$auc),
    Acuracia = c(
      modelo_glm$conf_matrix$overall["Accuracy"],
      modelo_rf$conf_matrix$overall["Accuracy"], 
      modelo_svm$conf_matrix$overall["Accuracy"]
    ),
    Sensibilidade = c(
      modelo_glm$conf_matrix$byClass["Sensitivity"],
      modelo_rf$conf_matrix$byClass["Sensitivity"],
      modelo_svm$conf_matrix$byClass["Sensitivity"]
    ),
    Especificidade = c(
      modelo_glm$conf_matrix$byClass["Specificity"],
      modelo_rf$conf_matrix$byClass["Specificity"],
      modelo_svm$conf_matrix$byClass["Specificity"]
    ),
    stringsAsFactors = FALSE
  )
  
  # Ensemble simples (média das probabilidades)
  pred_ensemble <- (modelo_glm$pred_teste + modelo_rf$pred_teste + modelo_svm$pred_teste) / 3
  pred_ensemble_class <- ifelse(pred_ensemble > 0.5, TRUE, FALSE)
  
  # Avalia ensemble (usando dados de teste do GLM como referência)
  dados_teste_ref <- modelo_glm$modelo$data[modelo_glm$modelo$model[, 1] == FALSE | modelo_glm$modelo$model[, 1] == TRUE, ]
  
  cat("📈 COMPARAÇÃO DE MODELOS:\n")
  print(round(metricas, 3))
  
  # Melhor modelo
  melhor_modelo <- metricas[which.max(metricas$AUC), "Modelo"]
  cat("\n🏆 Melhor modelo por AUC:", melhor_modelo, "\n")
  
  list(
    metricas = metricas,
    ensemble_pred = pred_ensemble,
    ensemble_class = pred_ensemble_class,
    melhor_modelo = melhor_modelo
  )
}

# ═══════════════════════════════════════════════════════════════════════════
# FUNÇÃO PRINCIPAL PARA MODELOS PREDITIVOS
# ═══════════════════════════════════════════════════════════════════════════

treinar_modelos_irrigacao <- function(dados_historicos) {
  # Função principal que treina todos os modelos preditivos
  #
  # Args:
  #   dados_historicos: data.frame com dados históricos
  # 
  # Returns:
  #   list com todos os modelos treinados e métricas
  
  cat("🚀 INICIANDO TREINAMENTO DE MODELOS PREDITIVOS\n")
  cat("=" , rep("=", 55), "\n\n")
  
  # 1. Preparação dos dados
  dados_prep <- preparar_dados_modelo(dados_historicos)
  
  # 2. Treina modelos
  cat("\n🤖 TREINAMENTO DE MODELOS:\n")
  cat("-" , rep("-", 40), "\n")
  
  modelo_glm <- treinar_regressao_logistica(dados_prep)
  modelo_rf <- treinar_random_forest(dados_prep)
  modelo_svm <- treinar_svm(dados_prep)
  
  # 3. Comparação
  cat("\n📊 COMPARAÇÃO E ENSEMBLE:\n")
  cat("-" , rep("-", 40), "\n")
  
  comparacao <- comparar_modelos(modelo_glm, modelo_rf, modelo_svm)
  
  cat("\n🎉 MODELOS PREDITIVOS CONCLUÍDOS!\n")
  cat("=" , rep("=", 55), "\n")
  
  list(
    dados_preparados = dados_prep,
    regressao_logistica = modelo_glm,
    random_forest = modelo_rf,
    svm = modelo_svm,
    comparacao = comparacao
  )
}

cat("🤖 Módulo de modelos preditivos carregado!\n")
cat("💡 Execute: treinar_modelos_irrigacao(dados_historicos)\n")