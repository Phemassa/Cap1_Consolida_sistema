/*
 * Sistema de Irrigação Inteligente - FarmTech Solutions
 * Código PlatformIO para ESP32
 * Fase 2 - FIAP
 * 
 * Sensores e Atuadores:
 * - 3 Botões Verdes NPK (D2, D4, D5)
 * - LDR para pH (A0) 
 * - DHT22 Temperatura/Umidade (D21)
 * - Relé Bomba d'água (D18)
 * - LED Status (D23)
 * 
 * Este código é otimizado para PlatformIO com:
 * - Gerenciamento automático de dependências
 * - Build system otimizado
 * - Integração com Wokwi via wokwi.toml
 */

#include <Arduino.h>
#include <DHT.h>
#include <ArduinoJson.h>
#include <WiFi.h>

// ========================================
// DEFINIÇÕES DE HARDWARE
// ========================================

// Pinos dos sensores
#define BTN_NITROGEN    2
#define BTN_PHOSPHORUS  4
#define BTN_POTASSIUM   5
#define LDR_PH          A0
#define DHT_PIN         21
#define DHT_TYPE        DHT22
#define RELAY_PIN       18
#define LED_STATUS      23

// ========================================
// CONFIGURAÇÕES DO SISTEMA
// ========================================

// Inicialização do sensor DHT22
DHT dht(DHT_PIN, DHT_TYPE);

// Configurações de rede (opcional)
const char* WIFI_SSID = "FarmTech_WiFi";
const char* WIFI_PASSWORD = "farmtech123";

// Intervalos de operação (em milissegundos)
const unsigned long SENSOR_READ_INTERVAL = 2000;    // 2 segundos
const unsigned long IRRIGATION_CHECK_INTERVAL = 30000; // 30 segundos
const unsigned long DEBOUNCE_DELAY = 50;             // 50ms para debounce

// ========================================
// ESTRUTURAS DE DADOS
// ========================================

struct SensorReadings {
    bool nitrogen;
    bool phosphorus;
    bool potassium;
    int ldr_raw;
    float ph_level;
    float temperature;
    float humidity;
    bool pump_active;
    unsigned long timestamp;
};

struct CropParameters {
    const char* name;
    float ph_min;
    float ph_max;
    float humidity_min;
    float temp_min;
    float temp_max;
    bool needs_nitrogen;
    bool needs_phosphorus;
    bool needs_potassium;
};

// ========================================
// CONFIGURAÇÕES DAS CULTURAS
// ========================================

const CropParameters CROPS[] = {
    {"Tomate",  6.0, 6.8, 60.0, 18.0, 26.0, true,  true,  true},
    {"Milho",   6.0, 7.0, 55.0, 20.0, 30.0, true,  true,  true},
    {"Soja",    6.0, 7.0, 50.0, 22.0, 28.0, false, true,  true},
    {"Banana",  5.5, 6.5, 65.0, 24.0, 30.0, true,  true,  true},
    {"Café",    6.0, 6.5, 70.0, 18.0, 24.0, true,  true,  false}
};

const int NUM_CROPS = sizeof(CROPS) / sizeof(CROPS[0]);

// ========================================
// VARIÁVEIS GLOBAIS
// ========================================

// Leituras atuais dos sensores
SensorReadings currentReading = {false, false, false, 512, 7.0, 25.0, 60.0, false, 0};

// Controle de timing
unsigned long lastSensorRead = 0;
unsigned long lastIrrigationCheck = 0;

// Estados dos botões para debounce
bool btnStates[3] = {false, false, false};
bool lastBtnStates[3] = {false, false, false};
unsigned long lastBtnDebounce[3] = {0, 0, 0};

// Cultura atual (índice no array CROPS)
int currentCrop = 0;  // Padrão: Tomate

// Configurações do sistema
bool autoIrrigationEnabled = true;
bool systemInitialized = false;

// ========================================
// FUNÇÕES DE INICIALIZAÇÃO
// ========================================

void setupPins() {
    // Configura pinos de entrada (botões e sensores)
    pinMode(BTN_NITROGEN, INPUT_PULLUP);
    pinMode(BTN_PHOSPHORUS, INPUT_PULLUP);
    pinMode(BTN_POTASSIUM, INPUT_PULLUP);
    pinMode(LDR_PH, INPUT);
    
    // Configura pinos de saída (atuadores)
    pinMode(RELAY_PIN, OUTPUT);
    pinMode(LED_STATUS, OUTPUT);
    
    // Estado inicial dos atuadores
    digitalWrite(RELAY_PIN, LOW);   // Bomba desligada
    digitalWrite(LED_STATUS, HIGH); // LED status ligado
}

