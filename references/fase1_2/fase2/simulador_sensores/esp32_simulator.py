"""
Simulador de Sensores ESP32 - Wokwi.com
Sistema de Irrigação Inteligente FarmTech Solutions

Este arquivo simula a comunicação com ESP32 e sensores:
- 3 Botões Verdes (NPK)
- Sensor LDR (pH)
- Sensor DHT22 (Temperatura e Umidade)
- Relé (Bomba d'água)
"""

import random
import time
import json
from datetime import datetime
from typing import Dict, Any
import threading

class ESP32Simulator:
    def __init__(self):
        """Inicializa o simulador do ESP32"""
        self.sensors = {
            'nitrogen_button': False,
            'phosphorus_button': False,
            'potassium_button': False,
            'ldr_value': 512,  # Valor analógico 0-1023
            'dht22_temp': 25.0,
            'dht22_humidity': 60.0,
            'relay_state': False
        }
        
        self.running = False
        self.update_interval = 2.0  # segundos
        
    def start_simulation(self):
        """Inicia a simulação dos sensores"""
        self.running = True
        self.simulation_thread = threading.Thread(target=self._simulation_loop)
        self.simulation_thread.daemon = True
        self.simulation_thread.start()
        print("Simulação ESP32 iniciada...")
    
    def stop_simulation(self):
        """Para a simulação"""
        self.running = False
        if hasattr(self, 'simulation_thread'):
            self.simulation_thread.join()
        print("Simulação ESP32 parada.")
    
    def _simulation_loop(self):
        """Loop principal da simulação"""
        while self.running:
            self._update_sensors()
            time.sleep(self.update_interval)
    
    def _update_sensors(self):
        """Atualiza valores dos sensores simulados"""
        
        # Simula variação natural dos botões NPK (mudança ocasional)
        if random.random() < 0.1:  # 10% chance de mudança
            self.sensors['nitrogen_button'] = random.choice([True, False])
        if random.random() < 0.1:
            self.sensors['phosphorus_button'] = random.choice([True, False])
        if random.random() < 0.1:
            self.sensors['potassium_button'] = random.choice([True, False])
        
        # Simula LDR (pH) - valor analógico que varia com NPK
        base_ldr = 512
        if self.sensors['nitrogen_button']:
            base_ldr += random.randint(-50, 50)
        if self.sensors['phosphorus_button']:
            base_ldr += random.randint(-30, 30)
        if self.sensors['potassium_button']:
            base_ldr += random.randint(-40, 40)
        
        # Adiciona ruído natural
        self.sensors['ldr_value'] = max(0, min(1023, base_ldr + random.randint(-20, 20)))
        
        # Simula DHT22 (temperatura e umidade com variação natural)
        self.sensors['dht22_temp'] += random.uniform(-1.0, 1.0)
        self.sensors['dht22_temp'] = max(15.0, min(40.0, self.sensors['dht22_temp']))
        
        self.sensors['dht22_humidity'] += random.uniform(-2.0, 2.0)
        self.sensors['dht22_humidity'] = max(20.0, min(95.0, self.sensors['dht22_humidity']))
    
    def get_sensor_readings(self) -> Dict[str, Any]:
        """
        Obtém leituras atuais dos sensores
        
        Returns:
            Dict com todos os valores dos sensores
        """
        # Converte LDR para pH (0-1023 -> 0-14)
        ph_value = (self.sensors['ldr_value'] / 1023.0) * 14.0
        
        return {
            'timestamp': datetime.now().isoformat(),
            'npk': {
                'nitrogen': self.sensors['nitrogen_button'],
                'phosphorus': self.sensors['phosphorus_button'],
                'potassium': self.sensors['potassium_button']
            },
            'ph': {
                'raw_value': self.sensors['ldr_value'],
                'ph_level': round(ph_value, 2)
            },
            'environment': {
                'temperature': round(self.sensors['dht22_temp'], 1),
                'humidity': round(self.sensors['dht22_humidity'], 1)
            },
            'actuators': {
                'irrigation_pump': self.sensors['relay_state']
            }
        }
    
    def set_relay_state(self, state: bool):
        """
        Controla o relé da bomba d'água
        
        Args:
            state: True para ligar, False para desligar
        """
        self.sensors['relay_state'] = state
        action = "ligada" if state else "desligada"
        print(f"Bomba d'água {action}")
    
    def simulate_button_press(self, button: str):
        """
        Simula pressão de botão NPK
        
        Args:
            button: 'nitrogen', 'phosphorus' ou 'potassium'
        """
        if button in ['nitrogen', 'phosphorus', 'potassium']:
            key = f"{button}_button"
            self.sensors[key] = not self.sensors[key]
            state = "pressionado" if self.sensors[key] else "liberado"
            print(f"Botão {button} {state}")
    
    def adjust_ldr(self, value: int):
        """
        Ajusta manualmente o valor do LDR (pH)
        
        Args:
            value: Valor entre 0-1023
        """
        self.sensors['ldr_value'] = max(0, min(1023, value))
        ph = (value / 1023.0) * 14.0
        print(f"LDR ajustado para {value} (pH: {ph:.2f})")
    
    def get_wokwi_diagram(self) -> str:
        """
        Retorna o diagrama de conexões para Wokwi.com
        
        Returns:
            String com o JSON do diagrama Wokwi
        """
        diagram = {
            "version": 1,
            "author": "FarmTech Solutions",
            "editor": "wokwi",
            "parts": [
                {
                    "type": "wokwi-esp32-devkit-v1",
                    "id": "esp",
                    "top": 0,
                    "left": 0,
                    "attrs": {}
                },
                {
                    "type": "wokwi-pushbutton",
                    "id": "btn_nitrogen",
                    "top": -38.4,
                    "left": 153.6,
                    "attrs": {"color": "green"}
                },
                {
                    "type": "wokwi-pushbutton", 
                    "id": "btn_phosphorus",
                    "top": -38.4,
                    "left": 211.2,
                    "attrs": {"color": "green"}
                },
                {
                    "type": "wokwi-pushbutton",
                    "id": "btn_potassium", 
                    "top": -38.4,
                    "left": 268.8,
                    "attrs": {"color": "green"}
                },
                {
                    "type": "wokwi-photoresistor-sensor",
                    "id": "ldr_ph",
                    "top": 105.6,
                    "left": 153.6,
                    "attrs": {}
                },
                {
                    "type": "wokwi-dht22",
                    "id": "dht",
                    "top": 105.6,
                    "left": 230.4,
                    "attrs": {}
                },
                {
                    "type": "wokwi-relay-module",
                    "id": "relay",
                    "top": 182.4,
                    "left": 153.6,
                    "attrs": {"color": "blue"}
                }
            ],
            "connections": [
                ["esp:TX0", "$serialMonitor:RX", "", []],
                ["esp:RX0", "$serialMonitor:TX", "", []],
                ["btn_nitrogen:1.l", "esp:D2", "green", ["h0"]],
                ["btn_nitrogen:1.r", "esp:GND.1", "black", ["h0"]],
                ["btn_phosphorus:1.l", "esp:D4", "green", ["h0"]],
                ["btn_phosphorus:1.r", "esp:GND.1", "black", ["h0"]],
                ["btn_potassium:1.l", "esp:D5", "green", ["h0"]],
                ["btn_potassium:1.r", "esp:GND.1", "black", ["h0"]],
                ["ldr_ph:VCC", "esp:3V3", "red", ["h0"]],
                ["ldr_ph:GND", "esp:GND.1", "black", ["h0"]],
                ["ldr_ph:AO", "esp:A0", "yellow", ["h0"]],
                ["dht:VCC", "esp:3V3", "red", ["h0"]],
                ["dht:GND", "esp:GND.1", "black", ["h0"]],
                ["dht:SDA", "esp:D21", "blue", ["h0"]],
                ["relay:VCC", "esp:3V3", "red", ["h0"]],
                ["relay:GND", "esp:GND.1", "black", ["h0"]],
                ["relay:IN", "esp:D18", "orange", ["h0"]]
            ],
            "dependencies": {}
        }
        
        return json.dumps(diagram, indent=2)

