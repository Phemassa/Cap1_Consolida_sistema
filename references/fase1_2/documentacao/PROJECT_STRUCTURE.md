# 📁 Estrutura do Projeto - FarmTech Solutions

```
FarmTechSolutions/
├── 📄 LICENSE                           # Licença MIT do projeto
├── 📄 README.md                         # Documentação principal do projeto
├── 📄 Fiap Projeto.code-workspace       # Workspace do VS Code
│
├── 📁 .github/                          # Configurações do GitHub
│   ├── 📁 ISSUE_TEMPLATE/
│   │   ├── 📄 bug_report.md             # Template para reportar bugs
│   │   ├── 📄 feature_request.md        # Template para solicitar features
│   │   └── 📄 documentation.md          # Template para issues de documentação
│   └── 📄 pull_request_template.md      # Template para Pull Requests
│
├── 📁 documentacao/                     # � Toda a Documentação do Projeto
│   ├── 📄 README.md                     # Documentação principal para usuários
│   ├── 📄 INSTALL.md                    # Guia de instalação e configuração
│   ├── 📄 TECHNICAL_DOCS.md             # Documentação técnica das funções
│   ├── 📄 CHANGELOG.md                  # Histórico de versões e mudanças
│   └── � PROJECT_STRUCTURE.md          # Este arquivo - estrutura do projeto
│
├── � python_app/                       # 🐍 Aplicação Python Principal
│   ├── � main.py                       # ⭐ Script principal da aplicação
│   ├── � requirements.txt              # Dependências Python (stdlib apenas)
│   ├── 📄 gerador_exemplos.py           # Gerador de dados de exemplo
│   ├── � teste.txt                     # Arquivo de teste
│   │
│   ├── � banana.csv                    # Dados da cultura banana
│   └── � milho.csv                     # Dados da cultura milho
│
└── 📁 r_app/                            # 📊 Aplicação R para Análises
    ├── 📄 analise.R                     # Script de análise estatística
    ├── 📄 clima.R                       # Script para análise climática
    └── 📄 requirements_r.txt            # Dependências R necessárias


```

## 📊 Estatísticas do Projeto

### 📈 Métricas de Código
- **Linguagens**: Python (principal), R (análises)
- **Linhas de código Python**: ~500+ linhas
- **Funções principais**: 15+ funções
- **Arquivos de documentação**: 6 arquivos
- **Templates GitHub**: 4 templates

### 🎯 Funcionalidades Implementadas
- ✅ **CRUD completo** para dados agrícolas
- ✅ **2 culturas suportadas** (Banana e Milho)
- ✅ **3 tipos de cálculo de área** (Retângulo, Triângulo, Círculo)
- ✅ **7 insumos pré-definidos** + opção personalizada
- ✅ **5 unidades de medida** + opção personalizada
- ✅ **Validação robusta** de entrada com tratamento de erros
- ✅ **Interface CLI** intuitiva com navegação fluida
- ✅ **Persistência CSV** com salvamento automático
- ✅ **Documentação completa** para usuários e desenvolvedores

### 🛡️ Qualidade e Robustez
- ✅ **Tratamento de exceções** abrangente
- ✅ **Validação de entrada** em todos os pontos
- ✅ **Navegação consistente** com opção "X" universal
- ✅ **Limpeza de tela** automática
- ✅ **Recuperação de erros** sem crashes
- ✅ **Backup automático** via salvamento contínuo

## 🎯 Pontos de Entrada

### 👤 Para Usuários
1. **Instalação**: Consulte `documentacao/INSTALL.md`
2. **Uso**: Execute `python python_app/main.py`
3. **Ajuda**: Consulte `documentacao/README.md`

### 👨‍💻 Para Desenvolvedores
1. **Contribuição**: Consulte `documentacao/CONTRIBUTING.md`
2. **API/Funções**: Consulte `documentacao/TECHNICAL_DOCS.md`
3. **Mudanças**: Consulte `documentacao/CHANGELOG.md`

### 🔬 Para Análises
1. **Script R**: Execute `r_app/analise.R`
2. **Dependências**: Instale conforme `r_app/requirements_r.txt`
3. **Gráficos**: Visualize os arquivos PNG gerados

## 🌟 Destaques do Projeto

### 💡 Inovações Implementadas
- **Parser de números brasileiros** (vírgulas e pontos)
- **Sistema de validação robusto** com função `get_numeric_input()`
- **Navegação universal** com "X" para sair
- **Auto-salvamento** após cada operação
- **Interface limpa** com `cls` automático

### 🏗️ Arquitetura Modular
- **Separação clara** entre entrada, processamento e saída
- **Funções especializadas** para cada tipo de operação
- **Estrutura escalável** para adicionar novas culturas
- **Código reutilizável** com funções utilitárias

### 📚 Documentação Profissional
- **6 arquivos de documentação** organizados na pasta `documentacao/`
- **Templates GitHub** para issues e PRs
- **Licença MIT** para uso livre
- **Guias específicos** para diferentes tipos de usuários

## 🚀 Status do Projeto

### ✅ Completo e Funcional
- Sistema principal totalmente implementado
- Documentação abrangente criada
- Tratamento de erros robusto
- Interface de usuário polida
- Pronto para uso em produção

### 🔮 Próximos Passos Sugeridos
- Interface gráfica (Tkinter/PyQt)
- Base de dados real (SQLite/PostgreSQL)
- Relatórios estatísticos avançados
- Suporte a mais culturas
- Sistema de backup automático

---

**FarmTech Solutions v1.0.0** - Sistema completo de gestão agrícola 🚜🌱
*Desenvolvido com ❤️ para a comunidade agrícola brasileira*
