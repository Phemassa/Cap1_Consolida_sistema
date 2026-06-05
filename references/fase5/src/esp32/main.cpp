#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT22
#define SOIL_PIN 34

const char* WIFI_SSID = "SEU_WIFI";
const char* WIFI_PASSWORD = "SUA_SENHA";
const char* API_URL = "https://SEU_ENDPOINT_AWS/sensores";

DHT dht(DHTPIN, DHTTYPE);

void connectWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  connectWiFi();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int soilRaw = analogRead(SOIL_PIN);

  if (isnan(temperature) || isnan(humidity)) {
    delay(5000);
    return;
  }

  String payload = "{";
  payload += "\"temperatura\":" + String(temperature, 2) + ",";
  payload += "\"umidade_ar\":" + String(humidity, 2) + ",";
  payload += "\"umidade_solo_raw\":" + String(soilRaw);
  payload += "}";

  HTTPClient http;
  http.begin(API_URL);
  http.addHeader("Content-Type", "application/json");
  int httpCode = http.POST(payload);

  Serial.println("HTTP status: " + String(httpCode));
  Serial.println(payload);

  http.end();
  delay(10000);
}
