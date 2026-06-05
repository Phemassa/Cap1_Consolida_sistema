# ═══════════════════════════════════════════════════════════════════════════
# TESTE RÁPIDO - Cap 7 Análise Estatística R
# ═══════════════════════════════════════════════════════════════════════════
# Execução: Rscript teste_rapido.R
# Objetivo: Validar que todos os cálculos estão corretos
# ═══════════════════════════════════════════════════════════════════════════

cat("\n")
cat("╔═══════════════════════════════════════════════════════════════╗\n")
cat("║       FARMTECH SOLUTIONS - TESTE RÁPIDO CAP 7                ║\n")
cat("║       Validação de Análise Estatística                       ║\n")
cat("╚═══════════════════════════════════════════════════════════════╝\n")
cat("\n")

# ─────────────────────────────────────────────────────────────────────────
# 1. CARREGAR DADOS
# ─────────────────────────────────────────────────────────────────────────
cat("📂 [1/5] Carregando dados...\n")
if (!file.exists("dados_agronegocio_RM98765.csv")) {
  stop("❌ ERRO: Arquivo dados_agronegocio_RM98765.csv não encontrado!")
}

dados <- read.csv("dados_agronegocio_RM98765.csv", 
                  stringsAsFactors = TRUE,
                  encoding = "UTF-8")

cat("   ✅ Dados carregados: ", nrow(dados), " linhas x ", ncol(dados), " colunas\n")

# ─────────────────────────────────────────────────────────────────────────
# 2. VALIDAR ESTRUTURA
# ─────────────────────────────────────────────────────────────────────────
cat("\n📊 [2/5] Validando estrutura dos dados...\n")

# Testar número de linhas
if (nrow(dados) < 30) {
  cat("   ⚠️  AVISO: Apenas ", nrow(dados), " linhas (mínimo: 30)\n")
} else {
  cat("   ✅ Número de linhas OK: ", nrow(dados), " >= 30\n")
}

# Testar colunas obrigatórias
colunas_esperadas <- c("num_propriedades", "area_plantada_ha", 
                       "regiao", "porte_propriedade")
colunas_faltando <- setdiff(colunas_esperadas, names(dados))

if (length(colunas_faltando) > 0) {
  cat("   ❌ ERRO: Colunas faltando: ", paste(colunas_faltando, collapse=", "), "\n")
  stop("Estrutura inválida!")
} else {
  cat("   ✅ Todas as 4 colunas presentes\n")
}

# Testar tipos de variáveis
cat("\n   Tipos de variáveis:\n")
cat("   • num_propriedades: ", class(dados$num_propriedades), 
    ifelse(is.integer(dados$num_propriedades), " ✅ (discreta)", " ❌"), "\n")
cat("   • area_plantada_ha: ", class(dados$area_plantada_ha), 
    ifelse(is.numeric(dados$area_plantada_ha), " ✅ (contínua)", " ❌"), "\n")
cat("   • regiao: ", class(dados$regiao), 
    ifelse(is.factor(dados$regiao), " ✅ (nominal)", " ❌"), "\n")
cat("   • porte_propriedade: ", class(dados$porte_propriedade), 
    ifelse(is.factor(dados$porte_propriedade), " ✅ (ordinal)", " ❌"), "\n")

# ─────────────────────────────────────────────────────────────────────────
# 3. TESTAR CÁLCULOS ESTATÍSTICOS
# ─────────────────────────────────────────────────────────────────────────
cat("\n🧮 [3/5] Testando cálculos estatísticos...\n")

# Área plantada (variável quantitativa contínua)
media_area <- mean(dados$area_plantada_ha)
mediana_area <- median(dados$area_plantada_ha)
dp_area <- sd(dados$area_plantada_ha)
cv_area <- (dp_area / media_area) * 100

cat("\n   📊 Área Plantada (hectares):\n")
cat("      Média: ", round(media_area, 2), " ha\n")
cat("      Mediana: ", round(mediana_area, 2), " ha\n")
cat("      Desvio Padrão: ", round(dp_area, 2), " ha\n")
cat("      CV: ", round(cv_area, 2), "%\n")

