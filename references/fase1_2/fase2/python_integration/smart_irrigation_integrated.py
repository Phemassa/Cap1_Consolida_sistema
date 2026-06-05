"""
Exemplo Avançado: Integração ESP32 + Python + API Meteorológica
FarmTech Solutions - Atividade Opcional 1

Este script demonstra a integração completa entre:
- ESP32 (sensores de campo)
- Python (processamento)
- API OpenWeatherMap (dados meteorológicos)

Fluxo de dados:
1. Python lê dados do ESP32
2. Python consulta API de clima
3. Python decide se deve irrigar
4. Python envia comando para ESP32
"""

import sys
import os
import time
import json
from datetime import datetime

# Adiciona path para importar módulos do projeto
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'api_clima'))
sys.path.append(os.path.dirname(__file__))

try:
    from weather_integration import WeatherAPI
except ImportError:
    print("⚠️  Módulo weather_integration não encontrado")
    WeatherAPI = None

try:
    from esp32_communication import ESP32Communication
except ImportError:
    print("❌ Erro: esp32_communication.py não encontrado")
    sys.exit(1)


class SmartIrrigationSystem:
    """Sistema de Irrigação Inteligente Integrado"""
    
    def __init__(self, esp_port: str = 'COM3'):
        """
        Inicializa sistema integrado
        
        Args:
            esp_port: Porta serial do ESP32
        """
        self.esp = ESP32Communication(port=esp_port)
        self.weather_api = WeatherAPI() if WeatherAPI else None
        self.last_decision = None
        
    def start(self) -> bool:
        """
        Inicia sistema
        
        Returns:
            True se iniciado com sucesso
        """
        print("="*60)
        print("🌾 Sistema de Irrigação Inteligente Integrado")
        print("   FarmTech Solutions - Atividade Opcional 1")
        print("="*60)
        
        # Conecta ao ESP32
        if not self.esp.connect():
            return False
        
        # Verifica API de clima
        if self.weather_api:
            print("✅ API meteorológica disponível")
        else:
            print("⚠️  API meteorológica não disponível (modo simulado)")
        
        return True
    
    def get_field_conditions(self) -> dict:
        """
        Obtém condições atuais do campo via ESP32
        
        Returns:
            Dicionário com dados dos sensores
        """
        data = self.esp.get_sensor_data()
        if not data:
            print("❌ Erro ao obter dados do ESP32")
            return None
        
        return {
            'npk': data.get('npk', {}),
            'ph': data.get('ph', {}).get('ph_level', 0),
            'temperature': data.get('environment', {}).get('temperature', 0),
            'humidity': data.get('environment', {}).get('humidity', 0),
            'pump_active': data.get('actuators', {}).get('irrigation_pump', False)
        }
    
    def get_weather_conditions(self, city: str = "São Paulo") -> dict:
        """
        Obtém condições meteorológicas
        
        Args:
            city: Nome da cidade
            
        Returns:
            Dicionário com dados climáticos
        """
        if not self.weather_api:
            return {
                'temperature': 25.0,
                'humidity': 60.0,
                'rain_expected': False,
                'description': 'Simulado',
                'source': 'mock'
            }
        
        current = self.weather_api.get_current_weather(city)
        forecast = self.weather_api.get_weather_forecast(city, days=1)
        
        # Verifica previsão de chuva
        rain_expected = any(
            day.get('rain_probability', 0) > 60 
            for day in forecast
        )
        
        return {
            'temperature': current.get('temperature', 0),
            'humidity': current.get('humidity', 0),
            'rain_expected': rain_expected,
            'description': current.get('description', ''),
            'wind_speed': current.get('wind_speed', 0),
            'source': current.get('source', 'api')
        }
    
    def make_irrigation_decision(self, field_data: dict, weather_data: dict) -> dict:
        """
        Decide se deve irrigar baseado em todos os dados
        
        Args:
            field_data: Dados dos sensores de campo
            weather_data: Dados meteorológicos
            
        Returns:
            Dicionário com decisão e justificativa
        """
        reasons = []
        should_irrigate = False
        
        # Regra 1: Se vai chover, não irrigar
        if weather_data.get('rain_expected', False):
            reasons.append("Previsão de chuva detectada")
            return {
                'should_irrigate': False,
                'reasons': reasons,
                'confidence': 90,
                'source': 'weather_api'
            }
        
        # Regra 2: Umidade externa alta
        if weather_data.get('humidity', 0) > 80:
            reasons.append(f"Alta umidade externa ({weather_data['humidity']:.1f}%)")
            return {
                'should_irrigate': False,
                'reasons': reasons,
                'confidence': 85,
                'source': 'weather_api'
            }
        
        # Regra 3: pH inadequado
        ph = field_data.get('ph', 7.0)
        if ph < 5.5 or ph > 7.5:
            should_irrigate = True
            reasons.append(f"pH inadequado ({ph:.2f})")
        
        # Regra 4: Umidade do solo baixa
        field_humidity = field_data.get('humidity', 0)
        if field_humidity < 55:
            should_irrigate = True
            reasons.append(f"Baixa umidade do solo ({field_humidity:.1f}%)")
        
        # Regra 5: NPK insuficiente
        npk = field_data.get('npk', {})
        if not npk.get('nitrogen', False):
            should_irrigate = True
            reasons.append("Falta nitrogênio")
        if not npk.get('phosphorus', False):
            should_irrigate = True
            reasons.append("Falta fósforo")
        if not npk.get('potassium', False):
            should_irrigate = True
            reasons.append("Falta potássio")
        
        # Regra 6: Temperatura muito alta
        temp = field_data.get('temperature', 0)
        if temp > 32:
            should_irrigate = True
            reasons.append(f"Temperatura muito alta ({temp:.1f}°C)")
        
        if not reasons:
            reasons.append("Condições ideais mantidas")
        
        return {
            'should_irrigate': should_irrigate,
            'reasons': reasons,
            'confidence': 80 if should_irrigate else 90,
            'source': 'integrated_analysis'
        }
    
    def execute_irrigation_control(self, decision: dict) -> bool:
        """
        Executa controle de irrigação no ESP32
        
        Args:
            decision: Decisão de irrigação
            
        Returns:
            True se executado com sucesso
        """
        should_irrigate = decision.get('should_irrigate', False)
        
        print(f"\n{'='*60}")
        print(f"🤖 Decisão Automática de Irrigação")
        print(f"{'='*60}")
        print(f"Ação: {'🟢 IRRIGAR' if should_irrigate else '🔴 NÃO IRRIGAR'}")
        print(f"Confiança: {decision.get('confidence', 0)}%")
        print(f"Fonte: {decision.get('source', 'unknown')}")
        print(f"\nJustificativa:")
        for reason in decision.get('reasons', []):
            print(f"  • {reason}")
        print(f"{'='*60}\n")
        
        # Envia comando para ESP32
        success = self.esp.set_relay(should_irrigate)
        
        if success:
            time.sleep(1)
            response = self.esp.read_line(timeout=1.0)
            if response:
                print(f"ESP32: {response}")
        
        self.last_decision = decision
        return success
    
    def run_monitoring_cycle(self, city: str = "São Paulo"):
        """
        Executa um ciclo completo de monitoramento e decisão
        
        Args:
            city: Cidade para consulta meteorológica
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n{'🔄'*30}")
        print(f"Ciclo de Monitoramento - {timestamp}")
        print(f"{'🔄'*30}\n")
        
        # 1. Coleta dados do campo
        print("📡 Coletando dados do campo...")
        field_data = self.get_field_conditions()
        if not field_data:
            print("❌ Erro ao coletar dados do campo")
            return
        
        self.esp.display_sensor_data(self.esp.get_sensor_data())
        
        # 2. Coleta dados meteorológicos
        print("\n🌤️  Consultando condições meteorológicas...")
        weather_data = self.get_weather_conditions(city)
        
        print(f"\nCondições Meteorológicas em {city}:")
        print(f"  🌡️  Temperatura: {weather_data['temperature']:.1f}°C")
        print(f"  💧 Umidade: {weather_data['humidity']:.1f}%")
        print(f"  🌧️  Chuva: {'SIM' if weather_data['rain_expected'] else 'NÃO'}")
        print(f"  📝 Descrição: {weather_data['description']}")
        print(f"  📊 Fonte: {weather_data['source']}")
        
        # 3. Toma decisão inteligente
        print("\n🧠 Processando decisão inteligente...")
        decision = self.make_irrigation_decision(field_data, weather_data)
        
        # 4. Executa ação
        self.execute_irrigation_control(decision)
    
    def run_continuous_monitoring(self, interval: int = 30, city: str = "São Paulo"):
        """
        Executa monitoramento contínuo
        
        Args:
            interval: Intervalo entre ciclos em segundos
            city: Cidade para consulta meteorológica
        """
        print(f"\n🔄 Monitoramento contínuo iniciado")
        print(f"   Intervalo: {interval} segundos")
        print(f"   Cidade: {city}")
        print(f"   Pressione Ctrl+C para parar\n")
        
        try:
            while True:
                self.run_monitoring_cycle(city)
                print(f"\n⏰ Aguardando {interval} segundos até próximo ciclo...\n")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n⏸️  Monitoramento interrompido pelo usuário")
    
    def stop(self):
        """Para sistema e desconecta"""
        self.esp.disconnect()
        print("\n👋 Sistema encerrado")


def main():
    """Função principal"""
    print("\n")
    print("="*60)
    print("🌾 Sistema de Irrigação Inteligente - Integração Completa")
    print("   FarmTech Solutions - Atividade Opcional 1")
    print("="*60)
    print("\nEste script demonstra:")
    print("  ✅ Comunicação Python ↔ ESP32 (Serial)")
    print("  ✅ Integração com API meteorológica")
    print("  ✅ Decisão inteligente de irrigação")
    print("  ✅ Controle automático via comandos")
    print("="*60)
    
    # Configuração
    port = input("\nPorta serial do ESP32 [COM3]: ").strip() or "COM3"
    city = input("Cidade para consulta meteorológica [São Paulo]: ").strip() or "São Paulo"
    
    # Cria sistema
    system = SmartIrrigationSystem(esp_port=port)
    
    # Inicia sistema
    if not system.start():
        print("\n❌ Falha ao iniciar sistema")
        return
    
    try:
        # Menu de opções
        while True:
            print("\n" + "="*60)
            print("Menu de Operação:")
            print("="*60)
            print("1. Executar ciclo único de monitoramento")
            print("2. Monitoramento contínuo automático")
            print("3. Ver status atual dos sensores")
            print("4. Ligar bomba manualmente")
            print("5. Desligar bomba manualmente")
            print("6. Sair")
            print("="*60)
            
            choice = input("Escolha uma opção: ").strip()
            
            if choice == '1':
                system.run_monitoring_cycle(city)
            
            elif choice == '2':
                interval = input("Intervalo entre ciclos (segundos) [30]: ").strip()
                interval = int(interval) if interval else 30
                system.run_continuous_monitoring(interval, city)
            
            elif choice == '3':
                data = system.esp.get_sensor_data()
                if data:
                    system.esp.display_sensor_data(data)
            
            elif choice == '4':
                system.esp.set_relay(True)
                print("✅ Bomba ligada manualmente")
            
            elif choice == '5':
                system.esp.set_relay(False)
                print("✅ Bomba desligada manualmente")
            
            elif choice == '6':
                break
            
            else:
                print("❌ Opção inválida")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário")
    
    finally:
        system.stop()


if __name__ == "__main__":
    main()
