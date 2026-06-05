# FarmTech Solutions - Sistema de Gestão Agrícola em Python

## 📋 Área do Agronegócio

**Gestão de Cultivos e Controle de Irrigação Inteligente**

Este projeto aplica tecnologia Python para otimizar a gestão de cultivos agrícolas, com foco em:
- Monitoramento de nutrientes do solo (NPK)
- Controle automatizado de irrigação
- Análise de condições ambientais (pH, temperatura, umidade)
- Gestão de estoque de insumos
- Rastreabilidade de aplicações e colheitas

## 🎯 Problema Identificado

Produtores rurais enfrentam desafios na gestão eficiente de cultivos devido a:

1. **Desperdício de recursos**: Irrigação excessiva ou insuficiente desperdiça água e energia
2. **Perdas de produtividade**: Nutrientes inadequados reduzem safras em até 30%
3. **Falta de dados organizados**: Decisões tomadas sem base em histórico confiável
4. **Custos elevados**: Aplicação incorreta de insumos aumenta despesas
5. **Dificuldade de rastreabilidade**: Impossível auditar práticas agrícolas

## 💡 Solução Proposta

Sistema Python integrado que:

### Funcionalidades Principais
- ✅ **Cadastro de cultivos** com requisitos específicos de NPK
- ✅ **Monitoramento em tempo real** de sensores (temperatura, umidade, pH)
- ✅ **Decisão automatizada de irrigação** baseada em 6 condições
- ✅ **Gestão de estoque** de fertilizantes e defensivos
- ✅ **Histórico completo** de aplicações e colheitas
- ✅ **Análise de dados** com relatórios estatísticos
- ✅ **Persistência** em JSON e banco de dados Oracle

### Diferencial Tecnológico
- Integração com sistema IoT (ESP32 do Cap 1)
- Algoritmo inteligente considerando cultura específica (Banana vs Milho)
- Interface CLI amigável com validação robusta de dados
- Arquitetura modular e escalável

## 🛠️ Tecnologias Utilizadas

### Python (Capítulos 3-6)
- **Cap 3**: Funções e procedimentos modulares
- **Cap 4**: Listas, tuplas e dicionários para estruturas de dados
- **Cap 5**: Manipulação de arquivos texto e JSON
- **Cap 6**: Conexão com Oracle Database

### Bibliotecas
- **Nativas Python** (incluídas na instalação):
  - `json`: Serialização/deserialização de dados
  - `datetime`: Controle de timestamps
  - `statistics`: Cálculos estatísticos (média, desvio padrão)
  - `os`: Operações de sistema
  
- **Opcionais** (instalar via pip):
  - `cx_Oracle 8.3.0`: Conexão com banco de dados Oracle
  - `pyserial 3.5`: Comunicação serial com ESP32

### Banco de Dados
- **Oracle Database (Cap 6)** - Integração implementada
  - ✅ Scripts SQL: `create_tables.sql` e `seed_data.sql`
  - ✅ Módulo `database.py` com cx_Oracle
  - ✅ 4 tabelas: cultivos, sensores, irrigacoes, estoque
  - ⚠️ **Sistema funciona 100% SEM Oracle instalado** (usa JSON)
  
- **JSON (Padrão)** - Persistência local
  - ✅ 4 arquivos em `data/`: cultivos, sensores, irrigacoes, estoque
  - ✅ Não requer instalação ou configuração
  - ✅ Ideal para testes e desenvolvimento

## 📁 Estrutura do Projeto

```
Cap 6/
├── README.md                    # Este arquivo
├── main.py                      # Aplicação principal com menu
├── cultivo_manager.py           # Gestão de cultivos (CRUD)
├── sensor_monitor.py            # Leitura e análise de sensores
├── irrigacao_controller.py      # Lógica de decisão de irrigação
├── estoque_manager.py           # Controle de insumos
├── database.py                  # Conexão e operações Oracle
├── file_utils.py                # Manipulação de arquivos JSON/texto
├── data/
│   ├── cultivos.json           # Dados de cultivos cadastrados
│   ├── sensores.json           # Leituras de sensores
│   ├── irrigacoes.json         # Histórico de irrigações
│   └── estoque.json            # Inventário de insumos
├── sql/
│   ├── create_tables.sql       # Script de criação das tabelas
│   └── seed_data.sql           # Dados iniciais
└── docs/
    ├── REQUISITOS_NPK.md       # Tabela de nutrientes por cultura
    └── LOGICA_IRRIGACAO.md     # Explicação do algoritmo
```

