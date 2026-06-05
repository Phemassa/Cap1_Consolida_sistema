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

SQL = "SELECT * FROM SENSORES ORDER BY DATA, HORA"

def _auto_scale(series, low, high, max_iter=15):
    s = pd.to_numeric(series, errors='coerce')
    if s.dropna().empty:
        return s

    scaled = s.copy()
    for _ in range(max_iter):
        med = scaled.median()
        if pd.isna(med):
            break
        if low <= med <= high:
            return scaled.round(3)
        if med > high:
            scaled = scaled / 10.0
            continue
        if med < low:
            scaled = scaled * 10.0
            continue
    return s

def main():
    print('Conectando ao Oracle e lendo dados (pode demorar dependendo do tamanho)...')
    conn = None
    try:
        conn = oracledb.connect(
            user=ORACLE_CONFIG['user'],
            password=ORACLE_CONFIG['password'],
            host=ORACLE_CONFIG['host'],
            port=ORACLE_CONFIG['port'],
            service_name=ORACLE_CONFIG['sid']
        )
        df = pd.read_sql(SQL, conn)

        if df.empty:
            print('Tabela SENSORES vazia ou consulta retornou 0 linhas.')
            return

        cols = ['TEMPERATURA','UMIDADE_AR','PRECIPITACAO','VENTO_KMH','PRESSAO_ATMOSFERICA','UMIDADE_SOLO']

        print('\n--- Medianas antes da normalização ---')
        for c in cols:
            if c in df.columns:
                print(f"{c}: {pd.to_numeric(df[c], errors='coerce').median()}")

        # apply scaling similar to dashboard
        scale_targets = {
            'TEMPERATURA': (-50, 60),
            'UMIDADE_SOLO': (0, 100),
            'PH_SOLO': (0, 14),
            'UMIDADE_AR': (0, 100),
            'PRESSAO_ATMOSFERICA': (800, 1100),
            'VENTO_KMH': (0, 200),
            'PRECIPITACAO': (0, 500),
            'PRODUTIVIDADE': (0, 100)
        }

        for col, (low, high) in scale_targets.items():
            if col in df.columns:
                df[col] = _auto_scale(df[col], low, high)

        print('\n--- Medianas depois da normalização ---')
        for c in cols:
            if c in df.columns:
                print(f"{c}: {pd.to_numeric(df[c], errors='coerce').median()}")

        ultima = df.iloc[-1]
        print('\n--- Última leitura (após normalização) ---')
        for c in cols:
            if c in df.columns:
                val = pd.to_numeric(ultima[c], errors='coerce')
                if pd.isna(val):
                    print(f"{c}: NaN")
                else:
                    if c == 'TEMPERATURA':
                        print(f"{c}: {val:.1f} °C")
                    elif c == 'UMIDADE_AR':
                        print(f"{c}: {val:.1f} %")
                    elif c == 'PRECIPITACAO':
                        print(f"{c}: {val:.1f} mm")
                    elif c == 'VENTO_KMH':
                        print(f"{c}: {val:.1f} km/h")
                    elif c == 'PRESSAO_ATMOSFERICA':
                        print(f"{c}: {val:.1f} hPa")
                    else:
                        print(f"{c}: {val}")

    except Exception as e:
        print('Erro durante o teste:', e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    main()
