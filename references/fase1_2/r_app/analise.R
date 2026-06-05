#grupo 59 FIAP
#rm566826 - Phellype Matheus Giacoia Flaibam Massarente
#rm567005 - Carlos Alberto Florindo Costato
#rm568140 - Cesar Martinho de Azeredo


library(readr)

# Script R para análise estatística dos dados exportados do Python
# Lê banana.csv e milho.csv e calcula média e desvio padrão de insumo
print("Script executado!")
if (!require('readr')) install.packages('readr', repos='https://cran.r-project.org/', dependencies=TRUE)
library(readr)

banana <- read_csv('../python_app/banana.csv', show_col_types = FALSE)
milho <- read_csv('../python_app/milho.csv', show_col_types = FALSE)

# Estatísticas para banana.csv
cat('\n--- Estatísticas Banana ---\n')
cat('Média comprimento:', mean(banana$comprimento), '\n')
cat('Desvio padrão comprimento:', sd(banana$comprimento), '\n')
cat('Média largura:', mean(banana$largura), '\n')
cat('Desvio padrão largura:', sd(banana$largura), '\n')
cat('Média qtd_insumo:', mean(banana$qtd_insumo), '\n')
cat('Desvio padrão qtd_insumo:', sd(banana$qtd_insumo), '\n')

# Estatísticas para milho.csv (mantido original)
cat('\n--- Percentual por tipo de geométrica (Milho) ---\n')
figura_nomes <- c('1' = 'Círculo', '2' = 'Retângulo', '3' = 'Quadrado')
milho_figura_pct <- prop.table(table(milho$figura)) * 100
for (tipo in names(milho_figura_pct)) {
  nome_figura <- figura_nomes[[as.character(tipo)]]
  if (is.null(nome_figura)) nome_figura <- tipo
  cat(sprintf('%s: %.1f%%\n', nome_figura, milho_figura_pct[[tipo]]))
}

cat('\n--- Percentual por unidade (Milho) ---\n')
milho_unidade_pct <- prop.table(table(milho$unidade)) * 100
for (unidade in names(milho_unidade_pct)) {
	cat(sprintf('Unidade %s: %.1f%%\n', unidade, milho_unidade_pct[[unidade]]))
}

cat('--- Estatísticas Milho ---\n')
cat('Média área:', mean(milho$area), '\n')
cat('Desvio padrão área:', sd(milho$area), '\n')
cat('Média insumo:', mean(milho$qtd_insumo), '\n')
cat('Desvio padrão insumo:', sd(milho$qtd_insumo), '\n')