## 🚀 Como Executar

### Pré-requisitos

1. **Python 3.8+** instalado
2. **Bibliotecas opcionais** (se desejar Oracle):
```bash
pip install cx_Oracle==8.3.0
```

> **⚠️ IMPORTANTE**: O sistema funciona **100% sem Oracle instalado**!  
> Veja [docs/INSTALACAO_ORACLE.md](docs/INSTALACAO_ORACLE.md) para detalhes.

### Configuração do Banco (OPCIONAL)

**Somente se quiser usar Oracle:**

1. Execute o script de criação:
```bash
sqlplus usuario/senha@host:porta/servicename @sql/create_tables.sql
```

2. Configure credenciais em `database.py` (linha ~20):
```python
DB_CONFIG = {
    'user': 'seu_usuario',      # RM da FIAP ou 'system'
    'password': 'sua_senha',
    'dsn': 'oracle.fiap.com.br:1521/ORCL'  # ou 'localhost:1521/XEPDB1'
}
```

3. No menu, escolha **opção 9** para sincronizar JSON → Oracle

### Execução (Funcionamento Padrão com JSON)

```bash
cd "C:\Fiap Projeto\Fase2\cursotiaor\pbl\Fase2\Cap 6"
python main.py
```

**Primeira execução:**
- ✅ Sistema cria automaticamente diretório `data/`
- ✅ Cria 4 arquivos JSON vazios
- ✅ Não requer configuração adicional

### Menu Principal

```
=== FarmTech Solutions - Gestão Agrícola ===

1. Cadastrar Cultivo
2. Monitorar Sensores
3. Controlar Irrigação
4. Gerenciar Estoque
5. Relatórios e Análises
6. Exportar/Importar JSON
7. Sincronizar com Oracle
0. Sair

Escolha uma opção:
```

## 📊 Funcionalidades Detalhadas

### 1. Cadastro de Cultivos

**Dados armazenados** (estrutura de dicionário):
```python
{
    'id': 1,
    'nome': 'Banana Prata',
    'cultura_tipo': 'BANANA',
    'area_hectares': 5.5,
    'data_plantio': '2025-08-15',
    'npk_requisitos': {
        'nitrogenio': 15.0,  # g/m²
        'fosforo': 10.0,
        'potassio': 20.0
    },
    'ph_ideal': 6.5,
    'umidade_ideal': 60.0
}
```

### 2. Monitoramento de Sensores

**Leitura integrada** com ESP32 (Cap 1):
- Temperatura (DHT22)
- Umidade do ar (DHT22) → Solo (×0.8)
- pH (LDR convertido)
- NPK (buttons digitais)

**Armazenamento em lista**:
```python
leituras_sensores = [
    {
        'timestamp': '2025-10-11 14:30:00',
        'cultivo_id': 1,
        'temperatura': 28.5,
        'umidade_solo': 32.0,
        'ph': 6.2,
        'npk_ok': {'N': True, 'P': True, 'K': False}
    },
    # ... mais leituras
]
```

### 3. Controle de Irrigação

**Algoritmo de decisão** (6 condições do Cap 1):

