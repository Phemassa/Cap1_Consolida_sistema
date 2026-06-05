# Cap 3 - Você tem pensamento computacional

## Sumário

# Cap 3 - Você tem pensamento computacional

Você tem pensamento computacional?9.1.3 Plano de teste “Aprovado” por exameComando de prompt 35-Plano de teste 3 do desafioFonte: Elaborado pelo autor (2022)----------------------P R I M E I RO   S E M E S T R EDigite o checkpoint 1:3Digite o checkpoint 2:4Digite o checkpoint 3:5Média dos checkpoints: 4.5Digite o sprint 1:2Digite o sprint 2:3Média dos sprints: 2.5Digite a prova semestral:4Média do primeirosemestre: 3.80----------------------S E G U N D O   S E M E S T R EDigite o checkpoint 1:5Digite o checkpoint 2:6Digite o checkpoint 3:3Média dos checkpoints: 5.5Digite o sprint 1:4Digite o sprint 2:5Média dos sprints: 4.5Digite a prova semestral:4Média do segundosemestre: 4.40Média final: 4.2 -ExameDigite a nota do exame:8.5Aprovado em exame com média 6.33Calcular a média de outro aluno? [S]im ou [N]ão: S
Você tem pensamento computacional?9.1.4Plano de teste “Aprovado” diretoComando de prompt 36-Plano de teste 4 do desafioFonte: Elaborado pelo autor (2022)Depois de desenvolver a sua solução, efetue esses quatrotestes para ver se a sua solução chega aos mesmos valores.

Caso chegue, você passou no desafio.----------------------P R I M E I R O   S E M E S T R EDigite o checkpoint 1:6Digite o checkpoint 2:7Digite o checkpoint 3:8Média dos checkpoints: 7.5Digite o sprint 1:9Digite o sprint 2:10Média dos sprints: 9.5Digite a prova semestral:9Média do primeirosemestre: 8.80----------------------S E G U N D O   S E M E S T R EDigite o checkpoint 1:8Digite o checkpoint 2:7Digite o checkpoint 3:6Média dos checkpoints: 7.5Digite o sprint 1:7Digite o sprint 2:8Média dos sprints: 7.5Digite a prova semestral:9Média do segundosemestre: 8.40Média final: 8.6 -Aprovado!

Calcular a média de outro aluno?[S]im ou [N]ão: N
Você tem pensamento computacional?10 ANEXO –RESOLUÇÃO DO DESAFIOCada  um desenvolvea  solução  de  uma  forma,  o  importante  é  que  todos  os requisitos  sejam  atendidos.

