"""
Sistema de Irrigação Inteligente - FarmTech Solutions
Fase 2 do Projeto: Coleta de Dados com Sensores

Este sistema simula um dispositivo ESP32 com sensores para monitoramento
e controle automático de irrigação baseado em:
- Elementos NPK (Nitrogênio, Fósforo, Potássio)
- pH do solo
- Umidade do solo
- Dados meteorológicos
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import random
import json
import datetime
import time
import logging
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
import os
import sys

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adiciona diretório pai para importar a API de clima
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from api_clima.weather_integration import WeatherAPI, get_weather_recommendation
except ImportError:
    # Fallback se API de clima não disponível
    WeatherAPI = None
    get_weather_recommendation = None

# Importa gerenciador de áreas de plantio
from planting_areas import PlantingAreaManager

# Importa ponte serial ESP32
try:
    from esp32_serial_bridge import get_bridge, connect_to_esp32
    ESP32_AVAILABLE = True
except ImportError:
    ESP32_AVAILABLE = False
    print("⚠️  Módulo ESP32 Serial Bridge não disponível - rodando em modo simulação")

app = Flask(__name__)

# Inicializa gerenciador de áreas de plantio (CSVs da Fase 1)
CSV_BASE_PATH = os.path.join(os.path.dirname(__file__), '../../python_app')
area_manager = PlantingAreaManager(CSV_BASE_PATH)

# Configurações das plataformas de desenvolvimento
DEVELOPMENT_PLATFORMS = {
    "arduino": {
        "name": "Arduino IDE",
        "description": "Desenvolvimento tradicional com Arduino IDE",
        "code_path": "../arduino_code/farm_irrigation_system.ino",
        "diagram_path": "../arduino_code/wokwi_diagram.json",
        "instructions_path": "../arduino_code/INSTRUCOES_WOKWI.md",
        "setup_instructions": [
            "1. Abra Arduino IDE",
            "2. Instale biblioteca DHT22",
            "3. Instale biblioteca ArduinoJson",
            "4. Copie o código .ino",
            "5. Configure ESP32 no IDE"
        ]
    },
    "platformio": {
        "name": "PlatformIO",
        "description": "Desenvolvimento profissional com PlatformIO",
        "code_path": "../../assets/platformio.ini",
        "diagram_path": "../../assets/wokwi.toml",
        "instructions_path": None,
        "setup_instructions": [
            "1. Instale PlatformIO: pip install platformio",
            "2. Navegue para pasta do projeto",
            "3. Execute: pio run",
            "4. Para upload: pio run --target upload",
            "5. Para Wokwi: pio run --target sim"
        ]
    }
}

@dataclass
class SensorData:
    """Classe para armazenar dados dos sensores"""
    timestamp: str
    nitrogen: bool
    phosphorus: bool
    potassium: bool
    ph_level: float
    soil_humidity: float
    air_temperature: float
    air_humidity: float
    irrigation_active: bool
    
@dataclass
class CultureSettings:
    """Configurações ideais para cada cultura"""
    name: str
    ph_min: float
    ph_max: float
    humidity_min: float
    humidity_max: float
    nitrogen_required: bool
    phosphorus_required: bool
    potassium_required: bool

# Configurações de culturas agrícolas baseadas em pesquisa
# ATUALIZADO: Apenas Banana e Milho conforme CSVs da Fase 1
CULTURES = {
    "banana": CultureSettings("Banana", 5.5, 7.0, 60, 80, True, True, True),
    "milho": CultureSettings("Milho", 5.8, 6.8, 50, 70, True, True, True)
}

# Armazenamento em memória dos dados (em produção usaria banco de dados)
sensor_history: List[SensorData] = []
current_culture = "banana"  # Começa com Banana
selected_area_id = None  # ID da área selecionada do CSV
system_settings = {
    "auto_irrigation": True,
    "irrigation_duration": 30,  # minutos
    "check_interval": 5  # minutos
}

# Instância da API meteorológica (Atividade Opcional 1)
weather_api = None

# Ponte serial ESP32
esp32_bridge = None
esp32_connected = False

def get_weather_api():
    """Obtém instância da API meteorológica com lazy loading"""
    global weather_api
    if weather_api is None and WeatherAPI is not None:
        weather_api = WeatherAPI()
    return weather_api

def init_esp32_connection():
    """Inicializa conexão com ESP32 (chamado ao iniciar Flask)"""
    global esp32_bridge, esp32_connected
    if ESP32_AVAILABLE and esp32_bridge is None:
        try:
            esp32_bridge = get_bridge()
            esp32_connected = esp32_bridge.connect()
            if esp32_connected:
                print("✅ ESP32 conectado via serial!")
                # Define callback para receber dados
                esp32_bridge.set_data_callback(lambda data: print(f"📡 Dados ESP32: {data}"))
            else:
                print("⚠️  ESP32 não conectado - rodando em modo simulação")
        except Exception as e:
            print(f"❌ Erro ao conectar ESP32: {e}")
            esp32_connected = False
    return esp32_connected

def get_esp32_sensor_data() -> Optional[Dict]:
    """
    Obtém dados reais do ESP32 via serial
    
    Returns:
        Dict com dados dos sensores ou None se não disponível
    """
    global esp32_bridge, esp32_connected
    
    if not esp32_connected or not esp32_bridge:
        return None
    
    try:
        # Solicita dados atuais do ESP32
        if esp32_bridge.send_command("GET_SENSORS"):
            time.sleep(0.2)  # Aguarda resposta
            data = esp32_bridge.get_last_data()
            
            if data and 'sensors' in data:
                sensors = data['sensors']
                return {
                    'nitrogen': sensors.get('N', False),
                    'phosphorus': sensors.get('P', False),
                    'potassium': sensors.get('K', False),
                    'ph_level': sensors.get('ph', 0.0),
                    'ldr_raw': sensors.get('ldr', 0),
                    'temperature': sensors.get('temp', 0.0),
                    'humidity': sensors.get('hum', 0.0),
                    'relay': sensors.get('relay', False)
                }
    except Exception as e:
        logger.error(f"❌ Erro ao ler dados ESP32: {e}")
    
    return None

def simulate_sensor_reading() -> SensorData:
    """Lê sensores reais do ESP32 ou simula se não disponível"""
    
    # Tenta obter dados reais do ESP32
    esp32_data = get_esp32_sensor_data()
    
    if esp32_data:
        # USA DADOS REAIS DO ESP32!
        logger.info("📡 Usando dados REAIS do ESP32")
        
        nitrogen = esp32_data['nitrogen']
        phosphorus = esp32_data['phosphorus']
        potassium = esp32_data['potassium']
        ph_level = esp32_data['ph_level']
        
        # DHT22 - Temperatura e Umidade do Ar
        air_temp = esp32_data['temperature']
        air_hum = esp32_data['humidity']
        
        # Umidade do solo (simulada baseada na umidade do ar)
        # Em produção, seria outro sensor
        soil_hum = air_hum * 0.8  # Estimativa
        
        # Atualiza estado NPK global
        npk_status['nitrogen'] = nitrogen
        npk_status['phosphorus'] = phosphorus
        npk_status['potassium'] = potassium
        
    else:
        # FALLBACK: Simula quando ESP32 não está conectado
        logger.debug("🔧 Simulando dados (ESP32 não conectado)")
        
        base_ph = random.uniform(5.0, 8.0)
        soil_hum = random.uniform(30, 90)
        
        # NPK baseado no estado atual controlado pela interface
        nitrogen = npk_status['nitrogen']
        phosphorus = npk_status['phosphorus'] 
        potassium = npk_status['potassium']
        
        ph_level = base_ph
        air_temp = random.uniform(18, 35)
        air_hum = random.uniform(40, 80)
    
    # Determina se irrigação deve estar ativa
    irrigation_needed = should_irrigate(
        ph_level, soil_hum, nitrogen, phosphorus, potassium
    )
    
    return SensorData(
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        nitrogen=nitrogen,
        phosphorus=phosphorus,
        potassium=potassium,
        ph_level=round(ph_level, 2),
        soil_humidity=round(soil_hum, 1),
        air_temperature=round(air_temp, 1),
        air_humidity=round(air_hum, 1),
        irrigation_active=irrigation_needed
    )

def should_irrigate(ph: float, humidity: float, n: bool, p: bool, k: bool) -> bool:
    """
    Lógica de decisão para irrigação baseada na cultura selecionada
    INCLUI verificação meteorológica (Atividade Opcional 1)
    
    Returns:
        bool: True se deve irrigar, False caso contrário
    """
    culture = CULTURES[current_culture]
    
    # NOVO: Verifica condições meteorológicas primeiro
    try:
        api = get_weather_api()
        if api:
            weather_check = api.should_skip_irrigation("São Paulo")
            if weather_check['skip_irrigation']:
                print(f"🌧️ Irrigação suspensa: {weather_check['reason']}")
                return False  # Não irrigar se vai chover
    except:
        pass  # Continua com lógica normal se API falhar
    
    # Verifica condições básicas
    ph_ok = culture.ph_min <= ph <= culture.ph_max
    humidity_ok = humidity >= culture.humidity_min
    
    # Verifica elementos NPK necessários
    npk_ok = True
    if culture.nitrogen_required and not n:
        npk_ok = False
    if culture.phosphorus_required and not p:
        npk_ok = False
    if culture.potassium_required and not k:
        npk_ok = False
    
    # Irrigação necessária se umidade baixa OU nutrientes insuficientes
    return humidity < culture.humidity_min or not npk_ok

@app.route('/')
def dashboard():
    """Página principal do dashboard"""
    # Gera nova leitura dos sensores
    latest_data = simulate_sensor_reading()
    sensor_history.append(latest_data)
    
    # Mantém apenas os últimos 50 registros
    if len(sensor_history) > 50:
        sensor_history.pop(0)
    
    # Obtém informações da área selecionada
    current_area = None
    if selected_area_id:
        current_area = area_manager.get_area_by_id(current_culture, selected_area_id)
    
    # Obtém estatísticas da cultura atual
    culture_stats = area_manager.get_statistics(current_culture)
    
    return render_template('dashboard.html', 
                         sensor_data=latest_data,
                         culture=CULTURES[current_culture],
                         cultures=CULTURES,
                         current_culture=current_culture,
                         current_area=current_area,
                         culture_stats=culture_stats,
                         system_settings=system_settings)

@app.route('/api/sensor_data')
def api_sensor_data():
    """API para obter dados dos sensores em tempo real"""
    latest_data = simulate_sensor_reading()
    sensor_history.append(latest_data)
    
    if len(sensor_history) > 50:
        sensor_history.pop(0)
    
    return jsonify(asdict(latest_data))

@app.route('/api/history')
def api_history():
    """API para obter histórico de dados"""
    return jsonify([asdict(data) for data in sensor_history[-20:]])

# Estado atual dos fertilizantes NPK (simulação de aplicação)
npk_status = {
    'nitrogen': False,
    'phosphorus': False,
    'potassium': False
}

# Dosagens recomendadas de NPK por m² para cada cultura (kg/m²)
NPK_DOSAGE = {
    'banana': {
        'nitrogen': 0.015,    # 15g/m² de Nitrogênio
        'phosphorus': 0.010,  # 10g/m² de Fósforo
        'potassium': 0.020    # 20g/m² de Potássio (banana precisa muito K)
    },
    'milho': {
        'nitrogen': 0.012,    # 12g/m² de Nitrogênio
        'phosphorus': 0.008,  # 8g/m² de Fósforo
        'potassium': 0.010    # 10g/m² de Potássio
    }
}

def calculate_npk_amount(nutrient: str) -> dict:
    """
    Calcula quantidade de NPK a aplicar baseado na área selecionada e cultura
    
    Returns:
        dict: Informações sobre a aplicação (quantidade, unidade, área)
    """
    # Se não há área selecionada, usa valor padrão
    if not selected_area_id:
        return {
            "amount": 0,
            "unit": "kg",
            "area": 0,
            "message": "Selecione uma área de plantio primeiro"
        }
    
    # Obtém área selecionada
    current_area = area_manager.get_area_by_id(current_culture, selected_area_id)
    if not current_area:
        return {
            "amount": 0,
            "unit": "kg",
            "area": 0,
            "message": "Área não encontrada"
        }
    
    # Obtém dosagem recomendada para a cultura
    dosage_per_m2 = NPK_DOSAGE.get(current_culture, {}).get(nutrient, 0.010)
    
    # Calcula quantidade total
    total_kg = current_area.area * dosage_per_m2
    
    # Define unidade apropriada
    if total_kg < 1:
        amount = total_kg * 1000  # Converte para gramas
        unit = "g"
    else:
        amount = total_kg
        unit = "kg"
    
    return {
        "amount": round(amount, 2),
        "unit": unit,
        "area": current_area.area,
        "dosage_per_m2": dosage_per_m2 * 1000,  # em gramas
        "message": f"{round(amount, 2)} {unit} para {current_area.area}m²"
    }

@app.route('/api/apply_fertilizer/<nutrient>', methods=['POST'])
def apply_fertilizer(nutrient):
    """API para aplicar/remover fertilizante NPK com cálculo de quantidade E INTEGRAÇÃO ESP32"""
    global npk_status, esp32_bridge, esp32_connected
    
    if nutrient not in ['nitrogen', 'phosphorus', 'potassium']:
        return jsonify({"error": "Nutriente inválido"}), 400
    
    # Alterna o status do fertilizante
    npk_status[nutrient] = not npk_status[nutrient]
    
    # 🚀 NOVO: Envia comando para ESP32 via serial
    esp32_success = False
    if esp32_connected and esp32_bridge:
        try:
            # Mapeia nome para letra
            nutrient_letter = nutrient[0].upper()  # N, P ou K
            esp32_success = esp32_bridge.toggle_npk(nutrient_letter)
            if esp32_success:
                print(f"✅ Comando TOGGLE_NPK:{nutrient_letter} enviado ao ESP32")
            else:
                print(f"⚠️  Falha ao enviar comando ao ESP32")
        except Exception as e:
            print(f"❌ Erro ao comunicar com ESP32: {e}")
    
    status = "aplicado" if npk_status[nutrient] else "removido"
    nutrient_names = {
        'nitrogen': 'Nitrogênio (N)',
        'phosphorus': 'Fósforo (P)', 
        'potassium': 'Potássio (K)'
    }
    
    # Calcula quantidade se estiver aplicando
    npk_calculation = None
    detailed_message = f"{nutrient_names[nutrient]} {status}"
    
    if npk_status[nutrient]:
        npk_calculation = calculate_npk_amount(nutrient)
        if npk_calculation['amount'] > 0:
            detailed_message = f"{nutrient_names[nutrient]} aplicado: {npk_calculation['amount']} {npk_calculation['unit']}"
    
    return jsonify({
        "success": True,
        "nutrient": nutrient,
        "status": npk_status[nutrient],
        "message": detailed_message,
        "calculation": npk_calculation
    })

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Página de configurações do sistema"""
    global current_culture, system_settings, selected_area_id
    
    if request.method == 'POST':
        # Atualiza cultura selecionada
        new_culture = request.form.get('culture')
        if new_culture in CULTURES:
            current_culture = new_culture
            selected_area_id = None  # Reseta área ao mudar cultura
        
        # Atualiza configurações do sistema
        system_settings['auto_irrigation'] = 'auto_irrigation' in request.form
        system_settings['irrigation_duration'] = int(request.form.get('irrigation_duration', 30))
        system_settings['check_interval'] = int(request.form.get('check_interval', 5))
        
        return redirect(url_for('dashboard'))
    
    return render_template('settings.html',
                         cultures=CULTURES,
                         current_culture=current_culture,
                         system_settings=system_settings)

