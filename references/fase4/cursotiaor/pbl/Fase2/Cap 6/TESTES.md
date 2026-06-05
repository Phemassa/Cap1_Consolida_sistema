# 🧪 Guia de Testes - FarmTech Solutions

## Como Testar o Sistema Cap 6

### ✅ Método 1: Testes Automatizados (RECOMENDADO)

Execute o script de testes completo que valida todas as funcionalidades:

```bash
cd "C:\Fiap Projeto\Fase2\cursotiaor\pbl\Fase2\Cap 6"
python test_farmtech.py
```

#### O que é testado:

1. **Cultivo Manager** (5 testes)
   - ✅ Cadastro de cultivo válido
   - ✅ Busca por ID
   - ✅ Listagem de cultivos
   - ✅ Validação de pH inválido
   - ✅ Cálculo de área total

2. **Sensor Monitor** (7 testes)
   - ✅ Registro de leitura
   - ✅ Conversão umidade ar → solo (×0.8)
   - ✅ Classificação de temperatura (FRIA/IDEAL/ALTA/CRÍTICA)
   - ✅ Classificação de pH (ÁCIDO/NEUTRO/ALCALINO)
   - ✅ Validação de temperatura inválida
   - ✅ Última leitura por cultivo
   - ✅ Média de temperatura

3. **Irrigação Controller** (8 testes - 6 condições)
   - ✅ Condição 1: Solo seco (<40%)
   - ✅ Condição 2: Solo encharcado (>80%)
   - ✅ Condição 3: NPK insuficiente (K para Banana, N para Milho)
   - ✅ Condição 4: pH fora da faixa (5.5-7.5)
   - ✅ Condição 5: Temperatura alta (>30°C)
   - ✅ Condição 6: Condições ideais (não irriga)
   - ✅ Registro no histórico
   - ✅ Taxa de acionamento

4. **Estoque Manager** (4 testes)
   - ✅ Adicionar produto
   - ✅ Listar estoque
   - ✅ Registrar aplicação (subtração)
   - ✅ Alertas de estoque baixo e vencimento próximo

5. **Persistência JSON** (2 testes)
   - ✅ Criação de arquivos JSON
   - ✅ Recarga de dados salvos

6. **Integração Completa** (1 teste)
   - ✅ Fluxo completo: Cadastro → Leitura → Decisão → Histórico

**Resultado Esperado:**
```
🎉 TODOS OS TESTES PASSARAM COM SUCESSO! 🎉

📊 RESUMO:
  ✅ Cultivos cadastrados: 1
  ✅ Leituras registradas: 7
  ✅ Irrigações no histórico: 1
  ✅ Produtos em estoque: 3
  ✅ Arquivos JSON persistidos: 4
```

---

### ✅ Método 2: Teste Interativo (Menu CLI)

Execute a aplicação principal para teste manual:

```bash
cd "C:\Fiap Projeto\Fase2\cursotiaor\pbl\Fase2\Cap 6"
python main.py
```

#### Cenário de Teste Sugerido:

**Passo 1: Cadastrar Cultivo**
- Opção: `1`
- Nome: `Banana Teste`
- Tipo: `1` (BANANA)
- Área: `10`
- Data plantio: `2025-08-15`
- NPK: N=`15`, P=`10`, K=`20`
- pH ideal: `6.5`
- Umidade ideal: `60`

**Passo 2: Listar Cultivos**
- Opção: `2`
- Verificar: Cultivo aparece com ID 1

**Passo 3: Simular Leitura (Solo Seco)**
- Opção: `3`
- Cultivo ID: `1`
- Temperatura: `28`
- Umidade ar: `45` (solo = 36%)
- pH: `6.2`
- N adequado: `s`
- P adequado: `s`
- K adequado: `n` (falta K)

**Passo 4: Verificar Irrigação**
- Opção: `4`
- Cultivo ID: `1`
- **Resultado esperado**: 💧 IRRIGAÇÃO NECESSÁRIA
- **Motivo**: Umidade crítica (36%) < 40%

