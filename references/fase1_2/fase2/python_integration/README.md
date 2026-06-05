# 🐍 Python-ESP32 Integration

## Integração Python com ESP32 para Sistema de Irrigação Inteligente

Esta pasta contém scripts Python para comunicação serial com o ESP32, implementando a **Atividade Opcional 1 - "IR ALÉM"** do projeto Fase 2.

---

## 📁 Arquivos

### 1. `esp32_communication.py`
**Descrição:** Script base para comunicação serial com ESP32

**Funcionalidades:**
- ✅ Conexão serial via USB/COM
- ✅ Envio de comandos para ESP32
- ✅ Leitura de dados dos sensores (JSON)
- ✅ Menu interativo de controle
- ✅ Monitoramento contínuo

**Uso:**
```bash
python esp32_communication.py
```

### 2. `smart_irrigation_integrated.py`
**Descrição:** Sistema integrado completo (ESP32 + API Meteorológica)

**Funcionalidades:**
- ✅ Comunicação com ESP32
- ✅ Integração com OpenWeatherMap API
- ✅ Decisão inteligente de irrigação
- ✅ Controle automático baseado em múltiplas fontes
- ✅ Monitoramento contínuo com decisões automáticas

**Uso:**
```bash
python smart_irrigation_integrated.py
```

---

## 🚀 Quick Start

### Passo 1: Instalar Dependências

```powershell
# Instalar PySerial
pip install pyserial

# Verificar instalação
python -m serial.tools.list_ports
```

### Passo 2: Conectar ESP32

**Opção A: Wokwi Simulator (VS Code)**
1. Abra `farm_irrigation_system.ino` no VS Code
2. Inicie simulação: `F1` → `Wokwi: Start Simulator`
3. Anote a porta serial virtual (geralmente RFC2217)

**Opção B: ESP32 Real (USB)**
1. Conecte ESP32 via cabo USB
2. Verifique porta no Gerenciador de Dispositivos (Windows)
3. Anote a porta COM (ex: COM3, COM4)

### Passo 3: Executar Script

```powershell
# Comunicação básica
python esp32_communication.py

# Sistema integrado (com API clima)
python smart_irrigation_integrated.py
```

---

## 📊 Comandos Disponíveis via Serial

| Comando | Descrição | Resposta |
|---------|-----------|----------|
| `GET_SENSORS` | Retorna dados JSON | `{"npk": {...}, "ph": {...}}` |
| `SET_RELAY:ON` | Liga bomba | `Relé (Bomba): LIGADA` |
| `SET_RELAY:OFF` | Desliga bomba | `Relé (Bomba): DESLIGADA` |
| `SET_CULTURE:N` | Muda cultura (0-4) | `Cultura alterada para: X` |
| `CHECK_IRRIGATION` | Verifica necessidade | Análise + decisão |
| `PRINT_DATA` | Dados formatados | Tabela formatada |
| `GET_STATUS` | Status sistema | `STATUS:ONLINE` |
| `HELP` | Lista comandos | Menu de ajuda |

---

## 🔧 Configuração

### Portas Seriais Comuns

**Windows:**
```
COM3, COM4, COM5, COM6, ...
```

**Linux:**
```
/dev/ttyUSB0
/dev/ttyUSB1
/dev/ttyACM0
```

**macOS:**
```
/dev/cu.usbserial-*
/dev/cu.SLAB_USBtoUART
```

### Listar Portas Disponíveis

**Windows PowerShell:**
```powershell
Get-WmiObject Win32_SerialPort | Select-Object Name, DeviceID
```

**Python:**
```python
python -m serial.tools.list_ports
```

---

## 📖 Exemplos de Uso

### Exemplo 1: Leitura Simples de Dados

```python
from esp32_communication import ESP32Communication

# Conecta
esp = ESP32Communication(port='COM3')
esp.connect()

# Obtém dados
data = esp.get_sensor_data()
print(f"pH: {data['ph']['ph_level']}")
print(f"Temperatura: {data['environment']['temperature']}°C")

# Desconecta
esp.disconnect()
```

### Exemplo 2: Controle da Bomba

```python
from esp32_communication import ESP32Communication
import time

esp = ESP32Communication(port='COM3')
esp.connect()

# Liga bomba por 10 segundos
esp.set_relay(True)
print("Bomba ligada")
time.sleep(10)

# Desliga bomba
esp.set_relay(False)
print("Bomba desligada")

esp.disconnect()
```

### Exemplo 3: Monitoramento com Decisão

```python
from esp32_communication import ESP32Communication

esp = ESP32Communication(port='COM3')
esp.connect()

while True:
    data = esp.get_sensor_data()
    
    # Verifica pH
    ph = data['ph']['ph_level']
    if ph < 6.0 or ph > 7.0:
        print(f"pH inadequado: {ph:.2f}")
        esp.set_relay(True)  # Liga irrigação
    else:
        print(f"pH adequado: {ph:.2f}")
        esp.set_relay(False)  # Desliga irrigação
    
    time.sleep(30)  # Aguarda 30 segundos
```

---

## 🌐 Integração com API Meteorológica

O script `smart_irrigation_integrated.py` integra dados do ESP32 com a API OpenWeatherMap:

### Fluxo de Decisão

