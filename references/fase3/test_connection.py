import oracledb
import pandas as pd

# Configurações de conexão Oracle
ORACLE_CONFIG = {
    'user': 'RM566826',
    'password': '161083',  # ← DIGITE SUA DATA DDMMAA (ex: 161083)
    'host': 'oracle.fiap.com.br',
    'port': 1521,
    'sid': 'ORCL'
}

def testar_conexao():
    """Testa a conexão com o banco Oracle e faz uma consulta simples"""
    try:
        print("🔄 Tentando conectar ao Oracle...")

        # Conectar diretamente
        connection = oracledb.connect(
            user=ORACLE_CONFIG['user'],
            password=ORACLE_CONFIG['password'],
            host=ORACLE_CONFIG['host'],
            port=ORACLE_CONFIG['port'],
            service_name=ORACLE_CONFIG['sid']
        )

        print("✅ Conexão estabelecida com sucesso!")

        # Listar tabelas disponíveis no schema do usuário
        cursor = connection.cursor()
        print("\n📋 Verificando tabelas disponíveis...")
        
        try:
            cursor.execute("SELECT table_name FROM user_tables ORDER BY table_name")
            tables = cursor.fetchall()
            
            if tables:
                print(f"📊 Tabelas encontradas ({len(tables)}):")
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("⚠️ Nenhuma tabela encontrada no seu schema.")
                print("💡 Verifique se o CSV foi carregado corretamente.")
        except Exception as e:
            print(f"❌ Erro ao listar tabelas: {e}")

        # Tentar diferentes nomes de tabela possíveis
        possible_tables = ['SENSORES', 'DEMO_DADOS_R', 'demo_dados_r', 'DEMO_DADOS_R.csv', 'demo_dados_r.csv']
        
        table_found = None
        for table_name in possible_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"\n✅ Tabela encontrada: {table_name} ({count} registros)")
                table_found = table_name
                break
            except:
                continue
        
        if not table_found:
            print("\n❌ Nenhuma das tabelas esperadas foi encontrada.")
            print("💡 Possíveis soluções:")
            print("   - Verifique o nome exato da tabela criada no Oracle")
            print("   - Execute: SELECT table_name FROM user_tables;")
            print("   - Atualize o nome da tabela no dashboard.py")
            cursor.close()
            connection.close()
            return False

        # Mostrar estrutura da tabela encontrada
        try:
            cursor.execute(f"SELECT * FROM {table_found} WHERE ROWNUM <= 3")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            print(f"\n📊 Colunas da tabela {table_found}: {', '.join(columns)}")
            print("📋 Primeiras 3 linhas:")
            for row in rows:
                print(f"  {row}")
        except Exception as e:
            print(f"❌ Erro ao consultar tabela: {e}")

        # Fechar conexão
        cursor.close()
        connection.close()

        print("\n✅ Teste de conexão concluído com sucesso!")
        print(f"🎯 Use o nome da tabela: {table_found}")
        return True

    except oracledb.Error as error:
        print(f"❌ Erro de Oracle: {error}")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Teste de Conexão - FarmTech Solutions Dashboard")
    print("=" * 50)

    sucesso = testar_conexao()

    if sucesso:
        print("\n🎉 Pronto para executar o dashboard!")
        print("Execute: streamlit run dashboard.py")
    else:
        print("\n⚠️ Verifique as configurações de conexão e tente novamente.")
        print("Possíveis problemas:")
        print("- Senha incorreta (data de nascimento DDMMAA)")
        print("- Oracle Instant Client não instalado")
        print("- Firewall bloqueando conexão")