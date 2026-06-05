# Requisitos de NPK por Cultura

## 📊 Tabela de Nutrientes (g/m²)

### Culturas Implementadas no Sistema

| Cultura | Nitrogênio (N) | Fósforo (P) | Potássio (K) | Nutriente Crítico | Fonte |
|---------|----------------|-------------|--------------|-------------------|-------|
| **Banana** | 15.0 | 10.0 | **20.0** | **K (Potássio)** | EMBRAPA, 2023 |
| **Milho** | **12.0** | 8.0 | 10.0 | **N (Nitrogênio)** | EMBRAPA, 2022 |

### Outras Culturas (Referência)

| Cultura | Nitrogênio (N) | Fósforo (P) | Potássio (K) | Fonte |
|---------|----------------|-------------|--------------|-------|
| Cana-de-açúcar | 100-140 | 40-60 | 100-150 | SOCICANA |
| Soja | 0-20* | 40-80 | 40-80 | EMBRAPA |
| Café | 200-400 | 40-80 | 150-300 | IAC |
| Algodão | 80-120 | 40-80 | 60-100 | ABR |
| Tomate | 150-250 | 100-200 | 200-350 | CEPEA |

*Soja: Fixação biológica de nitrogênio

## 🧪 Importância de Cada Nutriente

### Nitrogênio (N)
- **Função**: Crescimento vegetativo, fotossíntese, proteínas
- **Deficiência**: Folhas amareladas (clorose), crescimento lento
- **Excesso**: Crescimento vegetativo excessivo, atraso na maturação
- **Culturas críticas**: Milho, Trigo, Cana-de-açúcar

### Fósforo (P)
- **Função**: Desenvolvimento radicular, floração, energia celular (ATP)
- **Deficiência**: Folhas arroxeadas, raízes fracas, baixa produção
- **Excesso**: Pode bloquear absorção de micronutrientes (Zn, Fe)
- **Culturas críticas**: Soja, Feijão, Leguminosas

### Potássio (K)
- **Função**: Regulação hídrica, resistência a doenças, qualidade dos frutos
- **Deficiência**: Bordas das folhas queimadas, frutos pequenos
- **Excesso**: Compete com absorção de Ca e Mg
- **Culturas críticas**: Banana, Tomate, Batata

## 📈 Faixas Recomendadas por Fase de Desenvolvimento

### Banana (Ciclo: 12-14 meses)

| Fase | Idade | N (g/planta/mês) | P (g/planta/mês) | K (g/planta/mês) |
|------|-------|------------------|------------------|------------------|
| Vegetativa | 0-3 meses | 5-10 | 2-4 | 8-12 |
| Floração | 4-7 meses | 12-18 | 8-12 | 15-25 |
| Frutificação | 8-12 meses | 10-15 | 6-10 | 20-30 |

**Total no ciclo**: N=150-180g, P=100-120g, K=200-240g por planta

### Milho (Ciclo: 120-150 dias)

| Fase | Dias após plantio | N (kg/ha) | P (kg/ha) | K (kg/ha) |
|------|-------------------|-----------|-----------|----------|
| Plantio | 0 | 20-30 | 40-60 | 40-60 |
| V4-V6 (4-6 folhas) | 20-30 | 40-60 | 0 | 0 |
| V8-V10 (pré-pendoamento) | 40-50 | 40-60 | 0 | 40-60 |

**Total no ciclo**: N=100-150 kg/ha, P=40-60 kg/ha, K=80-120 kg/ha

## 🌱 Sintomas de Deficiência

### Visual Rápido

| Nutriente | Sintoma Principal | Onde Aparece Primeiro |
|-----------|-------------------|----------------------|
| **N** | Amarelamento generalizado | Folhas velhas (móvel) |
| **P** | Folhas roxas/escuras | Folhas velhas (móvel) |
| **K** | Bordas queimadas | Folhas velhas (móvel) |
| **Ca** | Ponta das folhas morre | Folhas novas (imóvel) |
| **Mg** | Clorose entre nervuras | Folhas velhas (móvel) |

### Sequência de Diagnóstico

1. **Identificar localização**: Folha velha = nutriente móvel (N, P, K, Mg)
2. **Observar padrão**: Generalizado ou localizado
3. **Confirmar com análise de solo**: Teor real de nutrientes
4. **Verificar pH**: Afeta disponibilidade (pH 6.0-7.0 ideal)

## 🔬 Análise de Solo - Interpretação

### Classificação de Teores (mg/dm³)

| Nutriente | Muito Baixo | Baixo | Médio | Alto | Muito Alto |
|-----------|-------------|-------|-------|------|------------|
| P | <5 | 5-10 | 10-20 | 20-40 | >40 |
| K | <30 | 30-60 | 60-120 | 120-180 | >180 |
| Ca | <15 | 15-30 | 30-60 | 60-90 | >90 |
| Mg | <5 | 5-10 | 10-20 | 20-30 | >30 |

### Conversão de Unidades

- **1 g/m² = 10 kg/ha**
- **1 cmolc/dm³ K = 391 mg/dm³**
- **1 ppm = 1 mg/kg = 1 mg/dm³**

## 📚 Fontes de Referência

### EMBRAPA
- **Banana**: BRS Platina - Recomendações Técnicas (2023)
- **Milho**: BRS Híbridos - Manual de Adubação (2022)

### Outras Fontes Confiáveis
- **IAC (Instituto Agronômico de Campinas)**: Café, Cana
- **ESALQ/USP**: Tabelas de adubação por cultura
- **CEPEA**: Custos e recomendações técnicas
- **CONAB**: Dados de produtividade nacional

## 🎯 Aplicação no FarmTech Solutions

### Lógica de Decisão NPK

```python
def verificar_npk_adequado(cultura, leitura_npk):
    if cultura.tipo == 'BANANA':
        # Potássio é CRÍTICO (20 g/m²)
        if not leitura_npk['K']:
            return False, "Deficiência de K (crítico para Banana)"
    
    elif cultura.tipo == 'MILHO':
        # Nitrogênio é CRÍTICO (12 g/m²)
        if not leitura_npk['N']:
            return False, "Deficiência de N (crítico para Milho)"
    
    # Verifica se todos estão adequados
    if all(leitura_npk.values()):
        return True, "NPK adequado"
    
    return False, "Um ou mais nutrientes insuficientes"
```

### Integração com ESP32 (Cap 1)

- **Botão GPIO 2**: Simula sensor de Nitrogênio (ON = adequado)
- **Botão GPIO 4**: Simula sensor de Fósforo (ON = adequado)
- **Botão GPIO 5**: Simula sensor de Potássio (ON = adequado)

**Leitura real**: Sensores NPK comerciais (Mod. RS485, 0-1999 mg/kg)

---

*Atualizado: Outubro 2025*  
*FarmTech Solutions - Grupo 59 FIAP*