Segue  a  correção  que foi  feita utilizando  os  conceitos apresentados neste capítulo:
```python
# -----------------DEFINIÇÃO DOS SUBALGORITMOS"""Verifica se uma nota é válida ou nãoPROTÓTIPO: notaValida(nota: Float): Boolean"""def notaValida(nota: float) -> bool:return nota >= 0 and nota <= 10"""Exibe uma mensagem de nota inválidaPROTÓTIPO: msgNotaInvalida(nota: Float): void"""def msgNotaInvalida(nota: float) -> None:print(f"A nota {nota} não é válida. \nDigite uma notaentre 0 e 10: ", end='')"""Retorna o menor entre três valoresPROTÓTIPO: menor3n(n1, n2, n3: Float): float"""def menor3n(n1, n2, n3: float) -> float:menor = n1if n2 < menor:menor = chk2if n3 < menor:menor = chk3return menor"""Calcular a média dos CheckPointsPROTÓTIPO: mediaCheckpoints(n1, n2, n3: Real): Real"""def mediaCheckpoints(n1, n2, n3: float) -> float:return (n1 + n2 + n3 -menor3n(n1, n2, n3)) / 2"""Calcular a média de 2 valoresPROTÓTIPO:media2n(n1, n2: Real): Real
Você tem pensamento computacional?"""def media2n(n1, n2: float) -> float:return (n1 + n2) / 2"""Calcular a porcentagem de um valorPROTÓTIPO: porcentagemValor(valor, percentual: Real): Real"""def porcentagemValor(valor, percentual: float) -> float:return valor * percentual"""Calcular a soma de 3 numerosPROTÓTIPO: soma3n(n1, n2, n3: Real): Real"""def soma3n(n1, n2, n3: float) -> float:return n1 + n2 + n3"""Calcular a soma de 2 numerosPROTÓTIPO: soma2n(n1, n2: Real): Real"""def soma2n(n1, n2: float) -> float:return n1 + n2"""Exibe se está aprovado ou reprovadoPROTÓTIPO: exibeStatus(media: Real): String"""def exibeStatusFunc(media: float) -> str:if media >= 6:return "Aprovado!"elif media < 4:return "Reprovado!"else:return "Exame""""Exibe se está aprovado ou reprovadoPROTÓTIPO: exibeStatus(media: Real): void"""def exibeStatusProc(media: float) -> None:if media >= 6:print("Aprovado!\n")elif media < 4:print("Reprovado!\n")
Você tem pensamento computacional?else:print("Exame\n")"""Exibe a mensagem de Aprovado ou Reprovado depois do examePROTÓTIPO: msgAprovReprovExame(mf: Real): void"""def msgAprovReprovExame(mf: float) -> None:if mf < 6:print(f"Reprovado em exame com média {mfinal}")else:print(f"Aprovado em exame com média {mfinal}")"""Verifica se foi digitado S de SimPROTÓTIPO: continua(op: string): Lógico"""def continua(op: str) -> bool:return op == "S" or op == "s""""Verifica se foi digitado S ou N de Sim ou NãoPROTÓTIPO: opcaoInvalida(op: string): Lógico"""def opcaoInvalida(op):return op != "s" and op != "S" and op != "n" and op != "N"# -------------------------PROGRAMA PRINCIPALopcao = 's'while continua(opcao):print("----------------------P R I M E I R O   S E M E S T R E")# Leitura dos checkPointschk1 = float(input("Digite o checkpoint 1:"))while not notaValida(chk1):msgNotaInvalida(chk1)chk1 = float(input())chk2 = float(input("Digite o checkpoint 2:"))while not notaValida(chk2):msgNotaInvalida(chk2)chk2 = float(input())chk3 = float(input("Digite o checkpoint 3:"))while not notaValida(chk3):
```

