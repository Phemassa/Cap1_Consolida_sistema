# 📸 Screenshots do Circuito Wokwi

Este diretório contém as capturas de tela do simulador Wokwi.com demonstrando o funcionamento do **Sistema de Irrigação Inteligente FarmTech v2.0** com a funcionalidade **NPK-pH**.

---

## 📋 Imagens Disponíveis

### 1. `circuito_wokwi.png` ✅
**Descrição:** Circuito completo do sistema de irrigação inteligente

**Componentes Visíveis:**
- ⚙️ **ESP32 DevKit v1** - Microcontrolador central
- 🟢 **3 Botões NPK:**
  - **N - Nitrogênio** (GPIO 2) - Primeiro botão verde
  - **P - Fósforo** (GPIO 4) - Segundo botão verde (meio)
  - **K - Potássio** (GPIO 5) - Terceiro botão verde (inferior)
- 💡 **LDR (Photoresistor)** - Simula sensor de pH do solo
  - Conectado ao GPIO 34 (ADC)
  - Painel mostra luminosidade (lux) simulando faixa de pH
- 🌡️ **DHT22** - Sensor de temperatura e umidade
  - GPIO 21 (direita do circuito)
  - Simula condições climáticas
- 🔌 **Relé Módulo** - Controle da bomba de irrigação
  - GPIO 18 (controle IN)
  - LED indicador de status
  - Vermelho/Azul (direita inferior)
- 🔵 **LED Status** - Indicador visual do sistema
  - Conectado ao topo do circuito

**Características Técnicas:**
- **Fios Azuis:** VCC (alimentação 3.3V/5V)
- **Fios Pretos:** GND (terra)
- **Fios Verdes:** Sinais digitais dos botões NPK
- **Fios Laranja:** Sinal de controle do relé
- **Fios Vermelhos:** Alimentação do relé

**Tempo de Simulação Visível:** ~865 ms (00:00.865)

---

### 2. `serial_monitor_npk_ph.png` ✅
**Descrição:** Terminal/Serial Monitor mostrando leituras NPK e decisão de irrigação

**Dados Exibidos:**
- 🧪 **NPK - Níveis de Nutrientes:**
  - ✅ **Nitrogênio (N):** OK (botão pressionado na imagem)
  - ❌ **Fósforo (P):** BAIXO
  - ❌ **Potássio (K):** BAIXO [crítico p/ banana]

**Funcionalidade NPK-pH v2.0:**
Esta imagem demonstra a **inovação principal** do projeto:
- Quando botões NPK são pressionados, o **pH é automaticamente ajustado**
- **Nitrogênio (N):** -0.4 pH (acidifica)
- **Fósforo (P):** -0.3 pH (acidifica)
- **Potássio (K):** +0.1 pH (alcaliniza levemente)
- **pH Final = pH Base (LDR) + Σ Ajustes NPK**

**Estado do Sistema:**
- 📊 Leituras de sensores em tempo real
- 💧 Decisão de irrigação baseada nas 6 condições hierárquicas
- 🌾 Cultura selecionada: Banana ou Milho
- ⚗️ pH calculado dinamicamente com base em NPK

**Informação Técnica:**
- **LEITURA #17** - Contador de ciclos (incrementa a cada 5 segundos)
- **~865 ms** - Tempo decorrido de simulação

---

## 🔌 Mapa de Conexões Físicas

Com base no `circuito_wokwi.png`, as conexões são:

| Componente | Pino ESP32 | Tipo | Função |
|------------|-----------|------|--------|
| **LED Status** | Topo do circuito | Digital Output | Indicador visual de operação |
| **Botão N (Nitrogênio)** | GPIO 2 | Digital Input (Pull-up) | Sensor NPK - Nitrogênio |
| **Botão P (Fósforo)** | GPIO 4 | Digital Input (Pull-up) | Sensor NPK - Fósforo |
| **Botão K (Potássio)** | GPIO 5 | Digital Input (Pull-up) | Sensor NPK - Potássio |
| **LDR (pH Sensor)** | GPIO 34 (A0) | Analog Input (ADC 12-bit) | Simula pH do solo (3.0-9.0) |
| **DHT22 Data** | GPIO 21 | Digital (OneWire) | Temperatura + Umidade |
| **DHT22 VCC** | 3.3V | Power | Alimentação sensor |
| **DHT22 GND** | GND | Ground | Terra sensor |
| **Relé IN (Signal)** | GPIO 18 | Digital Output | Controle liga/desliga bomba |
| **Relé VCC** | 5V | Power | Alimentação relé |
| **Relé GND** | GND | Ground | Terra relé |

