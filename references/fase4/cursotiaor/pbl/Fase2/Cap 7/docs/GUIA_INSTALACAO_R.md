# 📊 Guia de Instalação e Execução - R

## 🎯 Objetivo

Este guia ajudará você a instalar o R e executar a análise estatística do Cap 7.

---

## 🖥️ Instalação do R

### Windows

#### 1. Download do R Base

1. Acesse: https://cran.r-project.org/bin/windows/base/
2. Clique em **"Download R-4.x.x for Windows"** (versão mais recente)
3. Arquivo: `R-4.x.x-win.exe` (~80 MB)

#### 2. Instalação

1. Execute o arquivo baixado
2. Escolha o idioma: **Português**
3. Aceite os termos de licença
4. Pasta de instalação: `C:\Program Files\R\R-4.x.x` (padrão)
5. Componentes: Marque **todas as opções**
6. Opções de inicialização: Padrão
7. Clique em **"Instalar"**
8. Aguarde conclusão (~2 minutos)

### Download do RStudio (OPCIONAL mas RECOMENDADO)

#### 1. Download

1. Acesse: https://posit.co/download/rstudio-desktop/
2. Role até **"2: Install RStudio"**
3. Clique em **"Download RStudio Desktop for Windows"**
4. Arquivo: `RStudio-202x.xx.x-xxx.exe` (~600 MB)

#### 2. Instalação

1. Execute o arquivo baixado
2. Clique em **"Próximo"** várias vezes
3. Aguarde instalação (~3 minutos)
4. Clique em **"Concluir"**

---

## ✅ Verificação da Instalação

### Teste 1: Abrir R Console

1. Pressione `Windows + R`
2. Digite: `R`
3. Pressione Enter

**Resultado esperado:**
```
R version 4.x.x (2024-xx-xx) -- "Nome da Versão"
Copyright (C) 2024 The R Foundation for Statistical Computing
Platform: x86_64-w64-mingw32/x64

Type 'demo()' for some demos, 'help()' for help.
>
```

### Teste 2: Executar comando simples

No console R, digite:
```r
print("R funcionando!")
mean(c(1, 2, 3, 4, 5))
```

**Resultado esperado:**
```
[1] "R funcionando!"
[1] 3
```

---

## 🚀 Executando a Análise Estatística

### Método 1: RStudio (RECOMENDADO)

#### Passo 1: Abrir RStudio
- Clique no ícone do RStudio na área de trabalho
- Ou procure "RStudio" no menu Iniciar

#### Passo 2: Abrir o script
1. Menu: **File → Open File...**
2. Navegue até: `C:\Fiap Projeto\Fase2\cursotiaor\pbl\Fase2\Cap 7\`
3. Selecione: `analise_R_grupo19.R`
4. Clique em **"Abrir"**

#### Passo 3: Definir diretório de trabalho
No console do RStudio (painel inferior esquerdo), digite:
```r
setwd("C:/Fiap Projeto/Fase2/cursotiaor/pbl/Fase2/Cap 7")
```

#### Passo 4: Executar o script completo
- **Opção A:** Clique no botão **"Source"** (canto superior direito do editor)
- **Opção B:** Pressione `Ctrl + Shift + Enter`
- **Opção C:** Menu: **Code → Run Region → Run All**

#### Passo 5: Visualizar resultados
- **Console:** Painel inferior esquerdo - Resultados textuais
- **Plots:** Painel inferior direito - Gráficos gerados
- Use as setas **← →** para navegar entre gráficos

### Método 2: R Console (Direto)

#### Passo 1: Abrir R Console
- Pressione `Windows + R`
- Digite: `R`
- Pressione Enter

#### Passo 2: Navegar até a pasta
```r
setwd("C:/Fiap Projeto/Fase2/cursotiaor/pbl/Fase2/Cap 7")
```

#### Passo 3: Executar o script
```r
source("analise_RM98765.R")
```

#### Passo 4: Visualizar gráficos
- Os gráficos abrirão em janelas separadas automaticamente
- Use `windows()` antes de plotar para abrir nova janela

### Método 3: Terminal (PowerShell/CMD)

```powershell
cd "C:\Fiap Projeto\Fase2\cursotiaor\pbl\Fase2\Cap 7"
Rscript analise_RM98765.R
```

---

## 📊 Entendendo a Interface do RStudio

```
┌─────────────────────────────────────────────────────────────┐
│  Menu: File  Edit  Code  View  Plots  Session  Build  Help  │
├──────────────────────────┬──────────────────────────────────┤
│                          │                                  │
│  EDITOR (Script R)       │  ENVIRONMENT                     │
│  • Código do script      │  • Variáveis carregadas          │
│  • Edição de código      │  • Objetos em memória            │
│  • Syntax highlighting   │  • Datasets                      │
│                          │                                  │
├──────────────────────────┼──────────────────────────────────┤
│                          │                                  │
│  CONSOLE (R)             │  PLOTS / FILES / HELP            │
│  • Execução de comandos  │  • Gráficos gerados              │
│  • Resultados textuais   │  • Navegação de arquivos         │
│  • Mensagens de erro     │  • Documentação (help)           │
│                          │                                  │
└──────────────────────────┴──────────────────────────────────┘
```

---

## 🎨 Navegando pelos Gráficos

### No RStudio

**Painel "Plots" (inferior direito):**
- **Setas ← →** - Navegar entre gráficos
- **Zoom** - Ampliar gráfico em janela separada
- **Export** - Salvar como PNG, PDF, JPEG
- **Broom** (vassoura) - Limpar todos os gráficos

### Salvando Gráficos

#### Método 1: Botão Export
1. No painel "Plots", clique em **"Export"**
2. Escolha **"Save as Image..."**
3. Formato: PNG (recomendado)
4. Dimensões: 800x600 pixels (padrão)
5. Clique em **"Save"**

#### Método 2: Via código
```r
# Salvar gráfico atual
png("grafico_area_plantada.png", width = 800, height = 600)
hist(dados$area_plantada_ha, main = "Área Plantada")
dev.off()
```

---

## 📈 Ordem de Execução dos Gráficos

O script gerará **8 gráficos** nesta ordem:

### Variável Quantitativa (4 gráficos)
1. **Histograma** - Área Plantada
2. **Boxplot** - Área Plantada
3. **Curva de Densidade** - Área Plantada
4. **Q-Q Plot** - Teste de Normalidade

### Variável Qualitativa Nominal (2 gráficos)
5. **Gráfico de Barras** - Região
6. **Gráfico de Pizza** - Região

### Variável Qualitativa Ordinal (1 gráfico)
7. **Gráfico de Barras** - Porte da Propriedade

### Variável Quantitativa Discreta (1 gráfico)
8. **Histograma** - Número de Propriedades

---

## 🔧 Comandos Úteis do R

### Navegação
```r
# Ver diretório atual
getwd()

