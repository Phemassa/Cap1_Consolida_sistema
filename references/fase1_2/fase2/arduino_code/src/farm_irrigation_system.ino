/*
 * Sistema de Irrigação Inteligente - FarmTech Solutions
 * Código para ESP32 - Wokwi.com
 * Fase 2 - FIAP
 * 
 * Sensores e Atuadores:
 * - 3 Botões Verdes NPK (D2, D4, D5)
 * - LDR para pH (A0) 
 * - DHT22 Temperatura/Umidade (D21)
 * - Relé Bomba d'água (D18)
 * - LED Status (D23)
 * 
 * Iniciar Wokwi Simulator:
 * Abra farm_irrigation_system.ino
 * >> Pressione F1
 * >> Digite Wokwi: Start Simulator
 * 
 * 
 * 
 * 
 * 
 */

#include <DHT.h>
#include <WiFi.h>
#include <ArduinoJson.h>

// Definições dos pinos
#define BTN_NITROGEN 2
#define BTN_PHOSPHORUS 4
#define BTN_POTASSIUM 5
#define LDR_PH A0
#define DHT_PIN 21
#define DHT_TYPE DHT22
#define RELAY_PIN 18
#define LED_STATUS 23

// Inicialização do DHT
DHT dht(DHT_PIN, DHT_TYPE);

// Configurações de rede (para uso real)
const char* ssid = "FarmTech_WiFi";
const char* password = "farmtech123";

// Variáveis globais
struct SensorData {
  bool nitrogen;
  bool phosphorus;
  bool potassium;
  int ldr_raw;
  float ph_level;
  float temperature;
  float humidity;
  bool relay_state;
  unsigned long timestamp;
};

SensorData currentData;
unsigned long lastReading = 0;
unsigned long lastIrrigationCheck = 0;
const unsigned long READING_INTERVAL = 2000;    // 2 segundos
const unsigned long IRRIGATION_INTERVAL = 30000; // 30 segundos

// Estados dos botões (TOGGLE - liga/desliga)
bool npkStateN = false, npkStateP = false, npkStateK = false; // Estado NPK real
bool lastBtnN = false, lastBtnP = false, lastBtnK = false;
unsigned long lastDebounceN = 0, lastDebounceP = 0, lastDebounceK = 0;
const unsigned long DEBOUNCE_DELAY = 200; // Aumentei para 200ms

// Contadores de cliques (para simulação)
int clickCountN = 0, clickCountP = 0, clickCountK = 0;

// Configurações de culturas
struct CultureConfig {
  float ph_min;
  float ph_max;
  float humidity_min;
  float temp_min;
  float temp_max;
  bool needs_nitrogen;
  bool needs_phosphorus;
  bool needs_potassium;
};

// Cultura atual (padrão: tomate)
CultureConfig cultures[] = {
  // Tomate
  {6.0, 6.8, 60.0, 18.0, 26.0, true, true, true},
  // Milho  
  {6.0, 7.0, 55.0, 20.0, 30.0, true, true, true},
  // Soja
  {6.0, 7.0, 50.0, 22.0, 28.0, false, true, true},
  // Banana
  {5.5, 6.5, 65.0, 24.0, 30.0, true, true, true},
  // Café
  {6.0, 6.5, 70.0, 18.0, 24.0, true, true, false}
};

int currentCulture = 0; // Índice da cultura atual

void setup() {
  Serial.begin(115200);
  
  // Configuração dos pinos
  pinMode(BTN_NITROGEN, INPUT_PULLUP);
  pinMode(BTN_PHOSPHORUS, INPUT_PULLUP);
  pinMode(BTN_POTASSIUM, INPUT_PULLUP);
  pinMode(LDR_PH, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LED_STATUS, OUTPUT);
  
  // Estado inicial
  digitalWrite(RELAY_PIN, LOW);
  digitalWrite(LED_STATUS, HIGH); // LED ligado = sistema ativo
  
  // Inicializa DHT22
  dht.begin();
  
  // Aguarda estabilização
  delay(2000);
  
  Serial.println("========================================");
  Serial.println("Sistema de Irrigação Inteligente");
  Serial.println("FarmTech Solutions - Fase 2");
  Serial.println("ESP32 Wokwi - Pronto para operar");
  Serial.println("========================================");
  
  // Leitura inicial
  readAllSensors();
  printSensorData();
}

