# FarmTech Solutions - Sistema de Gestão Agrícola

## 📋 Descrição do Projeto

O FarmTech Solutions é um sistema de gestão agrícola desenvolvido em Python que permite o gerenciamento de dados de plantação para duas culturas principais: **Banana** e **Milho**. O sistema oferece funcionalidades completas de CRUD (Create, Read, Update, Delete) para dados agrícolas, incluindo cálculos automáticos de área e gestão de insumos.

## 🎯 Objetivos

- Facilitar o controle de dados de plantação
- Automatizar cálculos de área para diferentes figuras geométricas
- Gerenciar insumos agrícolas por metro quadrado
- Persistir dados em arquivos CSV para análise posterior
- Oferecer interface de linha de comando intuitiva

## 🛠️ Tecnologias Utilizadas

- **Python 3.x** - Linguagem principal
- **CSV** - Persistência de dados
- **OS** - Manipulação do sistema operacional
- **RE** - Expressões regulares para validação

## 📁 Estrutura do Projeto

```
python_app/
├── main.py              # Arquivo principal da aplicação
├── requirements.txt     # Dependências do projeto
├── banana.csv          # Dados persistidos da cultura banana
├── milho.csv           # Dados persistidos da cultura milho
├── teste.txt           # Arquivo de teste
├── gerador_exemplos.py # Gerador de dados de exemplo
└── README.md           # Documentação do projeto
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.x instalado
- Terminal/Prompt de comando

### Instalação
1. Clone o repositório ou baixe os arquivos
2. Navegue até a pasta `python_app`
3. Execute o arquivo principal:

```bash
cd python_app
python main.py
```

## 📖 Manual de Uso

### Menu Principal

O sistema apresenta 5 opções principais:

```
--- Menu FarmTech Solutions ---
1. Entrada de dados
2. Saída de dados
3. Atualizar dados
4. Deletar dados
5. Sair
```

### 1. Entrada de Dados

**Fluxo de entrada:**
1. Escolha a cultura (Banana ou Milho)
2. Selecione a figura geométrica do terreno:
   - **Retângulo**: comprimento × largura
   - **Triângulo**: (base × altura) ÷ 2
   - **Círculo**: π × raio²
3. Escolha o insumo (7 opções pré-definidas + personalizado)
4. Insira as dimensões do terreno
5. Selecione a unidade de medida (mL, L, kg, g + personalizada)
6. Informe a quantidade de insumo por m²

**Validações:**
- Entrada numérica com suporte a vírgulas e pontos
- Opção "X" para sair a qualquer momento
- Tratamento de erros para entradas inválidas

### 2. Saída de Dados

Exibe todos os registros cadastrados para ambas as culturas:
- Lista completa de dados da Banana
- Lista completa de dados do Milho
- Cálculo automático do total de insumo necessário
- Informações de geometria, área e unidades

### 3. Atualizar Dados

**Funcionalidades:**
- Seleção por índice do registro a ser atualizado
- Permite alterar todos os campos do registro
- Recalcula automaticamente a área com as novas dimensões
- Salva automaticamente as alterações no CSV

### 4. Deletar Dados

**Funcionalidades:**
- Remoção de registros por índice
- Confirmação visual do registro a ser deletado
- Atualização automática dos arquivos CSV

### 5. Sair

Encerra o programa de forma segura.

## 🧮 Cálculos Automáticos

### Figuras Geométricas Suportadas

1. **Retângulo**
   - Fórmula: Área = comprimento × largura
   - Campos: comprimento, largura

2. **Triângulo**
   - Fórmula: Área = (base × altura) ÷ 2
   - Campos: base, altura (armazenados como comprimento e largura)

3. **Círculo**
   - Fórmula: Área = π × raio²
   - Campos: raio (comprimento e largura calculados como 2 × raio)

### Cálculo de Insumos

```
Total de Insumo = Área do Terreno × Quantidade por m²
```

## 💾 Persistência de Dados

### Estrutura dos CSVs

**banana.csv / milho.csv:**
```csv
comprimento,largura,insumo,qtd_insumo,unidade,area,figura,raio
```

**Campos:**
- `comprimento`: Comprimento do terreno (m)
- `largura`: Largura do terreno (m)
- `insumo`: Nome do insumo agrícola
- `qtd_insumo`: Quantidade de insumo por m²
- `unidade`: Unidade de medida do insumo
- `area`: Área calculada automaticamente (m²)
- `figura`: Tipo de figura geométrica (1=Retângulo, 2=Triângulo, 3=Círculo)
- `raio`: Raio (apenas para círculos)

## 🔧 Funcionalidades Técnicas

### Validação de Entrada
- **Função `get_numeric_input()`**: Validação robusta de números
- **Função `parse_float()`**: Conversão de texto para float com suporte a vírgulas
- **Tratamento de exceções**: Prevenção de crashes por entrada inválida

### Interface de Usuário
- **Limpeza de tela automática**: Experiência visual limpa
- **Navegação intuitiva**: Opção "X" para sair em qualquer ponto
- **Mensagens de erro**: Feedback claro para o usuário
- **Pausa em visualizações**: Tempo para leitura dos dados

### Carregamento Automático
- **Função `carregar_csv_banana()`**: Carrega dados existentes da banana
- **Função `carregar_csv_milho()`**: Carrega dados existentes do milho
- **Inicialização automática**: Dados disponíveis imediatamente

### Salvamento Automático
- **Função `salvar_dados()`**: Persiste dados após operações
- **Salvamento imediato**: Após entrada, atualização ou deleção
- **Fieldnames dinâmicos**: Adapta-se aos campos disponíveis

## 📊 Insumos Pré-Cadastrados

1. Fosfato
2. Nitrogênio
3. Potássio
4. Pulverizar 500 mL/metro
5. Herbicida
6. Inseticida
7. Outro (digite manualmente)

## 🔍 Unidades de Medida Suportadas

- **mL** (mililitros)
- **L** (litros)
- **kg** (quilogramas)
- **g** (gramas)
- **Personalizada** (entrada manual)

## ⚠️ Tratamento de Erros

### Validações Implementadas
- Entrada numérica inválida
- Índices fora do intervalo
- Opções de menu inválidas
- Arquivos CSV corrompidos
- Campos obrigatórios vazios

### Recuperação de Erros
- Mensagens informativas
- Retorno seguro ao menu
- Preservação de dados existentes
- Continuidade da execução

## 🔄 Fluxo de Dados

```
1. Inicialização → Carrega CSVs existentes
2. Menu Principal → Apresenta opções
3. Operação CRUD → Modifica dados em memória
4. Salvamento → Persiste no CSV
5. Retorno → Volta ao menu principal
```

## 📝 Exemplos de Uso

### Entrada de Dados - Banana Retangular
```
Cultura: Banana
Figura: Retângulo
Comprimento: 50m
Largura: 30m
Insumo: Nitrogênio
Quantidade: 150 g/m²
Área calculada: 1500 m²
Total de insumo: 225000 g
```

### Entrada de Dados - Milho Circular
```
Cultura: Milho
Figura: Círculo
Raio: 25m
Insumo: Fosfato
Quantidade: 200 mL/m²
Área calculada: 1963.5 m²
Total de insumo: 392700 mL
```

## 🛡️ Recursos de Segurança

- **Validação robusta**: Previne crashes por entrada inválida
- **Backup automático**: Dados salvos após cada operação
- **Confirmação de ações**: Pausa antes de retornar ao menu
- **Escape universal**: Opção "X" sempre disponível

## 🎨 Interface do Usuário

### Características
- **Limpeza automática**: Tela limpa para melhor visualização
- **Navegação consistente**: Padrão uniforme em todos os menus
- **Feedback visual**: Mensagens claras e informativas
- **Fluxo intuitivo**: Sequência lógica de operações

## 📈 Benefícios do Sistema

1. **Automatização**: Cálculos automáticos de área e insumos
2. **Organização**: Dados estruturados e facilmente acessíveis
3. **Flexibilidade**: Suporte a diferentes geometrias e insumos
4. **Persistência**: Dados salvos para uso futuro
5. **Usabilidade**: Interface simples e intuitiva
6. **Robustez**: Tratamento completo de erros

## 🔮 Possíveis Melhorias Futuras

- Interface gráfica (GUI)
- Relatórios em PDF
- Integração com APIs de clima
- Análise estatística dos dados
- Backup em nuvem
- Suporte a mais culturas
- Cálculos de custo
- Planejamento de safras

## 👥 Suporte e Contribuição

Para suporte técnico ou contribuições:
- Reporte bugs através de issues
- Sugira melhorias
- Contribua com código
- Compartilhe feedback

---

**FarmTech Solutions** - Transformando a gestão agrícola através da tecnologia 🌱