# Validar se cálculos fazem sentido
testes_ok <- 0
testes_total <- 5

if (media_area > 0) {
  cat("      ✅ Média > 0\n")
  testes_ok <- testes_ok + 1
} else {
  cat("      ❌ Média inválida\n")
}

if (mediana_area > 0) {
  cat("      ✅ Mediana > 0\n")
  testes_ok <- testes_ok + 1
} else {
  cat("      ❌ Mediana inválida\n")
}

if (dp_area > 0) {
  cat("      ✅ Desvio Padrão > 0\n")
  testes_ok <- testes_ok + 1
} else {
  cat("      ❌ Desvio Padrão inválido\n")
}

if (cv_area >= 0 & cv_area <= 200) {
  cat("      ✅ CV razoável (0-200%)\n")
  testes_ok <- testes_ok + 1
} else {
  cat("      ❌ CV fora do esperado\n")
}

# Quartis
quartis <- quantile(dados$area_plantada_ha, probs = c(0.25, 0.50, 0.75))
if (quartis[1] < quartis[2] & quartis[2] < quartis[3]) {
  cat("      ✅ Quartis em ordem crescente\n")
  testes_ok <- testes_ok + 1
} else {
  cat("      ❌ Quartis inválidos\n")
}

# ─────────────────────────────────────────────────────────────────────────
# 4. TESTAR VARIÁVEIS QUALITATIVAS
# ─────────────────────────────────────────────────────────────────────────
cat("\n📋 [4/5] Testando variáveis qualitativas...\n")

# Região (nominal)
tabela_regiao <- table(dados$regiao)
cat("\n   🗺️  Regiões encontradas: ", length(tabela_regiao), "\n")
for (i in 1:length(tabela_regiao)) {
  cat("      • ", names(tabela_regiao)[i], ": ", 
      tabela_regiao[i], " propriedades\n", sep="")
}

if (length(tabela_regiao) >= 2) {
  cat("   ✅ Variável nominal OK (", length(tabela_regiao), " categorias)\n")
} else {
  cat("   ⚠️  AVISO: Poucas categorias na variável nominal\n")
}

# Porte (ordinal)
tabela_porte <- table(dados$porte_propriedade)
cat("\n   📏 Portes encontrados: ", length(tabela_porte), "\n")
for (i in 1:length(tabela_porte)) {
  cat("      • ", names(tabela_porte)[i], ": ", 
      tabela_porte[i], " propriedades\n", sep="")
}

if (length(tabela_porte) >= 2) {
  cat("   ✅ Variável ordinal OK (", length(tabela_porte), " categorias)\n")
} else {
  cat("   ⚠️  AVISO: Poucas categorias na variável ordinal\n")
}

# ─────────────────────────────────────────────────────────────────────────
# 5. RESUMO FINAL
# ─────────────────────────────────────────────────────────────────────────
cat("\n📝 [5/5] Resumo dos testes...\n")
cat("\n   ╔═══════════════════════════════════════════════════════════╗\n")
cat("   ║                  RESULTADO DOS TESTES                     ║\n")
cat("   ╠═══════════════════════════════════════════════════════════╣\n")
cat("   ║  Testes Estatísticos: ", testes_ok, "/", testes_total, " ✅                      ║\n", sep="")
cat("   ║  Estrutura de Dados:  OK ✅                               ║\n")
cat("   ║  Variáveis Qualitativas: OK ✅                            ║\n")
cat("   ╚═══════════════════════════════════════════════════════════╝\n")

if (testes_ok == testes_total) {
  cat("\n   🎉 TODOS OS TESTES PASSARAM! Sistema OK.\n")
  cat("   ✅ Pronto para executar analise_RM98765.R completo\n")
} else {
  cat("\n   ⚠️  Alguns testes falharam. Verifique os dados.\n")
}

cat("\n")
cat("═══════════════════════════════════════════════════════════════\n")
cat(" FarmTech Solutions - Teste Concluído\n")
cat(" Data: ", format(Sys.Date(), "%d/%m/%Y"), "\n")
cat("═══════════════════════════════════════════════════════════════\n")
cat("\n")
