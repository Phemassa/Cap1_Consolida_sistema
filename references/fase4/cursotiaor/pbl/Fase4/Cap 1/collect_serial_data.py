"""
FarmTech Solutions - Coletor de Dados via Serial
=================================================
Coleta dados reais do ESP32/Wokwi via porta serial
Salva em CSV/JSON para uso em Machine Learning
"""

import serial
import time
import csv
import json
from datetime import datetime
import re

class SerialDataCollector:
    """Coleta dados do ESP32 via Serial"""
    
    def __init__(self, port='COM3', baudrate=115200):
        """
        Inicializa conexão serial
        
        Args:
            port: Porta serial (COM3 no Windows, /dev/ttyUSB0 no Linux)
            baudrate: Taxa de transmissão (115200 para ESP32)
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        self.data_buffer = []
        
    def connect(self):
        """Conecta à porta serial"""
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Aguarda estabilização
            print(f"✅ Conectado à porta {self.port}")
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def parse_sensor_data(self, line):
        """
        Extrai dados de uma linha do Serial Monitor
        
        Formato esperado:
        🧪 NPK - Níveis de Nutrientes:
           🔵 Nitrogênio (N): ✅ OK
           🟡 Fósforo (P):    ❌ BAIXO
           🟢 Potássio (K):   ✅ OK
        
        🧪 pH do Solo:
           📊 LDR Value: 2048 → pH 6.5
        
        🌡️ Condições Ambientais:
           🌡️  Temperatura: 25.3 °C ✅ IDEAL
           💧 Umidade Solo: 45.2 % ⚠️ ABAIXO DO IDEAL
        
        💧 Sistema de Irrigação:
           🔌 Relé: ⚡ LIGADO (irrigando)
        """
        data = {
            'timestamp': datetime.now().isoformat(),
            'temperatura': None,
            'umidade_solo': None,
            'ph_solo': None,
            'nitrogenio': None,
            'fosforo': None,
            'potassio': None,
            'irrigacao_ativa': None
        }
        
        # Parse Nitrogênio
        if 'Nitrogênio' in line:
            data['nitrogenio'] = 1 if '✅ OK' in line else 0
        
        # Parse Fósforo
        if 'Fósforo' in line:
            data['fosforo'] = 1 if '✅ OK' in line else 0
        
        # Parse Potássio
        if 'Potássio' in line:
            data['potassio'] = 1 if '✅ OK' in line else 0
        
        # Parse pH
        ph_match = re.search(r'pH (\d+\.?\d*)', line)
        if ph_match:
            data['ph_solo'] = float(ph_match.group(1))
        
        # Parse Temperatura
        temp_match = re.search(r'Temperatura: (\d+\.?\d*)', line)
        if temp_match:
            data['temperatura'] = float(temp_match.group(1))
        
        # Parse Umidade
        umid_match = re.search(r'Umidade Solo: (\d+\.?\d*)', line)
        if umid_match:
            data['umidade_solo'] = float(umid_match.group(1))
        
        # Parse Irrigação
        if 'LIGADO' in line and 'irrigando' in line:
            data['irrigacao_ativa'] = 1
        elif 'DESLIGADO' in line and 'Relé' in line:
            data['irrigacao_ativa'] = 0
        
        return data
    
    def collect_data(self, duration_minutes=10, output_file='sensor_data_real.csv'):
        """
        Coleta dados durante um período especificado
        
        Args:
            duration_minutes: Duração da coleta (minutos)
            output_file: Nome do arquivo de saída
        """
        if not self.connect():
            return
        
        print(f"📊 Coletando dados por {duration_minutes} minutos...")
        print(f"💾 Salvando em: {output_file}\n")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        current_reading = {}
        
        try:
            with open(output_file, 'w', newline='') as csvfile:
                fieldnames = ['timestamp', 'temperatura', 'umidade_solo', 'ph_solo',
                            'nitrogenio', 'fosforo', 'potassio', 'irrigacao_ativa']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                while time.time() < end_time:
                    if self.serial_conn.in_waiting > 0:
                        line = self.serial_conn.readline().decode('utf-8', errors='ignore').strip()
                        
                        if line:
                            # Parse linha
                            parsed = self.parse_sensor_data(line)
                            
                            # Atualiza reading atual
                            for key, value in parsed.items():
                                if value is not None:
                                    current_reading[key] = value
                            
                            # Se temos todos os dados, salva
                            if all(current_reading.get(k) is not None for k in fieldnames):
                                writer.writerow(current_reading)
                                csvfile.flush()
                                
                                # Mostra progresso
                                elapsed = (time.time() - start_time) / 60
                                print(f"⏱️  {elapsed:.1f}min | "
                                      f"Temp: {current_reading['temperatura']}°C | "
                                      f"Umid: {current_reading['umidade_solo']}% | "
                                      f"pH: {current_reading['ph_solo']}")
                                
                                current_reading = {}
                    
                    time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\n⚠️  Coleta interrompida pelo usuário")
        except Exception as e:
            print(f"\n❌ Erro durante coleta: {e}")
        finally:
            self.disconnect()
            print(f"\n✅ Coleta finalizada!")
            print(f"📁 Dados salvos em: {output_file}")
    
    def disconnect(self):
        """Desconecta da porta serial"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("🔌 Desconectado")


def listar_portas_disponiveis():
    """Lista todas as portas seriais disponíveis"""
    import serial.tools.list_ports
    
    ports = serial.tools.list_ports.comports()
    print("\n📡 Portas Seriais Disponíveis:")
    for port in ports:
        print(f"   - {port.device}: {port.description}")
    
    return [port.device for port in ports]


if __name__ == "__main__":
    print("🌾 FarmTech Solutions - Coletor de Dados Serial\n")
    
    # Lista portas disponíveis
    portas = listar_portas_disponiveis()
    
    if not portas:
        print("\n❌ Nenhuma porta serial encontrada!")
        print("💡 Certifique-se de que o ESP32 está conectado\n")
        exit(1)
    
    # Seleciona porta (ajuste conforme necessário)
    porta_selecionada = portas[0] if portas else 'COM3'
    
    print(f"\n🔌 Usando porta: {porta_selecionada}")
    print("   (Edite o código para mudar a porta se necessário)\n")
    
    # Coleta dados
    collector = SerialDataCollector(port=porta_selecionada, baudrate=115200)
    
    # Coleta por 10 minutos (ajuste conforme necessário)
    collector.collect_data(
        duration_minutes=10,
        output_file='sensor_data_real.csv'
    )
    
    print("\n✅ Processo concluído!")
    print("💡 Use o arquivo CSV gerado para treinar modelos de ML")