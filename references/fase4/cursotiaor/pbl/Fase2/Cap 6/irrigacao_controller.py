"""
Módulo de Controle de Irrigação
Implementa lógica de decisão baseada nas 6 condições do Cap 1
"""

import json
from datetime import datetime
from file_utils import FileUtils


class IrrigacaoController:
    """Controlador de irrigação inteligente"""
    
    # Constantes de thresholds (do FarmTech.ino Cap 1)
    UMIDADE_MINIMA = 40.0
    UMIDADE_IDEAL = 60.0
    UMIDADE_MAXIMA = 80.0
    PH_MINIMO = 5.5
    PH_MAXIMO = 7.5
    TEMP_ALTA = 30.0
    
    def __init__(self):
        """Inicializa controlador com histórico vazio"""
        self.irrigacoes = []
        self.proximo_id = 1
        self.file_utils = FileUtils()
    
    def decidir_irrigacao(self, cultivo, leitura):
        """
        Decide se deve irrigar baseado nas 6 condições do Cap 1
        
        Args:
            cultivo (dict): Dados do cultivo
            leitura (dict): Leitura de sensores
        
        Returns:
            dict: {'deve_irrigar': bool, 'motivo': str, 'condicao': int}
        """
        umidade = leitura['umidade_solo']
        ph = leitura['ph']
        temp = leitura['temperatura']
        npk_ok = leitura['npk_ok']
        cultura_tipo = cultivo['cultura_tipo']
        
        # CONDIÇÃO 1: Solo muito seco (CRÍTICO)
        if umidade < self.UMIDADE_MINIMA:
            return {
                'deve_irrigar': True,
                'motivo': f'Umidade crítica ({umidade}%) < {self.UMIDADE_MINIMA}%',
                'condicao': 1
            }
        
        # CONDIÇÃO 2: Solo encharcado (NUNCA IRRIGAR)
        if umidade > self.UMIDADE_MAXIMA:
            return {
                'deve_irrigar': False,
                'motivo': f'Solo encharcado ({umidade}%) > {self.UMIDADE_MAXIMA}%',
                'condicao': 2
            }
        
        # CONDIÇÃO 3: NPK insuficiente + umidade subótima
        if not all(npk_ok.values()) and umidade < self.UMIDADE_IDEAL:
            faltantes = [k for k, v in npk_ok.items() if not v]
            
            # Verifica nutriente crítico por cultura (lógica do Cap 1)
            if cultura_tipo == 'BANANA':
                # Banana: Potássio crítico (20 g/m²)
                if not npk_ok.get('K', False):
                    return {
                        'deve_irrigar': True,
                        'motivo': f'NPK insuficiente (K crítico para BANANA) + umidade {umidade}% < {self.UMIDADE_IDEAL}%',
                        'condicao': 3
                    }
            elif cultura_tipo == 'MILHO':
                # Milho: Nitrogênio crítico (12 g/m²)
                if not npk_ok.get('N', False):
                    return {
                        'deve_irrigar': True,
                        'motivo': f'NPK insuficiente (N crítico para MILHO) + umidade {umidade}% < {self.UMIDADE_IDEAL}%',
                        'condicao': 3
                    }
            
            # Cultura genérica: qualquer NPK faltante
            return {
                'deve_irrigar': True,
                'motivo': f'NPK insuficiente ({", ".join(faltantes)}) + umidade {umidade}% < {self.UMIDADE_IDEAL}%',
                'condicao': 3
            }
        
        # CONDIÇÃO 4: pH fora da faixa + umidade baixa
        if (ph < self.PH_MINIMO or ph > self.PH_MAXIMO) and umidade < self.UMIDADE_IDEAL:
            return {
                'deve_irrigar': True,
                'motivo': f'pH fora da faixa ({ph}) + umidade {umidade}% < {self.UMIDADE_IDEAL}%',
                'condicao': 4
            }
        
        # CONDIÇÃO 5: Temperatura alta + umidade baixa
        if temp > self.TEMP_ALTA and umidade < self.UMIDADE_IDEAL:
            return {
                'deve_irrigar': True,
                'motivo': f'Temperatura alta ({temp}°C) > {self.TEMP_ALTA}°C + umidade {umidade}% < {self.UMIDADE_IDEAL}%',
                'condicao': 5
            }
        
        # CONDIÇÃO 6: Condições ideais
        return {
            'deve_irrigar': False,
            'motivo': 'Condições ótimas - irrigação desnecessária',
            'condicao': 6
        }
    
    def registrar_irrigacao(self, cultivo_id, leitura_id, acionado, motivo):
        """
        Registra decisão de irrigação no histórico
        
        Args:
            cultivo_id (int): ID do cultivo
            leitura_id (int): ID da leitura de sensores
            acionado (bool): Se irrigação foi acionada
            motivo (str): Motivo da decisão
        
        Returns:
            int: ID do registro criado
        """
        registro = {
            'id': self.proximo_id,
            'cultivo_id': cultivo_id,
            'leitura_id': leitura_id,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'acionado': acionado,
            'motivo': motivo
        }
        
        self.irrigacoes.append(registro)
        registro_id = self.proximo_id
        self.proximo_id += 1
        
        # Salva automaticamente
        self.salvar_json()
        
        return registro_id
    
    def listar_irrigacoes(self):
        """
        Lista todos os registros de irrigação
        
        Returns:
            list: Histórico completo
        """
        return self.irrigacoes.copy()
    
    def obter_irrigacoes_cultivo(self, cultivo_id):
        """
        Filtra irrigações por cultivo
        
        Args:
            cultivo_id (int): ID do cultivo
        
        Returns:
            list: Irrigações do cultivo
        """
        return [i for i in self.irrigacoes if i['cultivo_id'] == cultivo_id]
    
    def calcular_taxa_acionamento(self, cultivo_id=None):
        """
        Calcula taxa de acionamento de irrigação
        
        Args:
            cultivo_id (int, optional): ID do cultivo (None = todos)
        
        Returns:
            float: Taxa de acionamento (0-100%)
        """
        if cultivo_id is None:
            irrigacoes = self.irrigacoes
        else:
            irrigacoes = self.obter_irrigacoes_cultivo(cultivo_id)
        
        if not irrigacoes:
            return 0.0
        
        acionadas = sum(1 for i in irrigacoes if i['acionado'])
        return (acionadas / len(irrigacoes)) * 100
    
    def contar_irrigacoes_acionadas(self, cultivo_id=None):
        """
        Conta quantas irrigações foram acionadas
        
        Args:
            cultivo_id (int, optional): ID do cultivo (None = todos)
        
        Returns:
            int: Número de irrigações acionadas
        """
        if cultivo_id is None:
            irrigacoes = self.irrigacoes
        else:
            irrigacoes = self.obter_irrigacoes_cultivo(cultivo_id)
        
        return sum(1 for i in irrigacoes if i['acionado'])
    
    def obter_ultima_irrigacao(self, cultivo_id):
        """
        Obtém última irrigação de um cultivo
        
        Args:
            cultivo_id (int): ID do cultivo
        
        Returns:
            dict: Última irrigação ou None
        """
        irrigacoes = self.obter_irrigacoes_cultivo(cultivo_id)
        
        if not irrigacoes:
            return None
        
        # Ordena por timestamp (mais recente primeiro)
        irrigacoes.sort(key=lambda x: x['timestamp'], reverse=True)
        return irrigacoes[0]
    
    def salvar_json(self, arquivo='data/irrigacoes.json'):
        """
        Salva histórico em arquivo JSON
        
        Args:
            arquivo (str): Caminho do arquivo
        """
        self.file_utils.salvar_json(self.irrigacoes, arquivo)
    
    def carregar_json(self, arquivo='data/irrigacoes.json'):
        """
        Carrega histórico de arquivo JSON
        
        Args:
            arquivo (str): Caminho do arquivo
        """
        self.irrigacoes = self.file_utils.carregar_json(arquivo)
        
        # Atualiza próximo ID
        if self.irrigacoes:
            max_id = max(i['id'] for i in self.irrigacoes)
            self.proximo_id = max_id + 1