```python
def decidir_irrigacao(cultivo, leitura_sensor):
    """
    Retorna tupla: (deve_irrigar: bool, motivo: str)
    """
    umidade = leitura_sensor['umidade_solo']
    ph = leitura_sensor['ph']
    temp = leitura_sensor['temperatura']
    npk_ok = leitura_sensor['npk_ok']
    
    # Condição 1: Solo muito seco
    if umidade < 40.0:
        return (True, "Umidade crítica < 40%")
    
    # Condição 2: Solo encharcado
    if umidade > 80.0:
        return (False, "Solo encharcado > 80%")
    
    # Condição 3: NPK insuficiente + umidade subótima
    if not all(npk_ok.values()) and umidade < 60.0:
        nutriente_faltante = [k for k, v in npk_ok.items() if not v]
        return (True, f"NPK insuficiente ({nutriente_faltante}) + umidade baixa")
    
    # Condição 4: pH fora da faixa + umidade baixa
    if (ph < 5.5 or ph > 7.5) and umidade < 60.0:
        return (True, f"pH fora da faixa ({ph}) + umidade baixa")
    
    # Condição 5: Temperatura alta + umidade baixa
    if temp > 30.0 and umidade < 60.0:
        return (True, f"Temperatura alta ({temp}°C) + umidade baixa")
    
    # Condição 6: Condições ideais
    return (False, "Condições ótimas - irrigação desnecessária")
```

### 4. Gestão de Estoque

**Controle de insumos** (lista de dicionários):
```python
estoque = [
    {
        'produto': 'Ureia (45% N)',
        'tipo': 'fertilizante',
        'quantidade_kg': 500.0,
        'data_compra': '2025-09-01',
        'validade': '2026-09-01'
    },
    {
        'produto': 'Superfosfato Simples (18% P)',
        'tipo': 'fertilizante',
        'quantidade_kg': 300.0,
        'data_compra': '2025-09-10',
        'validade': '2027-09-10'
    }
]
```

**Operações**:
- Adicionar entrada de estoque
- Registrar aplicação (subtrai quantidade)
- Alertas de produtos em falta (<10% capacidade)
- Alertas de vencimento próximo (<30 dias)

### 5. Relatórios e Análises

**Funções estatísticas** (usando `statistics`):
```python
def gerar_relatorio_cultivo(cultivo_id):
    leituras = filtrar_leituras_por_cultivo(cultivo_id)
    
    temperaturas = [l['temperatura'] for l in leituras]
    umidades = [l['umidade_solo'] for l in leituras]
    
    return {
        'total_leituras': len(leituras),
        'temp_media': statistics.mean(temperaturas),
        'temp_desvio': statistics.stdev(temperaturas),
        'umidade_media': statistics.mean(umidades),
        'umidade_min': min(umidades),
        'umidade_max': max(umidades),
        'irrigacoes_realizadas': contar_irrigacoes(cultivo_id)
    }
```

**Visualização em tabela ASCII**:
```
╔══════════════════════════════════════════╗
║   RELATÓRIO: Banana Prata (5.5 ha)      ║
╠══════════════════════════════════════════╣
║ Período: 01/10/2025 - 11/10/2025        ║
║ Total de leituras: 240                   ║
║ Temperatura média: 26.8°C ±2.1           ║
║ Umidade média: 45.2% (MIN: 28%, MAX: 68%)║
║ Irrigações realizadas: 15                ║
║ Eficiência hídrica: 87%                  ║
╚══════════════════════════════════════════╝
```

### 6. Persistência de Dados

**Arquivos JSON** (Cap 5):
```python
def salvar_cultivos_json(cultivos, arquivo='data/cultivos.json'):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(cultivos, f, indent=2, ensure_ascii=False)

def carregar_cultivos_json(arquivo='data/cultivos.json'):
    with open(arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)
```

**Oracle Database** (Cap 6):
```python
def sincronizar_cultivo_oracle(cultivo):
    conn = cx_Oracle.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO cultivos (id, nome, cultura_tipo, area_hectares, 
                              data_plantio, nitrogenio_req, fosforo_req, potassio_req)
        VALUES (:id, :nome, :tipo, :area, TO_DATE(:plantio, 'YYYY-MM-DD'),
                :n, :p, :k)
    """, {
        'id': cultivo['id'],
        'nome': cultivo['nome'],
        'tipo': cultivo['cultura_tipo'],
        'area': cultivo['area_hectares'],
        'plantio': cultivo['data_plantio'],
        'n': cultivo['npk_requisitos']['nitrogenio'],
        'p': cultivo['npk_requisitos']['fosforo'],
        'k': cultivo['npk_requisitos']['potassio']
    })
    
    conn.commit()
    cursor.close()
    conn.close()
```

