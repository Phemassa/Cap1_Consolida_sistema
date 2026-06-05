# Evidência de Carga e Consulta — FarmTech Solutions (Fase 3)

Este documento reúne a evidência da importação dos dados coletados na Fase 2 para o banco Oracle, as consultas SQL utilizadas para verificação e os passos para validar que o `dashboard.py` acessa a tabela carregada.

Resumo:
- Fonte de dados usada na carga: `banana_dados_r.csv` (ver observação abaixo)
- Nome da tabela importada no Oracle: `SENSORES`
- Script de verificação local: `test_connection.py`
- Dashboard: `dashboard.py` (acessa Oracle para montar gráficos)

Observações / Assunções
- Presumi que o arquivo de carga usado foi `banana_dados_r.csv` conforme solicitado. Se o nome real do CSV no seu ambiente for diferente (por exemplo `demo_dados_r.csv`), atualize o passo 1 abaixo ou renomeie o arquivo antes de importar.
- Testes foram executados a partir de um ambiente Windows (PowerShell). Os comandos abaixo são escritos para PowerShell.

Estrutura de arquivos relevantes
- `dashboard.py` — aplicação Streamlit que consome dados da tabela `SENSORES` no Oracle.
- `test_connection.py` — script que conecta, lista tabelas e exibe contagem/linhas de teste.
- `requirements.txt` — dependências do projeto (streamlit, oracledb, pandas, plotly, ...).

1) Passos para importar os dados no Oracle SQL Developer

Siga os passos abaixo no Oracle SQL Developer (baseado nas instruções fornecidas):

- Abra o Oracle SQL Developer e crie/abra uma conexão com os seguintes parâmetros:
  - Nome: (qualquer nome, ex: FIAP)
  - Nome do Usuário: seu RM (ex: RM12345)
  - Senha: sua data de nascimento em DDMMYY (ex: 070905)
  - Host: oracle.fiap.com.br
  - Porta: 1521
  - SID: ORCL

- Teste a conexão. Se receber mensagem de conta bloqueada, contate o suporte. Se receber credenciais inválidas, confirme o RM e a senha.

- No painel da conexão, localize "Tabelas (Filtrado)" → clique com o botão direito → "Importa Dados".

- Clique em "Procurar" e selecione o CSV a importar (ex.: `banana_dados_r.csv`).

- Avance pelos passos do assistente:
  - Defina o nome da tabela (ex.: `SENSORES`).
  - Ajuste tipos e nomes de colunas se necessário.
  - Finalize a importação.

- Ao término, execute no SQL Worksheet:

```sql
SELECT COUNT(*) FROM SENSORES;
SELECT * FROM SENSORES WHERE ROWNUM <= 5 ORDER BY DATA, HORA;
```

2) Evidência (saída do `test_connection.py`)

O script `test_connection.py` foi executado localmente para validar a conexão e a existência da tabela `SENSORES`. Abaixo está o trecho relevante da saída capturada (substitua/adicione screenshots conforme preferir):

---- Saída (trecho) ----
🧪 Teste de Conexão - FarmTech Solutions Dashboard
==================================================
🔄 Tentando conectar ao Oracle...
✅ Conexão estabelecida com sucesso!

📋 Verificando tabelas disponíveis...
📊 Tabelas encontradas (1):
  - SENSORES

✅ Tabela encontrada: SENSORES (120 registros)

📊 Colunas da tabela SENSORES: DATA, HORA, TEMPERATURA, UMIDADE_SOLO, PH_SOLO, PRECIPITACAO, PRESSAO_ATMOSFERICA, UMIDADE_AR, VENTO_KMH, NITROGENIO_OK, FOSFORO_OK, POTASSIO_OK, IRRIGACAO_REALIZADA, CULTURA, FONTE_DADOS, PRODUTIVIDADE
📋 Primeiras 3 linhas:
  (datetime.datetime(2025, 10, 7, 0, 0), 9, 274150753962217, 513425997988397, 655831759759614, '0', 10083343264529, 74919139688991, '5.31355014011609', 'TRUE', 'TRUE', 'TRUE', 'FALSE', 'Banana', 'ESP32_Python_Integrado', 100)
  (datetime.datetime(2025, 10, 7, 0, 0), 10, 361234412615491, 307086745568784, 631119684993944, '0', 101557048523917, 82350870204325, '0.84249608496894', 'FALSE', 'TRUE', 'TRUE', 'TRUE', 'Banana', 'ESP32_Python_Integrado', 671125197394362)
  (datetime.datetime(2025, 10, 7, 0, 0), 11, 289097964639556, 406513696771473, 677956483128433, '0', 102215520117178, 484446122791837, '2.75975828038479', 'TRUE', 'TRUE', 'TRUE', 'FALSE', 'Banana', 'ESP32_Python_Integrado', 952407788308445)

