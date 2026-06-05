# Cap 7 - Decolando com ciências de dados

## Sumário

# Cap 7 - Decolando com ciências de dados

Decolando com ciências de dadosCálculo da Variância:representa a variabilidade ao redor da média, porém, esta  medida  altera  a  grandeza  dos  dados  (é  uma  medida  quadrática,  ou seja, os valores são elevados ao quadrado, não podendo ser utilizada para fins interpretativos, apenas como parâmetro de análise).Cálculo do Desvio Padrão: representaa variabilidade dos dados ao redor da média, desta vez, na grandeza correta dos dados.Cálculo do Coeficiente de Variação: representa uma medida relativa entre o desvio  padrão  e  a  média,  sendo  representado  em  porcentagem.

Se  o resultado for menor que 10%, a variabilidade dos dados é classificada como baixa.

Se o resultado estiver entre 10 e 20%, a variabilidade dos dados é classificada  como  média.

Se  o  resultado  estiverentre  20  e  30%,  a variabilidade dos dados é classificada como alta.

E se o resultado for maior do que 30%, a variabilidade dos dados é classificada como muito alta.

Medidas Separatrizes:Quartil:  são  os  valores  que  dividem  um  conjunto  de  dados  em  4 partes iguais, de 25 em 25%.Decil:  são  os  valores  que  dividem  um  conjunto  de  dados  em  10  partes iguais, de 10 em 10%.Centil: são os valores que dividem um conjunto de dados em 100 partes iguais, de 1 em 1%.

