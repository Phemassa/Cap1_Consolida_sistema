# 🗄️ Guia de Instalação Oracle Database (OPCIONAL)

## ⚠️ IMPORTANTE: Você NÃO precisa instalar Oracle!

O sistema FarmTech Cap 6 funciona **100% sem Oracle instalado**:
- ✅ Usa arquivos JSON para persistência
- ✅ Todos os 27 testes passam sem Oracle
- ✅ Aplicação completa funciona sem cx_Oracle

**Oracle é opcional** para demonstrar integração com SGBD empresarial.

---

## 📊 Por que Oracle foi incluído?

### Requisitos FIAP Cap 6:
> "O grupo deve desenvolver uma solução em Python que contemple **obrigatoriamente** os conteúdos estudados nos capítulos 3, 4, 5 e **6**"

**Cap 6 - Conteúdo**: "Python e além" - Conexão com banco de dados Oracle

### Implementação no Projeto:
- ✅ **database.py**: Módulo completo de integração Oracle
- ✅ **sql/create_tables.sql**: Script DDL (4 tabelas)
- ✅ **sql/seed_data.sql**: Dados de exemplo
- ✅ **Graceful Degradation**: Se cx_Oracle não instalado, sistema continua funcionando

---

## 🚀 Opção 1: Oracle Cloud Free Tier (RECOMENDADO FIAP)

### Vantagens:
- ✅ Gratuito para sempre
- ✅ Sem instalação local (não ocupa espaço)
- ✅ Já configurado na FIAP
- ✅ Acesso remoto de qualquer lugar

### Passo a Passo:

#### 1. Instalar apenas o cliente Python
```bash
pip install cx-Oracle==8.3.0
```

#### 2. Configurar credenciais FIAP em `database.py`

Edite o arquivo `database.py` linha ~20:

```python
# Configuração do Banco Oracle (FIAP)
DB_CONFIG = {
    'user': 'RM123456',  # Seu RM da FIAP
    'password': 'sua_senha_fiap',
    'dsn': 'oracle.fiap.com.br:1521/ORCL'
}
```

**Onde obter as credenciais:**
- **User**: Seu RM (ex: RM98765)
- **Password**: Senha fornecida pelo professor
- **DSN**: Servidor Oracle da FIAP

#### 3. Criar as tabelas no Oracle FIAP

**Opção A - Via SQL Developer:**
1. Baixe: https://www.oracle.com/database/sqldeveloper/
2. Conecte com suas credenciais FIAP
3. Execute `sql/create_tables.sql`
4. Execute `sql/seed_data.sql` (opcional)

**Opção B - Via Python (mais simples):**
```bash
cd "C:\Fiap Projeto\Fase2\cursotiaor\pbl\Fase2\Cap 6"
python
```

```python
from database import DatabaseOracle

# Conecta e cria tabelas automaticamente
db = DatabaseOracle()
db.conectar()
db.criar_tabelas()  # Executa create_tables.sql
print("✅ Tabelas criadas com sucesso!")
```

#### 4. Testar conexão

Execute no menu principal (opção 9):
```bash
python main.py
# Escolha: 9 - Sincronizar com Oracle
```

**Resultado esperado:**
```
✅ Conectado ao Oracle Database!
✅ Sincronização concluída com sucesso!
   - 1 cultivos sincronizados
   - 0 leituras sincronizadas
```

---

## 🖥️ Opção 2: Oracle XE Local (NÃO RECOMENDADO)

### Desvantagens:
- ❌ Download grande (~2.5 GB)
- ❌ Instalação complexa
- ❌ Consome recursos da máquina
- ❌ Configuração trabalhosa

### Se mesmo assim quiser instalar:

#### 1. Download Oracle XE 21c
- Link: https://www.oracle.com/database/technologies/xe-downloads.html
- Arquivo: `OracleXE213_Win64.zip` (~2.5 GB)

#### 2. Instalação
1. Extraia o ZIP
2. Execute `setup.exe`
3. Defina senha para usuário SYSTEM
4. Aguarde instalação (10-15 minutos)

#### 3. Instalar cx_Oracle
```bash
pip install cx-Oracle==8.3.0
```

#### 4. Configurar em `database.py`
```python
DB_CONFIG = {
    'user': 'system',  # Usuário padrão XE
    'password': 'sua_senha_definida',
    'dsn': 'localhost:1521/XEPDB1'  # Local
}
```

