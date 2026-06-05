"""
Sistema de Comunicação Serial Python - ESP32
FarmTech Solutions - Fase 2
FIAP - Projeto Interdisciplinar

Este script permite comunicação bidirecional entre Python e ESP32
para controle do sistema de irrigação inteligente.

Funcionalidades:
- Leitura de dados dos sensores em JSON
- Envio de comandos para o ESP32
- Controle da bomba de irrigação
- Monitoramento em tempo real
- Integração com dados meteorológicos
"""

import serial
import json
import time
import sys
from datetime import datetime
from typing import Optional, Dict, Any

class ESP32Communication:
    """Classe para gerenciar comunicação com ESP32"""
    
    def __init__(self, port: str = 'COM3', baudrate: int = 115200, timeout: int = 2):
        """
        Inicializa comunicação serial
        
        Args:
            port: Porta serial (COM3 para Windows, /dev/ttyUSB0 para Linux)
            baudrate: Taxa de transmissão (115200 padrão ESP32)
            timeout: Timeout para leitura em segundos
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.is_connected = False
        
    def connect(self) -> bool:
        """
        Estabelece conexão com ESP32
        
        Returns:
            True se conectado com sucesso
        """
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            time.sleep(2)  # Aguarda estabilização
            self.is_connected = True
            print(f"✅ Conectado ao ESP32 na porta {self.port}")
            return True
        except serial.SerialException as e:
            print(f"❌ Erro ao conectar: {e}")
            print(f"💡 Dica: Verifique se a porta {self.port} está correta")
            print("   Windows: COM3, COM4, etc.")
            print("   Linux: /dev/ttyUSB0, /dev/ttyACM0, etc.")
            self.is_connected = False
            return False
    
    def disconnect(self):
        """Fecha conexão serial"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            self.is_connected = False
            print("🔌 Desconectado do ESP32")
    
    def send_command(self, command: str) -> bool:
        """
        Envia comando para ESP32
        
        Args:
            command: Comando a ser enviado
            
        Returns:
            True se enviado com sucesso
        """
        if not self.is_connected:
            print("❌ Não conectado ao ESP32")
            return False
        
        try:
            self.serial_conn.write(f"{command}\n".encode())
            print(f"📤 Comando enviado: {command}")
            return True
        except Exception as e:
            print(f"❌ Erro ao enviar comando: {e}")
            return False
    
    def read_line(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Lê uma linha da serial
        
        Args:
            timeout: Timeout opcional em segundos
            
        Returns:
            Linha lida ou None
        """
        if not self.is_connected:
            return None
        
        try:
            if timeout:
                old_timeout = self.serial_conn.timeout
                self.serial_conn.timeout = timeout
            
            line = self.serial_conn.readline().decode('utf-8').strip()
            
            if timeout:
                self.serial_conn.timeout = old_timeout
            
            return line if line else None
        except Exception as e:
            print(f"❌ Erro ao ler: {e}")
            return None
    
    def get_sensor_data(self) -> Optional[Dict[str, Any]]:
        """
        Solicita e retorna dados dos sensores em JSON
        
        Returns:
            Dicionário com dados dos sensores ou None
        """
        if not self.send_command("GET_SENSORS"):
            return None
        
        time.sleep(0.5)  # Aguarda processamento
        
        # Lê resposta (pode ter múltiplas linhas antes do JSON)
        for _ in range(10):  # Tenta ler até 10 linhas
            line = self.read_line(timeout=1.0)
            if line and line.startswith('{'):
                try:
                    data = json.loads(line)
                    return data
                except json.JSONDecodeError:
                    continue
        
        print("⚠️  Não foi possível obter dados JSON")
        return None
    
    def set_relay(self, state: bool) -> bool:
        """
        Liga/desliga a bomba de irrigação
        
        Args:
            state: True para ligar, False para desligar
            
        Returns:
            True se comando enviado com sucesso
        """
        command = "SET_RELAY:ON" if state else "SET_RELAY:OFF"
        return self.send_command(command)
    
    def set_culture(self, culture_id: int) -> bool:
        """
        Define a cultura atual
        
        Args:
            culture_id: ID da cultura (0-4)
            
        Returns:
            True se comando enviado com sucesso
        """
        if not 0 <= culture_id <= 4:
            print("❌ ID de cultura inválido (0-4)")
            return False
        
        return self.send_command(f"SET_CULTURE:{culture_id}")
    
    def check_irrigation(self) -> bool:
        """
        Solicita verificação de necessidade de irrigação
        
        Returns:
            True se comando enviado com sucesso
        """
        return self.send_command("CHECK_IRRIGATION")
    
    def print_data(self) -> bool:
        """
        Solicita impressão formatada dos dados
        
        Returns:
            True se comando enviado com sucesso
        """
        return self.send_command("PRINT_DATA")
    
    def monitor_continuous(self, interval: int = 5, duration: Optional[int] = None):
        """
        Monitora dados continuamente
        
        Args:
            interval: Intervalo entre leituras em segundos
            duration: Duração total em segundos (None = infinito)
        """
        print(f"\n🔄 Monitoramento contínuo iniciado (intervalo: {interval}s)")
        print("   Pressione Ctrl+C para parar\n")
        
        start_time = time.time()
        
        try:
            while True:
                if duration and (time.time() - start_time) >= duration:
                    break
                
                data = self.get_sensor_data()
                if data:
                    self.display_sensor_data(data)
                
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n⏸️  Monitoramento interrompido")
    
    def display_sensor_data(self, data: Dict[str, Any]):
        """
        Exibe dados dos sensores formatados
        
        Args:
            data: Dicionário com dados dos sensores
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"\n{'='*50}")
        print(f"📊 Dados dos Sensores - {timestamp}")
        print(f"{'='*50}")
        
        # NPK
        npk = data.get('npk', {})
        print(f"🌱 NPK:")
        print(f"   N (Nitrogênio):  {'✅ SIM' if npk.get('nitrogen') else '❌ NÃO'}")
        print(f"   P (Fósforo):     {'✅ SIM' if npk.get('phosphorus') else '❌ NÃO'}")
        print(f"   K (Potássio):    {'✅ SIM' if npk.get('potassium') else '❌ NÃO'}")
        
        # pH
        ph = data.get('ph', {})
        ph_level = ph.get('ph_level', 0)
        print(f"\n🧪 pH do Solo:")
        print(f"   Valor: {ph_level:.2f}")
        print(f"   Raw ADC: {ph.get('raw_value', 0)}")
        
        # Ambiente
        env = data.get('environment', {})
        print(f"\n🌡️  Ambiente:")
        print(f"   Temperatura: {env.get('temperature', 0):.1f}°C")
        print(f"   Umidade:     {env.get('humidity', 0):.1f}%")
        
        # Atuadores
        actuators = data.get('actuators', {})
        pump_state = actuators.get('irrigation_pump', False)
        print(f"\n💧 Irrigação:")
        print(f"   Bomba: {'🟢 LIGADA' if pump_state else '🔴 DESLIGADA'}")
        
        print(f"{'='*50}\n")


