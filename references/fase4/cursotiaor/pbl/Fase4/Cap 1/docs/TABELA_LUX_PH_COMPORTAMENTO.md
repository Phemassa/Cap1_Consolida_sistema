# 📊 Tabela LUX → pH → Comportamento do Sistema

## 🎯 Como o LDR (Luminosidade) Afeta o Sistema Completo

Este documento explica **EXATAMENTE** como o ajuste do LDR no Wokwi afeta o pH e o comportamento da irrigação.

---

## 📐 **Fórmulas Utilizadas**

### 1. ADC → LUX (Display)
```cpp
ldrLux = (ldrValue / 4095.0) * 10000.0
```
- **Propósito**: Mostrar valor aproximado em LUX no Serial Monitor
- **Não afeta lógica**: Apenas visual/informativo

### 2. ADC → pH (Lógica Principal)
```cpp
phSolo = 9.0 - (ldrValue / 4095.0) * 6.0
```
- **Propósito**: Converter luminosidade em pH do solo (simulação)
- **Afeta lógica**: Sistema decide irrigação baseado neste valor

---

## 📋 **Tabela Completa de Comportamento**

### **Cenário 1: 100000 lux (Muito Claro - Máximo)**

| Parâmetro | Valor | Explicação |
|-----------|-------|------------|
| **🔆 LUX no Wokwi** | 100000 lux | Slider do LDR no máximo |
| **📈 ADC Value** | ~4095 | ESP32 ADC 12-bit (máximo) |
| **💡 LUX Calculado** | ~10000 lux | Display informativo |
| **🧪 pH Calculado** | **3.0** | pH = 9.0 - (4095/4095) * 6.0 = 3.0 |
| **📋 Status pH** | 🟥 **ÁCIDO** (< 5.5) | Muito abaixo do ideal |
| **💡 Recomendação** | Aplicar Fósforo (P) e Potássio (K) | Corrigir acidez |
| **💧 Irrigação?** | **LIGA** (se umidade < 60%) | Condição 4 ativada |

**Serial Monitor:**
```
📊 [SENSOR LDR/pH]
   💡 Luminosidade: 10000 lux
   📈 ADC Value: 4095 / 4095 (100.0%)
   🧪 pH Calculado: 3.0 → 🟥 ÁCIDO

🧪 pH do Solo:
   💡 Luminosidade: 10000 lux
   📊 LDR Value: 4095 → pH 3.0
   📋 Status: 🟥 ÁCIDO (< 5.5)
   💡 Recomendação: Aplicar Fósforo (P) e Potássio (K)

💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧
  🚨 IRRIGAÇÃO LIGADA!
💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧
  📌 Motivo: pH fora da faixa (3.0) + umidade baixa
💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧
```

---

### **Cenário 2: 500 lux (Médio - IDEAL)**

| Parâmetro | Valor | Explicação |
|-----------|-------|------------|
| **🔆 LUX no Wokwi** | 500 lux | Slider do LDR posição média |
| **📈 ADC Value** | ~1527 | ~37% do range ADC |
| **💡 LUX Calculado** | ~3730 lux | Display informativo |
| **🧪 pH Calculado** | **6.8** | pH = 9.0 - (1527/4095) * 6.0 ≈ 6.8 |
| **📋 Status pH** | 🟩 **NEUTRO** (5.5-7.5) | Faixa ideal! |
| **💡 Recomendação** | Nenhuma | pH adequado |
| **💧 Irrigação?** | **DESLIGA** (se estava ligada) | Condições adequadas |

**Serial Monitor:**
```
📊 [SENSOR LDR/pH]
   💡 Luminosidade: 3730 lux
   📈 ADC Value: 1527 / 4095 (37.3%)
   🧪 pH Calculado: 6.8 → 🟩 NEUTRO (IDEAL)

🧪 pH do Solo:
   💡 Luminosidade: 3730 lux
   📊 LDR Value: 1527 → pH 6.8
   📋 Status: 🟩 NEUTRO (5.5-7.5) - IDEAL

⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️
  ✅ IRRIGAÇÃO DESLIGADA
⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️
  📌 Motivo: Condições adequadas (umidade: 48.0%)
⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️
```

