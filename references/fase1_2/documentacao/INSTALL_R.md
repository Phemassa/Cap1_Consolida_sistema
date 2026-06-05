# ⚙️ Guia de Instalação - Scripts R

**Configuração Completa do Ambiente R para FarmTech Solutions**

Este guia fornece instruções detalhadas para configurar o ambiente R necessário para executar as análises estatísticas e coleta de dados meteorológicos.

## 📋 Pré-requisitos

### Sistema Operacional
- ✅ **Windows 10/11** (recomendado)
- ✅ **Linux Ubuntu 18.04+**
- ✅ **macOS 10.15+**

### Requisitos de Hardware
- **RAM**: Mínimo 4GB, recomendado 8GB+
- **Espaço em disco**: 2GB livres
- **Processador**: Qualquer CPU moderna
- **Conexão**: Internet para APIs e instalação de pacotes

## 🚀 Instalação do R

### Windows

#### Método 1: Download Oficial (Recomendado)
1. **Acesse**: https://cran.r-project.org/bin/windows/base/
2. **Download**: Clique em "Download R x.x.x for Windows"
3. **Execute**: O instalador `.exe` baixado
4. **Configuração**: Use as opções padrão
5. **Verificação**: Abra o R Console e digite `version`

#### Método 2: Via Chocolatey
```powershell
# Execute como Administrador
choco install r.project
```

#### Método 3: Via Winget
```powershell
winget install RProject.R
```

### Linux (Ubuntu/Debian)

#### Atualização do Sistema
```bash
sudo apt update
sudo apt upgrade -y
```

#### Instalação do R
```bash
# Instalar R base
sudo apt install r-base r-base-dev -y

# Dependências para compilação de pacotes
sudo apt install build-essential libcurl4-openssl-dev libssl-dev libxml2-dev -y
```

#### Verificação
```bash
R --version
```

### macOS

#### Método 1: Download Oficial
1. **Acesse**: https://cran.r-project.org/bin/macosx/
2. **Download**: R-x.x.x.pkg
3. **Instale**: Duplo clique no arquivo `.pkg`

#### Método 2: Via Homebrew
```bash
brew install r
```

## 📦 Instalação de Pacotes R

### Método Automático (Recomendado)

Os scripts R do FarmTech Solutions possuem instalação automática de dependências:

```r
# Os scripts verificam e instalam automaticamente
if (!require('readr')) install.packages('readr', repos='https://cran.r-project.org/', dependencies=TRUE)
if (!require('httr')) install.packages('httr', dependencies=TRUE)
```

### Método Manual

#### Via R Console
```r
# Abra o R Console e execute:
install.packages(c("readr", "httr"), dependencies=TRUE)
```

#### Via RScript (linha de comando)
```bash
Rscript -e "install.packages(c('readr', 'httr'), dependencies=TRUE)"
```

### Pacotes Necessários

| Pacote | Versão Mín. | Descrição | Uso no Projeto |
|--------|-------------|-----------|----------------|
| `readr` | 2.0.0 | Leitura eficiente de CSV | Importar dados do Python |
| `httr` | 1.4.0 | Requisições HTTP | API meteorológica |

### Pacotes Opcionais (Futuros)
```r
# Para visualizações avançadas
install.packages("ggplot2")

# Para manipulação de dados
install.packages("dplyr")

# Para relatórios
install.packages("rmarkdown")
```

## 🔧 Configuração do Ambiente

### Configuração de Repositório CRAN
```r
# Definir repositório padrão (melhor performance)
options(repos = c(CRAN = "https://cran.rstudio.com/"))

# Para usuários no Brasil
options(repos = c(CRAN = "https://cran-r.c3sl.ufpr.br/"))
```

### Configuração de Encoding
```r
# Windows - Para caracteres especiais
Sys.setlocale("LC_ALL", "Portuguese_Brazil.1252")

# Linux/Mac - UTF-8
Sys.setlocale("LC_ALL", "pt_BR.UTF-8")
```

### Configuração de Proxy (se necessário)
```r
# Configurar proxy corporativo
Sys.setenv(http_proxy = "http://proxy.empresa.com:8080")
Sys.setenv(https_proxy = "https://proxy.empresa.com:8080")
```

## 🧪 Teste da Instalação

### Teste Básico do R
```r
# 1. Verificar versão
version

# 2. Teste de operação matemática
2 + 2

# 3. Teste de criação de variável
teste <- "FarmTech Solutions"
print(teste)
```

### Teste dos Pacotes
```r
# 1. Testar readr
library(readr)
data.frame(a=1:3, b=4:6) |> write_csv("teste.csv")
read_csv("teste.csv")
file.remove("teste.csv")

# 2. Testar httr
library(httr)
res <- GET("https://httpbin.org/get")
status_code(res)  # Deve retornar 200
```

### Teste dos Scripts do Projeto

#### Estrutura de Teste
```bash
FarmTechSolutions/
├── python_app/
│   ├── banana.csv     # Deve existir
│   └── milho.csv      # Deve existir
└── r_app/
    ├── analise.R
    └── clima.R
```

#### Teste do analise.R
```bash
cd FarmTechSolutions/r_app
Rscript analise.R
```

**Saída Esperada**:
```
Script executado!
--- Estatísticas Banana ---
Média comprimento: [valor]
...
```

#### Teste do clima.R
```bash
cd FarmTechSolutions/r_app
Rscript clima.R
```

**Saída Esperada**:
```
Tempo atual em São Paulo:
Temperatura: [valor]°C
...
```

## 🔍 Resolução de Problemas

### Problema 1: R não é reconhecido no terminal

