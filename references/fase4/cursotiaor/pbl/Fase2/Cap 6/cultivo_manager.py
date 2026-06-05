"""
Módulo de Gerenciamento de Cultivos
Implementa CRUD de cultivos com validações
"""

import json
from datetime import datetime
from file_utils import FileUtils


class CultivoManager:
    """Gerenciador de cultivos agrícolas"""
    
    def __init__(self):
        """Inicializa gerenciador com lista vazia"""
        self.cultivos = []
        self.proximo_id = 1
        self.file_utils = FileUtils()
    
    def adicionar_cultivo(self, nome, cultura_tipo, area_hectares, data_plantio,
                         npk_requisitos, ph_ideal, umidade_ideal):
        """
        Adiciona novo cultivo à lista
        
        Args:
            nome (str): Nome do cultivo
            cultura_tipo (str): Tipo (BANANA, MILHO, OUTRO)
            area_hectares (float): Área em hectares
            data_plantio (str): Data no formato YYYY-MM-DD
            npk_requisitos (dict): {'nitrogenio': float, 'fosforo': float, 'potassio': float}
            ph_ideal (float): pH ideal do solo
            umidade_ideal (float): Umidade ideal (%)
        
        Returns:
            int: ID do cultivo criado
        """
        # Validações
        if not nome or len(nome.strip()) == 0:
            raise ValueError("Nome não pode ser vazio")
        
        if area_hectares <= 0:
            raise ValueError("Área deve ser maior que zero")
        
        if ph_ideal < 3.0 or ph_ideal > 9.0:
            raise ValueError("pH deve estar entre 3.0 e 9.0")
        
        if umidade_ideal < 0 or umidade_ideal > 100:
            raise ValueError("Umidade deve estar entre 0 e 100%")
        
        # Valida NPK
        for nutriente, valor in npk_requisitos.items():
            if valor < 0:
                raise ValueError(f"{nutriente} não pode ser negativo")
        
        # Cria dicionário do cultivo
        cultivo = {
            'id': self.proximo_id,
            'nome': nome.strip(),
            'cultura_tipo': cultura_tipo.upper(),
            'area_hectares': area_hectares,
            'data_plantio': data_plantio,
            'npk_requisitos': npk_requisitos,
            'ph_ideal': ph_ideal,
            'umidade_ideal': umidade_ideal,
            'data_cadastro': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.cultivos.append(cultivo)
        cultivo_id = self.proximo_id
        self.proximo_id += 1
        
        # Salva automaticamente
        self.salvar_json()
        
        return cultivo_id
    
    def obter_cultivo(self, cultivo_id):
        """
        Busca cultivo por ID
        
        Args:
            cultivo_id (int): ID do cultivo
        
        Returns:
            dict: Dados do cultivo ou None se não encontrado
        """
        for cultivo in self.cultivos:
            if cultivo['id'] == cultivo_id:
                return cultivo
        return None
    
    def listar_cultivos(self):
        """
        Lista todos os cultivos
        
        Returns:
            list: Lista de dicionários com cultivos
        """
        return self.cultivos.copy()
    
    def atualizar_cultivo(self, cultivo_id, **kwargs):
        """
        Atualiza campos de um cultivo
        
        Args:
            cultivo_id (int): ID do cultivo
            **kwargs: Campos a atualizar (nome, area_hectares, etc.)
        
        Returns:
            bool: True se atualizado, False se não encontrado
        """
        cultivo = self.obter_cultivo(cultivo_id)
        
        if not cultivo:
            return False
        
        # Atualiza apenas campos permitidos
        campos_permitidos = ['nome', 'area_hectares', 'ph_ideal', 'umidade_ideal', 'npk_requisitos']
        
        for campo, valor in kwargs.items():
            if campo in campos_permitidos:
                cultivo[campo] = valor
        
        self.salvar_json()
        return True
    
    def remover_cultivo(self, cultivo_id):
        """
        Remove cultivo da lista
        
        Args:
            cultivo_id (int): ID do cultivo
        
        Returns:
            bool: True se removido, False se não encontrado
        """
        for i, cultivo in enumerate(self.cultivos):
            if cultivo['id'] == cultivo_id:
                self.cultivos.pop(i)
                self.salvar_json()
                return True
        return False
    
    def obter_cultivos_por_tipo(self, cultura_tipo):
        """
        Filtra cultivos por tipo de cultura
        
        Args:
            cultura_tipo (str): Tipo (BANANA, MILHO, etc.)
        
        Returns:
            list: Cultivos do tipo especificado
        """
        return [c for c in self.cultivos if c['cultura_tipo'] == cultura_tipo.upper()]
    
    def calcular_area_total(self):
        """
        Calcula área total de todos os cultivos
        
        Returns:
            float: Área total em hectares
        """
        return sum(c['area_hectares'] for c in self.cultivos)
    
    def salvar_json(self, arquivo='data/cultivos.json'):
        """
        Salva cultivos em arquivo JSON
        
        Args:
            arquivo (str): Caminho do arquivo
        """
        self.file_utils.salvar_json(self.cultivos, arquivo)
    
    def carregar_json(self, arquivo='data/cultivos.json'):
        """
        Carrega cultivos de arquivo JSON
        
        Args:
            arquivo (str): Caminho do arquivo
        """
        self.cultivos = self.file_utils.carregar_json(arquivo)
        
        # Atualiza próximo ID
        if self.cultivos:
            max_id = max(c['id'] for c in self.cultivos)
            self.proximo_id = max_id + 1
