# Integração ESP32 (Cap 1) ↔ Python (Cap 6)

## 🔗 Arquitetura de Comunicação

```
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA FÍSICA (Cap 1)                     │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  NPK     │  │   LDR    │  │  DHT22   │  │  Relay   │   │
│  │ Buttons  │  │  (pH)    │  │ (Temp/   │  │ (Bomba)  │   │
│  │ GPIO 2,4,5│  │ GPIO 34  │  │ Umid)    │  │ GPIO 18  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       └────────────┬┴────────────┬┴─────────────┘          │
│                    │ESP32 DevKit v1│                        │
│                    │  FarmTech.ino │                        │
│                    └──────┬────────┘                        │
└───────────────────────────┼─────────────────────────────────┘
                            │ Serial USB (115200 baud)
                            │ JSON Format
┌───────────────────────────┼─────────────────────────────────┐
│                    CAMADA SOFTWARE (Cap 6)                   │
├───────────────────────────┴─────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────┐  │
│  │          Python Serial Reader (PySerial)              │  │
│  │  • Lê dados do ESP32 via COM/ttyUSB                   │  │
│  │  • Parse JSON: {'temp': 26.5, 'umid': 40, 'ph': 6.2} │  │
│  └──────────────────────┬────────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────┴───────────────────────────────┐   │
│  │       SensorMonitor.adicionar_leitura()              │   │
│  │  • Valida dados (ranges, tipos)                      │   │
│  │  • Converte umidade ar → solo (×0.8)                 │   │
│  │  • Armazena em JSON/Oracle                           │   │
│  └──────────────────────┬────────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────┴───────────────────────────────┐   │
│  │     IrrigacaoController.decidir_irrigacao()          │   │
│  │  • Aplica 6 condições de decisão                     │   │
│  │  • Registra histórico                                │   │
│  └──────────────────────┬────────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────┴───────────────────────────────┐   │
│  │         Python Serial Writer (PySerial)              │   │
│  │  • Envia comando para ESP32: {"relay": 1} ou 0      │   │
│  └──────────────────────┬────────────────────────────────┘  │
└───────────────────────────┼─────────────────────────────────┘
                            │ Serial USB
                            ▼
                  ┌─────────────────┐
                  │ ESP32 executa   │
                  │ digitalWrite()  │
                  └─────────────────┘
```

---

## 📡 Protocolo de Comunicação Serial

### Formato de Dados: JSON

#### ESP32 → Python (Leitura de Sensores)

**Estrutura**:
```json
{
  "cultivo_id": 1,
  "timestamp": "2025-10-11T14:30:00",
  "temperatura": 26.5,
  "umidade_ar": 50.0,
  "umidade_solo": 40.0,
  "ph": 6.2,
  "npk": {
    "N": true,
    "P": true,
    "K": false
  },
  "relay_status": false
}
```

**Código ESP32** (FarmTech.ino):
```cpp
void enviarDadosSerial() {
    Serial.print("{");
    Serial.print("\"cultivo_id\":");
    Serial.print(cultivo_id);
    Serial.print(",\"timestamp\":\"");
    Serial.print(obterTimestamp());
    Serial.print("\",\"temperatura\":");
    Serial.print(temperaturaAr, 1);
    Serial.print(",\"umidade_ar\":");
    Serial.print(umidadeAr, 1);
    Serial.print(",\"umidade_solo\":");
    Serial.print(umidadeSolo, 1);
    Serial.print(",\"ph\":");
    Serial.print(phSolo, 1);
    Serial.print(",\"npk\":{\"N\":");
    Serial.print(nitrogenioOK ? "true" : "false");
    Serial.print(",\"P\":");
    Serial.print(fosforoOK ? "true" : "false");
    Serial.print(",\"K\":");
    Serial.print(potassioOK ? "true" : "false");
    Serial.print("},\"relay_status\":");
    Serial.print(releLigado ? "true" : "false");
    Serial.println("}");
}
```

#### Python → ESP32 (Comando de Irrigação)

**Estrutura**:
```json
{
  "command": "SET_RELAY",
  "value": 1
}
```

**Código Python**:
```python
import serial
import json

ser = serial.Serial('COM3', 115200, timeout=1)  # Ajuste porta

comando = {"command": "SET_RELAY", "value": 1}
ser.write((json.dumps(comando) + '\n').encode())
```

**Código ESP32** (recepção):
```cpp
void loop() {
    if (Serial.available() > 0) {
        String comando = Serial.readStringUntil('\n');
        processarComando(comando);
    }
}

void processarComando(String json) {
    // Parse JSON (use biblioteca ArduinoJson)
    StaticJsonDocument<200> doc;
    deserializeJson(doc, json);
    
    if (doc["command"] == "SET_RELAY") {
        int valor = doc["value"];
        digitalWrite(RELE_PIN, valor == 1 ? HIGH : LOW);
        releLigado = (valor == 1);
    }
}
```

---

## 🐍 Script Python de Integração

