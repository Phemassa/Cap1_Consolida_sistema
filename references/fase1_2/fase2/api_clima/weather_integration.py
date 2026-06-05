"""
Integração com API de Clima - OpenWeatherMap
Atividade Opcional 1 do Projeto Fase 2

Este módulo integra dados meteorológicos para otimizar a irrigação:
- Previsão de chuva
- Temperatura externa
- Umidade externa
- Velocidade do vento
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import os

class WeatherAPI:
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o cliente da API de clima
        
        Args:
            api_key: Chave da API OpenWeatherMap
        """
        self.api_key = api_key or "demo_key"  # Em produção, usar variável de ambiente
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
    def get_current_weather(self, city: str = "São Paulo") -> Dict:
        """
        Obtém dados meteorológicos atuais
        
        Args:
            city: Nome da cidade
            
        Returns:
            Dict com dados meteorológicos
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'pt_br'
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_current_weather(data)
            else:
                # Retorna dados simulados se API não disponível
                return self._get_mock_weather()
                
        except Exception as e:
            print(f"Erro ao obter dados meteorológicos: {e}")
            return self._get_mock_weather()
    
    def get_weather_forecast(self, city: str = "São Paulo", days: int = 5) -> List[Dict]:
        """
        Obtém previsão meteorológica
        
        Args:
            city: Nome da cidade
            days: Número de dias da previsão
            
        Returns:
            Lista com previsão dos próximos dias
        """
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'pt_br'
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_forecast(data, days)
            else:
                # Retorna dados simulados se API não disponível
                return self._get_mock_forecast(days)
                
        except Exception as e:
            print(f"Erro ao obter previsão: {e}")
            return self._get_mock_forecast(days)
    
    def should_skip_irrigation(self, city: str = "São Paulo") -> Dict:
        """
        Determina se deve pular irrigação baseado na previsão
        
        Args:
            city: Nome da cidade
            
        Returns:
            Dict com recomendação e justificativa
        """
        forecast = self.get_weather_forecast(city, days=1)
        current = self.get_current_weather(city)
        
        # Critérios para pular irrigação
        rain_expected = any(day.get('rain_probability', 0) > 60 for day in forecast)
        high_humidity = current.get('humidity', 0) > 80
        recent_rain = current.get('rain_1h', 0) > 5  # mm na última hora
        
        skip_irrigation = rain_expected or high_humidity or recent_rain
        
        reasons = []
        if rain_expected:
            reasons.append("Previsão de chuva nas próximas 24h")
        if high_humidity:
            reasons.append(f"Alta umidade externa ({current.get('humidity')}%)")
        if recent_rain:
            reasons.append(f"Chuva recente ({current.get('rain_1h')}mm)")
        
        return {
            'skip_irrigation': skip_irrigation,
            'reasons': reasons,
            'weather_data': {
                'current': current,
                'forecast': forecast
            }
        }
    
    def _format_current_weather(self, data: Dict) -> Dict:
        """Formata dados meteorológicos atuais"""
        return {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'description': data['weather'][0]['description'],
            'wind_speed': data.get('wind', {}).get('speed', 0),
            'rain_1h': data.get('rain', {}).get('1h', 0),
            'clouds': data.get('clouds', {}).get('all', 0),
            'timestamp': datetime.now().isoformat()
        }
    
    def _format_forecast(self, data: Dict, days: int) -> List[Dict]:
        """Formata dados de previsão"""
        forecast_list = []
        
        for item in data['list'][:days * 8]:  # 8 previsões por dia (3h cada)
            forecast_item = {
                'datetime': item['dt_txt'],
                'temperature': item['main']['temp'],
                'humidity': item['main']['humidity'],
                'description': item['weather'][0]['description'],
                'rain_probability': item.get('pop', 0) * 100,  # Probability of precipitation
                'rain_volume': item.get('rain', {}).get('3h', 0),
                'wind_speed': item.get('wind', {}).get('speed', 0)
            }
            forecast_list.append(forecast_item)
        
        return forecast_list
    
    def _get_mock_weather(self) -> Dict:
        """Dados simulados para demonstração"""
        import random
        
        return {
            'temperature': round(random.uniform(18, 32), 1),
            'humidity': random.randint(40, 90),
            'pressure': random.randint(1010, 1025),
            'description': random.choice(['Ensolarado', 'Parcialmente nublado', 'Nublado', 'Chuva leve']),
            'wind_speed': round(random.uniform(0, 15), 1),
            'rain_1h': round(random.uniform(0, 5), 1),
            'clouds': random.randint(0, 100),
            'timestamp': datetime.now().isoformat(),
            'source': 'simulado'
        }
    
    def _get_mock_forecast(self, days: int) -> List[Dict]:
        """Previsão simulada para demonstração"""
        import random
        
        forecast = []
        for i in range(days):
            future_date = datetime.now() + timedelta(days=i)
            
            forecast_item = {
                'datetime': future_date.strftime('%Y-%m-%d 12:00:00'),
                'temperature': round(random.uniform(16, 30), 1),
                'humidity': random.randint(35, 85),
                'description': random.choice(['Sol', 'Nublado', 'Chuva', 'Trovoada']),
                'rain_probability': random.randint(0, 100),
                'rain_volume': round(random.uniform(0, 10), 1),
                'wind_speed': round(random.uniform(0, 12), 1),
                'source': 'simulado'
            }
            forecast.append(forecast_item)
        
        return forecast

def get_weather_recommendation(city: str = "São Paulo") -> Dict:
    """
    Função principal para obter recomendação meteorológica
    
    Args:
        city: Nome da cidade
        
    Returns:
        Dict com recomendação completa
    """
    weather_api = WeatherAPI()
    return weather_api.should_skip_irrigation(city)

if __name__ == "__main__":
    # Teste do módulo
    weather_api = WeatherAPI()
    
    print("=== Dados Meteorológicos Atuais ===")
    current = weather_api.get_current_weather()
    print(json.dumps(current, indent=2, ensure_ascii=False))
    
    print("\n=== Previsão do Tempo ===")
    forecast = weather_api.get_weather_forecast(days=3)
    for day in forecast:
        print(f"Data: {day['datetime']} | Temp: {day['temperature']}°C | "
              f"Chuva: {day['rain_probability']}% | {day['description']}")
    
    print("\n=== Recomendação de Irrigação ===")
    recommendation = weather_api.should_skip_irrigation()
    print(f"Pular irrigação: {'SIM' if recommendation['skip_irrigation'] else 'NÃO'}")
    if recommendation['reasons']:
        print("Motivos:", ", ".join(recommendation['reasons']))