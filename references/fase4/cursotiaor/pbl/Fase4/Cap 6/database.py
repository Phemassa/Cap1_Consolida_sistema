"""
Módulo de Conexão com Oracle Database
Implementa operações CRUD com cx_Oracle
"""

try:
    import cx_Oracle
    ORACLE_DISPONIVEL = True
except ImportError:
    ORACLE_DISPONIVEL = False
    print("⚠️  cx_Oracle não instalado. Funcionalidade Oracle desabilitada.")
    print("   Para instalar: pip install cx_Oracle")


class DatabaseOracle:
    """Gerenciador de conexão e operações com Oracle Database"""
    
    # Configurações de conexão (AJUSTE CONFORME SEU AMBIENTE)
    DB_CONFIG = {
        'user': 'seu_usuario',
        'password': 'sua_senha',
        'dsn': 'localhost:1521/XEPDB1'  # Ex: host:porta/servicename
    }
    
    def __init__(self):
        """Inicializa gerenciador de banco"""
        self.conexao = None
        self.cursor = None
    
    def conectar(self):
        """
        Estabelece conexão com Oracle
        
        Returns:
            bool: True se conectado, False se falha
        """
        if not ORACLE_DISPONIVEL:
            print("❌ cx_Oracle não disponível")
            return False
        
        try:
            self.conexao = cx_Oracle.connect(**self.DB_CONFIG)
            self.cursor = self.conexao.cursor()
            print("✅ Conectado ao Oracle Database")
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def desconectar(self):
        """Fecha conexão com Oracle"""
        if self.cursor:
            self.cursor.close()
        if self.conexao:
            self.conexao.close()
        print("🔌 Desconectado do Oracle")
    
    def criar_tabelas(self):
        """Cria tabelas necessárias no banco"""
        if not self.conexao:
            print("❌ Não conectado ao banco")
            return False
        
        try:
            # Tabela CULTIVOS
            self.cursor.execute("""
                CREATE TABLE cultivos (
                    id NUMBER PRIMARY KEY,
                    nome VARCHAR2(100) NOT NULL,
                    cultura_tipo VARCHAR2(50),
                    area_hectares NUMBER(10,2),
                    data_plantio DATE,
                    nitrogenio_req NUMBER(5,2),
                    fosforo_req NUMBER(5,2),
                    potassio_req NUMBER(5,2),
                    ph_ideal NUMBER(3,1),
                    umidade_ideal NUMBER(5,2),
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ Tabela CULTIVOS criada")
            
            # Tabela SENSORES
            self.cursor.execute("""
                CREATE TABLE sensores (
                    id NUMBER PRIMARY KEY,
                    cultivo_id NUMBER REFERENCES cultivos(id),
                    timestamp TIMESTAMP,
                    temperatura NUMBER(5,2),
                    umidade_solo NUMBER(5,2),
                    ph NUMBER(3,1),
                    npk_n NUMBER(1),
                    npk_p NUMBER(1),
                    npk_k NUMBER(1)
                )
            """)
            print("✅ Tabela SENSORES criada")
            
            # Tabela IRRIGACOES
            self.cursor.execute("""
                CREATE TABLE irrigacoes (
                    id NUMBER PRIMARY KEY,
                    cultivo_id NUMBER REFERENCES cultivos(id),
                    leitura_id NUMBER REFERENCES sensores(id),
                    timestamp TIMESTAMP,
                    acionado NUMBER(1),
                    motivo VARCHAR2(255)
                )
            """)
            print("✅ Tabela IRRIGACOES criada")
            
            # Tabela ESTOQUE
            self.cursor.execute("""
                CREATE TABLE estoque (
                    id NUMBER PRIMARY KEY,
                    produto VARCHAR2(100) NOT NULL,
                    tipo VARCHAR2(50),
                    quantidade_kg NUMBER(10,2),
                    data_compra DATE,
                    validade DATE,
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ Tabela ESTOQUE criada")
            
            self.conexao.commit()
            return True
            
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            if error.code == 955:  # Tabela já existe
                print("⚠️  Tabelas já existem")
                return True
            else:
                print(f"❌ Erro ao criar tabelas: {e}")
                return False
    
    def inserir_cultivo(self, cultivo):
        """
        Insere cultivo no banco
        
        Args:
            cultivo (dict): Dados do cultivo
        
        Returns:
            bool: True se inserido, False se falha
        """
        if not self.conexao:
            return False
        
        try:
            self.cursor.execute("""
                INSERT INTO cultivos (id, nome, cultura_tipo, area_hectares, 
                                    data_plantio, nitrogenio_req, fosforo_req, 
                                    potassio_req, ph_ideal, umidade_ideal)
                VALUES (:id, :nome, :tipo, :area, 
                        TO_DATE(:plantio, 'YYYY-MM-DD'),
                        :n, :p, :k, :ph, :umidade)
            """, {
                'id': cultivo['id'],
                'nome': cultivo['nome'],
                'tipo': cultivo['cultura_tipo'],
                'area': cultivo['area_hectares'],
                'plantio': cultivo['data_plantio'],
                'n': cultivo['npk_requisitos']['nitrogenio'],
                'p': cultivo['npk_requisitos']['fosforo'],
                'k': cultivo['npk_requisitos']['potassio'],
                'ph': cultivo['ph_ideal'],
                'umidade': cultivo['umidade_ideal']
            })
            
            self.conexao.commit()
            return True
            
        except Exception as e:
            print(f"❌ Erro ao inserir cultivo: {e}")
            self.conexao.rollback()
            return False
    
    def inserir_leitura_sensor(self, leitura):
        """
        Insere leitura de sensor no banco
        
        Args:
            leitura (dict): Dados da leitura
        
        Returns:
            bool: True se inserido, False se falha
        """
        if not self.conexao:
            return False
        
        try:
            self.cursor.execute("""
                INSERT INTO sensores (id, cultivo_id, timestamp, temperatura,
                                    umidade_solo, ph, npk_n, npk_p, npk_k)
                VALUES (:id, :cultivo_id, TO_TIMESTAMP(:ts, 'YYYY-MM-DD HH24:MI:SS'),
                        :temp, :umidade, :ph, :n, :p, :k)
            """, {
                'id': leitura['id'],
                'cultivo_id': leitura['cultivo_id'],
                'ts': leitura['timestamp'],
                'temp': leitura['temperatura'],
                'umidade': leitura['umidade_solo'],
                'ph': leitura['ph'],
                'n': 1 if leitura['npk_ok']['N'] else 0,
                'p': 1 if leitura['npk_ok']['P'] else 0,
                'k': 1 if leitura['npk_ok']['K'] else 0
            })
            
            self.conexao.commit()
            return True
            
        except Exception as e:
            print(f"❌ Erro ao inserir leitura: {e}")
            self.conexao.rollback()
            return False
    
    def buscar_cultivos(self):
        """
        Busca todos os cultivos do banco
        
        Returns:
            list: Lista de cultivos ou lista vazia se falha
        """
        if not self.conexao:
            return []
        
        try:
            self.cursor.execute("SELECT * FROM cultivos ORDER BY id")
            
            cultivos = []
            for row in self.cursor:
                cultivo = {
                    'id': row[0],
                    'nome': row[1],
                    'cultura_tipo': row[2],
                    'area_hectares': float(row[3]) if row[3] else 0,
                    'data_plantio': row[4].strftime('%Y-%m-%d') if row[4] else '',
                    'npk_requisitos': {
                        'nitrogenio': float(row[5]) if row[5] else 0,
                        'fosforo': float(row[6]) if row[6] else 0,
                        'potassio': float(row[7]) if row[7] else 0
                    },
                    'ph_ideal': float(row[8]) if row[8] else 6.5,
                    'umidade_ideal': float(row[9]) if row[9] else 60.0
                }
                cultivos.append(cultivo)
            
            return cultivos
            
        except Exception as e:
            print(f"❌ Erro ao buscar cultivos: {e}")
            return []
    
    def executar_query(self, query, parametros=None):
        """
        Executa query SQL genérica
        
        Args:
            query (str): Query SQL
            parametros (dict, optional): Parâmetros da query
        
        Returns:
            list: Resultados ou lista vazia
        """
        if not self.conexao:
            return []
        
        try:
            if parametros:
                self.cursor.execute(query, parametros)
            else:
                self.cursor.execute(query)
            
            return self.cursor.fetchall()
            
        except Exception as e:
            print(f"❌ Erro ao executar query: {e}")
            return []
