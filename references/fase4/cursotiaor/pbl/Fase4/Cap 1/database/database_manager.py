"""
FarmTech Solutions - Database Schema & Ingestion
================================================
Sistema de ingestão automática de dados IoT para banco SQL
Suporta SQLite (dev) e PostgreSQL (prod)
"""

import sqlite3
import pandas as pd
from datetime import datetime
import schedule
import time
import json
import logging
import sys
from pathlib import Path

# Definir diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / 'farmtech.log'
DB_PATH = BASE_DIR / 'database' / 'farmtech.db'

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Configurar logging com UTF-8
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class FarmTechDatabase:
    """Gerenciador do banco de dados FarmTech"""
    
    def __init__(self, db_path=None):
        """Inicializa conexão com banco de dados"""
        if db_path is None:
            db_path = DB_PATH
        
        # Criar diretório database se não existir
        db_path = Path(db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.db_path = str(db_path)
        self.conn = None
        self.connect()
        self.create_tables()
        logging.info(f"✅ Banco de dados inicializado: {self.db_path}")
    
    def connect(self):
        """Conecta ao banco de dados"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # Retorna dict-like rows
            return True
        except Exception as e:
            logging.error(f"❌ Erro ao conectar: {e}")
            return False
    
    def create_tables(self):
        """Cria estrutura de tabelas se não existirem"""
        cursor = self.conn.cursor()
        
        # Tabela: sensor_readings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                temperatura REAL NOT NULL,
                umidade_solo REAL NOT NULL,
                ph_solo REAL NOT NULL,
                nitrogenio INTEGER NOT NULL,
                fosforo INTEGER NOT NULL,
                potassio INTEGER NOT NULL,
                irrigacao_ativa INTEGER NOT NULL,
                cultura VARCHAR(50) NOT NULL
            )
        ''')
        
        # Índices para performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON sensor_readings(timestamp)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_cultura 
            ON sensor_readings(cultura)
        ''')
        
        # Tabela: predictions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                reading_id INTEGER NOT NULL,
                volume_irrigacao REAL,
                dosagem_n REAL,
                dosagem_p REAL,
                dosagem_k REAL,
                rendimento_estimado REAL,
                confianca REAL,
                modelo_versao VARCHAR(20),
                FOREIGN KEY (reading_id) REFERENCES sensor_readings(id)
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_predictions_timestamp 
            ON predictions(timestamp)
        ''')
        
        # Tabela: irrigation_actions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS irrigation_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                reading_id INTEGER NOT NULL,
                acao VARCHAR(20) NOT NULL,
                motivo TEXT,
                volume_aplicado REAL,
                duracao_minutos INTEGER,
                FOREIGN KEY (reading_id) REFERENCES sensor_readings(id)
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_actions_timestamp 
            ON irrigation_actions(timestamp)
        ''')
        
        # Tabela: culturas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS culturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(50) NOT NULL UNIQUE,
                n_ideal REAL NOT NULL,
                p_ideal REAL NOT NULL,
                k_ideal REAL NOT NULL,
                ph_minimo REAL NOT NULL,
                ph_maximo REAL NOT NULL,
                umidade_minima REAL NOT NULL,
                umidade_ideal REAL NOT NULL,
                rendimento_esperado REAL
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_culturas_nome 
            ON culturas(nome)
        ''')
        
        self.conn.commit()
        logging.info("✅ Tabelas criadas/verificadas com sucesso")
        
        # Popula culturas padrão
        self._seed_culturas()
    
    def _seed_culturas(self):
        """Insere culturas padrão se não existirem"""
        cursor = self.conn.cursor()
        
        culturas = [
            ('banana', 15.0, 10.0, 20.0, 5.5, 7.5, 40.0, 60.0, 25000.0),
            ('milho', 12.0, 8.0, 10.0, 5.5, 7.5, 40.0, 60.0, 8000.0)
        ]
        
        for cultura in culturas:
            cursor.execute('''
                INSERT OR IGNORE INTO culturas 
                (nome, n_ideal, p_ideal, k_ideal, ph_minimo, ph_maximo, 
                 umidade_minima, umidade_ideal, rendimento_esperado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', cultura)
        
        self.conn.commit()
    
    def insert_sensor_reading(self, data):
        """
        Insere leitura de sensor
        
        Args:
            data (dict): Dicionário com dados do sensor
        
        Returns:
            int: ID do registro inserido
        """
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO sensor_readings 
            (temperatura, umidade_solo, ph_solo, nitrogenio, 
             fosforo, potassio, irrigacao_ativa, cultura)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['temperatura'],
            data['umidade_solo'],
            data['ph_solo'],
            int(data['nitrogenio']),
            int(data['fosforo']),
            int(data['potassio']),
            int(data['irrigacao_ativa']),
            data['cultura']
        ))
        
        self.conn.commit()
        reading_id = cursor.lastrowid
        
        logging.info(f"📊 Leitura inserida: ID {reading_id} | "
                    f"Temp: {data['temperatura']}°C | "
                    f"Umid: {data['umidade_solo']}%")
        
        return reading_id
    
    def insert_prediction(self, reading_id, prediction_data):
        """
        Insere previsão do modelo ML
        
        Args:
            reading_id (int): ID da leitura relacionada
            prediction_data (dict): Dados da previsão
        
        Returns:
            int: ID da previsão inserida
        """
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions 
            (reading_id, volume_irrigacao, dosagem_n, dosagem_p, 
             dosagem_k, rendimento_estimado, confianca, modelo_versao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            reading_id,
            prediction_data.get('volume_irrigacao'),
            prediction_data.get('dosagem_n'),
            prediction_data.get('dosagem_p'),
            prediction_data.get('dosagem_k'),
            prediction_data.get('rendimento_estimado'),
            prediction_data.get('confianca', 0.95),
            prediction_data.get('modelo_versao', 'v1.0')
        ))
        
        self.conn.commit()
        pred_id = cursor.lastrowid
        
        logging.info(f"🔮 Previsão inserida: ID {pred_id} | "
                    f"Volume: {prediction_data.get('volume_irrigacao')}L/m²")
        
        return pred_id
    
    def insert_irrigation_action(self, reading_id, acao, motivo, volume=None, duracao=None):
        """Insere ação de irrigação"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO irrigation_actions 
            (reading_id, acao, motivo, volume_aplicado, duracao_minutos)
            VALUES (?, ?, ?, ?, ?)
        ''', (reading_id, acao, motivo, volume, duracao))
        
        self.conn.commit()
        logging.info(f"💧 Ação de irrigação: {acao} - {motivo}")
        
        return cursor.lastrowid
    
    def get_recent_readings(self, limit=100, cultura=None):
        """
        Retorna leituras recentes
        
        Args:
            limit (int): Número de registros
            cultura (str): Filtrar por cultura (opcional)
        
        Returns:
            DataFrame: Dados das leituras
        """
        query = "SELECT * FROM sensor_readings"
        params = []
        
        if cultura:
            query += " WHERE cultura = ?"
            params.append(cultura)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        df = pd.read_sql_query(query, self.conn, params=params)
        return df
    
    def get_statistics(self):
        """Retorna estatísticas gerais do banco"""
        cursor = self.conn.cursor()
        
        stats = {}
        
        # Total de leituras
        cursor.execute("SELECT COUNT(*) FROM sensor_readings")
        stats['total_leituras'] = cursor.fetchone()[0]
        
        # Total de previsões
        cursor.execute("SELECT COUNT(*) FROM predictions")
        stats['total_previsoes'] = cursor.fetchone()[0]
        
        # Total de ações de irrigação
        cursor.execute("SELECT COUNT(*) FROM irrigation_actions")
        stats['total_acoes'] = cursor.fetchone()[0]
        
        # Média de temperatura
        cursor.execute("SELECT AVG(temperatura) FROM sensor_readings")
        stats['temperatura_media'] = cursor.fetchone()[0]
        
        # Média de umidade
        cursor.execute("SELECT AVG(umidade_solo) FROM sensor_readings")
        stats['umidade_media'] = cursor.fetchone()[0]
        
        return stats
    
    def export_to_csv(self, table_name, output_file):
        """Exporta tabela para CSV"""
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
        df.to_csv(output_file, index=False)
        logging.info(f"📁 Tabela {table_name} exportada para {output_file}")
        return df
    
    def close(self):
        """Fecha conexão com banco"""
        if self.conn:
            self.conn.close()
            logging.info("🔌 Conexão com banco fechada")


class AutoIngestion:
    """Sistema de ingestão automática de dados"""
    
    def __init__(self, db: FarmTechDatabase, data_source='simulate'):
        """
        Inicializa sistema de ingestão
        
        Args:
            db: Instância do FarmTechDatabase
            data_source: 'simulate', 'serial', ou 'csv'
        """
        self.db = db
        self.data_source = data_source
        self.is_running = False
    
    def read_sensor_data(self):
        """Lê dados dos sensores (simulado ou real)"""
        if self.data_source == 'simulate':
            # Simula dados realistas
            import random
            import numpy as np
            
            data = {
                'temperatura': round(20 + random.uniform(0, 15), 1),
                'umidade_solo': round(30 + random.uniform(0, 60), 1),
                'ph_solo': round(5.5 + random.uniform(0, 2), 2),
                'nitrogenio': random.choice([0, 1]),
                'fosforo': random.choice([0, 1]),
                'potassio': random.choice([0, 1]),
                'irrigacao_ativa': random.choice([0, 1]),
                'cultura': random.choice(['banana', 'milho'])
            }
            return data
        
        elif self.data_source == 'serial':
            # TODO: Implementar leitura serial real
            pass
        
        elif self.data_source == 'csv':
            # TODO: Implementar leitura de CSV
            pass
    
    def predict_with_model(self, sensor_data):
        """
        Faz previsão com modelo ML (placeholder)
        
        Args:
            sensor_data (dict): Dados dos sensores
        
        Returns:
            dict: Previsões
        """
        # TODO: Carregar modelo real quando disponível
        # Por enquanto, usa lógica simplificada
        
        volume_irrigacao = 0.0
        if sensor_data['umidade_solo'] < 50:
            volume_irrigacao = 10 - (sensor_data['umidade_solo'] * 0.15)
        
        dosagem_n = 0 if sensor_data['nitrogenio'] else 12
        dosagem_p = 0 if sensor_data['fosforo'] else 8
        dosagem_k = 0 if sensor_data['potassio'] else 15
        
        # Rendimento baseado em condições
        rendimento_base = 25000 if sensor_data['cultura'] == 'banana' else 8000
        fator = 1.0
        
        if 50 <= sensor_data['umidade_solo'] <= 70:
            fator *= 1.0
        else:
            fator *= 0.85
        
        if 6.0 <= sensor_data['ph_solo'] <= 7.0:
            fator *= 1.0
        else:
            fator *= 0.9
        
        rendimento = rendimento_base * fator
        
        return {
            'volume_irrigacao': round(max(0, volume_irrigacao), 1),
            'dosagem_n': dosagem_n,
            'dosagem_p': dosagem_p,
            'dosagem_k': dosagem_k,
            'rendimento_estimado': round(rendimento, 0),
            'confianca': 0.85,
            'modelo_versao': 'v1.0_placeholder'
        }
    
    def ingest_cycle(self):
        """Executa um ciclo completo de ingestão"""
        try:
            # 1. Lê dados dos sensores
            sensor_data = self.read_sensor_data()
            
            # 2. Insere no banco
            reading_id = self.db.insert_sensor_reading(sensor_data)
            
            # 3. Faz previsão
            prediction = self.predict_with_model(sensor_data)
            
            # 4. Salva previsão
            self.db.insert_prediction(reading_id, prediction)
            
            # 5. Registra ação de irrigação se necessário
            if sensor_data['irrigacao_ativa']:
                motivo = "Umidade baixa" if sensor_data['umidade_solo'] < 40 else "Manutenção"
                self.db.insert_irrigation_action(
                    reading_id, 
                    'LIGAR', 
                    motivo,
                    volume=prediction['volume_irrigacao'],
                    duracao=30
                )
            
            logging.info(f"✅ Ciclo de ingestão completo: ID {reading_id}")
            
        except Exception as e:
            logging.error(f"❌ Erro no ciclo de ingestão: {e}")
    
    def start_auto_update(self, interval_seconds=5):
        """
        Inicia atualização automática
        
        Args:
            interval_seconds (int): Intervalo entre atualizações
        """
        self.is_running = True
        
        logging.info(f"🔄 Iniciando ingestão automática (intervalo: {interval_seconds}s)")
        logging.info("   Pressione Ctrl+C para parar")
        
        schedule.every(interval_seconds).seconds.do(self.ingest_cycle)
        
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("\n⚠️  Ingestão interrompida pelo usuário")
            self.is_running = False
    
    def stop(self):
        """Para a ingestão automática"""
        self.is_running = False
        logging.info("🛑 Ingestão automática parada")


if __name__ == "__main__":
    # Inicializa banco de dados
    db = FarmTechDatabase('database/farmtech.db')
    
    # Exibe estatísticas iniciais
    stats = db.get_statistics()
    print("\n📊 Estatísticas do Banco:")
    print(f"   Total de leituras: {stats['total_leituras']}")
    print(f"   Total de previsões: {stats['total_previsoes']}")
    print(f"   Total de ações: {stats['total_acoes']}")
    
    # Inicializa ingestão automática
    print("\n🚀 Iniciando sistema de ingestão automática...")
    print("   Modo: Simulação de dados")
    print("   Intervalo: 5 segundos")
    
    ingestion = AutoIngestion(db, data_source='simulate')
    
    try:
        ingestion.start_auto_update(interval_seconds=5)
    finally:
        db.close()
        print("\n✅ Sistema encerrado com sucesso")