# Lógica de Irrigação - FarmTech Solutions

## 🌊 Algoritmo de Decisão (6 Condições)

O sistema FarmTech Solutions implementa um algoritmo inteligente de decisão de irrigação baseado em **6 condições prioritárias**, seguindo a lógica do firmware ESP32 do Cap 1.

---

## 📊 Fluxograma de Decisão

```
┌─────────────────────────────────────┐
│   INÍCIO: Nova Leitura de Sensores  │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ CONDIÇÃO 1: Umidade < 40%?          │
├─────────────────────────────────────┤
│ Solo muito seco (CRÍTICO)           │
└─────────────┬───────────────────────┘
              │
         SIM  │  NÃO
    ┌─────────┼─────────┐
    │         │         │
    ▼         ▼         │
  LIGA    CONDIÇÃO 2    │
IRRIGAÇÃO  Umidade > 80%?│
            │           │
       SIM  │  NÃO      │
    ┌───────┼─────────┐ │
    │       │         │ │
    ▼       ▼         │ │
 NUNCA   CONDIÇÃO 3   │ │
 IRRIGA  NPK insuf +  │ │
         umid < 60%?  │ │
            │         │ │
       SIM  │  NÃO    │ │
    ┌───────┼─────────┼─┤
    │       │         │ │
    ▼       ▼         │ │
  LIGA   CONDIÇÃO 4   │ │
IRRIGAÇÃO pH fora +   │ │
         umid < 60%?  │ │
            │         │ │
       SIM  │  NÃO    │ │
    ┌───────┼─────────┼─┤
    │       │         │ │
    ▼       ▼         │ │
  LIGA   CONDIÇÃO 5   │ │
IRRIGAÇÃO Temp > 30°C │ │
         + umid < 60%?│ │
            │         │ │
       SIM  │  NÃO    │ │
    ┌───────┼─────────┼─┤
    │       │         │ │
    ▼       ▼         │ │
  LIGA   CONDIÇÃO 6   │ │
IRRIGAÇÃO Condições   │ │
          ótimas      │ │
            │         │ │
            ▼         │ │
        DESLIGA       │ │
       IRRIGAÇÃO      │ │
            │         │ │
            └─────────┴─┘
                 │
                 ▼
         ┌───────────────┐
         │ FIM: Decisão  │
         │   Registrada  │
         └───────────────┘
```

---

## 🔢 Detalhamento das 6 Condições

### ✅ CONDIÇÃO 1: Solo Muito Seco (PRIORIDADE MÁXIMA)

**Trigger**: `umidade_solo < 40%`

**Decisão**: **LIGA IRRIGAÇÃO** imediatamente

**Motivo**: Solo em nível crítico, planta em estresse hídrico

**Código**:
```python
if umidade < 40.0:
    return {'deve_irrigar': True, 'motivo': 'Umidade crítica < 40%', 'condicao': 1}
```

**Exemplo**:
- Leitura: 35% umidade
- Ação: Irrigação acionada em 5 segundos

---

### ❌ CONDIÇÃO 2: Solo Encharcado (BLOQUEIO)

**Trigger**: `umidade_solo > 80%`

**Decisão**: **NUNCA IRRIGAR** (mesmo se outras condições pedirem)

**Motivo**: Excesso de água danifica raízes, causa apodrecimento

**Código**:
```python
if umidade > 80.0:
    return {'deve_irrigar': False, 'motivo': 'Solo encharcado > 80%', 'condicao': 2}
```

**Exemplo**:
- Leitura: 85% umidade
- Ação: Irrigação bloqueada mesmo com NPK insuficiente

---

### 🧪 CONDIÇÃO 3: NPK Insuficiente + Umidade Subótima

**Trigger**: `(NPK incompleto) AND (umidade < 60%)`

**Decisão**: **LIGA IRRIGAÇÃO** (ajuda absorção de nutrientes)

**Lógica Diferenciada por Cultura**:

#### Banana (K Crítico)
```python
if cultura_tipo == 'BANANA':
    if not npk_ok['K'] and umidade < 60:
        return {'deve_irrigar': True, 
                'motivo': 'NPK insuficiente (K crítico para BANANA) + umidade baixa'}
```

