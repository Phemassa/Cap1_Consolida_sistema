"""
ESP32 Serial Bridge - Comunicação entre Web App e ESP32 (Wokwi)
FarmTech Solutions - Fase 2

Este módulo permite comunicação bidirecional entre a aplicação web Flask
e o simulador ESP32 no Wokwi através da porta serial.
"""

import serial
import serial.tools.list_ports
import json
import time
import threading
from typing import Optional, Dict, Callable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ESP32SerialBridge:
    """
    Ponte de comunicação serial com ESP32 no Wokwi
    """
    
    def __init__(self, port: Optional[str] = None, baudrate: int = 115200):
        """
        Inicializa a ponte serial
        
        Args:
            port: Porta COM (ex: 'COM3'). Se None, tenta detectar automaticamente
            baudrate: Taxa de transmissão (padrão: 115200)
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_connection: Optional[serial.Serial] = None
        self.is_connected = False
        self.last_data: Dict = {}
        self.data_callback: Optional[Callable] = None
        self.read_thread: Optional[threading.Thread] = None
        self.running = False
        
    def find_esp32_port(self) -> Optional[str]:
        """
        Tenta encontrar automaticamente a porta do ESP32
        
        Returns:
            str: Nome da porta encontrada ou None
        """
        logger.info("🔍 Procurando porta ESP32...")
        ports = serial.tools.list_ports.comports()
        
        for port in ports:
            # ESP32 geralmente aparece como "USB Serial" ou "CH340"
            if any(keyword in port.description.upper() for keyword in 
                   ['USB', 'SERIAL', 'CH340', 'CP210', 'FTDI']):
                logger.info(f"✅ Porta encontrada: {port.device} - {port.description}")
                return port.device
        
        logger.warning("⚠️  Nenhuma porta ESP32 encontrada")
        return None
    
    def connect(self) -> bool:
        """
        Conecta à porta serial do ESP32
        
        Returns:
            bool: True se conectado com sucesso
        """
        try:
            # Se porta não especificada, tenta detectar
            if not self.port:
                self.port = self.find_esp32_port()
                if not self.port:
                    logger.error("❌ Não foi possível encontrar porta ESP32")
                    return False
            
            # Abre conexão serial
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1
            )
            
            # Aguarda ESP32 inicializar
            time.sleep(2)
            
            self.is_connected = True
            logger.info(f"✅ Conectado ao ESP32 em {self.port}")
            
            # Inicia thread de leitura
            self.running = True
            self.read_thread = threading.Thread(target=self._read_loop, daemon=True)
            self.read_thread.start()
            
            return True
            
        except serial.SerialException as e:
            logger.error(f"❌ Erro ao conectar: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self):
        """Desconecta da porta serial"""
        self.running = False
        if self.read_thread:
            self.read_thread.join(timeout=2)
        
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            logger.info("🔌 Desconectado do ESP32")
        
        self.is_connected = False
    
    def _read_loop(self):
        """Loop de leitura contínua em thread separada"""
        while self.running and self.serial_connection and self.serial_connection.is_open:
            try:
                if self.serial_connection.in_waiting > 0:
                    line = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        self._process_line(line)
            except Exception as e:
                logger.error(f"❌ Erro na leitura: {e}")
                time.sleep(0.1)
    
    def _process_line(self, line: str):
        """
        Processa linha recebida do ESP32
        
        Args:
            line: Linha recebida
        """
        # Tenta interpretar como JSON
        if line.startswith('{') and line.endswith('}'):
            try:
                data = json.loads(line)
                self.last_data = data
                if self.data_callback:
                    self.data_callback(data)
            except json.JSONDecodeError:
                logger.debug(f"📝 ESP32: {line}")
        else:
            logger.debug(f"📝 ESP32: {line}")
    
    def send_command(self, command: str) -> bool:
        """
        Envia comando para ESP32
        
        Args:
            command: Comando a enviar (ex: "GET_STATUS", "SET_RELAY:ON")
            
        Returns:
            bool: True se enviado com sucesso
        """
        if not self.is_connected or not self.serial_connection:
            logger.warning("⚠️  ESP32 não conectado")
            return False
        
        try:
            self.serial_connection.write(f"{command}\n".encode('utf-8'))
            logger.info(f"📤 Enviado: {command}")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao enviar comando: {e}")
            return False
    
    def set_npk(self, nitrogen: bool, phosphorus: bool, potassium: bool) -> bool:
        """
        Define estado dos fertilizantes NPK no ESP32
        
        Args:
            nitrogen: Estado do nitrogênio
            phosphorus: Estado do fósforo
            potassium: Estado do potássio
            
        Returns:
            bool: True se comandos enviados com sucesso
        """
        # ESP32 usa botões físicos, então enviamos comando para simular estado
        command = f"SET_NPK:{int(nitrogen)},{int(phosphorus)},{int(potassium)}"
        return self.send_command(command)
    
    def toggle_npk(self, nutrient: str) -> bool:
        """
        Alterna estado de um nutriente NPK
        
        Args:
            nutrient: 'N', 'P' ou 'K'
            
        Returns:
            bool: True se comando enviado
        """
        command = f"TOGGLE_NPK:{nutrient.upper()}"
        return self.send_command(command)
    
    def get_sensor_data(self) -> Optional[Dict]:
        """
        Solicita dados dos sensores ao ESP32
        
        Returns:
            dict: Último dado recebido ou None
        """
        if self.send_command("GET_SENSORS"):
            time.sleep(0.5)  # Aguarda resposta
            return self.last_data
        return None
    
    def get_last_data(self) -> Dict:
        """
        Retorna último dado recebido do ESP32
        
        Returns:
            dict: Último dado armazenado
        """
        return self.last_data.copy() if self.last_data else {}
    
    def get_status(self) -> Optional[Dict]:
        """
        Solicita status completo do sistema
        
        Returns:
            dict: Status do sistema
        """
        if self.send_command("GET_STATUS"):
            time.sleep(0.5)
            return self.last_data
        return None
    
    def set_relay(self, state: bool) -> bool:
        """
        Liga/desliga relé (bomba)
        
        Args:
            state: True para ligar, False para desligar
            
        Returns:
            bool: True se comando enviado
        """
        command = f"SET_RELAY:{'ON' if state else 'OFF'}"
        return self.send_command(command)
    
    def set_data_callback(self, callback: Callable[[Dict], None]):
        """
        Define callback para processar dados recebidos
        
        Args:
            callback: Função que recebe dict com dados
        """
        self.data_callback = callback
    
    def __enter__(self):
        """Context manager - entrada"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager - saída"""
        self.disconnect()


