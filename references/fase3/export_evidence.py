import os
import oracledb
import pandas as pd

ORACLE_CONFIG = {
    'user': 'RM566826',
    'password': '161083',
    'host': 'oracle.fiap.com.br',
    'port': 1521,
    'sid': 'ORCL'
}

OUT_DIR = os.path.join('docs')
OUT_FILE = os.path.join(OUT_DIR, 'evidence_sample.csv')

SQL = "SELECT * FROM SENSORES WHERE ROWNUM <= 20 ORDER BY DATA, HORA"

os.makedirs(OUT_DIR, exist_ok=True)

print(f"Conectando ao Oracle ({ORACLE_CONFIG['user']}@{ORACLE_CONFIG['host']})...")
conn = None
try:
    conn = oracledb.connect(
        user=ORACLE_CONFIG['user'],
        password=ORACLE_CONFIG['password'],
        host=ORACLE_CONFIG['host'],
        port=ORACLE_CONFIG['port'],
        service_name=ORACLE_CONFIG['sid']
    )
    print('Conectado. Executando consulta...')
    df = pd.read_sql(SQL, conn)
    if df.empty:
        print('Consulta retornou 0 linhas.')
    else:
        df.to_csv(OUT_FILE, index=False)
        print(f"Arquivo salvo: {OUT_FILE} ({len(df)} linhas)")
except Exception as e:
    print('Erro:', e)
finally:
    if conn:
        conn.close()

print('Pronto.')
