#grupo 59 FIAP
#rm566826 - Phellype Matheus Giacoia Flaibam Massarente
#rm567005 - Carlos Alberto Florindo Costato
#rm568140 - Cesar Martinho de Azeredo

# Script R para coletar e exibir dados meteorológicos de uma API pública
# Exemplo usando a API Open-Meteo (https://open-meteo.com/)

# Instale o pacote httr se necessário
if (!require('httr')) install.packages('httr', dependencies=TRUE)
library(httr)

# Defina a latitude e longitude da fazenda (exemplo: São Paulo)
latitude <- -23.55
longitude <- -46.63

# Monta a URL da API
url <- paste0('https://api.open-meteo.com/v1/forecast?latitude=', latitude,
              '&longitude=', longitude,
              '&current_weather=true')

# Faz a requisição
res <- GET(url)
if (status_code(res) == 200) {
  dados <- content(res, as='parsed')
  cat('Tempo atual em São Paulo:\n')
  cat('Temperatura:', dados$current_weather$temperature, '°C\n')
  cat('Vento:', dados$current_weather$windspeed, 'km/h\n')
  cat('Condição:', dados$current_weather$weathercode, '\n')
} else {
  cat('Erro ao acessar a API.\n')
}

# Lista de cidades com plantio de banana e milho
cidades_plantio <- list(
  banana = c("Registro", "Juquiá", "Sete Barras", "Miracatu", "Iguape"),
  milho = c("Sorriso", "Lucas do Rio Verde", "Primavera do Leste", "Unaí", "Rio Verde")
)

# Obter argumentos da linha de comando
args <- commandArgs(trailingOnly = TRUE)

if (length(args) > 0) {
  cultura <- tolower(args[1])
} else {
  cultura <- "banana"  # valor padrão
}

if (cultura %in% names(cidades_plantio)) {
  cat(sprintf("\nCidades com plantio de %s:\n", cultura))
  for (cidade in cidades_plantio[[cultura]]) {
    cat("- ", cidade, "\n")
  }
} else {
  cat("\nCultura não encontrada. Escolha 'banana' ou 'milho'.\n")
}