void loop() {
  // Processa comandos seriais
  if (Serial.available()) {
    String command = Serial.readString();
    command.trim();
    processSerialCommand(command);
  }
  
  // Leitura periódica dos sensores
  if (millis() - lastReading >= READING_INTERVAL) {
    readAllSensors();
    lastReading = millis();
    
    // Pisca LED para indicar atividade
    digitalWrite(LED_STATUS, LOW);
    delay(50);
    digitalWrite(LED_STATUS, HIGH);
  }
  
  // Verifica necessidade de irrigação
  if (millis() - lastIrrigationCheck >= IRRIGATION_INTERVAL) {
    checkIrrigationNeeds();
    lastIrrigationCheck = millis();
  }
  
  delay(100);
}

void readAllSensors() {
  // Leitura com debounce dos botões NPK
  readButtonsWithDebounce();
  
  // Leitura do LDR (pH)
  currentData.ldr_raw = analogRead(LDR_PH);
  // Conversão LDR para pH: 0-4095 -> 0-14 (ESP32 usa ADC 12-bit)
  currentData.ph_level = (currentData.ldr_raw / 4095.0) * 14.0;
  
  // Leitura do DHT22
  currentData.temperature = dht.readTemperature();
  currentData.humidity = dht.readHumidity();
  
  // Verifica se leituras DHT são válidas
  if (isnan(currentData.temperature)) {
    currentData.temperature = 25.0; // Valor padrão
  }
  if (isnan(currentData.humidity)) {
    currentData.humidity = 60.0; // Valor padrão
  }
  
  // Estado atual do relé
  currentData.relay_state = digitalRead(RELAY_PIN);
  
  // Timestamp
  currentData.timestamp = millis();
}