@app.route('/areas')
def areas():
    """Página de seleção de áreas de plantio (CSVs Fase 1)"""
    global current_culture
    
    # Permite trocar cultura via parâmetro URL
    culture_param = request.args.get('culture')
    if culture_param and culture_param in CULTURES:
        current_culture = culture_param
    
    # Obtém todas as áreas da cultura atual
    areas = area_manager.get_areas_by_culture(current_culture)
    culture_stats = area_manager.get_statistics(current_culture)
    
    return render_template('areas.html',
                         cultures=CULTURES,
                         current_culture=current_culture,
                         areas=areas,
                         selected_area_id=selected_area_id,
                         culture_stats=culture_stats)

@app.route('/api/select_area/<culture>/<int:area_id>', methods=['POST'])
def api_select_area(culture, area_id):
    """API para selecionar área de plantio"""
    global current_culture, selected_area_id
    
    if culture not in CULTURES:
        return jsonify({"error": "Cultura inválida"}), 400
    
    area = area_manager.get_area_by_id(culture, area_id)
    if not area:
        return jsonify({"error": "Área não encontrada"}), 404
    
    current_culture = culture
    selected_area_id = area_id
    
    return jsonify({
        "success": True,
        "culture": culture,
        "area_id": area_id,
        "area_size": area.area,
        "insumo": area.insumo,
        "message": f"Área #{area_id} de {culture.capitalize()} selecionada ({area.area}m²)"
    })