---

## 🎯 Como Usar Estas Imagens

### No README.md Principal:
```markdown
## 📸 Screenshots

### Circuito Wokwi Completo
![Circuito Wokwi](docs/images/circuito_wokwi.png)
*ESP32 + 3 botões NPK + LDR (pH) + DHT22 + Relé*

### Serial Monitor - NPK e pH v2.0
![Serial Monitor NPK-pH](docs/images/serial_monitor_npk_ph.png)
*Terminal mostrando Nitrogênio OK, Fósforo e Potássio baixos, com decisão de irrigação*
```

### Em Apresentações:
- Use `circuito_wokwi.png` para explicar **arquitetura do sistema**
- Use `serial_monitor_npk_ph.png` para demonstrar **lógica de decisão**

---

## 📝 Informações Adicionais

### Arquivos Relacionados:
- **COMO_SALVAR_IMAGENS.md** - Guia de como tirar screenshots no Wokwi
- **GUIA_RAPIDO_SCREENSHOTS.md** - Checklist de screenshots necessários

### Para Adicionar Mais Screenshots:

Se precisar de capturas adicionais:

1. **Acesse:** https://wokwi.com
2. **Carregue:** `diagram.json` + `FarmTech.ino`
3. **Execute simulação** e ajuste sensores
4. **Capture tela** (Print Screen ou ferramenta)
5. **Salve neste diretório** com nome descritivo:
   - `serial_monitor_irrigacao_ligada.png`
   - `serial_monitor_ph_ajustado.png`
   - `circuito_rele_ativo.png`

6. **Atualize este README.md** com descrição da nova imagem

---

## ✅ Status dos Screenshots

| Imagem | Status | Descrição | Uso |
|--------|--------|-----------|-----|
| `circuito_wokwi.png` | ✅ Disponível | Circuito completo com todos componentes | README principal, apresentação |
| `serial_monitor_npk_ph.png` | ✅ Disponível | Terminal com NPK-pH v2.0 | README principal, vídeo YouTube |

---

**Grupo 19 FIAP - 1 ano • 2025/2**  
**Data:** 12/10/2025  
**Projeto:** FarmTech Solutions - Sistema de Irrigação Inteligente v2.0


## ✅ Checklist de Screenshots Recomendados

### Obrigatórios (para entrega FIAP):
- [x] Circuito completo mostrando LDR
- [x] Circuito completo mostrando DHT22
- [ ] Serial Monitor com sistema iniciando (banner)
- [ ] Serial Monitor com leitura de sensores
- [ ] Serial Monitor com irrigação LIGADA
- [ ] Serial Monitor com irrigação DESLIGADA

### Opcionais (melhoram apresentação):
- [ ] Botões NPK pressionados (verde aceso)
- [ ] LDR em diferentes níveis de lux (pH diferentes)
- [ ] DHT22 em condições extremas (temp >30°C)
- [ ] Relé com LED indicador visível

---

## 🎥 Sugestão para Vídeo YouTube

Use estas imagens como referência para gravar o vídeo:
1. Mostrar circuito completo (0:00-0:30)
2. Explicar cada sensor (0:30-1:30)
3. Ajustar LDR e mostrar Serial (1:30-2:30)
4. Pressionar botões NPK (2:30-3:30)
5. Demonstrar irrigação liga/desliga (3:30-4:30)
6. Considerações finais (4:30-5:00)

---

**Última atualização:** 11/10/2025  
**Simulador:** [Wokwi.com](https://wokwi.com) - Community License
