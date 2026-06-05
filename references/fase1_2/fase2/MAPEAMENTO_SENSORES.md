# 🔬 Mapeamento de Sensores ESP32 → Farm Irrigation System

## 📋 Visão Geral

Este documento descreve como os sensores físicos do ESP32 (simulados no Wokwi) são mapeados para as métricas exibidas no front-end da aplicação web.

---

## 🎯 Mapeamento de Sensores

### 1. **pH do Solo** 🔬
- **Sensor Físico:** LDR (Light Dependent Resistor) - Pino Analog A0
- **Conversão:** Valor ADC (0-4095) → pH (0-14)
- **Código ESP32:**
  ```cpp
  int ldr_raw = analogRead(LDR_PH);  // 0-4095 (12-bit ADC)
  float ph_level = (ldr_raw / 4095.0) * 14.0;  // Mapeia para 0-14
  ```
- **Front-end:** Exibido como "pH do Solo"
- **Como funciona:** O LDR detecta luminosidade que varia quando fertilizantes NPK são aplicados, simulando alteração do pH

### 2. **Umidade do Solo** 💧
- **Sensor Físico:** Calculado a partir do DHT22
- **Conversão:** `Umidade Solo = Umidade do Ar × 0.8`
- **Código Web App:**
  ```python
  soil_humidity = air_humidity * 0.8  # Estimativa
  ```
- **Front-end:** Exibido como "Umidade Solo"
- **Nota:** Em produção real, seria usado um sensor de umidade de solo dedicado

### 3. **Temperatura do Ar** 🌡️
- **Sensor Físico:** DHT22 - Pino Digital D21
- **Leitura Direta:** Temperatura em °C
- **Código ESP32:**
  ```cpp
  float temperature = dht.readTemperature();  // °C
  ```
- **Front-end:** Exibido como "Temperatura Ar"
- **Faixa Normal:** 18°C - 35°C

### 4. **Umidade do Ar** 💨
- **Sensor Físico:** DHT22 - Pino Digital D21
- **Leitura Direta:** Umidade relativa em %
- **Código ESP32:**
  ```cpp
  float humidity = dht.readHumidity();  // %
  ```
- **Front-end:** Exibido como "Umidade Ar"
- **Faixa Normal:** 40% - 80%

---

## 🔌 Hardware ESP32 (Wokwi)

### Componentes Utilizados
```
ESP32-WROOM-32
├── D2  → Botão Nitrogênio (N)
├── D4  → Botão Fósforo (P)
├── D5  → Botão Potássio (K)
├── A0  → LDR (pH)
├── D21 → DHT22 (Temp + Umidade)
├── D18 → Relé (Bomba d'água)
└── D23 → LED Status
```

### Arquivo de Configuração
- **diagram.json:** Circuito Wokwi completo
- **platformio.ini:** Bibliotecas (DHT, ArduinoJson)
- **src/farm_irrigation_system.ino:** Código principal

---

## 🌐 Integração Web ↔ ESP32

### Fluxo de Dados

```
┌─────────────┐         ┌──────────────┐         ┌────────────┐
│   ESP32     │  Serial │  Python      │  HTTP   │  Front-end │
│  (Wokwi)    │ ──────→ │  Bridge      │ ──────→ │  (Flask)   │
└─────────────┘ 115200  └──────────────┘         └────────────┘
                         esp32_serial_bridge.py    dashboard.html
```

### Comandos Seriais

| Comando | Descrição | Resposta |
|---------|-----------|----------|
| `GET_SENSORS` | Solicita leitura de todos sensores | JSON com dados |
| `TOGGLE_NPK:N` | Alterna nitrogênio | Confirmação |
| `TOGGLE_NPK:P` | Alterna fósforo | Confirmação |
| `TOGGLE_NPK:K` | Alterna potássio | Confirmação |
| `SET_NPK:1,0,1` | Define estado NPK | Confirmação |
| `GET_STATUS` | Status completo do sistema | JSON status |

### Formato de Resposta JSON

```json
{
  "sensors": {
    "N": true,
    "P": false,
    "K": true,
    "ph": 6.5,
    "ldr": 2048,
    "temp": 25.4,
    "hum": 65.2,
    "relay": false
  },
  "timestamp": 12345
}
```

---

## 📊 Visualização no Front-end

### Dashboard (dashboard.html)

#### Card de pH
```html
<div class="metric-value">6.5</div>
<div class="metric-label">
  🔬 Sensor LDR (Analog A0)
  pH detectado via ESP32
</div>
```

#### Card de Temperatura
```html
<div class="metric-value">25.4°C</div>
<div class="metric-label">
  🌡️ Sensor DHT22 (D21)
  Temperatura ambiente
</div>
```