@app.route('/api/get_areas/<culture>')
def api_get_areas(culture):
    """API para obter áreas de uma cultura"""
    if culture not in ['banana', 'milho']:
        return jsonify({"error": "Cultura inválida"}), 400
    
    areas = area_manager.get_areas_by_culture(culture)
    
    return jsonify({
        "culture": culture,
        "count": len(areas),
        "areas": [{
            "id": a.id,
            "area": a.area,
            "insumo": a.insumo,
            "qtd_insumo": a.qtd_insumo,
            "unidade": a.unidade,
            "dimensions": a.get_dimensions_text(),
            "shape": a.get_shape_text()
        } for a in areas]
    })

@app.route('/manual_irrigation', methods=['POST'])
def manual_irrigation():
    """Endpoint para irrigação manual"""
    # Simula ativação manual da bomba d'água
    duration = int(request.form.get('duration', 15))
    
    # Registra ação manual
    manual_data = SensorData(
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        nitrogen=False, phosphorus=False, potassium=False,
        ph_level=0.0, soil_humidity=0.0,
        air_temperature=0.0, air_humidity=0.0,
        irrigation_active=True
    )
    
    return jsonify({
        "success": True, 
        "message": f"Irrigação manual ativada por {duration} minutos"
    })

@app.route('/reports')
def reports():
    """Página de relatórios e gráficos"""
    return render_template('reports.html', 
                         sensor_history=sensor_history[-20:],
                         culture=CULTURES[current_culture])