# Instância global (singleton)
_bridge_instance: Optional[ESP32SerialBridge] = None


def get_bridge(port: Optional[str] = None) -> ESP32SerialBridge:
    """
    Obtém instância singleton da ponte serial
    
    Args:
        port: Porta COM (opcional)
        
    Returns:
        ESP32SerialBridge: Instância da ponte
    """
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = ESP32SerialBridge(port=port)
    return _bridge_instance


def connect_to_esp32(port: Optional[str] = None) -> bool:
    """
    Conecta à ESP32
    
    Args:
        port: Porta COM (opcional, tenta autodetectar)
        
    Returns:
        bool: True se conectado
    """
    bridge = get_bridge(port)
    return bridge.connect()


def disconnect_esp32():
    """Desconecta do ESP32"""
    global _bridge_instance
    if _bridge_instance:
        _bridge_instance.disconnect()
        _bridge_instance = None


# Exemplo de uso
if __name__ == "__main__":
    print("=== Teste de Comunicação ESP32 ===\n")
    
    with ESP32SerialBridge() as bridge:
        if bridge.is_connected:
            print("✅ Conectado ao ESP32!")
            
            # Solicita status
            print("\n📊 Solicitando status...")
            bridge.get_status()
            time.sleep(1)
            
            # Alterna NPK
            print("\n🧪 Testando toggle NPK...")
            bridge.toggle_npk('N')
            time.sleep(1)
            bridge.toggle_npk('P')
            time.sleep(1)
            bridge.toggle_npk('K')
            time.sleep(1)
            
            # Solicita sensores
            print("\n📡 Lendo sensores...")
            data = bridge.get_sensor_data()
            if data:
                print(f"Dados: {json.dumps(data, indent=2)}")
            
            print("\n⏳ Aguardando 5 segundos para receber dados...")
            time.sleep(5)
        else:
            print("❌ Não foi possível conectar ao ESP32")
            print("💡 Dicas:")
            print("   - Verifique se o Wokwi Simulator está rodando")
            print("   - Verifique se a porta COM está correta")
            print("   - No Wokwi, vá em Settings > Serial Port")
