# 🔌 Integração Web App ↔ ESP32 (Wokwi)

## 📋 Visão Geral

Este sistema integra a aplicação web Flask com o simulador ESP32 no Wokwi através de comunicação serial, permitindo controle bidirecional dos fertilizantes NPK.

## 🎯 Funcionalidades

### 1. **Web → ESP32**
- Clicar botão NPK na web envia comando `TOGGLE_NPK:N/P/K` para ESP32
- ESP32 atualiza estado dos sensores
- Terminal Wokwi mostra mudança em tempo real

### 2. **ESP32 → Web** (futuro)
- Clicar botão no Wokwi atualiza estado na web
- Sincronização automática de status

## 🚀 Como Usar

### Passo 1: Preparar ESP32

1. **Compile o código atualizado:**
   ```powershell
   cd "c:\Fiap Projeto\FarmTechSolutions\fase2\arduino_code"
   python -m platformio run
   ```

2. **Inicie o Wokwi Simulator:**
   - Pressione F1 → "Wokwi: Start Simulator"
   - Aguarde ESP32 inicializar
   - Veja mensagens no "Wokwi Terminal"

3. **Identifique a porta COM:**
   - No Wokwi, vá em Settings
   - Procure "Serial Port" ou "COM Port"
   - Anote o número (ex: COM3, COM4)

### Passo 2: Configurar Python

1. **Instale PySerial:**
   ```powershell
   pip install pyserial
   ```

2. **Teste a conexão:**
   ```powershell
   cd "c:\Fiap Projeto\FarmTechSolutions\fase2\web_app"
   python esp32_serial_bridge.py
   ```

   **Saída esperada:**
   ```
   🔍 Procurando porta ESP32...
   ✅ Porta encontrada: COM3 - USB Serial Device
   ✅ Conectado ao ESP32 em COM3
   ```

### Passo 3: Iniciar Aplicação Web

1. **Inicie o Flask:**
   ```powershell
   cd "c:\Fiap Projeto\FarmTechSolutions\fase2\web_app"
   python app.py
   ```

   **Saída esperada:**
   ```
   ============================================================
   🌱 FarmTech Solutions - Sistema de Irrigação Inteligente
   ============================================================

   🔌 Tentando conectar ao ESP32...
   ✅ ESP32 conectado via serial!

   ✅ Servidor Flask iniciando...
   📡 Acesse: http://localhost:5000
   ============================================================
   ```

2. **Acesse o navegador:**
   - Abra http://localhost:5000
   - Vá para seção "Aplicação de Fertilizantes NPK"

### Passo 4: Testar Integração

1. **Clique no botão N (Nitrogênio) na web**

2. **No Wokwi Terminal você verá:**
   ```
   Comando recebido: TOGGLE_NPK:N
   ✅ TOGGLE N → High=1

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ⚡ SENSOR ALTERADO: NITROGÊNIO → High=1
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   --- Dados dos Sensores ---
   NPK: N=High=1 P=Low=0 K=Low=0
   LDR: 2187 (pH: 7.48)
   Temperatura: 36.3°C
   Umidade: 46.5%
   Bomba: DESLIGADA
   Cultura atual: Tomate
   --------------------------
   ```

3. **Na web aparecerá:**
   ```
   ✅ Nitrogênio (N) aplicado: 15 g
   ```

4. **Clique novamente para remover:**
   - Web: "❌ Nitrogênio (N) removido"
   - Wokwi: "TOGGLE N → Low=0"

## 📡 API Endpoints

### `/api/apply_fertilizer/<nutrient>`
- **Método:** POST
- **Parâmetros:** `nutrient` = nitrogen | phosphorus | potassium
- **Função:** Alterna estado NPK e envia comando para ESP32
- **Resposta:**
  ```json
  {
    "success": true,
    "nutrient": "nitrogen",
    "status": true,
    "message": "Nitrogênio (N) aplicado: 15 g",
    "calculation": {
      "amount": 15,
      "unit": "g",
      "area": 1000,
      "dosage_per_m2": 15,
      "message": "15 g para 1000m²"
    }
  }
  ```