# Mudar diretório
setwd("C:/Fiap Projeto/Fase2/cursotiaor/pbl/Fase2/Cap 7")

# Listar arquivos no diretório
list.files()
```

### Dados
```r
# Carregar dados
dados <- read.csv("dados_agronegocio_RM98765.csv")

# Ver estrutura
str(dados)

# Primeiras linhas
head(dados)

# Resumo estatístico
summary(dados)
```

### Ajuda
```r
# Ajuda sobre função
?mean
help(median)

# Exemplos de uso
example(hist)
```

### Limpeza
```r
# Limpar console
cat("\014")  # Ou: Ctrl + L

# Limpar ambiente (variáveis)
rm(list = ls())

# Limpar gráficos
dev.off()
```

---

## 🐛 Problemas Comuns

### Erro: "cannot open file"

**Causa:** Diretório errado

**Solução:**
```r
# Verificar diretório atual
getwd()

# Corrigir (use / ou \\)
setwd("C:/Fiap Projeto/Fase2/cursotiaor/pbl/Fase2/Cap 7")
```

### Erro: "object 'dados' not found"

**Causa:** Dados não carregados

**Solução:**
```r
dados <- read.csv("dados_agronegocio_RM98765.csv", header = TRUE)
```

### Erro: "could not find function 'read.csv'"

**Causa:** Pacote não carregado (raro - read.csv é base)

**Solução:** Reiniciar R/RStudio

### Gráficos não aparecem

**Causa:** Device gráfico fechado

**Solução:**
```r
# Abrir novo device
windows()  # Windows
# x11()     # Linux
# quartz()  # Mac
```

### Script trava ou demora

**Causa:** Processamento pesado

**Solução:**
- Espere alguns segundos
- Ou pressione `Esc` para interromper

---

## 📦 Pacotes Adicionais (Opcional)

O script básico usa apenas funções do R base. Para análises avançadas:

### Instalar pacotes
```r
# Pacotes úteis para estatística
install.packages("ggplot2")   # Gráficos avançados
install.packages("dplyr")     # Manipulação de dados
install.packages("tidyr")     # Limpeza de dados
install.packages("readxl")    # Ler arquivos Excel

# Carregar pacotes
library(ggplot2)
library(dplyr)
```

---

## ✅ Checklist de Execução

Antes de submeter para FIAP, verifique:

- [ ] R instalado e funcionando
- [ ] RStudio instalado (opcional)
- [ ] Arquivo `analise_RM98765.R` criado
- [ ] Primeira linha com identificação correta:
  ```r
  # SeuNomeCompleto_SEURM_fase2_cap7
  ```
- [ ] Arquivo `dados_agronegocio_RM98765.csv` com 30+ linhas
- [ ] Script executa sem erros
- [ ] 8 gráficos são gerados corretamente
- [ ] Resultados aparecem no console
- [ ] README.md criado com explicações

---

## 📚 Recursos de Aprendizado

### Tutoriais Online
- **R para Iniciantes:** https://cran.r-project.org/doc/manuals/r-release/R-intro.html
- **RStudio Education:** https://education.rstudio.com/
- **DataCamp:** https://www.datacamp.com/courses/free-introduction-to-r

### Vídeos YouTube
- **Estatística com R** - Buscar tutoriais em português
- **RStudio Tutorial** - Interface e básico

### Livros Gratuitos
- **R for Data Science:** https://r4ds.had.co.nz/
- **Modern Statistics for Modern Biology:** https://www.huber.embl.de/msmb/

---

## 🎓 Próximos Passos

Após completar esta análise:

1. **Personalizar RM:** Trocar `RM98765` pelo seu RM real
2. **Ajustar dados:** Usar dados reais de CONAB/IBGE se preferir
3. **Expandir análises:** Adicionar testes de hipótese, correlações
4. **Integrar com Cap 6:** Combinar dados Python + análise R

---

**FarmTech Solutions - Grupo 59 FIAP**  
**Data:** 12/10/2025  
**Versão:** 1.0
