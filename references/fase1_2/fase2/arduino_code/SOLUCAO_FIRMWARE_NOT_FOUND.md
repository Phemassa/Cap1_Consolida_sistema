# 🚨 SOLUÇÃO: firmware.bin not found

## Erro Específico:
```
Wokwi: firmware binary .pio/build/esp32/firmware.bin not found in workspace
```

---

## ✅ SOLUÇÃO RÁPIDA (3 Passos)

### 1️⃣ Deletar ou Renomear `wokwi.toml`

O problema é que o `wokwi.toml` está pedindo um arquivo binário que não existe.

**Execute no PowerShell:**
```powershell
cd "c:\Fiap Projeto\FarmTechSolutions\fase2\arduino_code"
mv wokwi.toml wokwi.toml.backup
```

Ou simplesmente delete o arquivo `wokwi.toml`.

### 2️⃣ O Wokwi usará compilação automática

Sem o `wokwi.toml`, o Wokwi:
- Detecta automaticamente o código `.ino`
- Compila internamente
- Usa o `diagram.json` para o circuito

### 3️⃣ Iniciar Simulação

1. Abra `farm_irrigation_system.ino`
2. `F1` → `Wokwi: Start Simulator`
3. Aguarde 20-30 segundos (primeira compilação)
4. ✅ Funcionando!

---

## 📋 Arquivos Necessários (Mínimo)

Para o Wokwi funcionar, você precisa apenas:

```
arduino_code/
├── farm_irrigation_system.ino  ✅ Código principal
├── diagram.json                 ✅ Circuito
└── libraries.txt               ✅ Bibliotecas (opcional)
```

**NÃO precisa:**
- ❌ wokwi.toml (causa o erro se configurado errado)
- ❌ firmware.bin (compilado automaticamente)
- ❌ firmware.elf (compilado automaticamente)
- ❌ .pio/ (pasta do PlatformIO)

---

## 🔧 Alternativa: Configurar wokwi.toml Corretamente

Se quiser manter o `wokwi.toml`, deixe vazio ou minimalista:

```toml
[wokwi]
version = 1
```

**Ou simplesmente delete o arquivo!**

---

## 🎯 Teste Agora

### Execute estes comandos:

```powershell
# 1. Ir para pasta do código
cd "c:\Fiap Projeto\FarmTechSolutions\fase2\arduino_code"

# 2. Remover wokwi.toml problemático
Remove-Item wokwi.toml

# 3. Abrir VS Code
code farm_irrigation_system.ino
```

### Depois no VS Code:

1. `F1`
2. Digite: `Wokwi: Start Simulator`
3. Aguarde
4. ✅ Deve funcionar!

---

## 📊 Verificação Final

### Antes de iniciar, confirme:

- [x] ✅ Extensão Wokwi instalada
- [x] ✅ Arquivo `farm_irrigation_system.ino` existe
- [x] ✅ Arquivo `diagram.json` existe
- [x] ❌ Arquivo `wokwi.toml` **NÃO existe** (ou está vazio)

---

## 🆘 Se Ainda Não Funcionar

### Opção 1: Usar online
1. Vá para https://wokwi.com/
2. New Project → ESP32
3. Cole o código do .ino
4. Cole o diagram.json

### Opção 2: Recriar diagram.json simples

Crie um diagram.json básico:

```json
{
  "version": 1,
  "author": "FarmTech Solutions",
  "editor": "wokwi",
  "parts": [
    { "type": "wokwi-esp32-devkit-v1", "id": "esp", "top": 0, "left": 0, "attrs": {} }
  ],
  "connections": [
    [ "esp:TX0", "$serialMonitor:RX", "", [] ],
    [ "esp:RX0", "$serialMonitor:TX", "", [] ]
  ]
}
```

---

## ✅ Resumo da Solução

### O Problema:
- `wokwi.toml` estava configurado para usar binário pré-compilado
- Binário não existe
- Wokwi não consegue iniciar

### A Solução:
- **Remover `wokwi.toml`**
- Deixar Wokwi compilar automaticamente
- Mais simples e funciona melhor

---

## 🚀 Execute Agora!

```powershell
cd "c:\Fiap Projeto\FarmTechSolutions\fase2\arduino_code"
Remove-Item wokwi.toml -ErrorAction SilentlyContinue
code .
```

Depois no VS Code:
- Abrir `farm_irrigation_system.ino`
- `F1` → `Wokwi: Start Simulator`

**Pronto! 🎉**