#### Windows
```powershell
# Verificar se R está no PATH
where R

# Se não estiver, adicionar manualmente:
# C:\Program Files\R\R-x.x.x\bin
```

#### Linux/Mac
```bash
# Verificar instalação
which R

# Se não encontrado, reinstalar
sudo apt install r-base  # Ubuntu
brew install r           # Mac
```

### Problema 2: Erro de permissão na instalação de pacotes

#### Windows (Executar como Administrador)
```r
# Instalar em diretório de usuário
install.packages("readr", lib="~/R/library")
```

#### Linux
```bash
# Instalar dependências do sistema
sudo apt install libcurl4-openssl-dev libssl-dev libxml2-dev
```

### Problema 3: Erro de conexão com CRAN

#### Trocar Mirror CRAN
```r
# Listar mirrors disponíveis
getCRANmirrors()

# Usar mirror específico
options(repos = c(CRAN = "https://cloud.r-project.org/"))
```

#### Instalação Manual
```bash
# Download manual do pacote
wget https://cran.r-project.org/src/contrib/readr_2.1.4.tar.gz
R CMD INSTALL readr_2.1.4.tar.gz
```

### Problema 4: Erro na API meteorológica

#### Verificar Conectividade
```r
# Teste de conexão básica
library(httr)
res <- GET("https://httpbin.org/get")
status_code(res)  # Deve ser 200
```

#### Configuração de Timeout
```r
# Aumentar timeout para conexões lentas
library(httr)
res <- GET(url, timeout(30))  # 30 segundos
```

## 🎯 IDEs Recomendados

### RStudio (Recomendado)
```bash
# Download: https://www.rstudio.com/products/rstudio/download/
# Recursos: Autocomplete, debugging, visualização
```

### VS Code com Extensão R
```bash
# Instalar extensão: R Extension for Visual Studio Code
# Configurar: R.exe path nas configurações
```

### Jupyter com IRkernel
```r
# Instalar IRkernel
install.packages("IRkernel")
IRkernel::installspec()

# Usar: jupyter notebook
```

## 📊 Configuração para Produção

### Script de Inicialização
Crie um arquivo `setup_r_environment.R`:

```r
#!/usr/bin/env Rscript

# FarmTech Solutions - Setup do Ambiente R
cat("Configurando ambiente R para FarmTech Solutions...\n")

# 1. Configurar repositório
options(repos = c(CRAN = "https://cran.rstudio.com/"))

# 2. Instalar pacotes necessários
pacotes_necessarios <- c("readr", "httr")
pacotes_faltantes <- setdiff(pacotes_necessarios, installed.packages()[,"Package"])

if (length(pacotes_faltantes) > 0) {
  cat("Instalando pacotes:", paste(pacotes_faltantes, collapse=", "), "\n")
  install.packages(pacotes_faltantes, dependencies=TRUE)
}

# 3. Verificar instalações
for (pacote in pacotes_necessarios) {
  if (require(pacote, character.only=TRUE)) {
    cat("✅", pacote, "instalado com sucesso\n")
  } else {
    cat("❌ Erro ao instalar", pacote, "\n")
  }
}

# 4. Teste de conectividade
tryCatch({
  library(httr)
  res <- GET("https://api.open-meteo.com/v1/forecast?latitude=-23.55&longitude=-46.63&current_weather=true")
  if (status_code(res) == 200) {
    cat("✅ Conectividade com API meteorológica OK\n")
  } else {
    cat("⚠️  API meteorológica não acessível\n")
  }
}, error = function(e) {
  cat("❌ Erro na conectividade:", e$message, "\n")
})

cat("✅ Configuração concluída!\n")
```

### Execução do Setup
```bash
Rscript setup_r_environment.R
```

## 🔄 Automação e Agendamento

### Windows - Task Scheduler
```batch
@echo off
cd "C:\Caminho\Para\FarmTechSolutions\r_app"
Rscript analise.R >> logs\analise.log 2>&1
Rscript clima.R >> logs\clima.log 2>&1
```

### Linux - Crontab
```bash
# Editar crontab
crontab -e

# Executar análise diária às 8h
0 8 * * * cd /caminho/para/FarmTechSolutions/r_app && Rscript analise.R

# Dados meteorológicos a cada 6h
0 */6 * * * cd /caminho/para/FarmTechSolutions/r_app && Rscript clima.R
```

### Docker (Avançado)
```dockerfile
FROM r-base:4.3.0

WORKDIR /app
COPY r_app/ ./
COPY python_app/*.csv ./data/

RUN R -e "install.packages(c('readr', 'httr'), dependencies=TRUE)"

CMD ["Rscript", "analise.R"]
```

## ✅ Checklist de Instalação

### Básico
- [ ] R instalado (versão 3.6.0+)
- [ ] Pacotes `readr` e `httr` instalados
- [ ] Scripts executam sem erro
- [ ] Conectividade com internet funcionando

### Avançado
- [ ] IDE configurado (RStudio/VS Code)
- [ ] Encoding UTF-8 configurado
- [ ] Proxy configurado (se necessário)
- [ ] Logs de execução configurados
- [ ] Agendamento configurado (se desejado)

### Produção
- [ ] Script de setup automatizado
- [ ] Monitoramento de erros
- [ ] Backup de dados configurado
- [ ] Documentação atualizada

---

**Guia de Instalação R v1.0.0**
*Configuração completa para análises agrícolas* 📊🌱

**Suporte**: Consulte [TECHNICAL_DOCS_R.md](./TECHNICAL_DOCS_R.md) para detalhes técnicos