Você tem pensamento computacional?msgNotaInvalida(chk3)chk3 = float(input())
```python
# Calcula a média dos checkpoints do primeiro semestremediaChk = mediaCheckpoints(chk1, chk2, chk3)print(f"Média dos checkpoints: {mediaChk:.1f}\n")# Leitura dos Sprintssprint1 = float(input("Digite o sprint 1:"))while not notaValida(sprint1):msgNotaInvalida(sprint1)sprint1 = float(input())sprint2 = float(input("Digite o sprint 2:"))while not notaValida(sprint2):msgNotaInvalida(sprint2)sprint2 = float(input())# Calculando a média dos SprintsmediaSprint = media2n(sprint1, sprint2)print(f"Média dos sprints: {mediaSprint:.1f}\n")# Lendo a  nota da prova semestralprovaSemestral = float(input("Digite prova semestral:"))while not notaValida(provaSemestral):msgNotaInvalida(provaSemestral)provaSemestral = float(input())# Ponderando os valores das médiaspontosChk = porcentagemValor(mediaChk, 0.2)pontosSprints =porcentagemValor(mediaSprint, 0.2)pontosSemestral = porcentagemValor(provaSemestral, 0.6)# Cálculo da médiado primeiro semestremediaPrimeiroSemestre = soma3n(pontosChk, pontosSprints, pontosSemestral)print(f"Média do primeirosemestre: {mediaPrimeiroSemestre:.2f}\n")# Pontos obtidos no primeiro semestrepontosPrimeiroSemestre = porcentagemValor(mediaPrimeiroSemestre, 0.4)print("----------------------S E G U N D O   S E M E S T R E")# Leitura dos checkPointschk1 = float(input("Digite o checkpoint 1:"))while not notaValida(chk1):msgNotaInvalida(chk1)chk1 = float(input())
Você tem pensamento computacional?chk2 = float(input("Digite o checkpoint 2:"))while not notaValida(chk2):msgNotaInvalida(chk2)chk2 = float(input())chk3 = float(input("Digite o checkpoint 3:"))while not notaValida(chk3):msgNotaInvalida(chk3)chk3 = float(input())# Calcula a médiados checkpoints do primeiro semestremediaChk = mediaCheckpoints(chk1, chk2, chk3)print(f"Média dos checkpoints: {mediaChk:.1f}\n")# Leitura dos Sprintssprint1 = float(input("Digite o sprint 1:"))while not notaValida(sprint1):msgNotaInvalida(sprint1)sprint1 = float(input())sprint2 = float(input("Digite o sprint 2:"))while not notaValida(sprint2):msgNotaInvalida(sprint2)sprint2 = float(input())# Calculando a média dos SprintsmediaSprint = media2n(sprint1, sprint2)print(f"Média dos sprints: {mediaSprint:.1f}\n")# Lendo a  nota da prova semestralprovaSemestral = float(input("Digite prova semestral:"))while not notaValida(provaSemestral):msgNotaInvalida(provaSemestral)provaSemestral = float(input())# Ponderando os valores das médiaspontosChk = porcentagemValor(mediaChk, 0.2)pontosSprints = porcentagemValor(mediaSprint, 0.2)pontosSemestral = porcentagemValor(provaSemestral, 0.6)# Cálculo da médiado primeiro semestremediaSegundoSemestre = soma3n(pontosChk, pontosSprints, pontosSemestral)print(f"Média do segundosemestre: {mediaSegundoSemestre:.2f}\n\n")# Pontos obtidos no primeiro semestrepontosSegundoSemestre = porcentagemValor(mediaSegundoSemestre, 0.6)# Cálculo da média final
```

Você tem pensamento computacional?mediaFinal = soma2n(pontosPrimeiroSemestre, pontosSegundoSemestre)print(f"Média final: {mediaFinal:.1f} -", end="")exibeStatusProc(mediaFinal)if exibeStatusFunc(mediaFinal) == "Exame":
```python
# Leitura dos SprintsnotaExame = float(input("Digite a nota do exame:"))while not notaValida(notaExame):msgNotaInvalida(notaExame)notaExame = float(input())mfinal = media2n(mediaFinal, notaExame)msgAprovReprovExame(mfinal)opcao = input("Calcular a média de outro aluno? [S]im ou [N]ão.")while opcaoInvalida(opcao):opcao = input("ERRO!

Digite [S]im ou [N]ão:")print('''---------------------------------------Obrigado por utilizar o nosso programa!---------------------------------------''')Código-fonte 43-Correção do desafioFonte: Elaborado pelo autor (2022)
Você tem pensamento computacional?

REFERÊNCIASUFF.

Entendendo Recursão.17       maio 2015.

Disponível       em: <http://www.estatisticacomr.uff.br/?p=98>.

Acesso em: 27jun. 2024.

Você tem pensamento computacional?

GLOSSÁRIOSubalgoritmosPartes menores de códigos.

ModularizaçãoProgramar utilizando subalgoritmos.

Subalgoritmos nativosOs que vêm na instalação da linguagem.

Subalgoritmos própriosOs criados pelo programador.

ProcedimentoDefinição de subalgoritmo que não retorna valor.

FunçãoDefinição de subalgoritmo que retorna valor.

ParâmetrosIdentificadores que transportam valores entre algoritmos e subalgoritmos.

IdentificadorTudo aquilo que é armazenado na memória do computadorcomtipo variável.

Default Algo padrão.*argsTipo de parâmetro incontável.

EncadeadoDependente.

RecursividadeChamada sucessiva de si.

ImportComando para acessar outro arquivo
```