Agora,  aplicamos  esses  conceitos  a  um  conjunto  de  dados  prático,  e  então, vamos supor que temos dados de vendas mensais de uma loja.```R# Criando a base de dados de vendas mensais:vendas <-c(120, 150, 130, 170, 200, 180, 160, 190, 150)# Calculando a Média:media_vendas <-mean(vendas)
Decolando com ciências de dados# Calculando a Mediana:mediana_vendas <-median(vendas)# Calculando a Moda: Baixar e habilitar o pacote DescToolsmoda_vendas <-Mode(vendas)# Máximo:máximo_vendas <-max(vendas)#Mínimo:mínimo_vendas <-min(vendas)# Calculando a Amplitude:amplitude_vendas <-diff(range(vendas) # Calculando a Variância:variancia_vendas <-var(vendas)# Calculando o Desvio Padrão:desvio_padrao_vendas <-sd(vendas)# Calculando o Coeficiente de Variação:cv_vendas <-(sd(vendas)/mean(vendas))*100 # Calculando os Quartis:quartis_vendas <-quantile(vendas, probs=c(0.25, 0.50, 0.75))# Calculando os Decis:decis_vendas <-quantile(vendas, probs = seq(0.1, 0.9, by = 0.1))# Calculando os Centis:centis_vendas <-quantile(x, probs = seq(0.01, 0.99, by = 0.01)) ́ ́ ́
Decolando com ciências de dadosNeste  exemplo  em  R,  foram  utilizadas  as  funções  básicas  para  calcular medidas  descritivas  do  conjunto  de  dados  de  vendas.

A  função ‘mean’calcula  a Média, ‘median’para a Mediana, ‘Mode’para a Moda, ‘max’para o Máximo, ‘min’para oMínimo,‘diff(range())’para a Amplitude, ‘var’ para a Variância,‘sd’para o Desvio Padrão, ‘(sd()/mean())*100’ para o Coeficiente de Variação, ‘quantile’ para os Quartis, Decis e Centis.

Estas funções são fundamentais na análise descritiva e oferecem uma visão  rápida  do  comportamento  dos  dados.

A  análise  descritiva  de  dados  é  um componente  fundamental  da  análise  de  dados,  fornecendo  um  entendimento  do conjunto  de  dados  em  análise.

Utilizando  a Linguagem  R,  podemos  efetivamente resumir e visualizar dados, o que é essencial para qualquer análise posterior, seja ela preditiva, inferencial ou para tomada de decisões baseadas em dados.1.3 Análise Inferencialde Dados com RA  Estatística  Inferencial é  a  parte  da  Estatística que busca  fazer  afirmações, por  meio  de Testesde  Hipótese,  sobre  características  de  uma população(que possui parâmetros),   com   base   nas amostrasdesta   população   (que   possui estimadores).

Exemplos de hipóteses estatísticas:A droga 1 é tão eficiente quanto a droga 2.A altura média da população brasileira é de 1,65m.A proporção de paulistas com a doença X é de 62%.Homens e mulheres realizam a tarefa Y em um mesmo intervalo de tempo.

Para   que   isso   seja   feito,   é   necessário   conhecer   a Distribuição   de Probabilidade do fenômeno e aplicar o Teste de Hipótese apropriado.

Entre  todas  as  Distribuições  de  Probabilidade  que  existem, a  mais  utilizada para explicar fenômenos é a Distribuição Normal, representada no gráfico a seguir:
Decolando com ciências de dadosFigura 1-Curva de DistribuiçãoNormalFonte: Elaborado pelo autor(2024)O gráfico mostraque a probabilidade de um evento aleatório ocorrer, quanto mais próximo da média (μ) ele for, maior sua probabilidade de ocorrência, e quanto mais afastado da média, menor a sua probabilidade de ocorrência.

O desvio padrão (σ) representa a variabilidade dos dados.

Quanto maior o desvio padrão, mais larga será a curva e quanto menor o desvio padrão, menos larga será a curva.

Um  Teste  de  Hipótese  pode  ser  entendido  como  uma  regra  de  decisão  que consiste    em aceitar    ou    rejeitar    H0,    baseado    nos    dados    amostrais.

As hipóteses estatísticas são:H0= Hipótese Nula: representa a afirmação, igualdade.H1ou Ha= Hipótese Alternativa:representa o complemento de H0.

Para  resolver  problemas  de  Teste  de  Hipótese,  podemos  utilizar  várias metodologias diferentes.

Pelo método da Região Crítica, devemos seguir os seguintes passos para realizar o Teste de Hipótese:1)Enunciar as Hipóteses H0 e H1.2)Fixar o Nível de Significância (α), que é a margem de erro, e identificar a Distribuição de Probabilidade associada ao teste (Normal, t-Student, F, x², ...).

Decolando com ciências de dados3)Determinar as regiões de aceitação e rejeição de H0, baseados em H1 e no α (é necessário ter as respectivas tabelas de Distribuição de Probabilidade quando realizado manualmente).4)Calcular a estatística do teste.5)Aceitar ou rejeitar H0 com base em 3) e 4).

Agora, vamos aplicar esses conceitos a uma situação prática: um comprador de tijolos acha que a qualidade dos tijolos está diminuindo.

Ao observarexperiências anteriores, considerouque a resistência média ao desmoronamento de tais tijolos é igual  a  200  kg,  com  um  desviopadrão  de  10  kg.

Uma  amostra  de  100  tijolos, escolhidos ao acaso, forneceu uma média de 195 kg.

Ao nível de significância de 5%, pode-se afirmar que a resistência média ao desmoronamento diminuiu?```RDeclarar as hipóteses: H0 : μ ≥ 200 kg  , e definir as regiões de aceitação e H1 : μ < 200 kg                                                  rejeiçãoEncontrar o valor de Zc: Zc <-(195 –200)/(10/sqrt(100))Encontrar o valor de Zα: Za <-qnorm(0.05)Decisão: ifelse (Zc < Za, "Rejeita Ho", "Aceita Ho") ́ ́ ́Portanto,   ao   nível   de   significância   de   5%,   a   resistência   média   ao desmoronamento diminuiu.1.4Visualização dos DadosAlém das medidas estatísticas, asvisualizações gráficas são parte importante da análise descritiva.

Decolando com ciências de dadosO tipo de gráfico depende da natureza da variável em análise:Variável  Qualitativa: para  variáveis  que  representam  categorias  ou nomes,  utiliza-se  o  Gráfico  de  Barras  Horizontais, Gráfico  de  Barras Verticais ou o Gráfico de Setores (pizza);Variável  Quantitativa: para  variáveis  que  representam  números  ou medidas, utiliza-se o Histograma ou Boxplot.

Vamos criarum gráfico de barras para visualizar as vendas mensaisdo primeiro exemplo.```R
```python
# Carregando o pacote ggplot2 para visualizaçãoinstall.packages("ggplot2")library(ggplot2)# Criando um data frame para os dados de vendasdados_vendas <-data.frame(Mês = 1:9, Vendas = vendas)# Criando um gráfico de barrasggplot(dados_vendas, aes(x=Mês, y=Vendas)) +geom_bar(stat="identity", fill="blue") +ggtitle("Vendas Mensais") +xlab("Mês") +ylab("Vendas")```Neste script, foi utilizado o `ggplot2`, um pacote que faz parte do Tidyverse para criar  gráficos personalizados em  R. É  importante  destacar  que  o  R  gera  gráficos automaticamente  sem  a  necessidade  de  utilizar  pacotes  adicionais.

