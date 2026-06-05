"""
Módulo de Monitoramento de Sensores
Registra e analisa leituras de sensores IoT
"""

import json
from datetime import datetime
from file_utils import FileUtils


class SensorMonitor:
    """Monitor de sensores agrícolas (temperatura, umidade, pH, NPK)"""
    
    def __init__(self):
        """Inicializa monitor com lista vazia de leituras"""
        self.leituras = []
        self.proximo_id = 1
        self.file_utils = FileUtils()
    
    def adicionar_leitura(self, cultivo_id, temperatura, umidade_ar, ph, npk_ok):
        """
        Registra nova leitura de sensores
        
        Args:
            cultivo_id (int): ID do cultivo monitorado
            temperatura (float): Temperatura em °C
            umidade_ar (float): Umidade do ar em %
            ph (float): pH do solo
            npk_ok (dict): Status NPK {'N': bool, 'P': bool, 'K': bool}
        
        Returns:
            int: ID da leitura criada
        """
        # Validações
        if temperatura < -10 or temperatura > 50:
            raise ValueError("Temperatura deve estar entre -10°C e 50°C")
        
        if umidade_ar < 0 or umidade_ar > 100:
            raise ValueError("Umidade do ar deve estar entre 0 e 100%")
        
        if ph < 3.0 or ph > 9.0:
            raise ValueError("pH deve estar entre 3.0 e 9.0")
        
        # Converte umidade ar → solo (fórmula do Cap 1)
        umidade_solo = umidade_ar * 0.8
        
        # Classifica temperatura
        if temperatura < 15:
            temp_status = 'FRIA'
        elif temperatura <= 25:
            temp_status = 'IDEAL'
        elif temperatura <= 35:
            temp_status = 'ALTA'
        else:
            temp_status = 'CRÍTICA'
        
        # Classifica pH
        if ph < 5.5:
            ph_status = 'ÁCIDO'
        elif ph <= 7.5:
            ph_status = 'NEUTRO'
        else:
            ph_status = 'ALCALINO'
        
        # Cria leitura
        leitura = {
            'id': self.proximo_id,
            'cultivo_id': cultivo_id,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'temperatura': temperatura,
            'temp_status': temp_status,
            'umidade_ar': umidade_ar,
            'umidade_solo': round(umidade_solo, 1),
            'ph': ph,
            'ph_status': ph_status,
            'npk_ok': npk_ok
        }
        
        self.leituras.append(leitura)
        leitura_id = self.proximo_id
        self.proximo_id += 1
        
        # Salva automaticamente
        self.salvar_json()
        
        return leitura_id
    
    def obter_leitura(self, leitura_id):
        """
        Busca leitura por ID
        
        Args:
            leitura_id (int): ID da leitura
        
        Returns:
            dict: Dados da leitura ou None
        """
        for leitura in self.leituras:
            if leitura['id'] == leitura_id:
                return leitura
        return None
    
    def listar_leituras(self):
        """
        Lista todas as leituras
        
        Returns:
            list: Lista de leituras
        """
        return self.leituras.copy()
    
    def obter_leituras_cultivo(self, cultivo_id):
        """
        Filtra leituras por cultivo
        
        Args:
            cultivo_id (int): ID do cultivo
        
        Returns:
            list: Leituras do cultivo especificado
        """
        return [l for l in self.leituras if l['cultivo_id'] == cultivo_id]
    
    def obter_ultima_leitura(self, cultivo_id):
        """
        Obtém leitura mais recente de um cultivo
        
        Args:
            cultivo_id (int): ID do cultivo
        
        Returns:
            dict: Última leitura ou None
        """
        leituras_cultivo = self.obter_leituras_cultivo(cultivo_id)
        
        if not leituras_cultivo:
            return None
        
        # Ordena por timestamp (mais recente primeiro)
        leituras_cultivo.sort(key=lambda x: x['timestamp'], reverse=True)
        return leituras_cultivo[0]
    
    def calcular_media_temperatura(self, cultivo_id):
        """
        Calcula temperatura média de um cultivo
        
        Args:
            cultivo_id (int): ID do cultivo
        
        Returns:
            float: Temperatura média ou None
        """
        leituras = self.obter_leituras_cultivo(cultivo_id)
        
        if not leituras:
            return None
        
        temperaturas = [l['temperatura'] for l in leituras]
        return sum(temperaturas) / len(temperaturas)
    
    def calcular_media_umidade(self, cultivo_id):
        """
        Calcula umidade média do solo de um cultivo
        
        Args:
            cultivo_id (int): ID do cultivo
        
        Returns:
            float: Umidade média ou None
        """
        leituras = self.obter_leituras_cultivo(cultivo_id)
        
        if not leituras:
            return None
        
        umidades = [l['umidade_solo'] for l in leituras]
        return sum(umidades) / len(umidades)
    
    def verificar_npk_disponivel(self, leitura):
        """
        Verifica quais nutrientes estão adequados
        
        Args:
            leitura (dict): Dados da leitura
        
        Returns:
            tuple: (todos_ok: bool, faltantes: list)
        """
        npk_ok = leitura['npk_ok']
        faltantes = [nutriente for nutriente, ok in npk_ok.items() if not ok]
        
        return (len(faltantes) == 0, faltantes)
    
    def salvar_json(self, arquivo='data/sensores.json'):
        """
        Salva leituras em arquivo JSON
        
        Args:
            arquivo (str): Caminho do arquivo
        """
        self.file_utils.salvar_json(self.leituras, arquivo)
    
    def carregar_json(self, arquivo='data/sensores.json'):
        """
        Carrega leituras de arquivo JSON
        
        Args:
            arquivo (str): Caminho do arquivo
        """
        self.leituras = self.file_utils.carregar_json(arquivo)
        
        # Atualiza próximo ID
        if self.leituras:
            max_id = max(l['id'] for l in self.leituras)
            self.proximo_id = max_id + 1
