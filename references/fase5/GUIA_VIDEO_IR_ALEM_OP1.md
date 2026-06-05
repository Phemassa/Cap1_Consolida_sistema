# 📹 Guia de Gravação — Vídeo "Ir Além" Opção 1

> **Duração:** ≤ 5 minutos  
> **Formato:** MP4, 1080p ou 720p, não listado no YouTube  
> **Destino:** GitHub README (link do vídeo)

---

## 🎬 Roteiro Detalhado

### **ABERTURA (0:00 — 0:30)**

**Slide/Cenário:**
- Mostrar logo FarmTech Solutions ou FIAP
- Título na tela: **"Ir Além — Opção 1: Sistema de Coleta de Dados com ESP32"**

**Narração:**
> "Olá, somos a FarmTech Solutions. Esta é uma entrega extra — Ir Além — onde desenvolvemos um sistema real de coleta de dados agrícolas utilizando ESP32, sensores e comunicação Wi-Fi. Vamos demonstrar como funciona."

**O que aparecer na câmera:**
- Você falando (ou apenas tela compartilhada)
- Background: ambiente de trabalho ou fazenda (opcional)

---

### **CONTEXTO E JUSTIFICATIVA (0:30 — 1:30)**

**Slide 1: Sensores Escolhidos**
- Mostrar imagem ou ícone dos sensores

**Narração:**
> "Escolhemos dois sensores:
> 
> 1) **DHT22** — Temperatura e Umidade do Ar (°C e %)
>    - Faixa: -40°C a 80°C
>    - Uso: monitorar condições climáticas do campo
> 
> 2) **Sensor de Umidade do Solo** (analógico)
>    - Faixa: 0-1023 (ADC de 10 bits)
>    - Uso: decidir quando irrigar
> 
> **Justificativa:** Estas duas variáveis são críticas para previsão de rendimento de safra e decisões de irrigação em tempo real, alinhando perfeitamente com nossa solução de Machine Learning da Entrega 1."

**Slide 2: Arquitetura do Sistema**
- Exibir diagrama salvo em `assets/circuito_esp32_wokwi.svg` (abrir no navegador ou converter para PNG/screenshot)
- Mostrar as conexões: DHT22 (GPIO 4) + Sensor Solo (GPIO 34) → ESP32 → Wi-Fi → AWS

**Narração (complemento):**
> "A arquitetura é simples:
> - Sensores (DHT22 e Solo) → ESP32 (coleta via GPIO)
> - ESP32 → Wi-Fi (comunicação sem fio)
> - Wi-Fi → API HTTP na AWS (armazenamento em sa-east-1)
> 
> Isso permite monitoramento contínuo e em tempo real, com dados sincronizados na nuvem."

---

### **CIRCUITO NO WOKWI (1:30 — 2:30)**

**Ação 1: Abrir Wokwi.com no navegador**

**Narração:**
> "Para demonstrar, usamos a simulação do Wokwi — uma plataforma que nos permite montar e testar circuitos de ESP32 sem hardware físico. Aqui temos:"

**Ação 2: Mostrar/Explicar a Montagem**

**Mostre na tela do Wokwi ou em imagem salva:**
- ESP32 DevKit
- DHT22 conectado ao GPIO 4 (pinos DATA, VCC, GND)
- Sensor de solo conectado ao GPIO 34 (pinos AOUT, VCC, GND)

**Narração (explicando enquanto aponta):**
> "O DHT22 está no pino GPIO 4. É um sensor digital que comunica via protocolo 1-Wire.
> 
> O sensor de umidade do solo está no GPIO 34, que é um pino analógico (ADC) da ESP32.
> 
> Ambos compartilham VCC (3.3V) e GND da placa."

**Imagem Recomendada:**
- Salvar screenshot do Wokwi ou criar diagrama em `assets/wokwi_circuito.png`
- Adicionar anotações (setas, rótulos)

---

### **FIRMWARE — CÓDIGO C/C++ (2:30 — 3:45)**

**Ação: Abrir VS Code com `src/esp32/main.cpp`**

**Narração:**
> "Este é o firmware que roda no ESP32. Vou mostrar as partes principais:"

**Seção 1: Includes e Configuração**
```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT22
#define SOIL_PIN 34

const char* WIFI_SSID = "SEU_WIFI";
const char* WIFI_PASSWORD = "SUA_SENHA";
const char* API_URL = "https://SEU_ENDPOINT_AWS/sensores";
```

**Narração:**
> "Aqui definimos as bibliotecas necesárias (WiFi, DHT) e mapeamos os pinos dos sensores. As credenciais Wi-Fi e endpoint da API são preenchidas aqui."

**Seção 2: Setup e Loop**
```cpp
void setup() {
  Serial.begin(115200);
  dht.begin();
  connectWiFi();
}

void loop() {
  // Leitura dos sensores
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int soilRaw = analogRead(SOIL_PIN);
  
  // Envio HTTP
  // ... (mostrar JSON)
}
```

