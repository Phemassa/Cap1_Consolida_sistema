library(tibble)

# Criando o tibble
dados <- tibble(
  nome = c("Ana", "Bruno", "Carlos", "Diana", "Eduardo"),
  idade = c(20, 21, 19, 22, 20),
  nota = c(8.5, 6.7, 9.2, 7.0, 5.8)
)

# Média das notas
media_notas <- mean(dados$nota)

# Quem tirou a maior nota
maior_nota <- max(dados$nota)
aluno_maior_nota <- dados$nome[dados$nota == maior_nota]

# Lista dos aprovados (nota >= 7)
aprovados <- subset(dados, nota >= 7)

# Exibindo os resultados
print(dados)
cat("Média das notas:", media_notas, "\n")
cat("Maior nota:", maior_nota, "- Aluno:", aluno_maior_nota, "\n")
cat("Aprovados:\n")
print(aprovados)