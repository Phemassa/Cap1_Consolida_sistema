# 🧪 Dosagens de NPK por Cultura

## 📊 Tabela de Dosagens Recomendadas

### 🍌 Banana
| Nutriente | Dosagem | Observações |
|-----------|---------|-------------|
| **Nitrogênio (N)** | 15 g/m² | Essencial para crescimento vegetativo |
| **Fósforo (P)** | 10 g/m² | Importante para raízes e frutos |
| **Potássio (K)** | 20 g/m² | **CRÍTICO** - Banana precisa muito K para qualidade dos frutos |

**Justificativa Científica:**
- Banana é uma cultura **extremamente exigente em Potássio**
- K+ melhora sabor, tamanho e resistência ao transporte
- Deficiência de K causa frutos pequenos e casca fina

---

### 🌽 Milho
| Nutriente | Dosagem | Observações |
|-----------|---------|-------------|
| **Nitrogênio (N)** | 12 g/m² | Fundamental para produção de grãos |
| **Fósforo (P)** | 8 g/m² | Necessário no início do ciclo |
| **Potássio (K)** | 10 g/m² | Importante para enchimento de grãos |

**Justificativa Científica:**
- Milho tem alta demanda de Nitrogênio (produção de proteínas)
- P é crítico nas primeiras 4-6 semanas
- K garante enchimento uniforme dos grãos

---

## 🔬 Como o Sistema Calcula

### Fórmula Básica
```
Quantidade Total = Área (m²) × Dosagem Recomendada (kg/m²)
```

### Exemplo Real

**Área Selecionada:** Banana #2 - 468 m²

**Cálculos:**
- **Nitrogênio:** 468 m² × 0.015 kg/m² = **7.02 kg**
- **Fósforo:** 468 m² × 0.010 kg/m² = **4.68 kg**
- **Potássio:** 468 m² × 0.020 kg/m² = **9.36 kg**

---

## 📐 Conversão de Unidades

O sistema automaticamente converte para a unidade mais apropriada:

| Quantidade | Unidade Exibida |
|------------|-----------------|
| < 1 kg | **gramas (g)** |
| ≥ 1 kg | **quilogramas (kg)** |

**Exemplos:**
- 0.850 kg → **850 g**
- 5.250 kg → **5.25 kg**

---

## 🌱 Efeitos dos NPK no pH do Solo

### Nitrogênio (N) - Acidifica
- **Processo:** NH₄⁺ → NO₃⁻ + H⁺ (nitrificação)
- **Efeito:** pH ↓ (0.3 a 0.7 pontos)
- **Motivo:** Liberação de íons H⁺ durante oxidação

### Fósforo (P) - Neutraliza
- **Processo:** Fosfatos consomem H⁺
- **Efeito:** pH ↑ (0.2 a 0.5 pontos)
- **Motivo:** Superfosfato neutraliza acidez

### Potássio (K) - Estabiliza/Alcaliniza
- **Processo:** K₂CO₃ é ligeiramente alcalino
- **Efeito:** pH ↑ (0.1 a 0.3 pontos)
- **Motivo:** Íons K⁺ estabilizam pH

---

## 📚 Fontes Científicas

1. **EMBRAPA** - Recomendações de Adubação
2. **IAC** (Instituto Agronômico de Campinas)
3. **CEPEA/ESALQ-USP** - Dados econômicos
4. **Boletins Técnicos** - Nutricão mineral de culturas

---

## 💡 Como Usar no Sistema

1. **Selecione uma área** na página "Áreas de Plantio"
2. Vá para o **Dashboard**
3. **Clique nos botões NPK** (N, P, K)
4. Sistema calculará e exibirá:
   - ✅ Quantidade total a aplicar
   - ✅ Área tratada
   - ✅ Dosagem por m²
   - ✅ Unidade apropriada (g ou kg)

---

## ⚠️ Observações Importantes

### Sem Área Selecionada
Se você aplicar NPK **sem selecionar uma área**, o sistema irá:
- ⚠️ Mostrar mensagem: "Selecione uma área de plantio primeiro"
- ⚠️ Quantidade = 0
- ⚠️ Alerta em amarelo

### Com Área Selecionada
- ✅ Cálculo automático baseado no tamanho real
- ✅ Dosagem específica para a cultura
- ✅ Alerta verde com informações detalhadas

---

## 🎯 Exemplo Completo

**Cenário:**
- Cultura: **Banana**
- Área: **#5 - 1.350 m²**
- Ação: Aplicar **Nitrogênio**

**Resultado no Sistema:**

```
🌱 Nitrogênio (N) aplicado: 20.25 kg

📊 Área: 1350 m²
💊 Dosagem: 15 g/m²
📦 Total aplicado: 20.25 kg
```

**Console (F12):**
```
🧪 NPK Aplicado:
   Nutriente: NITROGEN
   Área: 1350 m²
   Dosagem: 15 g/m²
   Total: 20.25 kg
```

**Efeito Secundário:**
- 🧪 Sensor LDR detectará acidificação do pH
- pH diminuirá ~0.4 pontos (simulação do processo de nitrificação)

---

## 🔧 Código de Referência

### Backend (Python)
```python
NPK_DOSAGE = {
    'banana': {
        'nitrogen': 0.015,    # 15g/m²
        'phosphorus': 0.010,  # 10g/m²
        'potassium': 0.020    # 20g/m²
    },
    'milho': {
        'nitrogen': 0.012,    # 12g/m²
        'phosphorus': 0.008,  # 8g/m²
        'potassium': 0.010    # 10g/m²
    }
}
```

### Cálculo
```python
total_kg = current_area.area * dosage_per_m2

if total_kg < 1:
    amount = total_kg * 1000  # Converte para gramas
    unit = "g"
else:
    amount = total_kg
    unit = "kg"
```

---

**Sistema desenvolvido com base em dados técnicos reais!** 🌾