#### 5. Criar tabelas
Mesmos passos da Opção 1 (SQL Developer ou Python)

---

## 📋 Scripts SQL Fornecidos

### 1. create_tables.sql

Cria estrutura completa:

**Tabelas:**
- `cultivos` - Cadastro de cultivos agrícolas
- `sensores` - Leituras de temperatura, umidade, pH, NPK
- `irrigacoes` - Histórico de decisões de irrigação
- `estoque` - Controle de insumos (fertilizantes, defensivos)

**Sequences:**
- `seq_cultivo_id`
- `seq_sensor_id`
- `seq_irrigacao_id`
- `seq_estoque_id`

**Views:**
- `v_alertas_estoque` - Produtos com estoque baixo ou vencimento próximo
- `v_estatisticas_irrigacao` - Taxa de acionamento por cultivo

**Constraints:**
- CHECK: pH (3-9), temperatura (-10 a 50°C), umidade (0-100%)
- FOREIGN KEYS: Relacionamentos entre tabelas
- UNIQUE: Evita duplicatas

### 2. seed_data.sql

Dados de exemplo:
- 3 cultivos (Banana Prata, Milho Híbrido, Cana-de-açúcar)
- 5 leituras de sensores
- 5 registros de irrigação
- 7 produtos em estoque (NPK, Ureia, Calcário, etc.)

---

## 🧪 Testando a Integração Oracle

### Teste 1: Verificar conexão
```python
from database import DatabaseOracle

db = DatabaseOracle()
if db.conectar():
    print("✅ Conectado com sucesso!")
else:
    print("❌ Erro de conexão")
```

### Teste 2: Inserir cultivo
```python
from database import DatabaseOracle

db = DatabaseOracle()
db.conectar()

cultivo_id = db.inserir_cultivo(
    nome="Teste Oracle",
    cultura_tipo="BANANA",
    area_hectares=5.0,
    data_plantio="2025-10-01",
    npk_requisitos={'nitrogenio': 15, 'fosforo': 10, 'potassio': 20},
    ph_ideal=6.5,
    umidade_ideal=60.0
)

print(f"✅ Cultivo inserido com ID: {cultivo_id}")
```

### Teste 3: Buscar cultivos
```python
from database import DatabaseOracle

db = DatabaseOracle()
db.conectar()

cultivos = db.buscar_cultivos()
print(f"✅ Total de cultivos: {len(cultivos)}")

for c in cultivos:
    print(f"  - ID {c[0]}: {c[1]} ({c[2]})")
```

---

## 🔄 Como o Sistema Decide: JSON vs Oracle

### Lógica de Degradação Graciosa

O sistema tenta Oracle primeiro, se falhar usa JSON:

```python
# Em database.py
def __init__(self):
    try:
        import oracledb
        self.oracledb = oracledb
        self.oracle_disponivel = True
    except ImportError:
        print("⚠️ cx_Oracle não instalado. Usando JSON.")
        self.oracle_disponivel = False
```

### Persistência Híbrida

O sistema **sempre salva em JSON** e **opcionalmente sincroniza com Oracle**:

1. **Operações CRUD**: Salvam em JSON automaticamente
2. **Menu Opção 9**: Sincroniza JSON → Oracle manualmente
3. **Consultas**: Leem de JSON (rápido) ou Oracle (completo)

### Vantagens desta Abordagem:
- ✅ Funciona offline (JSON local)
- ✅ Demonstra integração SGBD (Oracle)
- ✅ Não trava se Oracle indisponível
- ✅ Atende requisitos FIAP Cap 6

---

## 🐛 Problemas Comuns

### Erro: "ModuleNotFoundError: No module named 'oracledb'"

**Causa**: cx_Oracle não instalado

**Solução**:
```bash
pip install cx-Oracle==8.3.0
```

### Erro: "ORA-12154: TNS:could not resolve the connect identifier"

**Causa**: DSN incorreto

**Solução**: Verifique `database.py`:
- FIAP: `oracle.fiap.com.br:1521/ORCL`
- Local XE: `localhost:1521/XEPDB1`

### Erro: "ORA-01017: invalid username/password"

**Causa**: Credenciais incorretas