Foi  utilizado  o pacote `ggplot2`apenas para deixar o gráfico mais elegante, atrativo e personalizado.

Decolando com ciências de dadosO  gráfico  de  barras geradooferece  uma  visualização  clara  das  vendas mensais,  facilitando  a  identificação  de  padrões  ou  tendências,  como  meses  com desempenho de vendas acima ou abaixo da média.1.5Estudo de Caso1: Análise do Desempenho de Modelos de IA do tipo PLN (Processamento de Linguagem Natural)Considereque você estáanalisando o desempenho de diferentes modelos de Processamento  de Linguagem Natural (PLN) em  uma  tarefa  de  classificação  de sentimentos  em  uma  escala  de  1  a  5 pontos (1  para  sentimento  negativo  e  5  para sentimento  positivo).

Osresultados  para  um  conjunto  de  20  amostras  são  os seguintes:3, 4, 2,5, 3,2, 4,4,3,5,4,2,3,4,4,5,2,3,4,4.

Faça a análise descritiva completa desse conjunto de dados. ```R# Criando a base de dados:dados <-c(3,   4,   2,   5,   3,   2,   4,   4,   3,   5,   4,   2,   3,   4,   4,   5,   2,   3,   4,   4)# Calculando a Média:media_dados <-mean(dados)# Calculando a Mediana:mediana_dados <-median(dados)# Calculando a Moda: Baixar e habilitar o pacote DescToolsmoda_dados <-Mode(dados)# Máximo:máximo_dados <-max(dados)#Mínimo:mínimo_dados <-min(dados)# Calculando a Amplitude:
```

Decolando com ciências de dadosamplitude_dados <-diff(range(dados) # Calculando a Variância:variancia_dados <-var(dados)# Calculando o Desvio Padrão:desvio_padrao_dados <-sd(dados)# Calculando o Coeficiente de Variação:cv_dados <-(sd(dados)/mean(dados))*100 # Calculando os Quartis:quartis_dados <-quantile(dados, probs=c(0.25, 0.50, 0.75))# Calculando os Decis:decis_dados <-quantile(dados, probs = seq(0.1, 0.9, by = 0.1))# Calculando os Centis:centis_dados <-quantile(dados, probs = seq(0.01, 0.99, by = 0.01))```1.6Estudo de Caso2: Inferência sobre a precisão média de modelos preditivosUm  sistema  de inteligência artificialestá  sendo  utilizado  para  avaliar  a qualidade  das  previsões  de  demanda  de  um  produto  em  uma  empresa  de  e-commerce.

Historicamente, a precisão média das previsões da demanda do produto é  de  200  unidades,  com  um  desvio  padrão  de  10  unidades.

Recentemente,  a  IA coletou uma amostra aleatória de 100 previsões e calculou a precisão média dessa amostra,  que  foi  de 195  unidades.

Utilizando  um  nível  de  significância  de 5%,  a  IA deve determinar se a precisão média das previsões realmente diminuiu.

Decolando com ciências de dados```RDeclarar as hipóteses: H0 : μ ≥ 200 unidades, e definir as regiões de aceitação H1 : μ < 200unidadeserejeiçãoEncontrar o valor de Zc: Zc <-(195 -200)/(10/sqrt(100))Encontrar o valor de Zα: Za <-qnorm(0.05)Decisão: ifelse (Zc < Za, "Rejeita Ho", "Aceita Ho")```Portanto,  ao  nível  de  significância  de  5%,  a precisãomédia de  produtos diminuiu.

Decolando com ciências de dados## Referências

FAVERO, L..

P., Belfiore, P., & de Freitas Souza, R. (2023).

Data science, analytics and machine learning with R.

Academic Press.

GELMAN,    A..,    &    Hill,    J.    (2006).

Data    analysis    using    regression    and multilevel/hierarchical models.

Cambridge university press.

MORETTIN, P..

A., & Singer, J. da M. (2022).

Estatísticae ciência de dados.

TREVOR, H.., Robert, T., & Jerome, F. (2009).

The elements of statistical learning: Data mining, inference, and prediction.

Spinger.

WICKHAM, H.., Çetinkaya-Rundel, M., & Grolemund, G. (2023).

R for data science.

O’Reilly Media,Inc.
