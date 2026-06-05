import oracledb
import pandas as pd

ORACLE_CONFIG = {
    'user': 'RM566826',
    'password': '161083',
    'host': 'oracle.fiap.com.br',
    'port': 1521,
    'sid': 'ORCL'
}

print("Connecting to Oracle...")
conn = None
try:
    conn = oracledb.connect(
        user=ORACLE_CONFIG['user'],
        password=ORACLE_CONFIG['password'],
        host=ORACLE_CONFIG['host'],
        port=ORACLE_CONFIG['port'],
        service_name=ORACLE_CONFIG['sid']
    )
    print("Connected. Reading SENSORES (first 10)...")
    df = pd.read_sql('SELECT * FROM SENSORES WHERE ROWNUM <= 10', conn)
    print('Columns and dtypes:')
    print(df.dtypes)

    # conversion logic from dashboard
    if 'DATA' in df.columns and 'HORA' in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df['DATA']):
            date_part = df['DATA'].dt.strftime('%Y-%m-%d')
        else:
            date_part = df['DATA'].astype(str)
        hora_part = df['HORA'].astype(str).str.zfill(2)
        df['DATA_HORA'] = pd.to_datetime(date_part + ' ' + hora_part + ':00:00', errors='coerce')
    print('\nAfter conversion:')
    print(df[['DATA','HORA','DATA_HORA']].head(10))

except Exception as e:
    print('Error:', e)
finally:
    if conn:
        conn.close()

print('Done')