class SerialCommunication:
    """Simula comunicação serial com ESP32"""
    
    def __init__(self, esp32_sim: ESP32Simulator):
        self.esp32 = esp32_sim
    
    def send_command(self, command: str) -> str:
        """
        Envia comando para ESP32 simulado
        
        Args:
            command: Comando a ser enviado
            
        Returns:
            Resposta do ESP32
        """
        
        if command.startswith("GET_SENSORS"):
            readings = self.esp32.get_sensor_readings()
            return json.dumps(readings)
        
        elif command.startswith("SET_RELAY"):
            state = command.split(":")[1].lower() == "on"
            self.esp32.set_relay_state(state)
            return f"RELAY_SET:{state}"
        
        elif command.startswith("PRESS_BUTTON"):
            button = command.split(":")[1]
            self.esp32.simulate_button_press(button)
            return f"BUTTON_PRESSED:{button}"
        
        elif command.startswith("SET_LDR"):
            value = int(command.split(":")[1])
            self.esp32.adjust_ldr(value)
            return f"LDR_SET:{value}"
        
        else:
            return "UNKNOWN_COMMAND"

def generate_arduino_code() -> str:
    """
    Gera código Arduino/C++ para ESP32
    
    Returns:
        Código C++ para upload no ESP32
    """
    
    code = """
/*
 * Sistema de Irrigação Inteligente - FarmTech Solutions
 * Código para ESP32 - Wokwi.com
 * 
 * Sensores:
 * - Botões NPK (D2, D4, D5)
 * - LDR pH (A0)
 * - DHT22 (D21)
 * - Relé Bomba (D18)
 */

#include <DHT.h>

// Definições dos pinos
#define BTN_NITROGEN 2
#define BTN_PHOSPHORUS 4
#define BTN_POTASSIUM 5
#define LDR_PH A0
#define DHT_PIN 21
#define DHT_TYPE DHT22
#define RELAY_PIN 18

// Inicialização do DHT
DHT dht(DHT_PIN, DHT_TYPE);

// Variáveis globais
bool lastN = false, lastP = false, lastK = false;
unsigned long lastReading = 0;
const unsigned long READING_INTERVAL = 2000; // 2 segundos

void setup() {
  Serial.begin(115200);
  
  // Configuração dos pinos
  pinMode(BTN_NITROGEN, INPUT_PULLUP);
  pinMode(BTN_PHOSPHORUS, INPUT_PULLUP);
  pinMode(BTN_POTASSIUM, INPUT_PULLUP);
  pinMode(LDR_PH, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  
  // Inicializa DHT
  dht.begin();
  
  // Estado inicial do relé
  digitalWrite(RELAY_PIN, LOW);
  
  Serial.println("Sistema de Irrigação Inteligente - FarmTech Solutions");
  Serial.println("ESP32 Inicializado");
}

void loop() {
  // Verifica comandos seriais
  if (Serial.available()) {
    String command = Serial.readString();
    command.trim();
    processCommand(command);
  }
  
  // Leitura periódica dos sensores
  if (millis() - lastReading > READING_INTERVAL) {
    readSensors();
    lastReading = millis();
  }
  
  delay(100);
}

void processCommand(String cmd) {
  if (cmd.startsWith("GET_SENSORS")) {
    sendSensorData();
  }
  else if (cmd.startsWith("SET_RELAY:")) {
    String state = cmd.substring(10);
    bool relayState = (state == "ON" || state == "on");
    digitalWrite(RELAY_PIN, relayState ? HIGH : LOW);
    Serial.println("RELAY_SET:" + String(relayState ? "ON" : "OFF"));
  }
  else if (cmd.startsWith("GET_STATUS")) {
    Serial.println("STATUS:ONLINE");
  }
  else {
    Serial.println("UNKNOWN_COMMAND");
  }
}

void readSensors() {
  // Leitura dos botões NPK
  bool nitrogen = !digitalRead(BTN_NITROGEN);
  bool phosphorus = !digitalRead(BTN_PHOSPHORUS);
  bool potassium = !digitalRead(BTN_POTASSIUM);
  
  // Leitura do LDR (pH)
  int ldrValue = analogRead(LDR_PH);
  float phLevel = (ldrValue / 1023.0) * 14.0;
  
  // Leitura do DHT22
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  // Verifica se houve mudança nos botões
  if (nitrogen != lastN || phosphorus != lastP || potassium != lastK) {
    Serial.println("NPK_CHANGE");
    lastN = nitrogen;
    lastP = phosphorus;
    lastK = potassium;
  }
  
  // Envia dados se solicitado
  // (dados enviados apenas quando requisitado via comando)
}

void sendSensorData() {
  // Lê todos os sensores
  bool nitrogen = !digitalRead(BTN_NITROGEN);
  bool phosphorus = !digitalRead(BTN_PHOSPHORUS);
  bool potassium = !digitalRead(BTN_POTASSIUM);
  
  int ldrValue = analogRead(LDR_PH);
  float phLevel = (ldrValue / 1023.0) * 14.0;
  
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  bool relayState = digitalRead(RELAY_PIN);
  
  // Formata JSON
  Serial.print("{");
  Serial.print("\\"timestamp\\":\\"" + String(millis()) + "\\",");
  Serial.print("\\"nitrogen\\":" + String(nitrogen ? "true" : "false") + ",");
  Serial.print("\\"phosphorus\\":" + String(phosphorus ? "true" : "false") + ",");
  Serial.print("\\"potassium\\":" + String(potassium ? "true" : "false") + ",");
  Serial.print("\\"ldr_value\\":" + String(ldrValue) + ",");
  Serial.print("\\"ph_level\\":" + String(phLevel, 2) + ",");
  Serial.print("\\"temperature\\":" + String(temperature, 1) + ",");
  Serial.print("\\"humidity\\":" + String(humidity, 1) + ",");
  Serial.print("\\"relay_state\\":" + String(relayState ? "true" : "false"));
  Serial.println("}");
}

/*
 * Funções auxiliares para análise de irrigação
 */
bool shouldIrrigate(float ph, float soilHumidity, bool n, bool p, bool k) {
  // Lógica de decisão baseada nos parâmetros da cultura
  // (implementar conforme necessidades específicas)
  
  // Exemplo para tomate:
  bool phOk = (ph >= 6.0 && ph <= 6.8);
  bool humidityOk = (soilHumidity >= 60.0);
  bool npkOk = (n && p && k); // Tomate precisa de NPK completo
  
  return !humidityOk || !npkOk;
}
"""
    
    return code