#### Card de Umidade Ar
```html
<div class="metric-value">65.2%</div>
<div class="metric-label">
  💨 Sensor DHT22 (D21)
  Umidade relativa do ar
</div>
```

#### Card de Umidade Solo
```html
<div class="metric-value">52.2%</div>
<div class="metric-label">
  💧 Calculada a partir do DHT22
  (Umidade Ar × 0.8)
</div>
```

---

## 🔧 Código Python - Leitura de Sensores

### Função Principal (app.py)

```python
def get_esp32_sensor_data() -> Optional[Dict]:
    """Obtém dados reais do ESP32 via serial"""
    global esp32_bridge, esp32_connected
    
    if not esp32_connected or not esp32_bridge:
        return None
    
    try:
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
```

### Fallback para Simulação

```python
def simulate_sensor_reading() -> SensorData:
    """Lê sensores reais do ESP32 ou simula se não disponível"""
    
    # Tenta obter dados reais do ESP32
    esp32_data = get_esp32_sensor_data()
    
    if esp32_data:
        # USA DADOS REAIS DO ESP32!
        logger.info("📡 Usando dados REAIS do ESP32")
        
        # Mapeia dados para estrutura da aplicação
        ph_level = esp32_data['ph_level']
        air_temp = esp32_data['temperature']
        air_hum = esp32_data['humidity']
        soil_hum = air_hum * 0.8  # Estimativa
        
    else:
        # FALLBACK: Simula quando ESP32 não está conectado
        logger.debug("🔧 Simulando dados (ESP32 não conectado)")
        ph_level = random.uniform(5.0, 8.0)
        air_temp = random.uniform(18, 35)
        air_hum = random.uniform(40, 80)
        soil_hum = random.uniform(30, 90)
    
    return SensorData(...)
```

---

## 🎮 Testando a Integração

### 1. Iniciar Wokwi Simulator
```
1. Abrir arquivo: fase2/arduino_code/src/farm_irrigation_system.ino
2. Pressionar F1
3. Digitar: "Wokwi: Start Simulator"
4. Aguardar ESP32 inicializar
```

### 2. Iniciar Aplicação Web
```bash
cd fase2/web_app
python app.py
```

### 3. Verificar Conexão
```
✅ ESP32 conectado via serial!
📡 Dados ESP32: {'sensors': {...}}
```

### 4. Testar Sensores
- **Clicar botões NPK no Wokwi** → Altera pH automaticamente
- **Dashboard atualiza automaticamente** a cada 2 segundos
- **Verificar logs** para confirmar dados reais

---

## 🐛 Troubleshooting

### Problema: "ESP32 não conectado"
**Solução:**
1. Verificar se Wokwi Simulator está rodando
2. Verificar porta COM no Windows (Device Manager)
3. Tentar conectar manualmente:
   ```python
   from esp32_serial_bridge import connect_to_esp32
   connect_to_esp32('COM3')  # Ajustar porta
   ```

### Problema: "Dados não atualizam"
**Solução:**
1. Verificar console do navegador (F12)
2. Verificar logs do Flask
3. Testar comando manual:
   ```bash
   python -c "from esp32_serial_bridge import *; bridge = ESP32SerialBridge(); bridge.connect(); bridge.get_sensor_data()"
   ```

### Problema: "Valores estranhos no pH"
**Solução:**
- LDR é afetado por luz ambiente no Wokwi
- Ajustar no código: `ph_level = constrain(ph_level, 0, 14)`
- Usar calibração customizada se necessário

---

## 📚 Referências

### Arquivos Principais
- **ESP32:** `fase2/arduino_code/src/farm_irrigation_system.ino`
- **Bridge Python:** `fase2/web_app/esp32_serial_bridge.py`
- **Web App:** `fase2/web_app/app.py`
- **Dashboard:** `fase2/web_app/templates/dashboard.html`
- **Áreas:** `fase2/web_app/templates/areas.html`

### Documentação Adicional
- `fase2/arduino_code/README_QUICK_START.md` - Guia de início rápido Wokwi
- `fase2/web_app/INTEGRACAO_ESP32.md` - Integração completa ESP32
- `fase2/GUIA_WOKWI_PYTHON_INTEGRACAO.md` - Guia de integração Python

---

## ✅ Checklist de Implementação

- [x] Sensor LDR → pH do Solo
- [x] Sensor DHT22 → Temperatura do Ar
- [x] Sensor DHT22 → Umidade do Ar  
- [x] Cálculo → Umidade do Solo (Umidade Ar × 0.8)
- [x] Integração serial ESP32 ↔ Python
- [x] Visualização no dashboard
- [x] Documentação completa
- [x] Fallback para simulação sem ESP32

---

**Versão:** 1.0  
**Data:** 08/10/2025  
**Autor:** FarmTech Solutions - Fase 2  
**Status:** ✅ Completo e Funcional