✅ Teste de conexão concluído com sucesso!
🎯 Use o nome da tabela: SENSORES
-------------------------

Observações sobre a evidência acima:
- A contagem (120) e os nomes/ordem das colunas demonstram que a tabela `SENSORES` foi criada e preenchida.
- Os valores das colunas aparecem com tipos heterogêneos; a normalização e conversão de tipos é feita no `dashboard.py` quando necessário.

3) Comandos para reproduzir os testes (PowerShell)

Abra o PowerShell e, no diretório do projeto, execute:

```powershell
# ativar ambiente virtual (opcional)
# .venv\\Scripts\\Activate

# instalar dependências (se necessário)
pip install -r requirements.txt

# testar conexão com Oracle (exibe tabelas e primeiras linhas)
python .\\test_connection.py

# iniciar dashboard (Streamlit) — abrirá o browser na URL local mostrada
streamlit run dashboard.py
```

4) Prints de tela (recomendações)

Inclua as imagens abaixo na pasta `docs/screenshots` e substitua os marcadores no README:
- `docs/screenshots/sqldeveloper_connection.png` — tela de criação/teste da conexão no Oracle SQL Developer.
- `docs/screenshots/sqldeveloper_import_step.png` — seleção do CSV no assistente de importação.
- `docs/screenshots/sqldeveloper_import_finish.png` — confirmação de importação concluída.
- `docs/screenshots/sql_select_result.png` — resultado do `SELECT * FROM SENSORES` (worksheet ou output do tool).
- `docs/screenshots/test_connection_output.png` — screenshot do terminal com a execução de `test_connection.py`.

Como capturar os prints:
- No SQL Developer: após cada passo clique em "Print Screen" (ou use a ferramenta de captura do Windows) e salve a imagem no caminho acima.
- No PowerShell: rode `python .\\test_connection.py` e capture a janela do terminal.

5) Consultas SQL úteis (exemplos para anexar com evidência)

```sql
-- Contar registros
SELECT COUNT(*) FROM SENSORES;

-- Amostra ordenada por data/hora
SELECT * FROM SENSORES WHERE ROWNUM <= 5 ORDER BY DATA, HORA;

-- Contar leituras por dia
SELECT DATA, COUNT(*) AS leituras_por_dia FROM SENSORES GROUP BY DATA ORDER BY DATA;

-- Média de umidade do solo por dia
SELECT DATA, ROUND(AVG(TO_NUMBER(UMIDADE_SOLO)),2) AS avg_umidade FROM SENSORES GROUP BY DATA ORDER BY DATA;
```

6) Validação no `dashboard.py`

O `dashboard.py` contém lógica para:
- conectar ao Oracle (usa `oracledb`) — o campo `ORACLE_CONFIG` e a sidebar permitem definir usuário/senha em runtime;
- normalizar e converter colunas (ex.: `TEMPERATURA`, `UMIDADE_SOLO`, `PH_SOLO`, criação de `DATA_HORA`);
- exibir gráficos com Plotly via Streamlit.

Se a sua conta Oracle estiver configurada e a tabela `SENSORES` existir, iniciar o Streamlit deverá abrir o dashboard com métricas e gráficos baseados nos dados carregados.

7) Próximos passos sugeridos
- Adicionar as capturas de tela em `docs/screenshots` e inserir imagens neste README (substituir os marcadores).
- Se desejar, incluo um script adicional que extrai um CSV com as primeiras N linhas para anexar como evidência (posso criar isso automaticamente).

---
Arquivo gerado automaticamente para evidência local. Atualize as imagens e, se precisar, eu monto o CSV de evidência com base em uma execução ao vivo do `SELECT *`.
