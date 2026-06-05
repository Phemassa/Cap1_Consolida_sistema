"""
Módulo de Utilitários de Arquivos
Funções para manipulação de JSON e arquivos texto
"""

import json
import os


class FileUtils:
    """Utilitários para manipulação de arquivos JSON e texto"""
    
    @staticmethod
    def salvar_json(dados, arquivo):
        """
        Salva dados em arquivo JSON
        
        Args:
            dados (list ou dict): Dados a serem salvos
            arquivo (str): Caminho do arquivo
        """
        # Garante que diretório existe
        diretorio = os.path.dirname(arquivo)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)
        
        # Salva com indentação legível
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def carregar_json(arquivo):
        """
        Carrega dados de arquivo JSON
        
        Args:
            arquivo (str): Caminho do arquivo
        
        Returns:
            list ou dict: Dados carregados ou lista vazia se arquivo não existe
        """
        if not os.path.exists(arquivo):
            return []
        
        with open(arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def salvar_texto(texto, arquivo, modo='w'):
        """
        Salva texto em arquivo
        
        Args:
            texto (str): Texto a ser salvo
            arquivo (str): Caminho do arquivo
            modo (str): Modo de abertura ('w' para sobrescrever, 'a' para anexar)
        """
        # Garante que diretório existe
        diretorio = os.path.dirname(arquivo)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)
        
        with open(arquivo, modo, encoding='utf-8') as f:
            f.write(texto)
    
    @staticmethod
    def carregar_texto(arquivo):
        """
        Carrega texto de arquivo
        
        Args:
            arquivo (str): Caminho do arquivo
        
        Returns:
            str: Conteúdo do arquivo ou string vazia se não existe
        """
        if not os.path.exists(arquivo):
            return ""
        
        with open(arquivo, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def arquivo_existe(arquivo):
        """
        Verifica se arquivo existe
        
        Args:
            arquivo (str): Caminho do arquivo
        
        Returns:
            bool: True se existe, False caso contrário
        """
        return os.path.exists(arquivo)
    
    @staticmethod
    def criar_diretorio(diretorio):
        """
        Cria diretório (e pais necessários)
        
        Args:
            diretorio (str): Caminho do diretório
        """
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
    
    @staticmethod
    def listar_arquivos(diretorio, extensao=None):
        """
        Lista arquivos em um diretório
        
        Args:
            diretorio (str): Caminho do diretório
            extensao (str, optional): Filtrar por extensão (ex: '.json')
        
        Returns:
            list: Lista de nomes de arquivos
        """
        if not os.path.exists(diretorio):
            return []
        
        arquivos = os.listdir(diretorio)
        
        if extensao:
            arquivos = [a for a in arquivos if a.endswith(extensao)]
        
        return arquivos
    
    @staticmethod
    def log_operacao(mensagem, arquivo='logs/operacoes.log'):
        """
        Registra operação em arquivo de log
        
        Args:
            mensagem (str): Mensagem a ser registrada
            arquivo (str): Caminho do arquivo de log
        """
        from datetime import datetime
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        linha_log = f"[{timestamp}] {mensagem}\n"
        
        FileUtils.salvar_texto(linha_log, arquivo, modo='a')
