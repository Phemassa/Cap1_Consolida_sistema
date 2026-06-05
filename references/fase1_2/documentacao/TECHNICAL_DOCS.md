# Documentação Técnica - FarmTech Solutions

## 📋 Índice de Funções

- [Funções Utilitárias](#funções-utilitárias)
- [Funções de Persistência](#funções-de-persistência)
- [Funções de Interface](#funções-de-interface)
- [Funções CRUD](#funções-crud)
- [Fluxo Principal](#fluxo-principal)

## 🔧 Funções Utilitárias

### `parse_float(text)`
**Descrição:** Converte texto para float com suporte a vírgulas brasileiras.

**Parâmetros:**
- `text` (str): Texto contendo número com vírgulas ou pontos

**Retorno:** `float` - Número convertido

**Exceções:** `ValueError` se o texto não contiver número válido

**Exemplo:**
```python
parse_float("123,45")  # Retorna: 123.45
parse_float("1.234,56")  # Retorna: 1234.56
```

### `get_numeric_input(prompt, input_type="float")`
**Descrição:** Obtém entrada numérica do usuário com validação robusta.

**Parâmetros:**
- `prompt` (str): Mensagem exibida ao usuário
- `input_type` (str): Tipo de conversão ("float" ou "int")

**Retorno:** 
- `float/int` - Número convertido
- `None` - Se usuário digitar "X"

**Características:**
- Loop até entrada válida
- Suporte a saída com "X"
- Mensagens de erro automáticas

**Exemplo:**
```python
valor = get_numeric_input("Digite um número: ")
if valor is None:
    return  # Usuário saiu
```

## 💾 Funções de Persistência

### `carregar_csv_banana()`
**Descrição:** Carrega dados da banana do arquivo CSV.

**Retorno:** `list` - Lista de dicionários com dados da banana

**Campos convertidos para float:**
- comprimento, largura, qtd_insumo, area

**Tratamento de erros:**
- Arquivo inexistente: retorna lista vazia
- Campos vazios: converte para None

### `carregar_csv_milho()`
**Descrição:** Carrega dados do milho do arquivo CSV.

**Retorno:** `list` - Lista de dicionários com dados do milho

**Campos convertidos para float:**
- raio, comprimento, largura, qtd_insumo, area

### `salvar_dados()`
**Descrição:** Salva todos os dados nas estruturas CSV.

**Funcionalidades:**
- Salva dados da banana em `banana.csv`
- Salva dados do milho em `milho.csv`
- Cria fieldnames dinâmicos baseados nos dados
- Codificação UTF-8 para caracteres especiais

**Estrutura de dados salvos:**
```python
# Banana
fieldnames = ['comprimento', 'largura', 'insumo', 'qtd_insumo', 'unidade', 'area', 'figura']

# Milho  
fieldnames = ['raio', 'comprimento', 'largura', 'insumo', 'qtd_insumo', 'unidade', 'area', 'figura']
```

## 🎨 Funções de Interface

### `menu()`
**Descrição:** Exibe menu principal e captura opção do usuário.

**Funcionalidades:**
- Limpa tela automaticamente
- Apresenta 5 opções numeradas
- Retorna escolha do usuário como string

**Menu exibido:**
```
--- Menu FarmTech Solutions ---
1. Entrada de dados
2. Saída de dados  
3. Atualizar dados
4. Deletar dados
5. Sair
```

## 📊 Funções CRUD

### `entrada_dados()`
**Descrição:** Função principal para entrada de novos dados.

**Fluxo de execução:**
1. **Seleção de cultura** (Banana/Milho)
2. **Seleção de figura geométrica** (Retângulo/Triângulo/Círculo)
3. **Seleção de insumo** (7 opções + personalizado)
4. **Entrada de dimensões** (validadas numericamente)
5. **Seleção de unidade** (5 opções + personalizada)
6. **Entrada de quantidade** (por metro quadrado)
7. **Salvamento automático**

**Cálculos automáticos:**
```python
# Retângulo
area = comprimento * largura

# Triângulo  
area = (base * altura) / 2

# Círculo
area = 3.1416 * raio ** 2
```

**Validações:**
- Entrada numérica obrigatória para dimensões
- Opção "X" disponível em todos os passos
- Tratamento de erro para opções inválidas

### `saida_dados()`
**Descrição:** Exibe todos os dados cadastrados.

**Funcionalidades:**
- Lista dados da banana e milho separadamente
- Calcula total de insumo por registro
- Exibe informações formatadas
- Pausa para leitura antes de retornar

**Formato de exibição:**
```
[0] Geométria: Retângulo | Área: 1500.00 m² | Insumo: Nitrogênio | Unidade: g | Total: 225000.00 g
```

**Campos exibidos:**
- Índice do registro
- Tipo de geometria
- Área calculada
- Nome do insumo
- Unidade de medida
- Total de insumo necessário

### `atualizar_dados()`
**Descrição:** Permite modificação de registros existentes.

**Fluxo de execução:**
1. **Seleção de cultura** (Banana/Milho)
2. **Seleção por índice** (com validação)
3. **Repetição do fluxo de entrada** (todos os campos)
4. **Substituição do registro** na posição do índice
5. **Salvamento automático**

**Validações específicas:**
- Verificação de existência de dados
- Validação de índice dentro do intervalo
- Tratamento de erro para índices inválidos

### `deletar_dados()`
**Descrição:** Remove registros específicos.

**Fluxo de execução:**
1. **Seleção de cultura** (Banana/Milho)
2. **Entrada de índice** (com validação)
3. **Remoção do registro** da lista
4. **Salvamento automático**

**Características:**
- Validação de índice obrigatória
- Opção "X" para cancelar operação
- Feedback de índice inválido

## 🔄 Fluxo Principal

### Inicialização
```python
# Carregamento automático de dados
dados_banana = carregar_csv_banana()
dados_milho = carregar_csv_milho()

# Limpeza inicial da tela
os.system('cls')

# Loop principal infinito
while True:
    op = menu()
    # Processamento das opções...
```

### Estrutura de Dados em Memória

**dados_banana (lista de dicionários):**
```python
{
    'comprimento': float,
    'largura': float, 
    'insumo': str,
    'qtd_insumo': float,
    'unidade': str,
    'area': float,
    'figura': str  # '1', '2', ou '3'
}
```

**dados_milho (lista de dicionários):**
```python
{
    'raio': float,          # Específico para círculos
    'comprimento': float,   # Calculado para círculos
    'largura': float,       # Calculado para círculos
    'insumo': str,
    'qtd_insumo': float,
    'unidade': str,
    'area': float,
    'figura': str  # '1', '2', ou '3'
}
```

## 🎯 Padrões de Codificação

### Convenções Utilizadas
- **Snake_case** para nomes de variáveis e funções
- **Strings descritivas** para mensagens de usuário
- **Validação consistente** em todas as entradas
- **Tratamento de exceções** robusto
- **Limpeza de tela** em transições de menu

### Mapeamento de Figuras
```python
figuras = {
    '1': 'Retângulo',
    '2': 'Triângulo', 
    '3': 'Círculo'
}
```

### Insumos Pré-definidos
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

### Unidades Pré-definidas
```python
unidades = ["mL", "L", "kg", "g", "Outro (digite manualmente)"]
```

## 🛡️ Tratamento de Erros

### Tipos de Exceções Tratadas
1. **ValueError** - Conversão numérica inválida
2. **IndexError** - Índice fora do intervalo
3. **FileNotFoundError** - Arquivo CSV inexistente
4. **KeyError** - Campo faltante no dicionário

### Estratégias de Recuperação
- **Entrada inválida**: Loop até entrada válida
- **Arquivo inexistente**: Criar estrutura vazia
- **Erro de conversão**: Mensagem e nova tentativa
- **Operação cancelada**: Retorno seguro ao menu

## ⚡ Otimizações Implementadas

### Performance
- **Carregamento único**: Dados carregados apenas na inicialização
- **Salvamento otimizado**: Apenas após modificações
- **Validação prévia**: Evita processamento desnecessário

### Usabilidade
- **Feedback imediato**: Mensagens instantâneas de erro
- **Navegação fluida**: Opção de saída sempre disponível
- **Interface limpa**: Limpeza automática da tela

### Manutenibilidade
- **Funções especializadas**: Responsabilidade única
- **Código reutilizável**: Validações centralizadas
- **Estrutura modular**: Fácil extensão e modificação

---

**Documentação Técnica** - FarmTech Solutions v1.0