void setupSensors() {
    // Inicializa sensor DHT22
    dht.begin();
    
    // Aguarda estabilização dos sensores
    delay(2000);
    
    Serial.println("Sensores inicializados:");
    Serial.println("- DHT22 (Temperatura/Umidade)");
    Serial.println("- LDR (Sensor pH)");
    Serial.println("- Botões NPK");
    Serial.println("- Relé de Irrigação");
}

void setupWiFi() {
    // Configuração WiFi opcional
    WiFi.mode(WIFI_STA);
    // WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    
    // Para simulação, não conecta WiFi
    Serial.println("WiFi: Modo simulação (desabilitado)");
}

// ========================================
// FUNÇÕES DE LEITURA DOS SENSORES
// ========================================

void readButtons() {
    // Lê botões NPK com debounce
    int buttons[] = {BTN_NITROGEN, BTN_PHOSPHORUS, BTN_POTASSIUM};
    
    for (int i = 0; i < 3; i++) {
        bool reading = !digitalRead(buttons[i]); // Inverte (pullup)
        
        // Verifica mudança de estado
        if (reading != lastBtnStates[i]) {
            lastBtnDebounce[i] = millis();
        }
        
        // Aplica debounce
        if ((millis() - lastBtnDebounce[i]) > DEBOUNCE_DELAY) {
            if (reading != btnStates[i]) {
                btnStates[i] = reading;
                
                // Log mudança de estado
                if (btnStates[i]) {
                    const char* names[] = {"NITROGÊNIO", "FÓSFORO", "POTÁSSIO"};
                    Serial.printf("Botão %s ATIVADO\n", names[i]);
                }
            }
        }
        
        lastBtnStates[i] = reading;
    }
    
    // Atualiza estrutura de dados
    currentReading.nitrogen = btnStates[0];
    currentReading.phosphorus = btnStates[1];
    currentReading.potassium = btnStates[2];
}

void readEnvironmentalSensors() {
    // Lê sensor LDR (pH)
    currentReading.ldr_raw = analogRead(LDR_PH);
    currentReading.ph_level = (currentReading.ldr_raw / 1023.0) * 14.0;
    
    // Lê sensor DHT22
    float temp = dht.readTemperature();
    float hum = dht.readHumidity();
    
    // Verifica se leituras são válidas
    if (!isnan(temp) && !isnan(hum)) {
        currentReading.temperature = temp;
        currentReading.humidity = hum;
    } else {
        // Usa valores padrão se sensor falhar
        Serial.println("Aviso: DHT22 não respondeu, usando valores padrão");
    }
}

void updateSensorReadings() {
    readButtons();
    readEnvironmentalSensors();
    
    // Atualiza timestamp
    currentReading.timestamp = millis();
    currentReading.pump_active = digitalRead(RELAY_PIN);
    
    // Feedback visual (pisca LED)
    digitalWrite(LED_STATUS, LOW);
    delay(50);
    digitalWrite(LED_STATUS, HIGH);
}

// ========================================
// FUNÇÕES DE CONTROLE DE IRRIGAÇÃO
// ========================================

bool shouldIrrigate() {
    if (!autoIrrigationEnabled) {
        return false;
    }
    
    const CropParameters& crop = CROPS[currentCrop];
    bool needsIrrigation = false;
    
    // Verifica parâmetros da cultura atual
    
    // 1. Verifica pH
    if (currentReading.ph_level < crop.ph_min || 
        currentReading.ph_level > crop.ph_max) {
        needsIrrigation = true;
    }
    
    // 2. Verifica umidade
    if (currentReading.humidity < crop.humidity_min) {
        needsIrrigation = true;
    }
    
    // 3. Verifica temperatura
    if (currentReading.temperature < crop.temp_min || 
        currentReading.temperature > crop.temp_max) {
        needsIrrigation = true;
    }
    
    // 4. Verifica NPK
    if (crop.needs_nitrogen && !currentReading.nitrogen) {
        needsIrrigation = true;
    }
    if (crop.needs_phosphorus && !currentReading.phosphorus) {
        needsIrrigation = true;
    }
    if (crop.needs_potassium && !currentReading.potassium) {
        needsIrrigation = true;
    }
    
    return needsIrrigation;
}