void displayNPKStatus(String changedButton, bool newValue) {
  // Mostra qual sensor mudou
  Serial.println("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  Serial.print("⚡ SENSOR ALTERADO: ");
  Serial.print(changedButton);
  Serial.print(" → ");
  if (newValue) {
    Serial.println("High=1");
  } else {
    Serial.println("Low=0");
  }
  Serial.println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  
  // Display compacto estilo sensor data
  Serial.println("\n--- Dados dos Sensores ---");
  Serial.print("NPK: N=");
  Serial.print(currentData.nitrogen ? "High=1" : "Low=0");
  Serial.print(" P=");
  Serial.print(currentData.phosphorus ? "High=1" : "Low=0");
  Serial.print(" K=");
  Serial.println(currentData.potassium ? "High=1" : "Low=0");
  
  Serial.print("LDR: ");
  Serial.print(currentData.ldr_raw);
  Serial.print(" (pH: ");
  Serial.print(currentData.ph_level, 2);
  Serial.println(")");
  
  Serial.print("Temperatura: ");
  Serial.print(currentData.temperature, 1);
  Serial.println("°C");
  
  Serial.print("Umidade: ");
  Serial.print(currentData.humidity, 1);
  Serial.println("%");
  
  Serial.print("Bomba: ");
  Serial.println(currentData.relay_state ? "LIGADA" : "DESLIGADA");
  
  Serial.print("Cultura atual: ");
  const char* culturas[] = {"Tomate", "Milho", "Soja", "Banana", "Café"};
  Serial.println(culturas[currentCulture]);
  Serial.println("--------------------------\n");
}

void readButtonsWithDebounce() {
  unsigned long currentTime = millis();
  
  // ===== Botão Nitrogênio =====
  bool readingN = !digitalRead(BTN_NITROGEN);
  
  // Se estado mudou, reinicia timer
  if (readingN != lastBtnN) {
    lastDebounceN = currentTime;
  }
  
  // Se passou o tempo de debounce E houve mudança estável
  if ((currentTime - lastDebounceN) > DEBOUNCE_DELAY) {
    // Detecta BORDA DE SUBIDA (botão foi pressionado AGORA)
    if (readingN == true && lastBtnN == false) {
      npkStateN = !npkStateN; // TOGGLE
      currentData.nitrogen = npkStateN;
      clickCountN++;
      Serial.println("✅ TOGGLE N → " + String(npkStateN ? "High=1" : "Low=0"));
      displayNPKStatus("NITROGÊNIO", npkStateN);
    }
    lastBtnN = readingN; // Atualiza estado anterior
  }
  
  // ===== Botão Fósforo =====
  bool readingP = !digitalRead(BTN_PHOSPHORUS);
  
  if (readingP != lastBtnP) {
    lastDebounceP = currentTime;
  }
  
  if ((currentTime - lastDebounceP) > DEBOUNCE_DELAY) {
    if (readingP == true && lastBtnP == false) {
      npkStateP = !npkStateP; // TOGGLE
      currentData.phosphorus = npkStateP;
      clickCountP++;
      Serial.println("✅ TOGGLE P → " + String(npkStateP ? "High=1" : "Low=0"));
      displayNPKStatus("FÓSFORO", npkStateP);
    }
    lastBtnP = readingP;
  }
  
  // ===== Botão Potássio =====
  bool readingK = !digitalRead(BTN_POTASSIUM);
  
  if (readingK != lastBtnK) {
    lastDebounceK = currentTime;
  }
  
  if ((currentTime - lastDebounceK) > DEBOUNCE_DELAY) {
    if (readingK == true && lastBtnK == false) {
      npkStateK = !npkStateK; // TOGGLE
      currentData.potassium = npkStateK;
      clickCountK++;
      Serial.println("✅ TOGGLE K → " + String(npkStateK ? "High=1" : "Low=0"));
      displayNPKStatus("POTÁSSIO", npkStateK);
    }
    lastBtnK = readingK;
  }
}

void processSerialCommand(String command) {
  Serial.println("Comando recebido: " + command);
  
  if (command.equals("GET_SENSORS")) {
    sendSensorDataJSON();
  }
  else if (command.startsWith("SET_RELAY:")) {
    String state = command.substring(10);
    bool newState = (state.equals("ON") || state.equals("1"));
    setRelayState(newState);
  }
  else if (command.equals("GET_STATUS")) {
    Serial.println("STATUS:ONLINE");
  }
  else if (command.equals("PRINT_DATA")) {
    printSensorData();
  }
  else if (command.startsWith("SET_CULTURE:")) {
    String cultureStr = command.substring(12);
    int culture = cultureStr.toInt();
    if (culture >= 0 && culture < 5) {
      currentCulture = culture;
      String cultures_names[] = {"Tomate", "Milho", "Soja", "Banana", "Café"};
      Serial.println("Cultura alterada para: " + cultures_names[culture]);
    }
  }
  else if (command.startsWith("TOGGLE_NPK:")) {
    String nutrient = command.substring(11);
    nutrient.toUpperCase();
    if (nutrient.equals("N")) {
      npkStateN = !npkStateN;
      currentData.nitrogen = npkStateN;
      Serial.println("✅ TOGGLE N → " + String(npkStateN ? "High=1" : "Low=0"));
      displayNPKStatus("NITROGÊNIO", npkStateN);
    }
    else if (nutrient.equals("P")) {
      npkStateP = !npkStateP;
      currentData.phosphorus = npkStateP;
      Serial.println("✅ TOGGLE P → " + String(npkStateP ? "High=1" : "Low=0"));
      displayNPKStatus("FÓSFORO", npkStateP);
    }
    else if (nutrient.equals("K")) {
      npkStateK = !npkStateK;
      currentData.potassium = npkStateK;
      Serial.println("✅ TOGGLE K → " + String(npkStateK ? "High=1" : "Low=0"));
      displayNPKStatus("POTÁSSIO", npkStateK);
    }
  }
  else if (command.startsWith("SET_NPK:")) {
    // Formato: SET_NPK:1,0,1 (N,P,K)
    String values = command.substring(8);
    int firstComma = values.indexOf(',');
    int secondComma = values.indexOf(',', firstComma + 1);
    
    if (firstComma > 0 && secondComma > 0) {
      npkStateN = values.substring(0, firstComma).toInt() == 1;
      npkStateP = values.substring(firstComma + 1, secondComma).toInt() == 1;
      npkStateK = values.substring(secondComma + 1).toInt() == 1;
      
      currentData.nitrogen = npkStateN;
      currentData.phosphorus = npkStateP;
      currentData.potassium = npkStateK;
      
      Serial.println("✅ NPK atualizado via comando serial");
      Serial.print("N="); Serial.print(npkStateN ? "High=1" : "Low=0");
      Serial.print(" P="); Serial.print(npkStateP ? "High=1" : "Low=0");
      Serial.print(" K="); Serial.println(npkStateK ? "High=1" : "Low=0");
    }
  }
  else if (command.equals("CHECK_IRRIGATION")) {
    checkIrrigationNeeds();
  }
  else if (command.equals("HELP")) {
    printCommands();
  }
  else {
    Serial.println("Comando não reconhecido. Digite HELP para ver comandos disponíveis.");
  }
}

void sendSensorDataJSON() {
  // Cria JSON com dados dos sensores
  StaticJsonDocument<512> doc;
  
  doc["timestamp"] = currentData.timestamp;
  
  JsonObject npk = doc.createNestedObject("npk");
  npk["nitrogen"] = currentData.nitrogen;
  npk["phosphorus"] = currentData.phosphorus;
  npk["potassium"] = currentData.potassium;
  
  JsonObject ph = doc.createNestedObject("ph");
  ph["raw_value"] = currentData.ldr_raw;
  ph["ph_level"] = round(currentData.ph_level * 100) / 100.0;
  
  JsonObject environment = doc.createNestedObject("environment");
  environment["temperature"] = round(currentData.temperature * 10) / 10.0;
  environment["humidity"] = round(currentData.humidity * 10) / 10.0;
  
  JsonObject actuators = doc.createNestedObject("actuators");
  actuators["irrigation_pump"] = currentData.relay_state;
  
  String jsonString;
  serializeJson(doc, jsonString);
  Serial.println(jsonString);
}

void printSensorData() {
  Serial.println("\n--- Dados dos Sensores ---");
  Serial.println("NPK: N=" + String(currentData.nitrogen ? "SIM" : "NÃO") + 
                 " P=" + String(currentData.phosphorus ? "SIM" : "NÃO") + 
                 " K=" + String(currentData.potassium ? "SIM" : "NÃO"));
  Serial.println("LDR: " + String(currentData.ldr_raw) + " (pH: " + String(currentData.ph_level, 2) + ")");
  Serial.println("Temperatura: " + String(currentData.temperature, 1) + "°C");
  Serial.println("Umidade: " + String(currentData.humidity, 1) + "%");
  Serial.println("Bomba: " + String(currentData.relay_state ? "LIGADA" : "DESLIGADA"));
  
  String cultures_names[] = {"Tomate", "Milho", "Soja", "Banana", "Café"};
  Serial.println("Cultura atual: " + cultures_names[currentCulture]);
  Serial.println("-------------------------\n");
}

void setRelayState(bool state) {
  digitalWrite(RELAY_PIN, state ? HIGH : LOW);
  currentData.relay_state = state;
  
  Serial.println("Relé (Bomba): " + String(state ? "LIGADA" : "DESLIGADA"));
  
  // Feedback visual com LED
  if (state) {
    // Pisca rápido quando liga bomba
    for (int i = 0; i < 5; i++) {
      digitalWrite(LED_STATUS, LOW);
      delay(100);
      digitalWrite(LED_STATUS, HIGH);
      delay(100);
    }
  }
}

void checkIrrigationNeeds() {
  CultureConfig config = cultures[currentCulture];
  bool needsIrrigation = false;
  String reason = "";
  
  // Verifica pH
  if (currentData.ph_level < config.ph_min || currentData.ph_level > config.ph_max) {
    needsIrrigation = true;
    reason += "pH inadequado (" + String(currentData.ph_level, 2) + ") ";
  }
  
  // Verifica umidade
  if (currentData.humidity < config.humidity_min) {
    needsIrrigation = true;
    reason += "Baixa umidade (" + String(currentData.humidity, 1) + "%) ";
  }
  
  // Verifica temperatura
  if (currentData.temperature < config.temp_min || currentData.temperature > config.temp_max) {
    needsIrrigation = true;
    reason += "Temperatura inadequada (" + String(currentData.temperature, 1) + "°C) ";
  }
  
  // Verifica NPK
  if (config.needs_nitrogen && !currentData.nitrogen) {
    needsIrrigation = true;
    reason += "Falta Nitrogênio ";
  }
  if (config.needs_phosphorus && !currentData.phosphorus) {
    needsIrrigation = true;
    reason += "Falta Fósforo ";
  }
  if (config.needs_potassium && !currentData.potassium) {
    needsIrrigation = true;
    reason += "Falta Potássio ";
  }
  
  // Ação automática
  if (needsIrrigation && !currentData.relay_state) {
    Serial.println("\n🚨 IRRIGAÇÃO AUTOMÁTICA ATIVADA");
    Serial.println("Motivo: " + reason);
    Serial.println("\n📊 Status Sensores NPK:");
    Serial.print("   N (Nitrogênio): ");
    Serial.println(currentData.nitrogen ? "High=1" : "Low=0");
    Serial.print("   P (Fósforo):    ");
    Serial.println(currentData.phosphorus ? "High=1" : "Low=0");
    Serial.print("   K (Potássio):   ");
    Serial.println(currentData.potassium ? "High=1" : "Low=0");
    Serial.print("\nRelé (Bomba): ");
    Serial.println("LIGADA");
    setRelayState(true);
  }
  else if (!needsIrrigation && currentData.relay_state) {
    Serial.println("\n✅ IRRIGAÇÃO AUTOMÁTICA DESATIVADA");
    Serial.println("Condições ideais atingidas");
    Serial.println("\n📊 Status Sensores NPK:");
    Serial.print("   N (Nitrogênio): ");
    Serial.println(currentData.nitrogen ? "High=1" : "Low=0");
    Serial.print("   P (Fósforo):    ");
    Serial.println(currentData.phosphorus ? "High=1" : "Low=0");
    Serial.print("   K (Potássio):   ");
    Serial.println(currentData.potassium ? "High=1" : "Low=0");
    Serial.print("\nRelé (Bomba): ");
    Serial.println("DESLIGADA");
    setRelayState(false);
  }
  else if (needsIrrigation) {
    Serial.println("\n⚠️  ATENÇÃO: Irrigação necessária - " + reason);
    Serial.println("\n📊 Status Sensores NPK:");
    Serial.print("   N (Nitrogênio): ");
    Serial.println(currentData.nitrogen ? "High=1" : "Low=0");
    Serial.print("   P (Fósforo):    ");
    Serial.println(currentData.phosphorus ? "High=1" : "Low=0");
    Serial.print("   K (Potássio):   ");
    Serial.println(currentData.potassium ? "High=1" : "Low=0");
  }
  else {
    Serial.println("\n✅ Condições ideais para a cultura");
    Serial.println("\n📊 Status Sensores NPK:");
    Serial.print("   N (Nitrogênio): ");
    Serial.println(currentData.nitrogen ? "High=1" : "Low=0");
    Serial.print("   P (Fósforo):    ");
    Serial.println(currentData.phosphorus ? "High=1" : "Low=0");
    Serial.print("   K (Potássio):   ");
    Serial.println(currentData.potassium ? "High=1" : "Low=0");
  }
}

void printCommands() {
  Serial.println("\n=== Comandos Disponíveis ===");
  Serial.println("GET_SENSORS       - Retorna dados em JSON");
  Serial.println("SET_RELAY:ON      - Liga a bomba");
  Serial.println("SET_RELAY:OFF     - Desliga a bomba");
  Serial.println("GET_STATUS        - Status do sistema");
  Serial.println("PRINT_DATA        - Mostra dados formatados");
  Serial.println("SET_CULTURE:N     - Muda cultura (0-4)");
  Serial.println("CHECK_IRRIGATION  - Verifica necessidade irrigação");
  Serial.println("HELP              - Mostra estes comandos");
  Serial.println("============================\n");
  
  Serial.println("Culturas disponíveis:");
  Serial.println("0 - Tomate   1 - Milho   2 - Soja");
  Serial.println("3 - Banana   4 - Café\n");
}