**Passo 5: Histórico**
- Opção: `5`
- Cultivo ID: `1`
- Verificar: Registro de irrigação acionada

**Passo 6: Gerenciar Estoque**
- Opção: `6` → `1` (Adicionar)
- Produto: `Ureia 45% N`
- Tipo: `1` (fertilizante)
- Quantidade: `500`
- Data compra: `2025-09-01`
- Validade: `2026-09-01`

**Passo 7: Relatórios**
- Opção: `7` → `2` (Análise de irrigações)
- Verificar: Estatísticas de acionamento

**Passo 8: Exportar JSON**
- Opção: `8`
- Verificar: Mensagem de sucesso

**Passo 9: Sair**
- Opção: `0`
- Dados salvos automaticamente

---

### ✅ Método 3: Teste de Funções Individuais

Teste funções específicas no Python REPL:

```bash
cd "C:\Fiap Projeto\Fase2\cursotiaor\pbl\Fase2\Cap 6"
python
```

#### Teste rápido de Cultivo:
```python
from cultivo_manager import CultivoManager

cultivo_mgr = CultivoManager()
cultivo_id = cultivo_mgr.adicionar_cultivo(
    nome="Teste REPL",
    cultura_tipo="BANANA",
    area_hectares=5.0,
    data_plantio="2025-10-01",
    npk_requisitos={'nitrogenio': 15, 'fosforo': 10, 'potassio': 20},
    ph_ideal=6.5,
    umidade_ideal=60.0
)
print(f"Cultivo criado com ID: {cultivo_id}")
cultivos = cultivo_mgr.listar_cultivos()
print(f"Total: {len(cultivos)} cultivos")
```

#### Teste rápido de Decisão de Irrigação:
```python
from irrigacao_controller import IrrigacaoController

irrigacao_ctrl = IrrigacaoController()

# Simula cultivo e leitura
cultivo = {'cultura_tipo': 'BANANA'}
leitura = {
    'umidade_solo': 35.0,  # SECO
    'ph': 6.5,
    'temperatura': 28.0,
    'npk_ok': {'N': True, 'P': True, 'K': True}
}

resultado = irrigacao_ctrl.decidir_irrigacao(cultivo, leitura)
print(f"Deve irrigar: {resultado['deve_irrigar']}")
print(f"Motivo: {resultado['motivo']}")
print(f"Condição: {resultado['condicao']}")
```

**Resultado esperado:**
```
Deve irrigar: True
Motivo: Umidade crítica (35.0%) < 40.0%
Condição: 1
```

---

### ✅ Método 4: Verificar Arquivos JSON

Após executar testes, verifique os dados persistidos:

```bash
# Windows PowerShell
cat data\cultivos.json
cat data\sensores.json
cat data\irrigacoes.json
cat data\estoque.json
```

**Estrutura esperada em `data/cultivos.json`:**
```json
[
  {
    "id": 1,
    "nome": "Banana Prata Teste",
    "cultura_tipo": "BANANA",
    "area_hectares": 5.5,
    "data_plantio": "2025-08-15",
    "npk_requisitos": {
      "nitrogenio": 15.0,
      "fosforo": 10.0,
      "potassio": 20.0
    },
    "ph_ideal": 6.5,
    "umidade_ideal": 60.0,
    "data_cadastro": "2025-10-12 09:00:00"
  }
]
```

---

### ✅ Método 5: Teste de Validações (Esperando Erros)

Teste que validações funcionam corretamente:

```python
from cultivo_manager import CultivoManager

cultivo_mgr = CultivoManager()

# Teste 1: pH inválido (deve dar erro)
try:
    cultivo_mgr.adicionar_cultivo(
        nome="Inválido",
        cultura_tipo="MILHO",
        area_hectares=10.0,
        data_plantio="2025-09-01",
        npk_requisitos={'nitrogenio': 12, 'fosforo': 8, 'potassio': 10},
        ph_ideal=15.0,  # INVÁLIDO (>9.0)
        umidade_ideal=55.0
    )
    print("❌ ERRO: Deveria ter lançado exceção!")
except ValueError as e:
    print(f"✅ OK: Validação funcionou - {e}")

# Teste 2: Área negativa (deve dar erro)
try:
    cultivo_mgr.adicionar_cultivo(
        nome="Inválido 2",
        cultura_tipo="BANANA",
        area_hectares=-5.0,  # INVÁLIDO (<0)
        data_plantio="2025-08-01",
        npk_requisitos={'nitrogenio': 15, 'fosforo': 10, 'potassio': 20},
        ph_ideal=6.5,
        umidade_ideal=60.0
    )
    print("❌ ERRO: Deveria ter lançado exceção!")
except ValueError as e:
    print(f"✅ OK: Validação funcionou - {e}")
```

**Resultado esperado:**
```
✅ OK: Validação funcionou - pH deve estar entre 3.0 e 9.0
✅ OK: Validação funcionou - Área deve ser maior que zero
```

---

### ✅ Método 6: Teste com Oracle Database (Opcional)

⚠️ **Requer Oracle instalado e configurado**

1. **Configurar credenciais** em `database.py`:
```python
DB_CONFIG = {
    'user': 'seu_usuario',
    'password': 'sua_senha',
    'dsn': 'localhost:1521/XEPDB1'
}
```

2. **Criar tabelas**:
```bash
sqlplus usuario/senha@host:porta/servicename @sql/create_tables.sql
```

3. **Popular com dados de exemplo**:
```bash
sqlplus usuario/senha@host:porta/servicename @sql/seed_data.sql
```

4. **Testar sincronização no menu**:
- Opção: `9` (Sincronizar com Oracle)
- Verificar: Mensagem de sucesso

---

## 📊 Checklist de Testes

Use este checklist para validar que tudo está funcionando:

- [ ] ✅ Testes automatizados (`python test_farmtech.py`) passam 100%
- [ ] ✅ Menu CLI (`python main.py`) abre sem erros
- [ ] ✅ Cadastro de cultivo funciona
- [ ] ✅ Leitura de sensores registra corretamente
- [ ] ✅ Decisão de irrigação retorna resultado esperado
- [ ] ✅ 6 condições de irrigação testadas (manual ou automatizado)
- [ ] ✅ Gestão de estoque adiciona/remove produtos
- [ ] ✅ Alertas de estoque funcionam (baixo, vencimento)
- [ ] ✅ Relatórios exibem estatísticas
- [ ] ✅ Arquivos JSON criados em `data/`
- [ ] ✅ Dados persistidos podem ser recarregados
- [ ] ✅ Validações rejeitam dados inválidos (pH, temperatura, etc.)

---

## 🐛 Solução de Problemas

### Problema: `Import "file_utils" could not be resolved`
**Solução**: Erro apenas do linter (Pylance). Execute o código normalmente:
```bash
python main.py
```

### Problema: `cx_Oracle não instalado`
**Solução**: Funcionalidade Oracle é opcional. Para instalar:
```bash
pip install cx-Oracle
```

### Problema: Arquivos JSON não são criados
**Solução**: Verifique se diretório `data/` existe. O sistema cria automaticamente, mas se houver erro de permissão:
```bash
mkdir data
```

### Problema: Validações não funcionam
**Solução**: Verifique ranges:
- pH: 3.0 - 9.0
- Temperatura: -10°C - 50°C
- Umidade: 0% - 100%
- Área: > 0

---

## 📚 Documentação de Referência

- **README.md**: Visão geral do projeto
- **docs/REQUISITOS_NPK.md**: Tabela de nutrientes por cultura
- **docs/LOGICA_IRRIGACAO.md**: Fluxograma das 6 condições
- **docs/INTEGRACAO_ESP32.md**: Como conectar com Cap 1

---

**Atualizado**: 12/10/2025  
**Status**: ✅ Sistema totalmente funcional e testado  
**FarmTech Solutions - Grupo 59 FIAP**
