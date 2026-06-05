"""
═══════════════════════════════════════════════════════════════════════════
FarmTech Solutions - Integração Meteorológica (IR ALÉM 1)
═══════════════════════════════════════════════════════════════════════════

OBJETIVO: Integrar dados meteorológicos de APIs públicas para otimizar irrigação

FUNCIONALIDADES:
- Consulta API OpenWeatherMap para previsão de chuva
- Suspende irrigação automaticamente se há previsão de chuva
- Economia de recursos hídricos
- Comunicação via Serial com ESP32
- Modo manual para inserção de dados via Serial Monitor

AUTORES: Grupo 59 FIAP
DATA: Outubro 2025
═══════════════════════════════════════════════════════════════════════════
"""

import requests
import json
import serial
import time
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class WeatherAPI:
    """Classe para integração com OpenWeatherMap API"""
    
    def __init__(self, api_key: str = None, city: str = "São Paulo", country: str = "BR"):
        """
        Inicializa a classe WeatherAPI
        
        Args:
            api_key: Chave da API OpenWeatherMap (obter em openweathermap.org)
            city: Cidade para consulta meteorológica
            country: Código do país (BR para Brasil)
        """
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')
        self.city = city
        self.country = country
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.serial_port = None
        
        # Cache para evitar muitas consultas à API
        self.last_weather_data = None
        self.last_update = None
        self.cache_duration = 600  # 10 minutos
        
        print(f"🌤️ WeatherAPI inicializada para {city}, {country}")
        if not self.api_key:
            print("⚠️ API Key não encontrada! Configure OPENWEATHER_API_KEY ou use modo manual")
    
    def get_current_weather(self) -> Optional[Dict]:
        """
        Obtém dados meteorológicos atuais
        
        Returns:
            Dict com dados do clima ou None se erro
        """
        if not self.api_key:
            print("❌ API Key não configurada!")
            return None
        
        # Verifica cache
        if self._is_cache_valid():
            print("📋 Usando dados do cache...")
            return self.last_weather_data
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': f"{self.city},{self.country}",
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'pt_br'
            }
            
            print(f"🌐 Consultando API para {self.city}...")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Processa dados
            weather_data = {
                'temperatura': data['main']['temp'],
                'umidade': data['main']['humidity'],
                'pressao': data['main']['pressure'],
                'descricao': data['weather'][0]['description'],
                'vento_velocidade': data['wind']['speed'],
                'nuvens': data['clouds']['all'],
                'cidade': data['name'],
                'timestamp': datetime.now().isoformat()
            }
            
            # Atualiza cache
            self.last_weather_data = weather_data
            self.last_update = datetime.now()
            
            print("✅ Dados meteorológicos obtidos com sucesso!")
            return weather_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na consulta à API: {e}")
            return None
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return None
    
    def get_rain_forecast(self, hours: int = 12) -> Optional[Dict]:
        """
        Obtém previsão de chuva para próximas horas
        
        Args:
            hours: Número de horas para previsão (máximo 48h)
            
        Returns:
            Dict com previsão de chuva
        """
        if not self.api_key:
            print("❌ API Key não configurada!")
            return None
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': f"{self.city},{self.country}",
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'pt_br'
            }
            
            print(f"🌧️ Consultando previsão de chuva para {hours}h...")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Analisa próximas horas
            rain_forecast = {
                'vai_chover': False,
                'probabilidade_maxima': 0,
                'quantidade_chuva_mm': 0,
                'horas_ate_chuva': None,
                'previsoes': []
            }
            
            now = datetime.now()
            target_time = now + timedelta(hours=hours)
            
            for item in data['list']:
                forecast_time = datetime.fromtimestamp(item['dt'])
                
                if forecast_time <= target_time:
                    # Verifica se há chuva prevista
                    weather_main = item['weather'][0]['main'].lower()
                    has_rain = 'rain' in weather_main or 'drizzle' in weather_main
                    
                    # Quantidade de chuva (se disponível)
                    rain_mm = 0
                    if 'rain' in item and '3h' in item['rain']:
                        rain_mm = item['rain']['3h']
                    
                    # Probabilidade (aproximada baseada em umidade e nuvens)
                    probability = min(item['clouds']['all'] + item['main']['humidity']) / 2
                    
                    if has_rain or rain_mm > 0:
                        rain_forecast['vai_chover'] = True
                        rain_forecast['quantidade_chuva_mm'] += rain_mm
                        
                        if not rain_forecast['horas_ate_chuva']:
                            rain_forecast['horas_ate_chuva'] = (forecast_time - now).total_seconds() / 3600
                    
                    if probability > rain_forecast['probabilidade_maxima']:
                        rain_forecast['probabilidade_maxima'] = probability
                    
                    rain_forecast['previsoes'].append({
                        'horario': forecast_time.strftime('%H:%M'),
                        'temperatura': item['main']['temp'],
                        'umidade': item['main']['humidity'],
                        'descricao': item['weather'][0]['description'],
                        'chuva_mm': rain_mm,
                        'probabilidade': probability
                    })
            
            print(f"✅ Previsão obtida: {'Chuva prevista' if rain_forecast['vai_chover'] else 'Sem chuva'}")
            return rain_forecast
            
        except Exception as e:
            print(f"❌ Erro ao obter previsão: {e}")
            return None
    
    def should_skip_irrigation(self, threshold_mm: float = 2.0, threshold_hours: int = 6) -> Dict:
        """
        Decide se deve suspender a irrigação baseado na previsão
        
        Args:
            threshold_mm: Quantidade mínima de chuva (mm) para suspender
            threshold_hours: Horas para considerar na previsão
            
        Returns:
            Dict com decisão e justificativa
        """
        print(f"\n🤔 Analisando se deve suspender irrigação...")
        print(f"   Limites: {threshold_mm}mm em {threshold_hours}h")
        
        # Obtém previsão
        forecast = self.get_rain_forecast(threshold_hours)
        
        decision = {
            'suspender_irrigacao': False,
            'motivo': 'Sem previsão de chuva significativa',
            'previsao': forecast
        }
        
        if forecast and forecast['vai_chover']:
            rain_amount = forecast['quantidade_chuva_mm']
            hours_to_rain = forecast['horas_ate_chuva']
            
            if rain_amount >= threshold_mm:
                decision['suspender_irrigacao'] = True
                decision['motivo'] = f"Chuva prevista: {rain_amount:.1f}mm em {hours_to_rain:.1f}h"
            elif forecast['probabilidade_maxima'] > 80:
                decision['suspender_irrigacao'] = True
                decision['motivo'] = f"Alta probabilidade de chuva: {forecast['probabilidade_maxima']:.0f}%"
        
        print(f"   Decisão: {'🚫 Suspender' if decision['suspender_irrigacao'] else '✅ Continuar'}")
        print(f"   Motivo: {decision['motivo']}")
        
        return decision
    
    def _is_cache_valid(self) -> bool:
        """Verifica se o cache ainda é válido"""
        if not self.last_update or not self.last_weather_data:
            return False
        
        time_diff = (datetime.now() - self.last_update).total_seconds()
        return time_diff < self.cache_duration
    
    def connect_serial(self, port: str, baudrate: int = 115200) -> bool:
        """
        Conecta à porta serial do ESP32
        
        Args:
            port: Porta serial (ex: 'COM3' no Windows, '/dev/ttyUSB0' no Linux)
            baudrate: Taxa de transmissão
            
        Returns:
            True se conectou com sucesso
        """
        try:
            self.serial_port = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Aguarda estabilização
            print(f"✅ Conectado à porta serial {port}")
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar serial: {e}")
            return False
    
    def send_weather_data(self, data: Dict) -> bool:
        """
        Envia dados meteorológicos via serial para ESP32
        
        Args:
            data: Dados meteorológicos para enviar
            
        Returns:
            True se enviou com sucesso
        """
        if not self.serial_port:
            print("❌ Porta serial não conectada!")
            return False
        
        try:
            # Formato: WEATHER:temp,humid,pressure,rain_forecast
            current = self.get_current_weather()
            forecast = self.get_rain_forecast(6)
            
            if current and forecast:
                message = f"WEATHER:{current['temperatura']:.1f},{current['umidade']},{current['pressao']:.0f},{int(forecast['vai_chover'])}\n"
                
                self.serial_port.write(message.encode())
                self.serial_port.flush()
                
                print(f"📤 Enviado: {message.strip()}")
                return True
            else:
                print("❌ Dados meteorológicos não disponíveis")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar dados: {e}")
            return False
    
    def listen_for_requests(self):
        """
        Escuta requisições do ESP32 e responde com dados meteorológicos
        """
        if not self.serial_port:
            print("❌ Porta serial não conectada!")
            return
        
        print("👂 Aguardando requisições do ESP32...")
        print("   Envie 'GET_WEATHER' do ESP32 para receber dados")
        print("   Pressione Ctrl+C para parar\n")
        
        try:
            while True:
                if self.serial_port.in_waiting > 0:
                    message = self.serial_port.readline().decode().strip()
                    
                    if message == "GET_WEATHER":
                        print("📥 Requisição recebida do ESP32")
                        self.send_weather_data({})
                    elif message:
                        print(f"📨 ESP32: {message}")
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n🛑 Parando escuta...")
        except Exception as e:
            print(f"❌ Erro na comunicação: {e}")
    
    def print_weather_report(self):
        """Exibe relatório meteorológico completo"""
        print("\n" + "="*70)
        print("🌤️ RELATÓRIO METEOROLÓGICO - FARMTECH SOLUTIONS")
        print("="*70)
        
        # Dados atuais
        current = self.get_current_weather()
        if current:
            print(f"\n📍 Localização: {current['cidade']}")
            print(f"🌡️ Temperatura: {current['temperatura']:.1f}°C")
            print(f"💧 Umidade: {current['umidade']}%")
            print(f"🔽 Pressão: {current['pressao']:.0f} hPa")
            print(f"☁️ Condições: {current['descricao']}")
            print(f"💨 Vento: {current['vento_velocidade']:.1f} m/s")
            print(f"☁️ Nuvens: {current['nuvens']}%")
        
        # Previsão de chuva
        forecast = self.get_rain_forecast(12)
        if forecast:
            print(f"\n🌧️ PREVISÃO DE CHUVA (próximas 12h):")
            print(f"   Status: {'Chuva prevista ☔' if forecast['vai_chover'] else 'Sem chuva ☀️'}")
            
            if forecast['vai_chover']:
                print(f"   Quantidade: {forecast['quantidade_chuva_mm']:.1f} mm")
                if forecast['horas_ate_chuva']:
                    print(f"   Início: {forecast['horas_ate_chuva']:.1f} horas")
            
            print(f"   Probabilidade máxima: {forecast['probabilidade_maxima']:.0f}%")
        
        # Decisão de irrigação
        decision = self.should_skip_irrigation()
        print(f"\n💧 DECISÃO DE IRRIGAÇÃO:")
        print(f"   Ação: {'🚫 SUSPENDER' if decision['suspender_irrigacao'] else '✅ CONTINUAR'}")
        print(f"   Motivo: {decision['motivo']}")
        
        print("="*70)
        print(f"🕐 Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*70)

def main():
    """Função principal para teste e demonstração"""
    print("🚀 Iniciando FarmTech Weather Integration...")
    
    # Configuração
    weather = WeatherAPI(
        city="São Paulo",
        country="BR"
    )
    
    # Exibe relatório meteorológico
    weather.print_weather_report()
    
    # Opção de comunicação serial (descomente para usar)
    # weather.connect_serial('COM3')  # Ajustar porta conforme necessário
    # weather.listen_for_requests()

if __name__ == "__main__":
    main()