```
1. Coleta dados do ESP32
   └─► NPK, pH, Temperatura, Umidade

2. Consulta API OpenWeatherMap
   └─► Previsão de chuva, Temperatura externa, Umidade externa

3. Análise Inteligente
   ├─► Se vai chover → NÃO irrigar
   ├─► Se umidade externa alta → NÃO irrigar
   ├─► Se pH inadequado → irrigar
   ├─► Se umidade solo baixa → irrigar
   └─► Se NPK insuficiente → irrigar

4. Executa ação no ESP32
   └─► Liga/desliga bomba automaticamente
```

### Exemplo de Uso Integrado

```bash
python smart_irrigation_integrated.py
```

**Saída esperada:**
```
🌾 Sistema de Irrigação Inteligente - Integração Completa
==============================================================
✅ Conectado ao ESP32 na porta COM3
✅ API meteorológica disponível

Ciclo de Monitoramento - 2025-10-07 14:30:00
🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄🔄

📡 Coletando dados do campo...

📊 Dados dos Sensores - 14:30:00
==================================================
🌱 NPK:
   N (Nitrogênio):  ✅ SIM
   P (Fósforo):     ❌ NÃO
   K (Potássio):    ✅ SIM

🧪 pH do Solo:
   Valor: 6.45
   Raw ADC: 1890

🌡️  Ambiente:
   Temperatura: 24.5°C
   Umidade:     52.3%

💧 Irrigação:
   Bomba: 🔴 DESLIGADA
==================================================

🌤️  Consultando condições meteorológicas...

Condições Meteorológicas em São Paulo:
  🌡️  Temperatura: 26.2°C
  💧 Umidade: 55.0%
  🌧️  Chuva: NÃO
  📝 Descrição: Parcialmente nublado
  📊 Fonte: api

🧠 Processando decisão inteligente...

============================================================
🤖 Decisão Automática de Irrigação
============================================================
Ação: 🟢 IRRIGAR
Confiança: 80%
Fonte: integrated_analysis

Justificativa:
  • Falta fósforo
  • Baixa umidade do solo (52.3%)
============================================================

ESP32: Relé (Bomba): LIGADA

⏰ Aguardando 30 segundos até próximo ciclo...
```

---

## 🐛 Troubleshooting

### Erro: "Access Denied" na porta COM

**Causa:** Outra aplicação está usando a porta

**Solução:**
1. Feche Arduino IDE, PlatformIO, etc.
2. Reinicie o computador
3. Tente novamente

### Erro: "No module named 'serial'"

**Solução:**
```bash
pip install pyserial
```

### ESP32 não responde

**Verificações:**
1. ✅ Cabo USB conectado
2. ✅ ESP32 ligado (LED aceso)
3. ✅ Porta COM correta
4. ✅ Baudrate 115200
5. ✅ Código .ino carregado no ESP32

### Dados JSON malformados

**Causa:** Buffer serial com dados incompletos

**Solução:**
```python
# Limpar buffer antes de ler
esp.serial_conn.reset_input_buffer()
data = esp.get_sensor_data()
```

---

## 📚 Documentação Adicional

- **Guia Completo:** [`../GUIA_WOKWI_PYTHON_INTEGRACAO.md`](../GUIA_WOKWI_PYTHON_INTEGRACAO.md)
- **Código ESP32:** [`../arduino_code/farm_irrigation_system.ino`](../arduino_code/farm_irrigation_system.ino)
- **API Meteorológica:** [`../api_clima/weather_integration.py`](../api_clima/weather_integration.py)

---

## ✅ Checklist de Implementação

### Atividade Opcional 1 - "IR ALÉM"

- [x] Script Python de comunicação serial
- [x] Leitura de dados JSON do ESP32
- [x] Envio de comandos para ESP32
- [x] Integração com API meteorológica
- [x] Decisão inteligente baseada em múltiplas fontes
- [x] Controle automático de irrigação
- [x] Menu interativo de operação
- [x] Monitoramento contínuo
- [x] Documentação completa
- [x] Exemplos de uso

---

## 🎯 Critérios de Avaliação FIAP

### Funcionalidades Implementadas

✅ **Comunicação Bidirecional:**
- Python envia comandos → ESP32 executa
- ESP32 envia dados → Python processa

✅ **Transferência de Dados:**
- Formato JSON estruturado
- Múltiplos tipos de dados (NPK, pH, temperatura, umidade)
- Timestamp e metadados

✅ **Integração Avançada:**
- API meteorológica externa
- Decisão baseada em múltiplas fontes
- Controle automático inteligente

✅ **Documentação:**
- Código comentado
- Exemplos práticos
- Guia de uso detalhado

---

## 🏆 Destaques do Projeto

> **"Grupos que desenvolverem itens opcionais serão monitorados internamente e poderão ser convidados para outros programas da FIAP."**

Este projeto implementa:
1. ✅ Comunicação serial Python-ESP32 completa
2. ✅ Integração com API meteorológica pública
3. ✅ Sistema de decisão inteligente multi-fonte
4. ✅ Automação completa do processo
5. ✅ Código modular e reutilizável

---

**FarmTech Solutions** | FIAP 2025 | Tecnologia em IA e Robótica

**Atividade Opcional 1 - Implementada com Sucesso! 🎉**
