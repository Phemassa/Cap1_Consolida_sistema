# 👉 Agora pratique com os conceitos aprendidos.
 
# Crie um tibble com os seguintes dados fictícios:
# nome, idade e nota de 5 colegas
# Depois calcule:
#   - a média das notas
#   - quem tirou a maior nota
#   - a lista dos aprovados (nota >= 7)
 
# Dica: use tibble(), mean(), max(), subset()
 
#### Criação do tibble
 
library(tibble)
 
notas  <- tibble(
        nome = c("Laisa", "Paulo", "João", "Marcos", "Samuel"),
        nota = c(7.5,8.0,6.5,9.0,8.5)
)
 
### Imprimindo as notas na tela
 
print(notas)
 
#### Média das notas
 
media <- mean(notas$nota)
print(media)
 
###### A maior nota da turma
 
maiorNota <- max(notas$nota)
melhorColega <- subset(notas, nota == maiorNota)
print(melhorColega)
 
#### Colegas aprovados
 
aprovados <- subset(notas, nota >= 7)
print(aprovados)