# ═══════════════════════════════════════════════════════════════════════════
# FarmTech Solutions - Modelos Preditivos de Irrigação (IR ALÉM 2) - CORRIGIDO
# ═══════════════════════════════════════════════════════════════════════════

# Carrega script base (se não carregado)
if (!exists("CULTURA_CONFIG")) {
  source("analise_estatistica.R")
}

# Carrega bibliotecas adicionais 
library(randomForest)
library(e1071)
library(caret)
library(pROC)
library(zoo) # Para rollmean

# ═══════════════════════════════════════════════════════════════════════════
# PREPARAÇÃO DE DADOS PARA MODELAGEM
# ═══════════════════════════════════════════════════════════════════════════

preparar_dados_modelo <- function(dados) {
  # Prepara dataset para modelagem preditiva
  
  cat("🔧 Preparando dados para modelagem...\n")
  
  # Feature Engineering
  dados_modelo <- dados %>%
    mutate(
      # Variáveis temporais
      dia_semana = wday(data, label = TRUE),
      trimestre = quarter(data),
      
      # Índices compostos
      deficit_umidade = pmax(0, 50 - umidade_solo),  # Déficit hídrico
      stress_termico = abs(temperatura - 25),  # Stress térmico
      ph_desbalanceado = abs(ph_solo - 6.5),  # Desbalanceamento de pH
      
      # NPK combinado
      npk_score = (as.numeric(nitrogenio_ok) + as.numeric(fosforo_ok) + as.numeric(potassio_ok)) / 3,
      npk_deficiente = npk_score < 0.7,
      
      # Condições meteorológicas
      condicao_seca = temperatura > 30 & umidade_ar < 40,
      condicao_chuva = precipitacao > 10,
      
      # Variáveis lag (valores anteriores) 
      temp_lag1 = lag(temperatura, 1),
      umidade_lag1 = lag(umidade_solo, 1),
      
      # Médias móveis (usando rollmean do pacote zoo)
      temp_ma3 = rollmean(temperatura, k = 3, fill = NA, align = "right"),
      umidade_ma3 = rollmean(umidade_solo, k = 3, fill = NA, align = "right"),
      
      # Target variable
      necessita_irrigacao = irrigacao_realizada,
      
      # Score de irrigação (0-100)
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
    filter(!is.na(temp_lag1))
  
  # Seleciona features para modelos
  features_principais <- c(
    "temperatura", "umidade_solo", "ph_solo", "precipitacao",
    "pressao_atmosferica", "umidade_ar", "vento_kmh",
    "deficit_umidade", "stress_termico", "ph_desbalanceado", "npk_score",
    "temp_lag1", "umidade_lag1", "temp_ma3", "umidade_ma3", "dia_ano"
  )
  
  # Dataset final para modelos
  dados_final <- dados_modelo[complete.cases(dados_modelo[features_principais]), ]
  
  # Split treino/teste (80/20)
  set.seed(42)
  indices_treino <- sample(nrow(dados_final), size = floor(0.8 * nrow(dados_final)))
  
  dados_treino <- dados_final[indices_treino, ]
  dados_teste <- dados_final[-indices_treino, ]
  
  cat("✅ Dados preparados:\n")
  cat("   - Treino:", nrow(dados_treino), "observações\n") 
  cat("   - Teste:", nrow(dados_teste), "observações\n")
  cat("   - Features:", length(features_principais), "\n\n")
  
  list(
    dados_completo = dados_final,
    treino = dados_treino,
    teste = dados_teste,
    features = features_principais
  )
}

# ═══════════════════════════════════════════════════════════════════════════
# MODELO 1: REGRESSÃO LOGÍSTICA
# ═══════════════════════════════════════════════════════════════════════════

treinar_regressao_logistica <- function(dados_prep) {
  # Treina modelo de regressão logística para decisão de irrigação
  
  cat("🤖 Treinando Regressão Logística...\n")
  
  # Prepara fórmula
  formula_str <- paste("necessita_irrigacao ~", paste(dados_prep$features, collapse = " + "))
  formula_obj <- as.formula(formula_str)
  
  # Treina modelo
  modelo_glm <- glm(
    formula_obj,
    data = dados_prep$treino,
    family = binomial(link = "logit")
  )
  
  # Predições
  pred_teste <- predict(modelo_glm, dados_prep$teste, type = "response")
  pred_teste_class <- ifelse(pred_teste > 0.5, TRUE, FALSE)
  
  # Métricas básicas
  accuracy <- mean(pred_teste_class == dados_prep$teste$necessita_irrigacao, na.rm = TRUE)
  
  # AUC-ROC (se biblioteca pROC disponível)
  auc_score <- NA
  if ("pROC" %in% loadedNamespaces()) {
    tryCatch({
      roc_obj <- roc(dados_prep$teste$necessita_irrigacao, pred_teste)
      auc_score <- auc(roc_obj)
    }, error = function(e) {
      cat("Aviso: Erro ao calcular AUC\n")
    })
  }
  
  cat("✅ Regressão Logística treinada:\n")
  cat("   - Acurácia Teste:", round(accuracy, 3), "\n")
  if (!is.na(auc_score)) {
    cat("   - AUC Teste:", round(auc_score, 3), "\n")
  }
  cat("\n")
  
  list(
    modelo = modelo_glm,
    pred_teste = pred_teste,
    pred_teste_class = pred_teste_class,
    accuracy = accuracy,
    auc = auc_score
  )
}

# ═══════════════════════════════════════════════════════════════════════════
# MODELO 2: RANDOM FOREST
# ═══════════════════════════════════════════════════════════════════════════

treinar_random_forest <- function(dados_prep) {
  # Treina modelo Random Forest para classificação de irrigação
  
  cat("🌳 Treinando Random Forest...\n")
  
  # Prepara dados
  treino_features <- dados_prep$treino[, dados_prep$features]
  treino_target <- dados_prep$treino$necessita_irrigacao
  
  teste_features <- dados_prep$teste[, dados_prep$features]
  teste_target <- dados_prep$teste$necessita_irrigacao
  
  # Treina modelo
  set.seed(42)
  modelo_rf <- randomForest(
    x = treino_features,
    y = as.factor(treino_target),
    ntree = 300,
    mtry = floor(sqrt(length(dados_prep$features))),
    importance = TRUE
  )
  
  # Predições
  pred_teste_rf <- predict(modelo_rf, teste_features, type = "class")
  pred_prob_teste_rf <- predict(modelo_rf, teste_features, type = "prob")[, "TRUE"]
  
  # Métricas
  accuracy_rf <- mean(pred_teste_rf == teste_target, na.rm = TRUE)
  
  # AUC-ROC
  auc_rf <- NA
  if ("pROC" %in% loadedNamespaces()) {
    tryCatch({
      roc_rf <- roc(teste_target, pred_prob_teste_rf)
      auc_rf <- auc(roc_rf)
    }, error = function(e) {
      cat("Aviso: Erro ao calcular AUC para RF\n")
    })
  }
  
  # Feature importance
  importance_rf <- importance(modelo_rf)
  
  cat("✅ Random Forest treinado:\n")
  cat("   - Acurácia Teste:", round(accuracy_rf, 3), "\n")
  if (!is.na(auc_rf)) {
    cat("   - AUC Teste:", round(auc_rf, 3), "\n")
  }
  cat("   - OOB Error:", round(modelo_rf$err.rate[nrow(modelo_rf$err.rate), "OOB"], 3), "\n")
  cat("\n")
  
  list(
    modelo = modelo_rf,
    pred_teste = pred_prob_teste_rf,
    pred_teste_class = pred_teste_rf,
    accuracy = accuracy_rf,
    auc = auc_rf,
    importance = importance_rf
  )
}

# ═══════════════════════════════════════════════════════════════════════════
# MODELO 3: SUPPORT VECTOR MACHINE (SVM)
# ═══════════════════════════════════════════════════════════════════════════

treinar_svm <- function(dados_prep) {
  # Treina modelo SVM para classificação de irrigação
  
  cat("⚙️ Treinando SVM...\n")
  
  # Prepara e normaliza dados
  treino_features <- dados_prep$treino[, dados_prep$features]
  treino_target <- dados_prep$treino$necessita_irrigacao
  
  teste_features <- dados_prep$teste[, dados_prep$features]
  teste_target <- dados_prep$teste$necessita_irrigacao
  
  # Normalização
  treino_scaled <- scale(treino_features)
  teste_scaled <- scale(teste_features, center = attr(treino_scaled, "scaled:center"),
                        scale = attr(treino_scaled, "scaled:scale"))
  
  # Treina SVM
  set.seed(42)
  modelo_svm <- svm(
    x = treino_scaled,
    y = as.factor(treino_target),
    kernel = "radial",
    probability = TRUE,
    cost = 1
  )
  
  # Predições
  pred_teste_svm <- predict(modelo_svm, teste_scaled)
  
  # Predições com probabilidade
  pred_prob_svm <- NA
  tryCatch({
    pred_prob_obj <- predict(modelo_svm, teste_scaled, probability = TRUE)
    pred_prob_svm <- attr(pred_prob_obj, "probabilities")[, "TRUE"]
  }, error = function(e) {
    cat("Aviso: Erro ao obter probabilidades do SVM\n")
  })
  
  # Métricas
  accuracy_svm <- mean(pred_teste_svm == teste_target, na.rm = TRUE)
  
  # AUC (se probabilidades disponíveis)
  auc_svm <- NA
  if (!any(is.na(pred_prob_svm)) && "pROC" %in% loadedNamespaces()) {
    tryCatch({
      roc_svm <- roc(teste_target, pred_prob_svm)
      auc_svm <- auc(roc_svm)
    }, error = function(e) {
      cat("Aviso: Erro ao calcular AUC para SVM\n")
    })
  }
  
  cat("✅ SVM treinado:\n")
  cat("   - Acurácia Teste:", round(accuracy_svm, 3), "\n")
  if (!is.na(auc_svm)) {
    cat("   - AUC Teste:", round(auc_svm, 3), "\n")
  }
  cat("\n")
  
  list(
    modelo = modelo_svm,
    pred_teste = pred_prob_svm,
    pred_teste_class = pred_teste_svm,
    accuracy = accuracy_svm,
    auc = auc_svm,
    scaler = list(
      center = attr(treino_scaled, "scaled:center"),
      scale = attr(treino_scaled, "scaled:scale")
    )
  )
}

# ═══════════════════════════════════════════════════════════════════════════
# COMPARAÇÃO DE MODELOS
# ═══════════════════════════════════════════════════════════════════════════

comparar_modelos <- function(modelo_glm, modelo_rf, modelo_svm) {
  # Compara performance dos modelos
  
  cat("📊 Comparando modelos...\n")
  
  # Métricas de comparação
  metricas <- data.frame(
    Modelo = c("Regressão Logística", "Random Forest", "SVM"),
    Acuracia = c(
      ifelse(is.null(modelo_glm$accuracy), NA, modelo_glm$accuracy),
      ifelse(is.null(modelo_rf$accuracy), NA, modelo_rf$accuracy), 
      ifelse(is.null(modelo_svm$accuracy), NA, modelo_svm$accuracy)
    ),
    AUC = c(
      ifelse(is.null(modelo_glm$auc) || is.na(modelo_glm$auc), NA, modelo_glm$auc),
      ifelse(is.null(modelo_rf$auc) || is.na(modelo_rf$auc), NA, modelo_rf$auc),
      ifelse(is.null(modelo_svm$auc) || is.na(modelo_svm$auc), NA, modelo_svm$auc)
    ),
    stringsAsFactors = FALSE
  )
  
  cat("📈 COMPARAÇÃO DE MODELOS:\n")
  print(round(metricas, 3))
  
  # Melhor modelo por acurácia
  melhor_idx <- which.max(metricas$Acuracia)
  melhor_modelo <- metricas[melhor_idx, "Modelo"]
  cat("\n🏆 Melhor modelo por Acurácia:", melhor_modelo, "\n")
  
  # Melhor modelo por AUC (se disponível)
  if (!all(is.na(metricas$AUC))) {
    melhor_idx_auc <- which.max(metricas$AUC)
    melhor_modelo_auc <- metricas[melhor_idx_auc, "Modelo"]
    cat("🏆 Melhor modelo por AUC:", melhor_modelo_auc, "\n")
  }
  
  list(
    metricas = metricas,
    melhor_modelo = melhor_modelo
  )
}

# ═══════════════════════════════════════════════════════════════════════════
# FUNÇÃO PRINCIPAL PARA MODELOS PREDITIVOS
# ═══════════════════════════════════════════════════════════════════════════

treinar_modelos_irrigacao <- function(dados_historicos) {
  # Função principal que treina todos os modelos preditivos
  
  cat("🚀 INICIANDO TREINAMENTO DE MODELOS PREDITIVOS\n")
  cat("=", rep("=", 55), "\n\n")
  
  # 1. Preparação dos dados
  dados_prep <- preparar_dados_modelo(dados_historicos)
  
  # 2. Treina modelos
  cat("🤖 TREINAMENTO DE MODELOS:\n")
  cat("-", rep("-", 40), "\n")
  
  modelo_glm <- treinar_regressao_logistica(dados_prep)
  modelo_rf <- treinar_random_forest(dados_prep)
  modelo_svm <- treinar_svm(dados_prep)
  
  # 3. Comparação
  cat("📊 COMPARAÇÃO DE MODELOS:\n")
  cat("-", rep("-", 40), "\n")
  
  comparacao <- comparar_modelos(modelo_glm, modelo_rf, modelo_svm)
  
  cat("\n🎉 MODELOS PREDITIVOS CONCLUÍDOS!\n")
  cat("=", rep("=", 55), "\n")
  
  list(
    dados_preparados = dados_prep,
    regressao_logistica = modelo_glm,
    random_forest = modelo_rf,
    svm = modelo_svm,
    comparacao = comparacao
  )
}

# ═══════════════════════════════════════════════════════════════════════════
# FUNÇÃO DE PREDIÇÃO PARA NOVOS DADOS
# ═══════════════════════════════════════════════════════════════════════════

prever_irrigacao <- function(modelos_treinados, novos_dados) {
  # Faz predição usando o melhor modelo treinado
  
  melhor_modelo_nome <- modelos_treinados$comparacao$melhor_modelo
  
  # Seleciona o modelo correspondente
  if (melhor_modelo_nome == "Random Forest") {
    modelo <- modelos_treinados$random_forest$modelo
    features <- modelos_treinados$dados_preparados$features
    pred <- predict(modelo, novos_dados[features], type = "prob")[, "TRUE"]
  } else if (melhor_modelo_nome == "SVM") {
    modelo <- modelos_treinados$svm$modelo
    scaler <- modelos_treinados$svm$scaler
    features <- modelos_treinados$dados_preparados$features
    novos_dados_scaled <- scale(novos_dados[features], center = scaler$center, scale = scaler$scale)
    pred <- predict(modelo, novos_dados_scaled, probability = TRUE)
    pred <- attr(pred, "probabilities")[, "TRUE"]
  } else {
    # Regressão Logística (padrão)
    modelo <- modelos_treinados$regressao_logistica$modelo
    pred <- predict(modelo, novos_dados, type = "response")
  }
  
  list(
    probabilidade = pred,
    decisao = pred > 0.5,
    modelo_usado = melhor_modelo_nome
  )
}

cat("🤖 Módulo de modelos preditivos (CORRIGIDO) carregado!\n")
cat("💡 Execute: treinar_modelos_irrigacao(dados_historicos)\n")
cat("🔮 Para predições: prever_irrigacao(modelos, novos_dados)\n")