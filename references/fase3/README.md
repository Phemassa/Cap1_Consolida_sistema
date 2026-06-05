# Dashboard FarmTech Solutions - Novo Projeto

Este projeto contÃ©m o dashboard de visualizaÃ§Ã£o de dados Oracle/Streamlit.

# FarmTech Solutions — Documentação e Evidência

Este README descreve, passo a passo, como os dados coletados na Fase 2 foram importados para o Oracle (usando Oracle SQL Developer), como validar a importação com consultas SQL e como executar o dashboard Streamlit (`dashboard.py`) que consome a tabela `SENSORES`.

## Sumário

- [Pré-requisitos](#pré-requisitos)
- [Importação dos dados no Oracle (passo-a-passo)](#importação-dos-dados-no-oracle-passo-a-passo)
- [Evidências (prints)](#evidências-prints)
- [Consultas SQL usadas para validação](#consultas-sql-usadas-para-validação)
- [Executando o dashboard Streamlit](#executando-o-dashboard-streamlit)
- [Notas sobre normalização e tratamento de dados](#notas-sobre-normalização-e-tratamento-de-dados)
- [Arquivos gerados como evidência](#arquivos-gerados-como-evidência)


## Pré-requisitos

- Oracle SQL Developer (para importar CSV e inspecionar a tabela).
- Conta no Oracle fornecida pela FIAP (usuário no formato `RMxxxxx`, senha = data nascimento DDMMAA).
- Python 3.8+ e dependências do projeto (ver `requirements.txt`).
- Streamlit instalado (`pip install streamlit`) para rodar o dashboard.


## Importação dos dados no Oracle (passo-a-passo)

Siga estes passos no Oracle SQL Developer para importar o CSV (ex.: `banana_dados_r.csv`):

1. Abra o Oracle SQL Developer e crie uma nova conexão:
	 - Nome: (qualquer, ex.: `FIAP`)
	 - Nome do Usuário: seu RM (ex.: `RM12345`)
	 - Senha: sua data de nascimento (DDMMYY)
	 - Host: `oracle.fiap.com.br`
	 - Porta: `1521`
	 - SID: `ORCL`
	 - Clique em `Test` e depois em `Connect`.

2. No painel da conexão, expanda a conexão e localize `Tabelas (Filtrado)`.
3. Clique com o botão direito em `Tabelas (Filtrado)` → `Importa Dados`.
4. No assistente de importação, escolha o arquivo CSV (ex.: `banana_dados_r.csv` ou `demo_dados_r.csv`).
5. Avance (Next): defina o nome da tabela a ser criada (recomendo `SENSORES`).
	 - Observação: o nome da tabela não pode conter espaços, nem caracteres especiais, deve começar com letra e ter até 30 caracteres.
6. Verifique/ajuste tipos de coluna se necessário e finalize a importação (`Finish`).
7. Ao concluir, abra um SQL Worksheet e execute as consultas de verificação (ex.: `SELECT COUNT(*) FROM SENSORES;`).

(As instruções originais passo a passo estão em `Oracle SQL/sql.txt`.)


## Evidências (prints)

Inclua as imagens geradas durante o process no diretório `docs/screenshots` e referencie-as abaixo. Nomes sugeridos:

- `docs/screenshots/query_sql1.jpg` — screenshot do SQL Worksheet com a query executada (por exemplo `SELECT * FROM SENSORES;`).
- `docs/screenshots/tabela_sensores.jpg` — screenshot mostrando a tabela `SENSORES` no painel de objetos.

Exemplo de inserção no documento (substitua quando as imagens estiverem disponíveis):

![Query SQL - exemplo](docs/screenshots/query_sql1.jpg)

![Tabela SENSORES - exemplo](docs/screenshots/tabela_sensores.jpg)


## Consultas SQL usadas para validação

Cole aqui as queries que você executou no SQL Developer para evidência. Exemplos:

```sql
-- 1) Contar registros
SELECT COUNT(*) FROM SENSORES;

-- 2) Amostra ordenada por data/hora
SELECT * FROM SENSORES WHERE ROWNUM <= 5 ORDER BY DATA, HORA;

-- 3) Conferir estrutura
SELECT column_name, data_type, data_length
FROM user_tab_columns
WHERE table_name = 'SENSORES'
ORDER BY column_id;

-- 4) Estatísticas simples (médias)
SELECT DATA, ROUND(AVG(TO_NUMBER(UMIDADE_SOLO)),2) AS avg_umidade
FROM SENSORES
GROUP BY DATA
ORDER BY DATA;
```

> Dica: copie as saídas (ou faça screenshots) das execuções e salve como evidência.


## Executando o dashboard Streamlit

O `dashboard.py` foi implementado para se conectar à tabela `SENSORES` no Oracle e construir visualizações com Plotly via Streamlit.

Passos para executar localmente (PowerShell):

1. Abra PowerShell e navegue para o diretório do projeto (onde `dashboard.py` está localizado):

```powershell
cd "C:\Fiap Projeto\Fase3"
```

2. (Opcional) Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
. .venv\Scripts\Activate
```

3. Instale dependências (se ainda não instalou):

```powershell
pip install -r requirements.txt
```

4. (Opcional mas recomendado) Defina variáveis de ambiente temporárias na sessão do PowerShell para evitar digitar credenciais pela sidebar do Streamlit:

```powershell
$env:ORACLE_USER = "RM566826"
$env:ORACLE_PASSWORD = "161083"
```

5. Inicie o Streamlit:

```powershell
streamlit run .\dashboard.py
```

- Após iniciar, o Streamlit mostrará no terminal a URL local (por padrão `http://localhost:8501`). Abra essa URL no navegador.
- Se quiser forçar a porta/endereço:

```powershell
streamlit run .\dashboard.py --server.port 8501 --server.address 127.0.0.1
```

6. Na sidebar do dashboard, se necessário, você pode digitar manualmente o usuário/senha Oracle (campo: "Senha Oracle (DDMMAA)").


## Notas sobre normalização e tratamento de dados

- Durante a importação, algumas colunas numéricas foram inseridas como inteiros muito grandes (por exemplo, `172102137871826` ao invés de `17.210`). Para resolver isso o `dashboard.py` implementa uma função de normalização (`_auto_scale`) que divide por 10 sucessivas vezes até que a mediana caia num intervalo plausível (ex.: temperatura entre -50 e 60°C, pressão entre 800 e 1100 hPa, etc.).

- Exemplo de verificação já executada (saída do script `check_normalization.py`):

```
--- Medianas antes da normalização ---
TEMPERATURA: 2.3396e+14
UMIDADE_AR: 5.9797e+14
PRECIPITACAO: 0.0
VENTO_KMH: 1.742...
PRESSAO_ATMOSFERICA: 1.0131e+14
UMIDADE_SOLO: 5.671861e+14

--- Medianas depois da normalização ---
TEMPERATURA: 23.396
UMIDADE_AR: 59.7975
PRECIPITACAO: 0.0
VENTO_KMH: 1.742
PRESSAO_ATMOSFERICA: 1013.13
UMIDADE_SOLO: 56.7185

--- Última leitura (após normalização) ---
TEMPERATURA: 17.2 °C
UMIDADE_AR: 7.1 %
PRECIPITACAO: 0.0 mm
VENTO_KMH: 1.5 km/h
PRESSAO_ATMOSFERICA: 101.4 hPa
UMIDADE_SOLO: 75.364
```

- Se desejar ajuste fino, podemos:
	- Alterar os intervalos-alvo de cada coluna (por exemplo, para `PRESSAO_ATMOSFERICA` usar [900, 1050]).
	- Adicionar regras por coluna quando houver unidades conhecidas.


## Arquivos gerados como evidência (neste repositório)

- `README_EVIDENCIA.md` — documento de evidência com trecho da saída de `test_connection.py` e instruções (já criado).
- `docs/evidence_sample.csv` — amostra com as primeiras 20 linhas extraídas da tabela `SENSORES` (gerada pelo script `export_evidence.py`).
- `check_normalization.py` — script utilizado para verificar medianas antes/depois da normalização.


## Como anexar os prints ao README

1. Copie os arquivos de imagem (`query sql1.jpg`, `tabela sensores.jpg`) para `docs/screenshots/` renomeando-os para `query_sql1.jpg` e `tabela_sensores.jpg`.
2. Atualize este `README.md` removendo os placeholders e garantindo que as imagens aparecem corretamente.


## Observações finais

  video demonstração: https://youtu.be/vF4vQ3G4Ubg

- Se houver falha na conexão ao iniciar o dashboard, verifique:
	- Variáveis de ambiente `ORACLE_USER` e `ORACLE_PASSWORD` definidas na sessão do PowerShell.
	- Se o erro for `DPI-1047`, verifique a necessidade do Oracle Instant Client e a configuração do driver `oracledb`.

- Caso queira, eu posso:
	- (A) iniciar o Streamlit aqui e fornecer a URL/prints do dashboard em execução, ou
	- (B) atualizar automaticamente este README com as imagens se você fizer upload dos screenshots.

---

Documento gerado automaticamente com base nas instruções `sql.txt` e nos scripts do projeto. Atualize os prints e as credenciais conforme necessário para sua entrega de evidência.
