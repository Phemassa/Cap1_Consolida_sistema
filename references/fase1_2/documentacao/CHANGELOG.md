# Changelog - FarmTech Solutions

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2025-09-03

### ✨ Adicionado
- **Sistema CRUD completo** para gestão de dados agrícolas
- **Suporte a duas culturas**: Banana e Milho
- **Cálculo automático de área** para 3 figuras geométricas:
  - Retângulo (comprimento × largura)
  - Triângulo ((base × altura) ÷ 2)
  - Círculo (π × raio²)
- **Gestão de insumos agrícolas** com 7 opções pré-definidas
- **Sistema de unidades flexível** (mL, L, kg, g + personalizada)
- **Validação robusta de entrada** com suporte a "X" para sair
- **Interface de linha de comando** intuitiva e limpa
- **Persistência em CSV** com salvamento automático
- **Tratamento completo de erros** para entrada inválida
- **Navegação fluida** com limpeza automática de tela
- **Carregamento automático** de dados existentes na inicialização

### 🔧 Funcionalidades Técnicas
- **Função `get_numeric_input()`**: Validação de entrada numérica
- **Função `parse_float()`**: Conversão com suporte a vírgulas brasileiras
- **Função `salvar_dados()`**: Salvamento automático após operações
- **Funções de carregamento**: `carregar_csv_banana()` e `carregar_csv_milho()`
- **Menu principal centralizado** com opções numeradas
- **Estrutura modular** para fácil manutenção e extensão

### 📊 Recursos de Dados
- **Campos suportados**:
  - Dimensões do terreno (comprimento, largura, raio)
  - Informações do insumo (nome, quantidade, unidade)
  - Cálculos automáticos (área, total de insumo)
  - Metadados (figura geométrica)
- **Formatos de entrada flexíveis**: números com vírgulas e pontos
- **Validação de índices** para operações de atualização/deleção
- **Backup automático** via salvamento após cada operação

### 🎨 Interface do Usuário
- **Menu principal** com 5 opções:
  1. Entrada de dados
  2. Saída de dados (sem limpeza de tela)
  3. Atualizar dados
  4. Deletar dados
  5. Sair
- **Limpeza automática de tela** em todas as transições
- **Mensagens de erro informativas** com pausa para leitura
- **Opção universal "X"** para sair de qualquer submenu
- **Feedback visual** para todas as operações

### 🛡️ Segurança e Robustez
- **Tratamento de exceções** para:
  - ValueError (conversão numérica)
  - IndexError (índices inválidos)
  - FileNotFoundError (arquivos inexistentes)
  - KeyError (campos faltantes)
- **Validação prévia** antes de operações críticas
- **Recuperação automática** de erros sem crash
- **Preservação de dados** durante falhas

### 📁 Estrutura de Arquivos
```
python_app/
├── main.py              # Aplicação principal
├── requirements.txt     # Dependências (apenas stdlib)
├── README.md           # Documentação principal
├── TECHNICAL_DOCS.md   # Documentação técnica
├── INSTALL.md          # Guia de instalação
├── CHANGELOG.md        # Este arquivo
├── banana.csv          # Dados da cultura banana
├── milho.csv           # Dados da cultura milho
├── gerador_exemplos.py # Gerador de dados teste
└── teste.txt           # Arquivo de teste
```

### 🧮 Cálculos Implementados
- **Área de retângulo**: `comprimento × largura`
- **Área de triângulo**: `(base × altura) ÷ 2`
- **Área de círculo**: `π × raio²` (π = 3.1416)
- **Total de insumo**: `área × quantidade_por_m²`

### 📋 Insumos Pré-cadastrados
1. Fosfato
2. Nitrogênio
3. Potássio
4. Pulverizar 500 mL/metro
5. Herbicida
6. Inseticida
7. Outro (entrada personalizada)

### 📏 Unidades Suportadas
- **mL** (mililitros)
- **L** (litros)
- **kg** (quilogramas)
- **g** (gramas)
- **Personalizada** (entrada livre)

## [Próximas Versões] - Planejado

### 🔮 v1.1.0 - Melhorias de Interface
- [ ] Cores no terminal para melhor UX
- [ ] Confirmação antes de deletar registros
- [ ] Ordenação de dados por diferentes campos
- [ ] Busca/filtro de registros

### 🔮 v1.2.0 - Recursos Avançados
- [ ] Relatórios estatísticos
- [ ] Exportação para diferentes formatos
- [ ] Importação de dados externos
- [ ] Validação de dados mais rigorosa

### 🔮 v2.0.0 - Interface Gráfica
- [ ] Interface gráfica com Tkinter
- [ ] Gráficos e visualizações
- [ ] Sistema de backup automático
- [ ] Suporte a múltiplas fazendas

## Tipos de Mudanças
- **Adicionado** para novas funcionalidades
- **Alterado** para mudanças em funcionalidades existentes
- **Depreciado** para funcionalidades que serão removidas
- **Removido** para funcionalidades removidas
- **Corrigido** para correção de bugs
- **Segurança** para correções de vulnerabilidades

---

**Histórico de Versões** - FarmTech Solutions