---

### **Cenário 3: 10 lux (Muito Escuro - Mínimo)**

| Parâmetro | Valor | Explicação |
|-----------|-------|------------|
| **🔆 LUX no Wokwi** | 10 lux | Slider do LDR no mínimo |
| **📈 ADC Value** | ~50 | ~1% do range ADC |
| **💡 LUX Calculado** | ~122 lux | Display informativo |
| **🧪 pH Calculado** | **8.9** | pH = 9.0 - (50/4095) * 6.0 ≈ 8.9 |
| **📋 Status pH** | 🟦 **ALCALINO** (> 7.5) | Muito acima do ideal |
| **💡 Recomendação** | Aplicar Nitrogênio (N) | Corrigir alcalinidade |
| **💧 Irrigação?** | **LIGA** (se umidade < 60%) | Condição 4 ativada |

**Serial Monitor:**
```
📊 [SENSOR LDR/pH]
   💡 Luminosidade: 122 lux
   📈 ADC Value: 50 / 4095 (1.2%)
   🧪 pH Calculado: 8.9 → 🟦 ALCALINO

🧪 pH do Solo:
   💡 Luminosidade: 122 lux
   📊 LDR Value: 50 → pH 8.9
   📋 Status: 🟦 ALCALINO (> 7.5)
   💡 Recomendação: Aplicar Nitrogênio (N)

💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧
  🚨 IRRIGAÇÃO LIGADA!
💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧
  📌 Motivo: pH fora da faixa (8.9) + umidade baixa
💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧
```

---

### **Cenário 4: 2000 lux (Claro)**

| Parâmetro | Valor | Explicação |
|-----------|-------|------------|
| **🔆 LUX no Wokwi** | 2000 lux | Slider do LDR alto |
| **📈 ADC Value** | ~3200 | ~78% do range ADC |
| **💡 LUX Calculado** | ~7814 lux | Display informativo |
| **🧪 pH Calculado** | **4.3** | pH = 9.0 - (3200/4095) * 6.0 ≈ 4.3 |
| **📋 Status pH** | 🟥 **ÁCIDO** (< 5.5) | Abaixo do ideal |
| **💡 Recomendação** | Aplicar Fósforo (P) e Potássio (K) | Corrigir acidez |
| **💧 Irrigação?** | **LIGA** (se umidade < 60%) | Condição 4 ativada |

---

### **Cenário 5: 200 lux (Escuro)**

| Parâmetro | Valor | Explicação |
|-----------|-------|------------|
| **🔆 LUX no Wokwi** | 200 lux | Slider do LDR baixo |
| **📈 ADC Value** | ~400 | ~10% do range ADC |
| **💡 LUX Calculado** | ~977 lux | Display informativo |
| **🧪 pH Calculado** | **8.4** | pH = 9.0 - (400/4095) * 6.0 ≈ 8.4 |
| **📋 Status pH** | 🟦 **ALCALINO** (> 7.5) | Acima do ideal |
| **💡 Recomendação** | Aplicar Nitrogênio (N) | Corrigir alcalinidade |
| **💧 Irrigação?** | **LIGA** (se umidade < 60%) | Condição 4 ativada |

---

## 🎯 **Resumo Visual - Escala LUX → pH**