@app.route('/npk-dosages')
def npk_dosages():
    """Página de consulta de dosagens NPK por cultura"""
    # Informações detalhadas sobre dosagens NPK
    npk_info = {
        'banana': {
            'name': 'Banana',
            'icon': '🍌',
            'dosages': {
                'nitrogen': {'amount': 15, 'unit': 'g/m²', 'importance': 'Alta'},
                'phosphorus': {'amount': 10, 'unit': 'g/m²', 'importance': 'Média'},
                'potassium': {'amount': 20, 'unit': 'g/m²', 'importance': 'Crítica'}
            },
            'observations': [
                'Banana é EXTREMAMENTE exigente em Potássio',
                'K+ melhora sabor, tamanho e resistência ao transporte',
                'Deficiência de K causa frutos pequenos e casca fina',
                'Aplicar Potássio durante todo o ciclo'
            ],
            'effects': {
                'nitrogen': 'Acidifica o solo (pH ↓ 0.3-0.7)',
                'phosphorus': 'Neutraliza acidez (pH ↑ 0.2-0.5)',
                'potassium': 'Estabiliza pH (pH ↑ 0.1-0.3)'
            }
        },
        'milho': {
            'name': 'Milho',
            'icon': '🌽',
            'dosages': {
                'nitrogen': {'amount': 12, 'unit': 'g/m²', 'importance': 'Crítica'},
                'phosphorus': {'amount': 8, 'unit': 'g/m²', 'importance': 'Alta'},
                'potassium': {'amount': 10, 'unit': 'g/m²', 'importance': 'Média'}
            },
            'observations': [
                'Milho tem alta demanda de Nitrogênio (produção de proteínas)',
                'Fósforo é crítico nas primeiras 4-6 semanas',
                'Potássio garante enchimento uniforme dos grãos',
                'Dividir aplicação de N em cobertura'
            ],
            'effects': {
                'nitrogen': 'Acidifica o solo (pH ↓ 0.3-0.7)',
                'phosphorus': 'Neutraliza acidez (pH ↑ 0.2-0.5)',
                'potassium': 'Estabiliza pH (pH ↑ 0.1-0.3)'
            }
        }
    }
    
    return render_template('npk_dosages.html',
                         npk_info=npk_info,
                         current_culture=current_culture,
                         NPK_DOSAGE=NPK_DOSAGE)

