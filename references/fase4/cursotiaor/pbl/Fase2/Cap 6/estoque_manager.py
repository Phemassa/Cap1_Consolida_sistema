"""
Módulo de Gerenciamento de Estoque
Controla insumos agrícolas (fertilizantes, defensivos, sementes)
"""

import json
from datetime import datetime, timedelta
from file_utils import FileUtils


class EstoqueManager:
    """Gerenciador de estoque de insumos agrícolas"""
    
    def __init__(self):
        """Inicializa gerenciador com estoque vazio"""
        self.estoque = []
        self.file_utils = FileUtils()
    
    def adicionar_produto(self, produto, tipo, quantidade_kg, data_compra, validade):
        """
        Adiciona produto ao estoque
        
        Args:
            produto (str): Nome do produto
            tipo (str): Tipo (fertilizante, defensivo, sementes, outro)
            quantidade_kg (float): Quantidade em kg ou litros
            data_compra (str): Data de compra (YYYY-MM-DD)
            validade (str): Data de validade (YYYY-MM-DD)
        
        Returns:
            int: Índice do produto no estoque
        """
        # Validações
        if not produto or len(produto.strip()) == 0:
            raise ValueError("Nome do produto não pode ser vazio")
        
        if quantidade_kg <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        
        # Cria produto
        item = {
            'produto': produto.strip(),
            'tipo': tipo.lower(),
            'quantidade_kg': quantidade_kg,
            'data_compra': data_compra,
            'validade': validade,
            'data_cadastro': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.estoque.append(item)
        
        # Salva automaticamente
        self.salvar_json()
        
        return len(self.estoque) - 1
    
    def listar_estoque(self):
        """
        Lista todos os produtos em estoque
        
        Returns:
            list: Lista de produtos
        """
        return self.estoque.copy()
    
    def obter_produto(self, indice):
        """
        Obtém produto por índice
        
        Args:
            indice (int): Índice do produto na lista
        
        Returns:
            dict: Dados do produto ou None
        """
        if 0 <= indice < len(self.estoque):
            return self.estoque[indice]
        return None
    
    def registrar_aplicacao(self, indice, quantidade_aplicada):
        """
        Registra aplicação de produto (subtrai do estoque)
        
        Args:
            indice (int): Índice do produto
            quantidade_aplicada (float): Quantidade aplicada (kg ou L)
        
        Returns:
            float: Quantidade restante após aplicação
        """
        produto = self.obter_produto(indice)
        
        if not produto:
            raise ValueError(f"Produto com índice {indice} não encontrado")
        
        if quantidade_aplicada <= 0:
            raise ValueError("Quantidade aplicada deve ser maior que zero")
        
        if quantidade_aplicada > produto['quantidade_kg']:
            raise ValueError(f"Quantidade insuficiente em estoque ({produto['quantidade_kg']} kg disponíveis)")
        
        # Subtrai quantidade
        produto['quantidade_kg'] -= quantidade_aplicada
        
        # Salva
        self.salvar_json()
        
        return produto['quantidade_kg']
    
    def obter_produtos_por_tipo(self, tipo):
        """
        Filtra produtos por tipo
        
        Args:
            tipo (str): Tipo (fertilizante, defensivo, etc.)
        
        Returns:
            list: Produtos do tipo especificado
        """
        return [p for p in self.estoque if p['tipo'] == tipo.lower()]
    
    def verificar_alertas(self):
        """
        Verifica produtos com estoque baixo ou vencimento próximo
        
        Returns:
            list: Lista de alertas (strings descritivas)
        """
        alertas = []
        hoje = datetime.now()
        
        for i, produto in enumerate(self.estoque):
            # Alerta de estoque baixo (<10% do valor inicial estimado)
            # Estimamos valor inicial: se <50kg, alerta aos 5kg; se >50kg, alerta aos 10kg
            limite_baixo = 5.0 if produto['quantidade_kg'] < 50 else 10.0
            
            if produto['quantidade_kg'] < limite_baixo:
                alertas.append(f"⚠️  [{i}] {produto['produto']}: Estoque BAIXO ({produto['quantidade_kg']:.2f} kg)")
            
            # Alerta de vencimento próximo (<30 dias)
            try:
                validade = datetime.strptime(produto['validade'], '%Y-%m-%d')
                dias_ate_vencer = (validade - hoje).days
                
                if dias_ate_vencer < 0:
                    alertas.append(f"❌ [{i}] {produto['produto']}: VENCIDO desde {produto['validade']}")
                elif dias_ate_vencer < 30:
                    alertas.append(f"⚠️  [{i}] {produto['produto']}: Vencimento PRÓXIMO em {dias_ate_vencer} dias ({produto['validade']})")
            
            except ValueError:
                # Data inválida, ignora verificação de vencimento
                pass
        
        return alertas
    
    def calcular_valor_estoque(self, precos_unitarios=None):
        """
        Calcula valor total do estoque (requer preços)
        
        Args:
            precos_unitarios (dict, optional): Mapa {produto: preco_kg}
        
        Returns:
            float: Valor total ou None se preços não fornecidos
        """
        if not precos_unitarios:
            return None
        
        total = 0.0
        
        for produto in self.estoque:
            nome = produto['produto']
            quantidade = produto['quantidade_kg']
            
            if nome in precos_unitarios:
                preco = precos_unitarios[nome]
                total += quantidade * preco
        
        return total
    
    def remover_produto(self, indice):
        """
        Remove produto do estoque
        
        Args:
            indice (int): Índice do produto
        
        Returns:
            bool: True se removido, False se não encontrado
        """
        if 0 <= indice < len(self.estoque):
            self.estoque.pop(indice)
            self.salvar_json()
            return True
        return False
    
    def salvar_json(self, arquivo='data/estoque.json'):
        """
        Salva estoque em arquivo JSON
        
        Args:
            arquivo (str): Caminho do arquivo
        """
        self.file_utils.salvar_json(self.estoque, arquivo)
    
    def carregar_json(self, arquivo='data/estoque.json'):
        """
        Carrega estoque de arquivo JSON
        
        Args:
            arquivo (str): Caminho do arquivo
        """
        self.estoque = self.file_utils.carregar_json(arquivo)