#### Milho (N Crítico)
```python
elif cultura_tipo == 'MILHO':
    if not npk_ok['N'] and umidade < 60:
        return {'deve_irrigar': True, 
                'motivo': 'NPK insuficiente (N crítico para MILHO) + umidade baixa'}
```

**Exemplo**:
- Cultura: Banana
- Leitura: K=OFF, umidade=55%
- Ação: Irrigação acionada para ajudar absorção de K

---

### 🧪 CONDIÇÃO 4: pH Fora da Faixa + Umidade Baixa

**Trigger**: `(pH < 5.5 OR pH > 7.5) AND (umidade < 60%)`

**Decisão**: **LIGA IRRIGAÇÃO** (diluir acidez/alcalinidade)

**Código**:
```python
if (ph < 5.5 or ph > 7.5) and umidade < 60:
    return {'deve_irrigar': True, 
            'motivo': f'pH fora da faixa ({ph}) + umidade baixa'}
```

**Faixas de pH**:
| Classificação | Valor pH | Ação |
|---------------|----------|------|
| Muito Ácido | < 5.0 | Irrigação + Calagem urgente |
| Ácido | 5.0-5.5 | Irrigação recomendada |
| **Ideal** | **5.5-7.5** | **Sem ajuste** |
| Alcalino | 7.5-8.5 | Irrigação recomendada |
| Muito Alcalino | > 8.5 | Irrigação + Gesso agrícola |

**Exemplo**:
- Leitura: pH=4.8, umidade=58%
- Ação: Irrigação acionada para diluir acidez

---

### 🌡️ CONDIÇÃO 5: Temperatura Alta + Umidade Baixa

**Trigger**: `(temperatura > 30°C) AND (umidade < 60%)`

**Decisão**: **LIGA IRRIGAÇÃO** (evapotranspiração alta)

**Código**:
```python
if temp > 30.0 and umidade < 60:
    return {'deve_irrigar': True, 
            'motivo': f'Temperatura alta ({temp}°C) + umidade baixa'}
```

**Faixas de Temperatura**:
| Classificação | Temperatura | Resposta |
|---------------|-------------|----------|
| Fria | < 15°C | Irrigação reduzida |
| Ideal | 15-25°C | Irrigação normal |
| Alta | 25-35°C | Irrigação aumentada |
| **Crítica** | **> 35°C** | **Irrigação máxima + sombreamento** |

**Exemplo**:
- Leitura: 32°C, umidade=55%
- Ação: Irrigação acionada para compensar evaporação

---

### ✅ CONDIÇÃO 6: Condições Ótimas

**Trigger**: Nenhuma das condições 1-5 ativada

**Decisão**: **DESLIGA IRRIGAÇÃO**

**Critérios de "Ótimo"**:
- ✅ Umidade entre 40-80%
- ✅ NPK adequado (ou umidade >60%)
- ✅ pH entre 5.5-7.5 (ou umidade >60%)
- ✅ Temperatura <30°C (ou umidade >60%)

**Código**:
```python
return {'deve_irrigar': False, 
        'motivo': 'Condições ótimas - irrigação desnecessária', 
        'condicao': 6}
```

**Exemplo**:
- Leitura: 65% umidade, 24°C, pH 6.5, NPK OK
- Ação: Irrigação desligada, economia de água

---

## 📊 Tabela de Decisão Resumida

| Condição | Umidade | NPK | pH | Temp (°C) | Decisão | Prioridade |
|----------|---------|-----|----|-----------|---------| ---------- |
| **1** | <40% | - | - | - | **LIGA** | 🔴 CRÍTICA |
| **2** | >80% | - | - | - | **NUNCA** | 🔴 BLOQUEIO |
| **3** | <60% | ❌ | - | - | **LIGA** | 🟡 MÉDIA |
| **4** | <60% | - | <5.5 ou >7.5 | - | **LIGA** | 🟡 MÉDIA |
| **5** | <60% | - | - | >30 | **LIGA** | 🟡 MÉDIA |
| **6** | 40-80% | ✅ | 5.5-7.5 | <30 | **DESLIGA** | 🟢 NORMAL |