**Narração:**
> "Na inicialização, conectamos ao Wi-Fi. No loop principal:
> 1. Lemos temperatura e umidade do DHT22
> 2. Lemos a umidade do solo via ADC
> 3. Construímos um JSON com os dados
> 4. Enviamos via HTTP POST para a API na AWS
> 5. Aguardamos 10 segundos e repetimos"

**Destaque:**
```json
{
  "temperatura": 28.5,
  "umidade_ar": 65.0,
  "umidade_solo_raw": 2500
}
```

**Narração (complemento):**
> "O formato JSON é padronizado para facil integração com a API e análise em tempo real."

---

### **TESTE LOCAL — SIMULADOR PYTHON (3:45 — 4:45)**

**Ação: Abrir Terminal / PowerShell**

**Comando:**
```bash
cd /home/phemassa/FIAP
python src/esp32/simulator.py
```

**Narração:**
> "Como não temos um hardware ESP32 disponível no momento, usamos um simulador em Python que gera dados realistas de sensores. Ele também testa o envio HTTP para a API."

**Saída esperada (mostrar na tela):**
```
=== Simulador ESP32 FarmTech ===
Endpoint: http://localhost:8000/sensores
Intervalo: 5s | Leituras: 5

[Leitura 1] {"device_id": "ESP32_FARM_001", "seq": 1, "timestamp": "2026-03-17T21:09:30Z", "temperatura": 34.13, "umidade_ar": 93.85, "umidade_solo_raw": 3053, "valid": true}
Envio: FALHA | erro: Connection refused

[Leitura 2] ...
```

**Narração (explicando):**
> "O simulador:
> 1. Gera leituras realistas de temperatura (18-36°C), umidade do ar (0-100%) e umidade do solo (900-4000 ADC)
> 2. Valida os dados para garantir consistência
> 3. Tenta enviar via HTTP para um endpoint local
> 4. A falha de conexão é esperada pois não há API rodando no momento — em produção, a API receberá os dados"

**Comentário adicional:**
> "Este simulador valida nosso pipeline de coleta → validação → envio. Em ambiente real, isso rodaria continuamente no ESP32 físico."

---

### **FLUXO COMPLETO E DOCUMENTAÇÃO (4:45 — 5:00)**

**Ação: Mostrar GitHub README ou documento Markdown**

**Navegue para:** `src/esp32/readme.md` ou seção "Ir Além" do README principal

**Narração:**
> "Toda a documentação está no GitHub, incluindo:
> - Código-fonte comentado
> - Justificativa dos sensores
> - Arquitetura visual do circuito
> - Instruções para próximos passos
> 
> O sistema está pronto para ser testado em Wokwi ou com hardware real. Obrigado!"

**Fechamento (visual):**
- Logo FIAP
- Logo FarmTech Solutions
- Nome do repositório

---

## ✅ CHECKLIST PRÉ-GRAVAÇÃO

### **Materiais Prontos:**
- [ ] Arquivo `src/esp32/main.cpp` — código comentado e funcional
- [ ] Arquivo `src/esp32/simulator.py` — testado e rodando sem erros
- [ ] Arquivo `src/esp32/readme.md` — documentação completa
- [ ] Imagem do circuito Wokwi em `assets/wokwi_circuito.png` (screenshot ou diagrama)
- [ ] GitHub README com seção "Ir Além" atualizada

### **Técnica de Gravação:**
- [ ] Câmera/microfone funcionando
- [ ] Tela com boa resolução (1080p ou 720p)
- [ ] Zoom em fontes legível (font size 16+ no editor)
- [ ] Sem ruído de fundo
- [ ] Gravação em MP4 ou WebM

### **Pós-Gravação:**
- [ ] Editar vídeo (adicionar títulos, transições suaves)
- [ ] Exportar em 1080p ou 720p
- [ ] Upload no YouTube como "Não listado"
- [ ] Copiar URL do vídeo
- [ ] Adicionar link no README (`## 📹 Ir Além`)
- [ ] Fazer commit final e push ao GitHub

---

## 📝 DICAS DE APRESENTAÇÃO

1. **Fale com confiança:** Você construiu uma solução real.
2. **Vá devagar:** 5 minutos é tempo curto; deixe claro cada ponto.
3. **Use exemplos visuais:** Mostre código, gráficos, arquitetura — não apenas fale.
4. **Explique o "porquê":** Não apenas "como" — conexão com Entrega 1 (ML) e decisões técnicas.
5. **Mostre a integração:** Enfatize que é um sistema IoT completo, não partes isoladas.

---

## 🎥 DURAÇÃO ESPERADA POR SEÇÃO

| Seção | Duração |
|-------|---------|
| Abertura | 30 s |
| Contexto + Justificativa | 1 min |
| Circuito Wokwi | 1 min |
| Firmware C/C++ | 1 min 15 s |
| Teste Simulador | 1 min |
| Fluxo + Documentação | 15 s |
| **TOTAL** | **~5 min** |

---

**Boa gravação! 🚀**