def interactive_menu(esp: ESP32Communication):
    """Menu interativo para controle do ESP32"""
    
    cultures = {
        '0': 'Tomate',
        '1': 'Milho',
        '2': 'Soja',
        '3': 'Banana',
        '4': 'Café'
    }
    
    while True:
        print("\n" + "="*50)
        print("🌾 FarmTech Solutions - Menu de Controle")
        print("="*50)
        print("1. 📊 Obter dados dos sensores")
        print("2. 💧 Ligar bomba de irrigação")
        print("3. 🛑 Desligar bomba de irrigação")
        print("4. 🌱 Mudar cultura")
        print("5. 🔍 Verificar necessidade de irrigação")
        print("6. 📝 Imprimir dados formatados")
        print("7. 🔄 Monitoramento contínuo")
        print("8. 📋 Ver comandos disponíveis")
        print("9. 🚪 Sair")
        print("="*50)
        
        choice = input("Escolha uma opção: ").strip()
        
        if choice == '1':
            data = esp.get_sensor_data()
            if data:
                esp.display_sensor_data(data)
        
        elif choice == '2':
            esp.set_relay(True)
            time.sleep(1)
            esp.read_line()
        
        elif choice == '3':
            esp.set_relay(False)
            time.sleep(1)
            esp.read_line()
        
        elif choice == '4':
            print("\nCulturas disponíveis:")
            for key, name in cultures.items():
                print(f"  {key} - {name}")
            culture_id = input("Digite o ID da cultura: ").strip()
            if culture_id in cultures:
                esp.set_culture(int(culture_id))
                time.sleep(1)
                esp.read_line()
        
        elif choice == '5':
            esp.check_irrigation()
            time.sleep(1)
            # Lê múltiplas linhas de resposta
            for _ in range(5):
                line = esp.read_line(timeout=0.5)
                if line:
                    print(line)
        
        elif choice == '6':
            esp.print_data()
            time.sleep(1)
            # Lê múltiplas linhas de resposta
            for _ in range(15):
                line = esp.read_line(timeout=0.5)
                if line:
                    print(line)
        
        elif choice == '7':
            interval = input("Intervalo entre leituras (segundos) [5]: ").strip()
            interval = int(interval) if interval else 5
            esp.monitor_continuous(interval=interval)
        
        elif choice == '8':
            esp.send_command("HELP")
            time.sleep(1)
            for _ in range(20):
                line = esp.read_line(timeout=0.5)
                if line:
                    print(line)
        
        elif choice == '9':
            print("👋 Encerrando...")
            break
        
        else:
            print("❌ Opção inválida")


def main():
    """Função principal"""
    print("="*60)
    print("🌾 FarmTech Solutions - Comunicação Python-ESP32")
    print("   Sistema de Irrigação Inteligente - Fase 2")
    print("="*60)
    
    # Configuração da porta
    port = input("\nPorta serial [COM3]: ").strip() or "COM3"
    
    # Cria instância de comunicação
    esp = ESP32Communication(port=port)
    
    # Conecta ao ESP32
    if not esp.connect():
        print("\n💡 Dicas de troubleshooting:")
        print("   1. Verifique se o ESP32 está conectado via USB")
        print("   2. Instale drivers: pip install pyserial")
        print("   3. Verifique a porta no Gerenciador de Dispositivos (Windows)")
        print("   4. No Wokwi VS Code, use porta virtual RFC2217")
        return
    
    try:
        # Aguarda mensagens iniciais
        print("\n📡 Aguardando mensagens iniciais...")
        time.sleep(2)
        for _ in range(10):
            line = esp.read_line(timeout=0.5)
            if line:
                print(line)
        
        # Inicia menu interativo
        interactive_menu(esp)
    
    finally:
        esp.disconnect()


if __name__ == "__main__":
    main()