---

## 💧 Eficiência Hídrica

### Economia Esperada

Comparado a irrigação tradicional (tempo fixo):

| Sistema | Água Utilizada | Economia |
|---------|----------------|----------|
| Tradicional (timer) | 100% | 0% |
| **FarmTech (inteligente)** | **65-70%** | **30-35%** |

### Cálculo de Economia

**Exemplo: Banana 5.5 hectares**

- Irrigação tradicional: 60 mm/dia × 5.5 ha = 3.300 m³/dia
- FarmTech: 40 mm/dia × 5.5 ha = 2.200 m³/dia
- **Economia diária**: 1.100 m³ = 33%
- **Economia mensal** (30 dias): 33.000 m³
- **Valor econômico** (R$ 5/m³): R$ 165.000/mês

---

## 🎛️ Parâmetros Ajustáveis

### Constantes de Threshold

```python
class IrrigacaoController:
    UMIDADE_MINIMA = 40.0   # Condição 1
    UMIDADE_IDEAL = 60.0    # Condições 3, 4, 5
    UMIDADE_MAXIMA = 80.0   # Condição 2
    PH_MINIMO = 5.5         # Condição 4
    PH_MAXIMO = 7.5         # Condição 4
    TEMP_ALTA = 30.0        # Condição 5
```

### Customização por Cultura

Ajuste conforme tolerâncias específicas:

```python
if cultura_tipo == 'BANANA':
    UMIDADE_IDEAL = 65.0  # Banana prefere mais úmido
elif cultura_tipo == 'MILHO':
    UMIDADE_IDEAL = 55.0  # Milho tolera mais seco
```

---

## 🧪 Validação e Testes

### Cenários de Teste

#### Teste 1: Solo Seco
- **Input**: umidade=35%, NPK=OK, pH=6.5, temp=25°C
- **Output**: LIGA (Condição 1)
- **Motivo**: "Umidade crítica (35%) < 40%"

#### Teste 2: Solo Encharcado
- **Input**: umidade=85%, NPK=FALTA N, pH=5.0, temp=32°C
- **Output**: NUNCA IRRIGA (Condição 2)
- **Motivo**: "Solo encharcado (85%) > 80%"

#### Teste 3: NPK Insuficiente (Banana)
- **Input**: umidade=55%, NPK=FALTA K, pH=6.5, temp=26°C
- **Output**: LIGA (Condição 3)
- **Motivo**: "NPK insuficiente (K crítico para BANANA) + umidade 55% < 60%"

#### Teste 4: pH Ácido
- **Input**: umidade=50%, NPK=OK, pH=4.5, temp=24°C
- **Output**: LIGA (Condição 4)
- **Motivo**: "pH fora da faixa (4.5) + umidade 50% < 60%"

#### Teste 5: Temperatura Alta
- **Input**: umidade=52%, NPK=OK, pH=6.8, temp=33°C
- **Output**: LIGA (Condição 5)
- **Motivo**: "Temperatura alta (33°C) > 30°C + umidade 52% < 60%"

#### Teste 6: Condições Ideais
- **Input**: umidade=68%, NPK=OK, pH=6.3, temp=23°C
- **Output**: DESLIGA (Condição 6)
- **Motivo**: "Condições ótimas - irrigação desnecessária"

---

## 📈 Logs e Histórico

### Formato de Registro

```json
{
  "id": 1,
  "cultivo_id": 1,
  "leitura_id": 5,
  "timestamp": "2025-10-11 14:30:00",
  "acionado": true,
  "motivo": "Umidade crítica (35%) < 40%",
  "condicao": 1
}
```

### Análise de Histórico

```python
# Taxa de acionamento
taxa = (irrigacoes_acionadas / total_verificacoes) * 100

# Condições mais frequentes
condicoes_freq = Counter([i['condicao'] for i in irrigacoes])
```

---

*Atualizado: Outubro 2025*  
*FarmTech Solutions - Grupo 59 FIAP*