### `/api/esp32/status`
- **Método:** GET
- **Função:** Retorna status da conexão ESP32
- **Resposta:**
  ```json
  {
    "connected": true,
    "port": "COM3",
    "available": true,
    "last_data": { ... }
  }
  ```

### `/api/esp32/reconnect`
- **Método:** POST
- **Função:** Tenta reconectar ao ESP32
- **Resposta:**
  ```json
  {
    "success": true,
    "connected": true,
    "message": "ESP32 conectado!"
  }
  ```

## 🔧 Comandos Serial Suportados

### Enviados pela Web App:

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `TOGGLE_NPK:N` | Alterna Nitrogênio | Web clica botão N |
| `TOGGLE_NPK:P` | Alterna Fósforo | Web clica botão P |
| `TOGGLE_NPK:K` | Alterna Potássio | Web clica botão K |
| `SET_NPK:1,0,1` | Define N=1, P=0, K=1 | Sincronização |
| `GET_STATUS` | Solicita status | Status check |
| `GET_SENSORS` | Solicita dados JSON | Leitura completa |

### Enviados pelo ESP32:

| Resposta | Formato | Quando |
|----------|---------|--------|
| Status NPK | `N=High=1 P=Low=0 K=Low=0` | Após TOGGLE |
| Dados Sensores | JSON completo | Após GET_SENSORS |
| Confirmação | `✅ TOGGLE N → High=1` | Após comando |

## 🐛 Troubleshooting

### ❌ "ESP32 não conectado - rodando em modo simulação"

**Causas possíveis:**
1. Wokwi Simulator não está rodando
2. Porta COM incorreta
3. PySerial não instalado

**Soluções:**
```powershell
# 1. Verificar PySerial
pip install pyserial

# 2. Listar portas disponíveis
python -c "import serial.tools.list_ports; print([p.device for p in serial.tools.list_ports.comports()])"

# 3. Testar conexão manual
python esp32_serial_bridge.py
```

### ❌ "Permissão negada na porta COM"

**Solução:** Feche outros programas usando a porta (Arduino IDE, PuTTY, etc.)

### ❌ "Botão na web não atualiza Wokwi"

**Verificações:**
1. Wokwi Terminal mostra "Comando recebido"?
   - ✅ Sim: ESP32 recebeu, verifique código
   - ❌ Não: Problema na comunicação serial

2. No terminal Flask aparece "Comando enviado"?
   - ✅ Sim: Serial enviou corretamente
   - ❌ Não: ESP32 não conectado

## 📊 Fluxo de Dados

```
┌─────────────────┐         Serial         ┌──────────────┐
│   Web Browser   │◄────────(USB)──────────►│   ESP32      │
│  (localhost)    │                         │   (Wokwi)    │
└────────┬────────┘                         └──────┬───────┘
         │                                         │
         │ HTTP POST                               │
         │ /api/apply_fertilizer/nitrogen          │
         │                                         │
         ▼                                         ▼
    ┌────────┐                              ┌──────────┐
    │ Flask  │──TOGGLE_NPK:N──Serial──────►│ Arduino  │
    │  App   │                              │   Code   │
    └────────┘                              └──────────┘
         │                                         │
         │                                         │
         │◄────────────JSON Response───────────────┤
         │         {npk: {N:1,P:0,K:0}}           │
         │                                         ▼
         │                                  ┌──────────────┐
         └─────►Atualiza Interface          │ Wokwi        │
                Web com novo estado         │ Terminal     │
                                            │ (Display)    │
                                            └──────────────┘
```

## 🎓 Próximos Passos

- [ ] Implementar ESP32 → Web (sincronização reversa)
- [ ] Adicionar WebSocket para updates em tempo real
- [ ] Criar dashboard de monitoramento ao vivo
- [ ] Histórico de aplicações NPK com timestamps
- [ ] Gráficos de variação de pH após aplicação

## 📝 Notas Técnicas

- **Baudrate:** 115200 (padrão ESP32)
- **Timeout:** 1 segundo
- **Thread de leitura:** Daemon (fecha com aplicação)
- **Formato comandos:** String ASCII + `\n`
- **Formato respostas:** JSON ou texto plano

---

✅ **Sistema funcionando!** Web e ESP32 agora conversam! 🚀
