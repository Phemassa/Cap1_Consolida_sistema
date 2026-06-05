# FarmTech Solutions - Dashboard de Irrigação

Dashboard em Python (Streamlit) para visualização de dados agrícolas do sistema IoT de irrigação inteligente.

## 📋 Funcionalidades

- **Níveis de Umidade, P, K e pH**: Gráficos em tempo real dos sensores
- **Status da Irrigação**: Indicadores visuais do sistema de irrigação
- **Sugestões de Irrigação**: Recomendações baseadas em condições climáticas
- **Métricas Climáticas**: Temperatura, umidade do ar, precipitação, vento, pressão
- **Produtividade**: Acompanhamento da produtividade estimada

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

**Nota**: O `oracledb` (nova versão do cx_Oracle) é usado e não requer Oracle Instant Client para conexões básicas.

### 2. Configurar Conexão Oracle

**IMPORTANTE**: Antes de executar, você deve configurar a senha correta no arquivo `dashboard.py`:

1. Abra o arquivo `dashboard.py`
2. Localize a linha com `password`: 
3. Substitua `'161083'` pela sua data de nascimento real (6 dígitos, formato DDMMAA)

```python
ORACLE_CONFIG = {
    'user': 'RM12345',
    'password': 'SUA_DATA_NASCIMENTO_AQUI',  # ← ALTERE AQUI
    'host': 'oracle.fiap.com.br',
    'port': 1521,
    'sid': 'ORCL'
}

Recomendado: use variáveis de ambiente para usuário e senha em vez de editar o arquivo:

PowerShell (temporário nesta sessão):
```powershell
$env:ORACLE_USER="RM566826"
$env:ORACLE_PASSWORD="161083"
```

Para persistir (user-level):
```powershell
setx ORACLE_USER "RM566826"
setx ORACLE_PASSWORD "161083"
# Abra uma nova janela do PowerShell para ver as variáveis
```
```

### 3. Testar Conexão

```bash
python test_connection.py
```

Este script testa a conexão com o banco Oracle. Se der erro de senha, verifique se você colocou a data de nascimento correta.

### 4. Executar Dashboard

```bash
streamlit run dashboard.py
```

O dashboard será aberto no navegador padrão.

## 🔧 Configuração do Banco Oracle

- **Usuário**: RM12345
- **Senha**: Sua data de nascimento (DDMMAA - 6 dígitos)
- **Host**: oracle.fiap.com.br
- **Porta**: 1521
- **SID**: ORCL
- **Tabela**: DEMO_DADOS_R

## 📊 Estrutura dos Dados

A tabela `DEMO_DADOS_R` contém as seguintes colunas principais:

- `DATA`, `HORA`: Data e hora da leitura
- `TEMPERATURA`: Temperatura ambiente (°C)
- `UMIDADE_SOLO`: Umidade do solo (%)
- `PH_SOLO`: pH do solo
- `PRECIPITACAO`: Precipitação (mm)
- `UMIDADE_AR`: Umidade do ar (%)
- `VENTO_KMH`: Velocidade do vento (km/h)
- `PRESSAO_ATMOSFERICA`: Pressão atmosférica (hPa)
- `NITROGENIO_OK`, `FOSFORO_OK`, `POTASSIO_OK`: Status dos nutrientes (TRUE/FALSE)
- `IRRIGACAO_REALIZADA`: Status da irrigação (TRUE/FALSE)
- `PRODUTIVIDADE`: Produtividade estimada (%)

## 💡 Lógica de Sugestões

O sistema analisa as condições atuais e sugere ações baseadas em:

- **Umidade do solo** < 40%: Irrigação recomendada
- **Temperatura** > 30°C: Verificar irrigação
- **Sem precipitação** + **Ar seco**: Irrigação necessária
- **Pressão baixa**: Possível mudança climática
- **Nutrientes baixos**: Recomendar fertilização
- **pH fora do ideal** (6.0-7.0): Correção necessária

## 🛠️ Requisitos do Sistema

- Python 3.8+
- Conexão com internet (para acessar oracle.fiap.com.br)
- `oracledb` (instalado automaticamente via requirements.txt)

## 📞 Suporte

Para dúvidas ou problemas:
- Execute `python test_connection.py` para verificar a conexão
- Confirme se a senha (data de nascimento) está correta
- Verifique se consegue acessar oracle.fiap.com.br:1521

**Equipe FarmTech Solutions**