@app.route('/weather')
def weather():
    """Página de dados meteorológicos - Atividade Opcional 1"""
    try:
        api = get_weather_api()
        if not api:
            raise Exception("API meteorológica não disponível")
            
        # Obtém dados meteorológicos atuais
        current_weather = api.get_current_weather("São Paulo")
        
        # Obtém recomendação de irrigação baseada no clima
        irrigation_recommendation = api.should_skip_irrigation("São Paulo")
        
        # Obtém previsão para os próximos dias
        forecast = api.get_weather_forecast("São Paulo", days=3)
        
        return render_template('weather.html',
                             current_weather=current_weather,
                             irrigation_recommendation=irrigation_recommendation,
                             forecast=forecast,
                             culture=CULTURES[current_culture])
    except Exception as e:
        # Em caso de erro, usar dados simulados
        try:
            api = get_weather_api()
            mock_data = api._get_mock_weather() if api else {
                'temperature': 25.0,
                'humidity': 65,
                'wind_speed': 12,
                'description': 'Tempo simulado',
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except:
            mock_data = {
                'temperature': 25.0,
                'humidity': 65,
                'wind_speed': 12,
                'description': 'Tempo simulado',
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        return render_template('weather.html',
                             current_weather=mock_data,
                             irrigation_recommendation={
                                 'skip_irrigation': False,
                                 'reason': 'Dados simulados - sem restrições climáticas',
                                 'confidence': 85
                             },
                             forecast=[mock_data],
                             culture=CULTURES[current_culture],
                             error_message=f"Erro na API: {str(e)}")

@app.route('/api/weather_check')
def api_weather_check():
    """API para verificar se deve suspender irrigação por clima"""
    try:
        if get_weather_recommendation:
            recommendation = get_weather_recommendation("São Paulo")
            
            # Formata a resposta corretamente
            skip_irrigation = recommendation.get('skip_irrigation', False)
            reasons_list = recommendation.get('reasons', [])
            
            # Combina as razões em uma string
            reason = ' | '.join(reasons_list) if reasons_list else 'Condições climáticas adequadas para irrigação'
            
            # Calcula confiança baseada no número de razões
            if skip_irrigation:
                confidence = min(85 + (len(reasons_list) * 5), 95)
            else:
                confidence = 90
            
            return jsonify({
                'skip_irrigation': skip_irrigation,
                'reason': reason,
                'confidence': confidence
            })
        else:
            return jsonify({
                'skip_irrigation': False,
                'reason': 'API meteorológica não disponível',
                'confidence': 0
            })
    except Exception as e:
        print(f"Erro em api_weather_check: {e}")
        return jsonify({
            'skip_irrigation': False,
            'reason': f'Erro na API meteorológica: {str(e)}',
            'confidence': 0
        })

@app.route('/development')
def development():
    """Página de seleção de plataforma de desenvolvimento"""
    return render_template('development.html', 
                         platforms=DEVELOPMENT_PLATFORMS)

@app.route('/development/<platform>')
def development_platform(platform):
    """Página específica da plataforma de desenvolvimento"""
    if platform not in DEVELOPMENT_PLATFORMS:
        return redirect(url_for('development'))
    
    platform_info = DEVELOPMENT_PLATFORMS[platform]
    
    # Lê arquivos de código se existirem
    code_content = ""
    diagram_content = ""
    
    try:
        if platform_info['code_path']:
            code_path = os.path.join(os.path.dirname(__file__), platform_info['code_path'])
            if os.path.exists(code_path):
                with open(code_path, 'r', encoding='utf-8') as f:
                    code_content = f.read()
    except:
        pass
    
    try:
        if platform_info['diagram_path']:
            diagram_path = os.path.join(os.path.dirname(__file__), platform_info['diagram_path'])
            if os.path.exists(diagram_path):
                with open(diagram_path, 'r', encoding='utf-8') as f:
                    diagram_content = f.read()
    except:
        pass
    
    return render_template('platform_detail.html',
                         platform=platform,
                         platform_info=platform_info,
                         code_content=code_content,
                         diagram_content=diagram_content)

@app.route('/api/download/<platform>/<file_type>')
def download_platform_file(platform, file_type):
    """API para download de arquivos da plataforma"""
    if platform not in DEVELOPMENT_PLATFORMS:
        return jsonify({"error": "Plataforma não encontrada"}), 404
    
    platform_info = DEVELOPMENT_PLATFORMS[platform]
    
    file_path = None
    if file_type == 'code':
        file_path = platform_info['code_path']
    elif file_type == 'diagram':
        file_path = platform_info['diagram_path']
    
    if not file_path:
        return jsonify({"error": "Arquivo não encontrado"}), 404
    
    try:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({"content": content, "filename": os.path.basename(full_path)})
        else:
            return jsonify({"error": "Arquivo não existe"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/esp32/status')
def esp32_status():
    """Retorna status da conexão ESP32"""
    global esp32_connected, esp32_bridge
    
    status_info = {
        "connected": esp32_connected,
        "port": esp32_bridge.port if esp32_bridge else None,
        "available": ESP32_AVAILABLE
    }
    
    if esp32_connected and esp32_bridge:
        try:
            # Tenta ler dados do ESP32
            data = esp32_bridge.get_status()
            status_info["last_data"] = data
        except:
            pass
    
    return jsonify(status_info)

@app.route('/api/esp32/reconnect', methods=['POST'])
def esp32_reconnect():
    """Tenta reconectar ao ESP32"""
    success = init_esp32_connection()
    return jsonify({
        "success": success,
        "connected": esp32_connected,
        "message": "ESP32 conectado!" if success else "Falha ao conectar ESP32"
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌱 FarmTech Solutions - Sistema de Irrigação Inteligente")
    print("="*60 + "\n")
    
    # Gera alguns dados iniciais para demonstração
    for i in range(10):
        sensor_history.append(simulate_sensor_reading())
    
    # Tenta conectar ao ESP32
    print("🔌 Tentando conectar ao ESP32...")
    init_esp32_connection()
    
    print("\n✅ Servidor Flask iniciando...")
    print("📡 Acesse: http://localhost:5000")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)