**Solução**:
- Verifique usuário e senha
- Para FIAP: Confirme RM e senha com professor
- Para XE local: Use senha definida na instalação

### Erro: "ORA-00942: table or view does not exist"

**Causa**: Tabelas não criadas

**Solução**:
```bash
python
>>> from database import DatabaseOracle
>>> db = DatabaseOracle()
>>> db.conectar()
>>> db.criar_tabelas()
```

### Sistema funciona mas Oracle não conecta

**Causa**: Sistema usa JSON como fallback

**Solução**: 
- ✅ Isso é esperado! Sistema continua funcionando.
- 💡 Se quiser Oracle: Instale cx_Oracle e configure credenciais

---

## 📊 Comparação: JSON vs Oracle

| Aspecto | JSON (Padrão) | Oracle (Opcional) |
|---------|---------------|-------------------|
| **Instalação** | ✅ Nenhuma | ⚠️ cx_Oracle + servidor |
| **Configuração** | ✅ Automática | ⚠️ Credenciais + DSN |
| **Performance** | ✅ Rápida (local) | ⚠️ Depende da rede |
| **Escalabilidade** | ⚠️ Limitada | ✅ Milhões de registros |
| **Concorrência** | ❌ Arquivo único | ✅ Multi-usuário |
| **Backup** | ⚠️ Manual (copiar .json) | ✅ Automático (RMAN) |
| **Consultas** | ⚠️ Python (lento) | ✅ SQL (otimizado) |
| **Integridade** | ⚠️ Validação Python | ✅ Constraints BD |
| **FIAP Cap 6** | ⚠️ Não atende | ✅ Atende requisito |
| **Projeto funciona?** | ✅ 100% | ✅ 100% |

---

## 📝 Resumo Executivo

### Para aprovar na FIAP Cap 6:

**Você DEVE ter**:
- ✅ Código Python com funções/procedimentos (Cap 3)
- ✅ Listas, tuplas, dicionários (Cap 4)
- ✅ Arquivos texto e JSON (Cap 5)
- ✅ **Integração Oracle** (Cap 6) - **JÁ IMPLEMENTADO!**

**O que você JÁ TEM**:
- ✅ `database.py` com cx_Oracle completo
- ✅ `sql/create_tables.sql` e `seed_data.sql`
- ✅ Menu opção 9 para sincronização
- ✅ Sistema funciona sem Oracle (graceful degradation)

**O que você PRECISA fazer**:
1. **Nada** - Sistema já atende requisitos!
2. **Opcional**: Instalar cx_Oracle e testar sincronização
3. **Documentação**: Explicar no README que Oracle está implementado

### No README.md do Cap 6:

```markdown
## Banco de Dados

### Oracle Database (Cap 6)
O sistema possui integração completa com Oracle Database:
- ✅ Módulo `database.py` com cx_Oracle
- ✅ Scripts SQL: `create_tables.sql` e `seed_data.sql`
- ✅ 4 tabelas: cultivos, sensores, irrigacoes, estoque
- ✅ Views, sequences, constraints implementadas

### Persistência Híbrida
- **JSON** (padrão): 4 arquivos em `data/` para funcionamento offline
- **Oracle** (opcional): Sincronização via menu opção 9

### Como Habilitar Oracle
```bash
pip install cx-Oracle==8.3.0
# Configurar credenciais em database.py
```

**Nota**: Sistema funciona 100% sem Oracle instalado (usa JSON).
```

---

## 🎓 Conclusão

**Você NÃO precisa instalar Oracle para:**
- ✅ Sistema funcionar completamente
- ✅ Passar nos 27 testes automatizados
- ✅ Usar todas as funcionalidades do menu
- ✅ Ter persistência de dados

**Você SÓ precisa instalar Oracle se:**
- 🎯 Quiser demonstrar integração SGBD empresarial
- 🎯 Professor exigir teste de conexão Oracle
- 🎯 Quiser aprender cx_Oracle na prática

**O projeto JÁ ATENDE Cap 6 porque:**
- ✅ Código de integração Oracle implementado
- ✅ Scripts SQL fornecidos e testados
- ✅ Arquitetura permite uso com/sem Oracle

---

**FarmTech Solutions - Grupo 59 FIAP**  
**Data**: 12/10/2025  
**Status Oracle**: ✅ Implementado com degradação graciosa