void setPumpState(bool state) {
    digitalWrite(RELAY_PIN, state ? HIGH : LOW);
    currentReading.pump_active = state;
    
    Serial.printf("💧 Bomba de irrigação: %s\n", state ? "LIGADA" : "DESLIGADA");
    
    // Feedback visual
    if (state) {
        // Pisca LED rapidamente quando liga bomba
        for (int i = 0; i < 6; i++) {
            digitalWrite(LED_STATUS, LOW);
            delay(100);
            digitalWrite(LED_STATUS, HIGH);
            delay(100);
        }
    }
}

void checkIrrigationNeeds() {
    bool shouldActivate = shouldIrrigate();
    bool currentlyActive = currentReading.pump_active;
    
    if (shouldActivate && !currentlyActive) {
        Serial.println("\n🚨 ATIVANDO IRRIGAÇÃO AUTOMÁTICA");
        printIrrigationReason();
        setPumpState(true);
    }
    else if (!shouldActivate && currentlyActive) {
        Serial.println("\n✅ DESATIVANDO IRRIGAÇÃO - Condições ideais");
        setPumpState(false);
    }
}

void printIrrigationReason() {
    const CropParameters& crop = CROPS[currentCrop];
    Serial.printf("Cultura: %s\n", crop.name);
    
    // Verifica e reporta problemas específicos
    if (currentReading.ph_level < crop.ph_min) {
        Serial.printf("❌ pH muito baixo: %.2f (mín: %.1f)\n", 
                     currentReading.ph_level, crop.ph_min);
    }
    if (currentReading.ph_level > crop.ph_max) {
        Serial.printf("❌ pH muito alto: %.2f (máx: %.1f)\n", 
                     currentReading.ph_level, crop.ph_max);
    }
    if (currentReading.humidity < crop.humidity_min) {
        Serial.printf("❌ Umidade baixa: %.1f%% (mín: %.0f%%)\n", 
                     currentReading.humidity, crop.humidity_min);
    }
    if (crop.needs_nitrogen && !currentReading.nitrogen) {
        Serial.println("❌ Falta Nitrogênio");
    }
    if (crop.needs_phosphorus && !currentReading.phosphorus) {
        Serial.println("❌ Falta Fósforo");
    }
    if (crop.needs_potassium && !currentReading.potassium) {
        Serial.println("❌ Falta Potássio");
    }
}

// ========================================
// FUNÇÕES DE COMUNICAÇÃO SERIAL
// ========================================

void sendSensorDataJSON() {
    // Cria documento JSON
    DynamicJsonDocument doc(1024);
    
    doc["timestamp"] = currentReading.timestamp;
    doc["system"]["crop"] = CROPS[currentCrop].name;
    doc["system"]["auto_irrigation"] = autoIrrigationEnabled;
    
    // Dados NPK
    JsonObject npk = doc.createNestedObject("npk");
    npk["nitrogen"] = currentReading.nitrogen;
    npk["phosphorus"] = currentReading.phosphorus;
    npk["potassium"] = currentReading.potassium;
    
    // Dados pH
    JsonObject ph = doc.createNestedObject("ph");
    ph["raw_value"] = currentReading.ldr_raw;
    ph["level"] = round(currentReading.ph_level * 100) / 100.0;
    
    // Dados ambientais
    JsonObject env = doc.createNestedObject("environment");
    env["temperature"] = round(currentReading.temperature * 10) / 10.0;
    env["humidity"] = round(currentReading.humidity * 10) / 10.0;
    
    // Dados da bomba
    JsonObject pump = doc.createNestedObject("irrigation");
    pump["active"] = currentReading.pump_active;
    pump["auto_mode"] = autoIrrigationEnabled;
    
    // Serializa e envia
    String jsonString;
    serializeJson(doc, jsonString);
    Serial.println(jsonString);
}

void printFormattedData() {
    Serial.println("\n╔══════════════════════════════════╗");
    Serial.println("║     DADOS DOS SENSORES           ║");
    Serial.println("╠══════════════════════════════════╣");
    
    // NPK
    Serial.printf("║ NPK: N:%s P:%s K:%s              ║\n",
                 currentReading.nitrogen ? "✓" : "✗",
                 currentReading.phosphorus ? "✓" : "✗",
                 currentReading.potassium ? "✓" : "✗");
    
    // pH
    Serial.printf("║ pH: %.2f (LDR: %d)            ║\n",
                 currentReading.ph_level, currentReading.ldr_raw);
    
    // Ambiente
    Serial.printf("║ Temp: %.1f°C  Umidade: %.1f%%    ║\n",
                 currentReading.temperature, currentReading.humidity);
    
    // Bomba
    Serial.printf("║ Bomba: %-8s Cultura: %-8s ║\n",
                 currentReading.pump_active ? "LIGADA" : "DESLIG.",
                 CROPS[currentCrop].name);
    
    Serial.println("╚══════════════════════════════════╝\n");
}

