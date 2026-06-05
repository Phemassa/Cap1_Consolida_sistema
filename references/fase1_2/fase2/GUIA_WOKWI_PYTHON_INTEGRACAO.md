# 🔌 Guia de Integração Wokwi + Python-ESP32

## FarmTech Solutions - Sistema de Irrigação Inteligente
**Fase 2 - FIAP | Projeto Interdisciplinar**

---

## 📋 Sumário

1. [Instalação e Configuração](#1-instalação-e-configuração)
2. [Usando Wokwi no VS Code](#2-usando-wokwi-no-vs-code)
3. [Comunicação Python-ESP32](#3-comunicação-python-esp32)
4. [Comandos Disponíveis](#4-comandos-disponíveis)
5. [Exemplos de Uso](#5-exemplos-de-uso)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. Instalação e Configuração

### 1.1 Pré-requisitos

✅ **Software necessário:**
- [x] Visual Studio Code
- [x] Python 3.8+ instalado
- [x] Extensão "Wokwi Embedded Simulator" instalada

### 1.2 Instalar Biblioteca PySerial

```powershell
# No terminal do VS Code ou PowerShell
pip install pyserial
```

### 1.3 Estrutura de Arquivos

```
fase2/
├── arduino_code/
│   ├── farm_irrigation_system.ino    # Código ESP32
│   ├── diagram.json                  # Diagrama do circuito Wokwi
│   ├── wokwi.toml                    # Configuração Wokwi
│   └── libraries.txt                 # Bibliotecas necessárias
└── python_integration/
    └── esp32_communication.py        # Script Python de comunicação
```

---

## 2. Usando Wokwi no VS Code

### 2.1 Iniciar Simulação

1. **Abra o arquivo** `farm_irrigation_system.ino` no VS Code
2. **Pressione** `F1` ou `Ctrl+Shift+P`
3. **Digite** `Wokwi: Start Simulator`
4. **Ou** clique no ícone ▶️ "Start Simulation" na barra superior

### 2.2 Interagir com o Circuito

**Botões NPK (Verde):**
- Clique nos botões para simular presença de nutrientes
- N = Nitrogênio
- P = Fósforo
- K = Potássio

**Sensor LDR (pH):**
- Clique no LDR e ajuste o slider para simular diferentes níveis de pH
- Valores: 0-4095 (ADC 12-bit)
- pH = (valor / 4095) × 14

**Sensor DHT22:**
- Clique no DHT22 para ajustar:
  - Temperatura (°C)
  - Umidade (%)

**Relé (Bomba):**
- LED no relé indica estado:
  - 🟢 Verde = Bomba LIGADA
  - 🔴 Vermelho = Bomba DESLIGADA

### 2.3 Monitor Serial

**Abrir Monitor Serial:**
- No simulador Wokwi, clique em **"Serial Monitor"** no canto inferior
- Ou pressione `Ctrl+Shift+S`

**Enviar Comandos:**
- Digite comandos no campo de texto
- Pressione Enter para enviar
- Exemplo: `GET_SENSORS`

---

## 3. Comunicação Python-ESP32

### 3.1 Modos de Comunicação

#### **Modo 1: Wokwi Simulação (Local)**

Quando rodando no Wokwi VS Code, a comunicação é feita via porta virtual.

```python
# A porta pode variar
python esp32_communication.py
# Quando solicitado, digite: RFC2217
```

#### **Modo 2: ESP32 Real (USB)**

Com ESP32 físico conectado via USB:

**Windows:**
```python
# Verificar porta no Gerenciador de Dispositivos
python esp32_communication.py
# Digite: COM3, COM4, COM5, etc.
```

**Linux/Mac:**
```bash
# Verificar porta com: ls /dev/tty*
python esp32_communication.py
# Digite: /dev/ttyUSB0 ou /dev/ttyACM0
```

### 3.2 Executar Script Python

```powershell
# Navegue até a pasta
cd "c:\Fiap Projeto\FarmTechSolutions\fase2\python_integration"

# Execute o script
python esp32_communication.py
```

### 3.3 Menu Interativo

Após conectar, você verá um menu:

```
🌾 FarmTech Solutions - Menu de Controle
==================================================
1. 📊 Obter dados dos sensores
2. 💧 Ligar bomba de irrigação
3. 🛑 Desligar bomba de irrigação
4. 🌱 Mudar cultura
5. 🔍 Verificar necessidade de irrigação
6. 📝 Imprimir dados formatados
7. 🔄 Monitoramento contínuo
8. 📋 Ver comandos disponíveis
9. 🚪 Sair
==================================================
```

---

## 4. Comandos Disponíveis

### 4.1 Comandos Via Serial Monitor

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `GET_SENSORS` | Retorna dados JSON dos sensores | `GET_SENSORS` |
| `SET_RELAY:ON` | Liga a bomba de irrigação | `SET_RELAY:ON` |
| `SET_RELAY:OFF` | Desliga a bomba | `SET_RELAY:OFF` |
| `GET_STATUS` | Status do sistema | `GET_STATUS` |
| `PRINT_DATA` | Mostra dados formatados | `PRINT_DATA` |
| `SET_CULTURE:N` | Muda cultura (0-4) | `SET_CULTURE:3` |
| `CHECK_IRRIGATION` | Verifica necessidade de irrigação | `CHECK_IRRIGATION` |
| `HELP` | Lista todos os comandos | `HELP` |

### 4.2 Culturas Disponíveis

| ID | Cultura | pH Ideal | Umidade Min | Temp Ideal |
|----|---------|----------|-------------|------------|
| 0 | Tomate | 6.0-6.8 | 60% | 18-26°C |
| 1 | Milho | 6.0-7.0 | 55% | 20-30°C |
| 2 | Soja | 6.0-7.0 | 50% | 22-28°C |
| 3 | Banana | 5.5-6.5 | 65% | 24-30°C |
| 4 | Café | 6.0-6.5 | 70% | 18-24°C |

---

## 5. Exemplos de Uso

### 5.1 Cenário 1: Monitoramento Básico

```python
# 1. Execute o script Python
python esp32_communication.py

# 2. Digite a porta quando solicitado
Porta serial [COM3]: COM3

# 3. No menu, escolha opção 1
Escolha uma opção: 1

# 4. Visualize os dados:
📊 Dados dos Sensores - 14:30:25
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
   Umidade:     62.3%

💧 Irrigação:
   Bomba: 🔴 DESLIGADA
==================================================
```

### 5.2 Cenário 2: Teste de Irrigação Automática

**No Wokwi Simulator:**

1. Ajuste LDR para pH baixo (< 5.5)
2. Desmarque botões NPK
3. Aguarde 30 segundos
4. Sistema ativará irrigação automaticamente

**Saída esperada no Serial Monitor:**
```
🚨 IRRIGAÇÃO AUTOMÁTICA ATIVADA
Motivo: pH inadequado (5.2) Falta Fósforo 
Relé (Bomba): LIGADA
```

### 5.3 Cenário 3: Controle Manual via Python

```python
# Opção 2: Ligar bomba
Escolha uma opção: 2
📤 Comando enviado: SET_RELAY:ON
Relé (Bomba): LIGADA

# Aguardar 10 segundos

# Opção 3: Desligar bomba
Escolha uma opção: 3
📤 Comando enviado: SET_RELAY:OFF
Relé (Bomba): DESLIGADA
```

### 5.4 Cenário 4: Mudança de Cultura

```python
# Opção 4: Mudar cultura
Escolha uma opção: 4

Culturas disponíveis:
  0 - Tomate
  1 - Milho
  2 - Soja
  3 - Banana
  4 - Café
Digite o ID da cultura: 3

📤 Comando enviado: SET_CULTURE:3
Cultura alterada para: Banana
```

### 5.5 Cenário 5: Monitoramento Contínuo

```python
# Opção 7: Monitoramento contínuo
Escolha uma opção: 7
Intervalo entre leituras (segundos) [5]: 10

🔄 Monitoramento contínuo iniciado (intervalo: 10s)
   Pressione Ctrl+C para parar

# Dados serão exibidos a cada 10 segundos
# Pressione Ctrl+C para parar
```

---

## 6. Troubleshooting

### 6.1 Erro: "Porta serial não encontrada"

**Problema:** Python não consegue conectar ao ESP32

**Soluções:**

**Windows:**
```powershell
# Verificar porta no Gerenciador de Dispositivos
# Dispositivos > Portas (COM & LPT)
# Procure por "Silicon Labs CP210x" ou "CH340"
```

**Wokwi Simulator:**
- Certifique-se que a simulação está rodando
- Use porta virtual RFC2217 (porta pode variar)

### 6.2 Erro: "ModuleNotFoundError: No module named 'serial'"

**Problema:** PySerial não instalado

**Solução:**
```powershell
pip install pyserial

# Ou com Python específico
python -m pip install pyserial
```

### 6.3 Dados JSON não aparecem

**Problema:** Comando GET_SENSORS não retorna JSON

**Soluções:**
1. Aguarde 2-3 segundos após enviar comando
2. Verifique se simulação Wokwi está rodando
3. Reinicie o simulador Wokwi
4. Verifique bibliotecas no código Arduino (DHT, ArduinoJson)

### 6.4 Relé não responde

**Problema:** Comando SET_RELAY não funciona

**Verificações:**
1. Conexão do pino D18 no diagram.json
2. Estado do LED azul no relé
3. Mensagem de confirmação no Serial Monitor
4. Código do `processSerialCommand()` no .ino

### 6.5 Wokwi não inicia

**Problema:** Simulação não carrega

**Soluções:**
1. Reinstale a extensão Wokwi
2. Verifique arquivo `diagram.json`
3. Certifique-se que o arquivo `.ino` está na mesma pasta
4. Atualize VS Code para última versão

### 6.6 Bibliotecas não encontradas

**Problema:** Erro de compilação com DHT ou ArduinoJson

**Solução via Wokwi:**
1. Crie arquivo `libraries.txt` na mesma pasta do `.ino`
2. Adicione:
```
DHT sensor library
ArduinoJson
```
3. Reinicie simulação

**Solução Arduino IDE:**
```
Sketch > Incluir Biblioteca > Gerenciar Bibliotecas
Instale:
- DHT sensor library (Adafruit)
- ArduinoJson (Benoit Blanchon)
```

---

## 7. Integração com Sistema Web Flask

### 7.1 Fluxo de Dados

```
┌─────────────┐      Serial/USB      ┌──────────┐
│   ESP32     │ ◄──────────────────► │  Python  │
│  (Wokwi)    │                      │  Script  │
└─────────────┘                      └──────────┘
                                           │
                                           │ HTTP
                                           ▼
                                    ┌──────────────┐
                                    │  Flask Web   │
                                    │  Application │
                                    └──────────────┘
```

### 7.2 Próximos Passos

Para integrar com a aplicação Flask web (`fase2/web_app/app.py`):

1. **Modificar `esp32_communication.py`** para exportar dados
2. **Criar endpoint** em Flask para receber dados do ESP32
3. **Atualizar dashboard** com dados reais do hardware
4. **Implementar WebSocket** para atualização em tempo real

---

## 8. Referências

### 8.1 Documentação Oficial

- **Wokwi:** https://docs.wokwi.com/
- **ESP32:** https://docs.espressif.com/
- **PySerial:** https://pyserial.readthedocs.io/
- **ArduinoJson:** https://arduinojson.org/

### 8.2 Requisitos do Projeto

Conforme **Atividade - Cap 1 - Um Mapa do Tesouro**:

✅ **Obrigatórios:**
- [x] Código C/C++ ESP32 (`.ino`)
- [x] Simulação Wokwi com sensores NPK, LDR, DHT22, Relé
- [x] Comunicação serial funcional
- [x] Lógica de decisão de irrigação

✅ **Opcional 1 (IR ALÉM):**
- [x] Integração Python com ESP32
- [x] Transferência de dados bidirecional
- [x] Script de comunicação serial

---

## 9. Checklist de Entrega

### 9.1 Arquivos para Entrega FIAP

- [ ] `farm_irrigation_system.ino` - Código ESP32
- [ ] `diagram.json` - Diagrama Wokwi
- [ ] `wokwi.toml` - Configuração
- [ ] `esp32_communication.py` - Script Python
- [ ] `README.md` - Documentação completa
- [ ] Screenshots do circuito funcionando
- [ ] Vídeo demonstrativo (YouTube, até 5min)
- [ ] Link do repositório GitHub

### 9.2 Demonstração no Vídeo

Incluir no vídeo (até 5 minutos):

1. ✅ Apresentação do circuito Wokwi
2. ✅ Explicação dos sensores e conexões
3. ✅ Demonstração dos botões NPK
4. ✅ Ajuste do LDR (pH)
5. ✅ Acionamento da bomba (manual e automático)
6. ✅ Comunicação Python-ESP32
7. ✅ Leitura de dados JSON
8. ✅ Controle via comandos seriais

---

## 📝 Observações Finais

> **⚠️ IMPORTANTE:** Não altere o repositório GitHub após a data de entrega. Alterações após prazo resultam em desconto na nota.

> **💡 DICA:** Documente todo o processo de desenvolvimento, incluindo decisões técnicas e desafios encontrados.

> **🏆 IR ALÉM:** Implementação da comunicação Python-ESP32 é atividade opcional que demonstra conhecimento avançado em IoT.

---

**FarmTech Solutions** | FIAP 2025 | Tecnologia em IA e Robótica