## 📚 Dados Utilizados

### Fontes Oficiais (conforme atividade)

- **EMBRAPA**: Requisitos de NPK por cultura
  - Banana: N=15g/m², P=10g/m², K=20g/m²
  - Milho: N=12g/m², P=8g/m², K=10g/m²
  
- **CONAB**: Dados de produtividade e safras

- **CEPEA/ESALQ**: Preços de insumos e commodities

## 🎓 Conteúdos FIAP Aplicados

### ✅ Capítulo 3: Subalgoritmos
- **Funções**: `decidir_irrigacao()`, `gerar_relatorio()`, `calcular_eficiencia()`
- **Procedimentos**: `exibir_menu()`, `cadastrar_cultivo()`, `listar_sensores()`
- **Parâmetros**: Passagem por valor e referência

### ✅ Capítulo 4: Estruturas de Dados
- **Listas**: `leituras_sensores`, `estoque_insumos`, `historico_irrigacoes`
- **Tuplas**: Retorno de múltiplos valores `(deve_irrigar, motivo)`
- **Dicionários**: Cultivos, configurações, NPK requisitos
- **Tabelas de memória**: Matriz de leituras indexada por timestamp

### ✅ Capítulo 5: Arquivos
- **Texto**: Logs de operações (`logs/irrigacao.log`)
- **JSON**: Persistência de todos os dados estruturados

### ✅ Capítulo 6: Banco de Dados
- **Conexão Oracle**: `cx_Oracle.connect()`
- **Operações CRUD**: INSERT, SELECT, UPDATE, DELETE
- **Transações**: Commit/rollback de operações críticas

## 🔒 Validações Implementadas

- ✅ **Tipos de dados**: Verificação de int, float, string
- ✅ **Ranges**: Temperatura (-10 a 50°C), pH (3.0 a 9.0), umidade (0-100%)
- ✅ **Datas**: Formato ISO 8601, validação de datas futuras
- ✅ **Unicidade**: IDs únicos para cultivos
- ✅ **Consistência**: NPK não negativo, área > 0

## 🏆 Inovações do Projeto

1. **Integração IoT**: Conexão com ESP32 do Cap 1 via Serial
2. **Algoritmo adaptativo**: Decisão varia por cultura (Banana vs Milho)
3. **Histórico completo**: Rastreabilidade total de operações
4. **Interface intuitiva**: Menu CLI com feedback visual
5. **Arquitetura modular**: Fácil manutenção e expansão

## 👥 Autores

**Grupo 59 - FIAP Fase 2**

- **Phellype Massa**: Arquitetura e desenvolvimento Python
- **Carlos**: Integração com banco de dados Oracle
- **Cesar**: Validações e testes de qualidade

## 📅 Cronograma

- ✅ **01/10/2025**: Análise de requisitos
- ✅ **05/10/2025**: Desenvolvimento módulos principais
- ✅ **10/10/2025**: Integração Oracle e testes
- 🔄 **11/10/2025**: Documentação e refinamento
- ⏰ **15/10/2025**: **ENTREGA FINAL**

## 📖 Documentação Complementar

- [REQUISITOS_NPK.md](docs/REQUISITOS_NPK.md): Tabela completa de nutrientes
- [LOGICA_IRRIGACAO.md](docs/LOGICA_IRRIGACAO.md): Fluxograma de decisão
- [INTEGRACAO_ESP32.md](docs/INTEGRACAO_ESP32.md): Como conectar com Cap 1

## 🌱 Impacto Esperado

- **Redução de 30%** no consumo de água
- **Aumento de 20%** na produtividade por otimização de NPK
- **Economia de R$ 5.000/ano** por hectare em insumos
- **Rastreabilidade 100%** para certificações (Orgânico, Fair Trade)

---

**FarmTech Solutions** - Tecnologia a serviço do campo 🌾

*Desenvolvido como parte da disciplina "Desenvolvimento Python" - FIAP 2025*