void processSerialCommands() {
    if (!Serial.available()) return;
    
    String command = Serial.readStringUntil('\n');
    command.trim();
    command.toUpperCase();
    
    Serial.printf("Comando recebido: %s\n", command.c_str());
    
    if (command == "GET_SENSORS") {
        sendSensorDataJSON();
    }
    else if (command.startsWith("SET_PUMP:")) {
        bool state = command.endsWith("ON") || command.endsWith("1");
        setPumpState(state);
        Serial.printf("Bomba %s manualmente\n", state ? "ligada" : "desligada");
    }
    else if (command.startsWith("SET_CROP:")) {
        int crop = command.substring(9).toInt();
        if (crop >= 0 && crop < NUM_CROPS) {
            currentCrop = crop;
            Serial.printf("Cultura alterada para: %s\n", CROPS[crop].name);
        }
    }
    else if (command == "SET_AUTO:ON") {
        autoIrrigationEnabled = true;
        Serial.println("Irrigação automática HABILITADA");
    }
    else if (command == "SET_AUTO:OFF") {
        autoIrrigationEnabled = false;
        Serial.println("Irrigação automática DESABILITADA");
    }
    else if (command == "STATUS") {
        printFormattedData();
    }
    else if (command == "CHECK_IRRIGATION") {
        checkIrrigationNeeds();
    }
    else if (command == "HELP") {
        printHelp();
    }
    else {
        Serial.println("❌ Comando não reconhecido. Digite HELP para ajuda.");
    }
}

void printHelp() {
    Serial.println("\n╔════════════════════════════════════════╗");
    Serial.println("║           COMANDOS DISPONÍVEIS         ║");
    Serial.println("╠════════════════════════════════════════╣");
    Serial.println("║ GET_SENSORS      - Dados JSON          ║");
    Serial.println("║ SET_PUMP:ON/OFF  - Controla bomba     ║");
    Serial.println("║ SET_CROP:N       - Muda cultura (0-4)  ║");
    Serial.println("║ SET_AUTO:ON/OFF  - Auto irrigação     ║");
    Serial.println("║ STATUS           - Dados formatados    ║");
    Serial.println("║ CHECK_IRRIGATION - Força verificação  ║");
    Serial.println("║ HELP             - Esta ajuda         ║");
    Serial.println("╚════════════════════════════════════════╝\n");
    
    Serial.println("Culturas disponíveis:");
    for (int i = 0; i < NUM_CROPS; i++) {
        Serial.printf("%d - %s\n", i, CROPS[i].name);
    }
    Serial.println();
}

// ========================================
// FUNÇÕES PRINCIPAIS
// ========================================

void setup() {
    // Inicializa comunicação serial
    Serial.begin(115200);
    
    // Banner de inicialização
    Serial.println("\n╔════════════════════════════════════════╗");
    Serial.println("║    SISTEMA DE IRRIGAÇÃO INTELIGENTE    ║");
    Serial.println("║         FarmTech Solutions             ║");
    Serial.println("║           PlatformIO + ESP32           ║");
    Serial.println("╚════════════════════════════════════════╝");
    
    // Inicializa componentes
    setupPins();
    setupSensors();
    setupWiFi();
    
    // Leitura inicial
    updateSensorReadings();
    
    Serial.println("\n✅ Sistema inicializado com sucesso!");
    Serial.printf("🌱 Cultura padrão: %s\n", CROPS[currentCrop].name);
    Serial.printf("🔄 Irrigação automática: %s\n", autoIrrigationEnabled ? "ATIVA" : "INATIVA");
    Serial.println("\nDigite HELP para ver comandos disponíveis.\n");
    
    systemInitialized = true;
}

void loop() {
    unsigned long currentTime = millis();
    
    // Processa comandos seriais
    processSerialCommands();
    
    // Atualiza sensores periodicamente
    if (currentTime - lastSensorRead >= SENSOR_READ_INTERVAL) {
        updateSensorReadings();
        lastSensorRead = currentTime;
    }
    
    // Verifica necessidade de irrigação
    if (currentTime - lastIrrigationCheck >= IRRIGATION_CHECK_INTERVAL) {
        if (systemInitialized) {
            checkIrrigationNeeds();
        }
        lastIrrigationCheck = currentTime;
    }
    
    // Pequeno delay para não sobrecarregar o sistema
    delay(100);
}