### serial_reader.py (Recebe dados do ESP32)

```python
"""
Script de leitura contínua do ESP32 via Serial
Integra com FarmTech Solutions (Cap 6)
"""

import serial
import json
import time
from datetime import datetime
from sensor_monitor import SensorMonitor
from irrigacao_controller import IrrigacaoController
from cultivo_manager import CultivoManager

class ESP32Reader:
    """Leitor de dados do ESP32 via Serial"""
    
    def __init__(self, porta='COM3', baud=115200):
        """
        Inicializa conexão serial
        
        Args:
            porta (str): Porta COM (Windows) ou /dev/ttyUSB0 (Linux)
            baud (int): Baud rate (deve ser 115200)
        """
        self.porta = porta
        self.baud = baud
        self.serial = None
        self.sensor_mon = SensorMonitor()
        self.irrigacao_ctrl = IrrigacaoController()
        self.cultivo_mgr = CultivoManager()
        
        # Carrega dados existentes
        self.sensor_mon.carregar_json()
        self.irrigacao_ctrl.carregar_json()
        self.cultivo_mgr.carregar_json()
    
    def conectar(self):
        """Estabelece conexão serial"""
        try:
            self.serial = serial.Serial(self.porta, self.baud, timeout=1)
            print(f"✅ Conectado à porta {self.porta} (baud {self.baud})")
            time.sleep(2)  # Aguarda reset do Arduino
            return True
        except serial.SerialException as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def desconectar(self):
        """Fecha conexão serial"""
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("🔌 Desconectado")
    
    def ler_linha(self):
        """
        Lê uma linha da serial (JSON)
        
        Returns:
            dict: Dados parseados ou None se erro
        """
        if not self.serial or not self.serial.is_open:
            return None
        
        try:
            linha = self.serial.readline().decode('utf-8').strip()
            
            # Ignora linhas vazias ou que não começam com {
            if not linha or not linha.startswith('{'):
                return None
            
            # Parse JSON
            dados = json.loads(linha)
            return dados
            
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            print(f"⚠️  Erro ao parsear linha: {e}")
            return None
    
    def processar_dados(self, dados):
        """
        Processa dados recebidos do ESP32
        
        Args:
            dados (dict): Dados JSON do ESP32
        """
        try:
            cultivo_id = dados.get('cultivo_id', 1)
            
            # Busca cultivo
            cultivo = self.cultivo_mgr.obter_cultivo(cultivo_id)
            if not cultivo:
                print(f"⚠️  Cultivo {cultivo_id} não encontrado")
                return
            
            # Registra leitura
            npk_ok = dados.get('npk', {'N': True, 'P': True, 'K': True})
            
            leitura_id = self.sensor_mon.adicionar_leitura(
                cultivo_id=cultivo_id,
                temperatura=dados['temperatura'],
                umidade_ar=dados['umidade_ar'],
                ph=dados['ph'],
                npk_ok=npk_ok
            )
            
            print(f"📊 Leitura {leitura_id} registrada:")
            print(f"   Temp: {dados['temperatura']}°C")
            print(f"   Umidade solo: {dados['umidade_ar'] * 0.8:.1f}%")
            print(f"   pH: {dados['ph']}")
            print(f"   NPK: N={'✅' if npk_ok['N'] else '❌'} "
                  f"P={'✅' if npk_ok['P'] else '❌'} "
                  f"K={'✅' if npk_ok['K'] else '❌'}")
            
            # Decide irrigação
            leitura = self.sensor_mon.obter_leitura(leitura_id)
            resultado = self.irrigacao_ctrl.decidir_irrigacao(cultivo, leitura)
            
            if resultado['deve_irrigar']:
                print(f"💧💧💧 IRRIGAÇÃO NECESSÁRIA: {resultado['motivo']}")
                self.enviar_comando_relay(1)
            else:
                print(f"⏸️⏸️⏸️ IRRIGAÇÃO DESNECESSÁRIA: {resultado['motivo']}")
                self.enviar_comando_relay(0)
            
            # Registra decisão
            self.irrigacao_ctrl.registrar_irrigacao(
                cultivo_id=cultivo_id,
                leitura_id=leitura_id,
                acionado=resultado['deve_irrigar'],
                motivo=resultado['motivo']
            )
            
            print("─" * 60)
            
        except Exception as e:
            print(f"❌ Erro ao processar dados: {e}")
    
    def enviar_comando_relay(self, valor):
        """
        Envia comando para ligar/desligar relay
        
        Args:
            valor (int): 1 = ligar, 0 = desligar
        """
        if not self.serial or not self.serial.is_open:
            return
        
        comando = {"command": "SET_RELAY", "value": valor}
        self.serial.write((json.dumps(comando) + '\n').encode())
        print(f"📤 Comando enviado: {'LIGAR' if valor else 'DESLIGAR'} relay")
    
    def executar_loop(self):
        """Loop principal de leitura"""
        print("\n🌾 FarmTech ESP32 Reader iniciado")
        print("   Pressione Ctrl+C para parar\n")
        
        try:
            while True:
                dados = self.ler_linha()
                
                if dados:
                    self.processar_dados(dados)
                
                time.sleep(0.1)  # 100ms entre leituras
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupção detectada. Salvando dados...")
            self.sensor_mon.salvar_json()
            self.irrigacao_ctrl.salvar_json()
            print("✅ Dados salvos. Encerrando...")


def main():
    """Função principal"""
    # Ajuste a porta conforme seu sistema
    # Windows: COM3, COM4, etc.
    # Linux/Mac: /dev/ttyUSB0, /dev/tty.usbserial, etc.
    
    reader = ESP32Reader(porta='COM3', baud=115200)
    
    if reader.conectar():
        reader.executar_loop()
    
    reader.desconectar()


if __name__ == "__main__":
    main()
```