if __name__ == "__main__":
    # Demonstração do simulador
    print("=== Simulador ESP32 - Sistema de Irrigação ===")
    
    # Cria simulador
    esp32 = ESP32Simulator()
    esp32.start_simulation()
    
    # Cria comunicação serial
    serial_comm = SerialCommunication(esp32)
    
    try:
        # Simula alguns comandos
        time.sleep(1)
        print("\n--- Leitura inicial dos sensores ---")
        response = serial_comm.send_command("GET_SENSORS")
        print(json.dumps(json.loads(response), indent=2, ensure_ascii=False))
        
        time.sleep(2)
        print("\n--- Simulando pressão de botões ---")
        serial_comm.send_command("PRESS_BUTTON:nitrogen")
        serial_comm.send_command("PRESS_BUTTON:phosphorus")
        
        time.sleep(1)
        print("\n--- Leitura após mudanças ---")
        response = serial_comm.send_command("GET_SENSORS")
        print(json.dumps(json.loads(response), indent=2, ensure_ascii=False))
        
        time.sleep(2)
        print("\n--- Ativando irrigação ---")
        serial_comm.send_command("SET_RELAY:ON")
        
        time.sleep(3)
        print("\n--- Desativando irrigação ---")
        serial_comm.send_command("SET_RELAY:OFF")
        
        time.sleep(5)
        
    except KeyboardInterrupt:
        print("\nEncerrando simulação...")
    
    finally:
        esp32.stop_simulation()
    
    print("\n=== Diagrama Wokwi gerado ===")
    print("Copie o JSON abaixo para Wokwi.com:")
    print(esp32.get_wokwi_diagram())