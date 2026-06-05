# 🔧 Guia Rápido - Iniciar Wokwi no VS Code

## FarmTech Solutions - Fase 2

---

## ⚡ Método 1: Simulação Direta (RECOMENDADO - Mais Fácil)

### Passo a Passo:

1. **Abra o arquivo principal:**
   - `farm_irrigation_system.ino`

2. **Inicie o simulador:**
   - Pressione `F1`
   - Digite: `Wokwi: Start Simulator`
   - Ou clique no ícone ▶️ verde "Start Simulation"

3. **Pronto!**
   - O Wokwi compilará automaticamente
   - Aguarde 10-30 segundos na primeira vez
   - Circuito aparecerá na tela

### ✅ Vantagens:
- Mais simples
- Não precisa PlatformIO
- Compilação automática

---

## ⚙️ Método 2: Com PlatformIO (Avançado)

### Quando usar:
- Quer compilar manualmente
- Precisa do arquivo .bin
- Desenvolvimento mais avançado

### Passo a Passo:

1. **Instalar PlatformIO:**
   ```powershell
   pip install platformio
   ```

2. **Compilar o projeto:**
   ```powershell
   cd "c:\Fiap Projeto\FarmTechSolutions\fase2\arduino_code"
   pio run
   ```

3. **Arquivos gerados em:**
   ```
   .pio/build/esp32/
   ├── firmware.bin  ← Binário compilado
   └── firmware.elf  ← Debug info
   ```

4. **Atualizar wokwi.toml:**
   ```toml
   [wokwi]
   version = 1
   firmware = ".pio/build/esp32/firmware.bin"
   elf = ".pio/build/esp32/firmware.elf"
   ```

5. **Iniciar Wokwi:**
   - `F1` → `Wokwi: Start Simulator`

---

## 🐛 Resolução de Problemas

### Erro: "firmware.bin not found"

**Solução 1 - Usar compilação automática:**
```toml
# wokwi.toml
[wokwi]
version = 1
# Sem firmware/elf = compilação automática
```

**Solução 2 - Compilar com PlatformIO:**
```powershell
cd fase2/arduino_code
pio run
```

### Erro: "Library not found"

**Criar/verificar libraries.txt:**
```
DHT sensor library
ArduinoJson
```

### Erro: "diagram.json not found"

**Verificar arquivo:**
- Deve estar na mesma pasta do .ino
- Nome: `diagram.json`

---

## 📋 Checklist Antes de Iniciar

- [ ] ✅ Extensão "Wokwi Embedded Simulator" instalada
- [ ] ✅ Arquivo `farm_irrigation_system.ino` aberto
- [ ] ✅ Arquivo `diagram.json` na mesma pasta
- [ ] ✅ Arquivo `wokwi.toml` configurado
- [ ] ✅ Arquivo `libraries.txt` presente

---

## 🎯 Estado Atual do Projeto

### Arquivos na Pasta `arduino_code/`:
```
✅ farm_irrigation_system.ino  ← Código principal
✅ diagram.json                 ← Circuito
✅ wokwi.toml                   ← Configuração
✅ libraries.txt                ← Bibliotecas
✅ platformio.ini               ← Config PlatformIO (opcional)
```

### Configuração Atual (wokwi.toml):
```toml
[wokwi]
version = 1
# Compilação automática ativada
```

---

## 🚀 INICIAR AGORA (Método Simples)

### Comando Rápido:

1. Abra VS Code na pasta do projeto
2. Abra `farm_irrigation_system.ino`
3. Pressione `F1`
4. Digite `Wokwi: Start Simulator`
5. Aguarde compilação (primeira vez demora mais)
6. ✅ Pronto!

---

## 🔍 Verificar se Está Funcionando

### Após iniciar, você deve ver:

1. **Janela do Simulador** com:
   - ESP32 board
   - 3 botões verdes (NPK)
   - Sensor LDR
   - Sensor DHT22
   - Relé azul
   - LED de status

2. **Serial Monitor** mostrando:
   ```
   ========================================
   Sistema de Irrigação Inteligente
   FarmTech Solutions - Fase 2
   ESP32 Wokwi - Pronto para operar
   ========================================
   ```

---

## 📞 Se Nada Funcionar

### Última alternativa - Reinstalar:

1. **Desinstalar extensão Wokwi:**
   - Extensions → Wokwi → Uninstall

2. **Reiniciar VS Code**

3. **Reinstalar extensão:**
   - Extensions → Buscar "Wokwi"
   - Install

4. **Tentar novamente:**
   - Abrir .ino
   - F1 → Wokwi: Start Simulator

---

## ✅ Está Tudo Configurado!

Seu projeto está **pronto para simular**! 

Execute:
```
F1 → Wokwi: Start Simulator
```

**Boa sorte! 🚀**
