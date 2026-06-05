# Guia de Instalação e Configuração - FarmTech Solutions

## 🚀 Instalação Rápida

### Pré-requisitos
- **Python 3.6+** instalado no sistema
- **Terminal/Prompt de Comando** disponível
- **Sistema Operacional**: Windows, Linux ou macOS

### Verificar Instalação do Python
```bash
python --version
# ou
python3 --version
```

### Download do Projeto
1. **Opção 1 - Git Clone:**
```bash
git clone https://github.com/Phemassa/FarmTechSolutions.git
cd FarmTechSolutions/python_app
```

2. **Opção 2 - Download Direto:**
- Baixe o arquivo ZIP do repositório
- Extraia para uma pasta de sua escolha
- Navegue até a pasta `python_app`

## 📦 Instalação de Dependências

### Utilizando requirements.txt
```bash
# Navegar até a pasta do projeto
cd python_app

# Instalar dependências (apenas bibliotecas padrão)
# Não há dependências externas necessárias
```

### Dependências do Sistema
O projeto utiliza apenas bibliotecas padrão do Python:
- `csv` - Manipulação de arquivos CSV
- `os` - Operações do sistema operacional  
- `re` - Expressões regulares

## 🔧 Configuração Inicial

### Estrutura de Diretórios
Certifique-se de que a estrutura está assim:
```
python_app/
├── main.py              # ✅ Arquivo principal
├── requirements.txt     # ✅ Lista de dependências
├── README.md           # ✅ Documentação principal
├── TECHNICAL_DOCS.md   # ✅ Documentação técnica
├── INSTALL.md          # ✅ Este arquivo
├── banana.csv          # ⚡ Criado automaticamente
├── milho.csv           # ⚡ Criado automaticamente
├── gerador_exemplos.py # 🔧 Gerador de dados teste
└── teste.txt           # 📝 Arquivo de teste
```

### Arquivos Gerados Automaticamente
- `banana.csv` - Criado na primeira execução
- `milho.csv` - Criado na primeira execução

## ▶️ Primeira Execução

### Comando de Execução
```bash
# Windows
python main.py

# Linux/macOS
python3 main.py
```

### Teste de Funcionamento
1. Execute o programa
2. Selecione opção **"1. Entrada de dados"**
3. Escolha **"1. Banana"**
4. Complete um registro de teste
5. Selecione opção **"2. Saída de dados"** para verificar

## 🔍 Verificação de Instalação

### Checklist de Funcionamento
- [ ] O programa inicia sem erros
- [ ] Menu principal é exibido
- [ ] Entrada de dados funciona
- [ ] Saída de dados exibe informações
- [ ] Arquivos CSV são criados
- [ ] Navegação com "X" funciona
- [ ] Validação de entrada funciona

### Comandos de Teste
```bash
# Verificar se arquivos foram criados
ls -la *.csv

# Ver conteúdo dos CSVs (Linux/macOS)
cat banana.csv
cat milho.csv

# Ver conteúdo dos CSVs (Windows)
type banana.csv
type milho.csv
```

## 🐛 Solução de Problemas

### Erro: "Python não encontrado"
**Solução:**
```bash
# Verificar se Python está no PATH
which python
which python3

# Instalar Python se necessário
# Windows: Download do python.org
# Ubuntu: sudo apt install python3
# macOS: brew install python3
```

### Erro: "Arquivo não encontrado"
**Solução:**
```bash
# Verificar se está na pasta correta
pwd
ls -la

# Navegar para pasta correta
cd caminho/para/python_app
```

### Erro: "Permissão negada"
**Solução:**
```bash
# Linux/macOS - Dar permissão de execução
chmod +x main.py

# Windows - Executar como Administrador
```

### Erro: "Encoding/Caracteres especiais"
**Solução:**
- O sistema usa UTF-8 por padrão
- Certifique-se de que o terminal suporta UTF-8
- No Windows, use `chcp 65001` antes de executar

## ⚙️ Configurações Avançadas

### Modificar Insumos Padrão
No arquivo `main.py`, localizar e modificar:
```python
insumos_exemplo = [
    "Fosfato",
    "Nitrogênio", 
    "Potássio",
    "Pulverizar 500 mL/metro",
    "Herbicida",
    "Inseticida",
    "Outro (digite manualmente)"
]
```

### Modificar Unidades Padrão
```python
unidades = ["mL", "L", "kg", "g", "Outro (digite manualmente)"]
```

### Alterar Nomes dos Arquivos CSV
```python
# Na função salvar_dados()
with open('banana.csv', 'w', newline='', encoding='utf-8') as f:
with open('milho.csv', 'w', newline='', encoding='utf-8') as f:
```

## 📊 Geração de Dados de Teste

### Usar Gerador de Exemplos
```bash
# Executar gerador (se disponível)
python gerador_exemplos.py
```

### Criar Dados Manualmente
1. Execute o programa
2. Use opção "1. Entrada de dados"
3. Adicione vários registros para teste

## 🔐 Configurações de Segurança

### Backup de Dados
```bash
# Criar backup dos CSVs
cp banana.csv banana_backup.csv
cp milho.csv milho_backup.csv

# Windows
copy banana.csv banana_backup.csv
copy milho.csv milho_backup.csv
```

### Restaurar Backup
```bash
# Restaurar de backup
cp banana_backup.csv banana.csv
cp milho_backup.csv milho.csv
```

## 🌐 Ambientes de Desenvolvimento

### Visual Studio Code
1. Instale a extensão Python
2. Abra a pasta `python_app`
3. Configure o interpretador Python
4. Use F5 para debug

### PyCharm
1. Abra projeto na pasta `python_app`
2. Configure interpretador Python
3. Execute `main.py`

### Terminal/Linha de Comando
```bash
# Navegação básica
cd python_app
python main.py

# Com debug (se necessário)
python -u main.py
```

## 📈 Monitoramento e Logs

### Verificar Arquivos Gerados
```bash
# Tamanho dos arquivos
ls -lh *.csv

# Número de registros
wc -l *.csv

# Últimas modificações
ls -lt *.csv
```

### Debug Mode (Opcional)
Para ativar debug, adicione no início do `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔄 Atualizações

### Verificar Versão Atual
Verifique comentários no `main.py` ou `README.md`

### Atualizar Sistema
1. Faça backup dos dados CSV
2. Baixe nova versão
3. Substitua apenas `main.py`
4. Restaure arquivos CSV

## 📞 Suporte

### Problemas Comuns
- **Tela não limpa**: Normal em alguns terminais
- **Caracteres especiais**: Configurar UTF-8
- **Performance lenta**: Normal para muitos dados

### Contato para Suporte
- Criar issue no repositório GitHub
- Verificar documentação técnica
- Consultar README principal

---

**Guia de Instalação** - FarmTech Solutions v1.0

✅ Sistema pronto para uso após seguir este guia!