---

## 🔧 Configuração do Ambiente

### 1. Instalar PySerial

```bash
pip install pyserial
```

### 2. Identificar Porta Serial

**Windows**:
```powershell
# Gerenciador de Dispositivos → Portas (COM e LPT)
# Anote a porta (ex: COM3)
```

**Linux**:
```bash
ls /dev/ttyUSB*
# ou
ls /dev/ttyACM*
```

**Mac**:
```bash
ls /dev/tty.usbserial*
```

### 3. Testar Comunicação

```python
import serial
import time

# Substitua 'COM3' pela sua porta
ser = serial.Serial('COM3', 115200, timeout=1)
time.sleep(2)

print("Lendo 10 linhas...")
for i in range(10):
    linha = ser.readline().decode('utf-8').strip()
    print(linha)

ser.close()
```

---

## 📊 Fluxo de Dados Completo

### Passo a Passo

1. **ESP32 lê sensores** a cada 5 segundos
   - NPK: digitalRead(GPIO 2, 4, 5)
   - pH: analogRead(GPIO 34) convertido
   - Temp/Umid: dht.readTemperature(), dht.readHumidity()

2. **ESP32 envia JSON** via Serial USB (115200 baud)
   ```
   {"cultivo_id":1,"temperatura":26.5,"umidade_ar":50.0,...}
   ```

3. **Python lê Serial** com PySerial
   ```python
   dados = json.loads(serial.readline())
   ```

4. **Python registra leitura** no SensorMonitor
   ```python
   leitura_id = sensor_mon.adicionar_leitura(...)
   ```

5. **Python decide irrigação** com IrrigacaoController
   ```python
   resultado = irrigacao_ctrl.decidir_irrigacao(cultivo, leitura)
   ```

6. **Python envia comando** de volta ao ESP32
   ```python
   serial.write('{"command":"SET_RELAY","value":1}\n')
   ```

7. **ESP32 aciona relay** (GPIO 18)
   ```cpp
   digitalWrite(RELE_PIN, HIGH);
   ```

---

## 🔄 Sincronização Bidirecional

### Python → ESP32 (Comandos)

| Comando | JSON | Ação ESP32 |
|---------|------|------------|
| Ligar relay | `{"command":"SET_RELAY","value":1}` | digitalWrite(18, HIGH) |
| Desligar relay | `{"command":"SET_RELAY","value":0}` | digitalWrite(18, LOW) |
| Forçar leitura | `{"command":"READ_SENSORS"}` | lerSensores() imediato |
| Mudar cultivo | `{"command":"SET_CULTIVO","value":2}` | cultivo_id = 2 |

### ESP32 → Python (Dados)

| Tipo | Frequência | Conteúdo |
|------|------------|----------|
| Leitura sensores | 5s | JSON completo com todos sensores |
| Mudança relay | Instantâneo | Status on/off |
| Erro | Sob demanda | Mensagens de erro |

---

## ⚠️ Tratamento de Erros

### Python

```python
try:
    dados = json.loads(linha)
except json.JSONDecodeError:
    print("JSON inválido, ignorando linha")
    return

try:
    leitura_id = sensor_mon.adicionar_leitura(...)
except ValueError as e:
    print(f"Validação falhou: {e}")
    return
```

### ESP32

```cpp
if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    
    if (cmd.length() > 0 && cmd.startsWith("{")) {
        processarComando(cmd);
    }
}
```

---

## 🎯 Exemplos de Uso

### Monitoramento Contínuo

```bash
# Terminal 1: Executa ESP32 Reader
python serial_reader.py

# Terminal 2: Monitora logs em tempo real
tail -f logs/operacoes.log
```

### Teste Manual de Relay

```python
import serial
import json
import time

ser = serial.Serial('COM3', 115200)
time.sleep(2)

# Liga relay
ser.write(b'{"command":"SET_RELAY","value":1}\n')
time.sleep(5)

# Desliga relay
ser.write(b'{"command":"SET_RELAY","value":0}\n')

ser.close()
```

---

*Atualizado: Outubro 2025*  
*FarmTech Solutions - Grupo 59 FIAP*