```
┌─────────────────────────────────────────────────────────────┐
│                    ESCALA LDR / pH                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  10 lux ──────────► ADC: 50 ──────► pH: 8.9 🟦 ALCALINO   │
│  200 lux ─────────► ADC: 400 ─────► pH: 8.4 🟦 ALCALINO   │
│  500 lux ─────────► ADC: 1527 ────► pH: 6.8 🟩 IDEAL ✅   │
│  2000 lux ────────► ADC: 3200 ────► pH: 4.3 🟥 ÁCIDO      │
│  100000 lux ──────► ADC: 4095 ────► pH: 3.0 🟥 ÁCIDO      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 **Lógica de Decisão da Irrigação**

### **Condição 4 (pH Inadequado):**
```cpp
if ((phSolo < PH_MINIMO || phSolo > PH_MAXIMO) && umidadeSolo < UMIDADE_IDEAL) {
    deveIrrigar = true;
    motivo = "pH fora da faixa (" + String(phSolo, 1) + ") + umidade baixa";
}
```

**Quando LIGA:**
- pH < 5.5 (ÁCIDO) **E** umidade < 60%
- pH > 7.5 (ALCALINO) **E** umidade < 60%

**Quando NÃO LIGA:**
- pH entre 5.5 e 7.5 (NEUTRO)
- Umidade ≥ 60% (mesmo com pH inadequado)

---

## 🧪 **Teste Prático no Wokwi**

### **Passo a Passo:**

1. **Inicie simulação** no Wokwi (▶️)

2. **Clique no LDR** (photoresistor)

3. **Configure 100000 lux:**
   - Arraste slider para direita (máximo)
   - Observe Serial Monitor

4. **Aguarde 5 segundos** (intervalo de leitura)

5. **Observe saída esperada:**
   ```
   📊 [SENSOR LDR/pH]
      💡 Luminosidade: 10000 lux
      📈 ADC Value: 4095 / 4095 (100.0%)
      🧪 pH Calculado: 3.0 → 🟥 ÁCIDO
   
   🧪 pH do Solo:
      💡 Luminosidade: 10000 lux
      📊 LDR Value: 4095 → pH 3.0
      📋 Status: 🟥 ÁCIDO (< 5.5)
   
   💧 IRRIGAÇÃO LIGADA! (se umidade < 60%)
   ```

6. **Ajuste para 500 lux:**
   - Arraste slider para posição média
   - Aguarde 5 segundos

7. **Observe mudança:**
   ```
   📊 [SENSOR LDR/pH]
      💡 Luminosidade: 3730 lux
      📈 ADC Value: 1527 / 4095 (37.3%)
      🧪 pH Calculado: 6.8 → 🟩 NEUTRO (IDEAL)
   
   🧪 pH do Solo:
      💡 Luminosidade: 3730 lux
      📊 LDR Value: 1527 → pH 6.8
      📋 Status: 🟩 NEUTRO (5.5-7.5) - IDEAL
   
   ⏸️ IRRIGAÇÃO DESLIGADA!
   ```

---

## 📊 **O Que Mudou no Código**

### **Adicionado:**
1. **Variável `ldrLux`**: Armazena valor calculado em LUX
2. **Display detalhado** na função `lerSensores()`:
   - Mostra luminosidade em lux
   - Mostra ADC value com percentual
   - Mostra pH calculado com classificação
3. **Display atualizado** na função `exibirStatus()`:
   - Inclui luminosidade antes do LDR value

### **Não Mudou:**
- Lógica de decisão de irrigação (continua igual)
- Fórmula de cálculo do pH (continua igual)
- Comportamento do sistema (continua igual)

---

## ✅ **Resumo Executivo**

| LUX Wokwi | ADC | pH | Status | Irrigação (se umid < 60%) |
|-----------|-----|-----|--------|---------------------------|
| 10 lux | 50 | 8.9 | 🟦 ALCALINO | ✅ LIGA |
| 200 lux | 400 | 8.4 | 🟦 ALCALINO | ✅ LIGA |
| **500 lux** | **1527** | **6.8** | **🟩 NEUTRO** | **❌ DESLIGA** |
| 2000 lux | 3200 | 4.3 | 🟥 ÁCIDO | ✅ LIGA |
| 100000 lux | 4095 | 3.0 | 🟥 ÁCIDO | ✅ LIGA |

**Faixa Ideal:** 400-800 lux → pH 6.0-7.5 → Irrigação desligada (se umidade OK)

---

**Última atualização:** 11/10/2025  
**Autor:** GitHub Copilot  
**Projeto:** FarmTech Solutions - Fase 2 Cap 1
