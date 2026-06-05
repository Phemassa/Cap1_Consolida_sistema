"""
═══════════════════════════════════════════════════════════════════════════
FarmTech Solutions - Comunicação Serial com ESP32
═══════════════════════════════════════════════════════════════════════════

Script para comunicação entre Python (dados meteorológicos) e ESP32
Envia comandos via Serial Monitor para controle de irrigação baseado no clima

COMANDOS SUPORTADOS pelo ESP32:
- GET_WEATHER: Solicita dados meteorológicos atuais
- SET_WEATHER:temp,humid,pressure,rain: Define dados manualmente
- RAIN_ALERT:1/0: Alerta de chuva (1=chuva, 0=sem chuva)
- SUSPEND_IRRIGATION: Suspende irrigação por clima

═══════════════════════════════════════════════════════════════════════════
"""

import serial
import serial.tools.list_ports
import time
import json
from datetime import datetime
from weather_api import WeatherAPI

class SerialCommunicator:
    """Classe para comunicação serial com ESP32"""
    
    def __init__(self, baudrate: int = 115200):
        self.serial_port = None
        self.baudrate = baudrate
        self.weather_api = WeatherAPI()
        
    def list_available_ports(self):
        """Lista todas as portas seriais disponíveis"""
        ports = serial.tools.list_ports.comports()
        
        print("🔌 Portas seriais disponíveis:")
        if not ports:
            print("   Nenhuma porta encontrada")
            return []
        
        available_ports = []
        for i, port in enumerate(ports):
            print(f"   {i+1}. {port.device} - {port.description}")
            available_ports.append(port.device)
        
        return available_ports
    
    def connect(self, port: str = None) -> bool:
        """
        Conecta à porta serial do ESP32
        
        Args:
            port: Porta específica ou None para seleção automática
            
        Returns:
            True se conectou com sucesso
        """
        if not port:
            ports = self.list_available_ports()
            if not ports:
                print("❌ Nenhuma porta serial encontrada!")
                return False
            
            # Tenta conectar automaticamente na primeira porta
            port = ports[0]
            print(f"🔄 Tentando conectar automaticamente em {port}...")
        
        try:
            self.serial_port = serial.Serial(port, self.baudrate, timeout=1)
            time.sleep(2)  # Aguarda ESP32 reinicializar
            
            # Testa conexão
            self.send_command("PING")
            print(f"✅ Conectado com sucesso em {port}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao conectar em {port}: {e}")
            return False
    
    def disconnect(self):
        """Desconecta da porta serial"""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            print("🔌 Desconectado da porta serial")
    
    def send_command(self, command: str, wait_response: bool = True) -> str:
        """
        Envia comando para ESP32
        
        Args:
            command: Comando a ser enviado
            wait_response: Se deve aguardar resposta
            
        Returns:
            Resposta do ESP32 ou string vazia
        """
        if not self.serial_port or not self.serial_port.is_open:
            print("❌ Porta serial não conectada!")
            return ""
        
        try:
            # Envia comando
            message = f"{command}\n"
            self.serial_port.write(message.encode())
            self.serial_port.flush()
            
            print(f"📤 Enviado: {command}")
            
            if wait_response:
                # Aguarda resposta (timeout 5s)
                start_time = time.time()
                while time.time() - start_time < 5:
                    if self.serial_port.in_waiting > 0:
                        response = self.serial_port.readline().decode().strip()
                        if response:
                            print(f"📥 Resposta: {response}")
                            return response
                    time.sleep(0.1)
                
                print("⏰ Timeout aguardando resposta")
            
            return ""
            
        except Exception as e:
            print(f"❌ Erro ao enviar comando: {e}")
            return ""
    
    def send_weather_data(self, manual_data: dict = None) -> bool:
        """
        Envia dados meteorológicos para ESP32
        
        Args:
            manual_data: Dados manuais ou None para usar API
            
        Returns:
            True se enviou com sucesso
        """
        try:
            if manual_data:
                # Usa dados fornecidos manualmente
                temp = manual_data.get('temperatura', 25.0)
                humid = manual_data.get('umidade', 60)
                pressure = manual_data.get('pressao', 1013)
                rain = 1 if manual_data.get('vai_chover', False) else 0
            else:
                # Obtém dados da API
                current = self.weather_api.get_current_weather()
                forecast = self.weather_api.get_rain_forecast(6)
                
                if not current or not forecast:
                    print("❌ Não foi possível obter dados meteorológicos")
                    return False
                
                temp = current['temperatura']
                humid = current['umidade']
                pressure = current['pressao']
                rain = 1 if forecast['vai_chover'] else 0
            
            # Formato: SET_WEATHER:temperatura,umidade,pressão,chuva
            command = f"SET_WEATHER:{temp:.1f},{humid},{pressure:.0f},{rain}"
            response = self.send_command(command)
            
            return "OK" in response.upper()
            
        except Exception as e:
            print(f"❌ Erro ao enviar dados meteorológicos: {e}")
            return False
    
    def send_rain_alert(self, rain_predicted: bool) -> bool:
        """
        Envia alerta de chuva para ESP32
        
        Args:
            rain_predicted: True se há previsão de chuva
            
        Returns:
            True se enviou com sucesso
        """
        command = f"RAIN_ALERT:{1 if rain_predicted else 0}"
        response = self.send_command(command)
        return "OK" in response.upper()
    
    def request_irrigation_status(self) -> dict:
        """
        Solicita status atual da irrigação do ESP32
        
        Returns:
            Dict com status da irrigação
        """
        response = self.send_command("GET_STATUS")
        
        try:
            # Espera resposta no formato: STATUS:relay,humidity,temperature,npk_ok
            if response.startswith("STATUS:"):
                parts = response.split(":")[1].split(",")
                
                return {
                    'irrigacao_ligada': parts[0] == "1",
                    'umidade_solo': float(parts[1]),
                    'temperatura': float(parts[2]),
                    'npk_adequado': parts[3] == "1",
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"❌ Erro ao processar status: {e}")
        
        return {}
    
    def interactive_mode(self):
        """
        Modo interativo para comunicação com ESP32
        """
        if not self.serial_port or not self.serial_port.is_open:
            print("❌ Conecte à porta serial primeiro!")
            return
        
        print("\n" + "="*60)
        print("🤖 MODO INTERATIVO - COMUNICAÇÃO COM ESP32")
        print("="*60)
        print("Comandos disponíveis:")
        print("  weather    - Envia dados meteorológicos via API")
        print("  manual     - Envia dados meteorológicos manuais")
        print("  rain       - Envia alerta de chuva")
        print("  status     - Solicita status do ESP32")
        print("  ping       - Testa conexão")
        print("  listen     - Escuta mensagens do ESP32")
        print("  quit       - Sair")
        print("="*60)
        
        try:
            while True:
                command = input("\n💻 Comando: ").strip().lower()
                
                if command == "quit" or command == "q":
                    break
                elif command == "weather":
                    print("🌤️ Enviando dados meteorológicos via API...")
                    success = self.send_weather_data()
                    print("✅ Enviado!" if success else "❌ Falhou!")
                
                elif command == "manual":
                    print("📝 Inserindo dados meteorológicos manuais:")
                    try:
                        temp = float(input("   Temperatura (°C): "))
                        humid = int(input("   Umidade (%): "))
                        pressure = float(input("   Pressão (hPa): "))
                        rain = input("   Previsão de chuva (s/n): ").lower().startswith('s')
                        
                        manual_data = {
                            'temperatura': temp,
                            'umidade': humid,
                            'pressao': pressure,
                            'vai_chover': rain
                        }
                        
                        success = self.send_weather_data(manual_data)
                        print("✅ Enviado!" if success else "❌ Falhou!")
                        
                    except ValueError:
                        print("❌ Valores inválidos!")
                
                elif command == "rain":
                    rain_alert = input("   Alerta de chuva (s/n): ").lower().startswith('s')
                    success = self.send_rain_alert(rain_alert)
                    print("✅ Enviado!" if success else "❌ Falhou!")
                
                elif command == "status":
                    print("📊 Solicitando status...")
                    status = self.request_irrigation_status()
                    if status:
                        print("📋 Status atual:")
                        print(f"   🚰 Irrigação: {'LIGADA' if status['irrigacao_ligada'] else 'DESLIGADA'}")
                        print(f"   💧 Umidade solo: {status['umidade_solo']:.1f}%")
                        print(f"   🌡️ Temperatura: {status['temperatura']:.1f}°C")
                        print(f"   🧪 NPK adequado: {'SIM' if status['npk_adequado'] else 'NÃO'}")
                    else:
                        print("❌ Não foi possível obter status")
                
                elif command == "ping":
                    response = self.send_command("PING")
                    print("🏓 Pong!" if "PONG" in response.upper() else "❌ Sem resposta")
                
                elif command == "listen":
                    print("👂 Escutando ESP32... (Ctrl+C para parar)")
                    try:
                        while True:
                            if self.serial_port.in_waiting > 0:
                                message = self.serial_port.readline().decode().strip()
                                if message:
                                    print(f"📨 ESP32: {message}")
                            time.sleep(0.1)
                    except KeyboardInterrupt:
                        print("\n🛑 Parando escuta...")
                
                else:
                    print("❌ Comando não reconhecido!")
        
        except KeyboardInterrupt:
            print("\n🛑 Saindo do modo interativo...")

def main():
    """Função principal"""
    print("🚀 FarmTech Serial Communication")
    
    comm = SerialCommunicator()
    
    # Lista portas disponíveis
    ports = comm.list_available_ports()
    
    if ports:
        # Tenta conectar
        if comm.connect():
            # Inicia modo interativo
            comm.interactive_mode()
        
        # Desconecta
        comm.disconnect()
    else:
        print("❌ Nenhuma porta serial encontrada!")
        print("💡 Verifique se o ESP32 está conectado via USB")

if __name__ == "__main__":
    main()