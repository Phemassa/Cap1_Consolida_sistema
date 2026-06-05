# Sistema de Irrigação Inteligente - FarmTech Solutions
## Fase 2 - FIAP - Atividade Cap 1

> 🌱 **Sistema IoT completo para automação de irrigação agrícola baseado em ESP32, sensores NPK, pH, temperatura e umidade**

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Instalação e Configuração](#instalação-e-configuração)
4. [Como Usar](#como-usar)
5. [Simulação no Wokwi](#simulação-no-wokwi)
6. [Demonstração Completa](#demonstração-completa)
7. [Características Técnicas](#características-técnicas)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

O **Sistema de Irrigação Inteligente FarmTech Solutions** é uma solução IoT completa que automatiza a irrigação agrícola baseada em:

- **Sensores NPK**: 3 botões verdes para simular presença de Nitrogênio, Fósforo e Potássio
- **Sensor pH**: LDR que simula medição de pH do solo (0-14)
- **Sensor Ambiental**: DHT22 para temperatura e umidade do ar
- **Atuador**: Relé para controle da bomba d'água
- **Interface Web**: Dashboard responsivo para monitoramento e controle
- **Automação**: Sistema inteligente que decide quando irrigar baseado na cultura plantada

### 🌾 Culturas Suportadas

| Cultura | pH Ideal | Umidade Mín. | Temperatura | NPK Necessário |
|---------|----------|--------------|-------------|----------------|
| 🍅 Tomate | 6.0-6.8 | 60% | 18-26°C | N, P, K |
| 🌽 Milho | 6.0-7.0 | 55% | 20-30°C | N, P, K |
| 🌱 Soja | 6.0-7.0 | 50% | 22-28°C | P, K |
| 🍌 Banana | 5.5-6.5 | 65% | 24-30°C | N, P, K |
| ☕ Café | 6.0-6.5 | 70% | 18-24°C | N, P |

---

## 📁 Estrutura do Projeto

```
FarmTechSolutions/fase2/
│
├── 🌐 web_app/                    # Aplicação Flask
│   ├── app.py                    # Servidor principal
│   ├── templates/                # Templates HTML
│   │   ├── base.html            # Layout base
│   │   ├── dashboard.html       # Dashboard principal  
│   │   ├── weather.html         # Meteorologia (Opcional 1)
│   │   ├── settings.html        # Configurações
│   │   └── reports.html         # Relatórios
│   └── static/                  # Arquivos estáticos (CSS, JS)
│
├── 🔧 simulador_sensores/         # Simulador ESP32
│   ├── esp32_simulator.py       # Simulador principal
│   └── flask_bridge.py          # Ponte Flask-ESP32
│
├── 🖥️ arduino_code/              # Código para ESP32
│   ├── farm_irrigation_system.ino # Código Arduino
│   ├── wokwi_diagram.json       # Diagrama Wokwi
│   └── INSTRUCOES_WOKWI.md      # Manual Wokwi
│
├── 🌤️ api_clima/                 # Integração clima (Atividade Opcional 1)
│   └── weather_integration.py   # API OpenWeatherMap - "IR ALÉM"
│
├── 🎬 demo_completo.py           # Demonstração completa
└── 📚 README.md                 # Este arquivo
```

---

## ⚙️ Instalação e Configuração

### Pré-requisitos

- **Python 3.7+**
- **Navegador web moderno**
- **Conta Wokwi.com** (opcional, para simulação)

### 1. Instalar Dependências

```bash
# Navegue até a pasta do projeto
cd "c:\Fiap Projeto\FarmTechSolutions\fase2"

# Instale as dependências Python
pip install flask requests
```

### 2. Estrutura de Arquivos

O projeto já está com todos os arquivos criados. Verifique se a estrutura está correta:

```bash
# Verificar arquivos principais
dir web_app\app.py
dir simulador_sensores\esp32_simulator.py
dir arduino_code\farm_irrigation_system.ino
```

---

## 🚀 Como Usar

### Opção 1: Demonstração Completa (Recomendada)

```bash
# Execute o script de demonstração
python demo_completo.py
```

Este script:
- ✅ Verifica dependências
- ✅ Inicia simulador ESP32
- ✅ Executa aplicação Flask  
- ✅ Abre dashboard no navegador
- ✅ Oferece demonstrações automáticas

### Opção 2: Execução Manual

#### 2a. Iniciar Simulador ESP32

```bash
cd simulador_sensores
python esp32_simulator.py
```

#### 2b. Iniciar Aplicação Flask

```bash
# Em outro terminal
cd web_app  
python app.py
```

#### 2c. Acessar Dashboard

Abra o navegador em: **http://localhost:5000**

### Opção 3: Simulação no Wokwi

1. Acesse [wokwi.com](https://wokwi.com)
2. Crie novo projeto ESP32
3. Copie conteúdo de `arduino_code/wokwi_diagram.json`
4. Copie código de `arduino_code/farm_irrigation_system.ino`
5. Execute a simulação

📖 **Instruções detalhadas**: `arduino_code/INSTRUCOES_WOKWI.md`

---

## 🎮 Interface do Sistema

### 🏠 Dashboard Principal

- **📊 Dados em Tempo Real**: NPK, pH, temperatura, umidade
- **💧 Status da Irrigação**: Estado atual da bomba
- **🌾 Seleção de Cultura**: 5 culturas pré-configuradas
- **📈 Gráficos**: Histórico dos últimos sensores

### ⚙️ Configurações

- **🎛️ Controle Manual**: Liga/desliga bomba manualmente
- **🔘 Simulação NPK**: Botões para simular presença de nutrientes
- **📏 Ajuste pH**: Controle deslizante para pH (0-14)
- **🔄 Modo Automático**: Habilita/desabilita automação

### 📊 Relatórios

- **📈 Gráficos Históricos**: Tendências dos sensores
- **📋 Resumo Diário**: Estatísticas de irrigação
- **🎯 Eficiência**: Análise de performance do sistema

### 🌤️ Meteorologia (Atividade Opcional 1 - "IR ALÉM")

- **�️ Clima Atual**: Temperatura, umidade, vento em tempo real
- **☔ Previsão de Chuva**: Suspende irrigação automaticamente
- **📅 Previsão 3 Dias**: Planejamento antecipado de irrigação
- **💧 Economia de Água**: Integração inteligente com OpenWeatherMap
- **🏆 Benefício FIAP**: Qualifica para programas avançados

---

## 🎯 Demonstrações Disponíveis

### 1. Automática
Executa cenários predefinidos:
- ✅ **Condições Ideais**: Todos parâmetros normais
- ❌ **Deficiência NPK**: Carência de nutrientes
- ⚠️ **pH Inadequado**: Solo muito ácido/básico
- 🔄 **Recuperação**: Volta às condições normais

### 2. Manual
Controle interativo:
- `n` - Toggle Nitrogênio
- `p` - Toggle Fósforo
- `k` - Toggle Potássio  
- `b` - Toggle Bomba
- `d` - Mostrar dados atuais

### 3. Monitoramento
Operação automática com exibição de status em tempo real.

---

## 🔧 Características Técnicas

### Hardware Simulado (ESP32)

| Componente | Pino | Função |
|------------|------|---------|
| **Botão Nitrogênio** | D2 | Simula presença de N |
| **Botão Fósforo** | D4 | Simula presença de P |
| **Botão Potássio** | D5 | Simula presença de K |
| **LDR (pH)** | A0 | Sensor de acidez (0-14) |
| **DHT22** | D21 | Temperatura e umidade |
| **Relé Bomba** | D18 | Controla irrigação |
| **LED Status** | D23 | Indica atividade |

### Software

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Bootstrap 5, Chart.js
- **Simulador**: Python com threads
- **Comunicação**: JSON via serial simulada
- **Banco de Dados**: Memória (histórico limitado)

### Algoritmo de Decisão

```python
def deve_irrigar(cultura, ph, npk, temp, umidade):
    """
    Decide se deve irrigar baseado nos parâmetros da cultura
    """
    config = CULTURAS[cultura]
    
    # Verifica cada condição
    ph_ok = config.ph_min <= ph <= config.ph_max
    temp_ok = config.temp_min <= temp <= config.temp_max  
    umidade_ok = umidade >= config.umidade_min
    npk_ok = verifica_npk_necessario(cultura, npk)
    
    # Irriga se alguma condição não estiver ideal
    return not (ph_ok and temp_ok and umidade_ok and npk_ok)
```

---

## 🌤️ Integração com Clima

O sistema inclui integração opcional com OpenWeatherMap:

```python
# Configurar API (opcional)
API_KEY = "sua_chave_aqui"

# O sistema funciona com dados simulados se não configurado
```

**Recursos climáticos**:
- 🌧️ Previsão de chuva (cancela irrigação)
- 🌡️ Temperatura externa (ajusta parâmetros)
- 💨 Vento e umidade (influencia decisões)

---

## 🐛 Troubleshooting

### Problema: Módulos não encontrados
```bash
# Solução: Instalar dependências
pip install flask requests
```

### Problema: Porta 5000 ocupada
```bash
# Solução: Mudar porta no app.py
app.run(port=5001)  # Use porta diferente
```

### Problema: Simulador não conecta
```bash
# Solução: Verificar se está na pasta correta
cd simulador_sensores
python esp32_simulator.py
```

### Problema: Dashboard não carrega
- ✅ Verifique se Flask está rodando
- ✅ Acesse http://localhost:5000
- ✅ Verifique console do navegador por erros

### Problema: Wokwi não funciona  
- ✅ Copie exatamente o código do .ino
- ✅ Use o diagrama JSON fornecido
- ✅ Verifique se ArduinoJson está incluído

---

## 📚 Arquivos de Referência

### Para Desenvolvimento
- `web_app/app.py` - Servidor Flask principal
- `simulador_sensores/flask_bridge.py` - Integração ESP32-Flask
- `arduino_code/farm_irrigation_system.ino` - Código ESP32

### Para Demonstração
- `demo_completo.py` - Script completo de demonstração
- `arduino_code/INSTRUCOES_WOKWI.md` - Manual detalhado Wokwi

### Para Configuração
- `arduino_code/wokwi_diagram.json` - Diagrama do circuito
- `api_clima/weather_integration.py` - Integração meteorológica

---

## 🎓 Contexto Acadêmico

Este projeto atende aos requisitos da **Atividade - Cap 1 - Um Mapa do Tesouro** do curso FIAP, implementando:

- ✅ **Item 3**: Descrição completa do projeto
- ✅ **Sensores ESP32**: NPK, pH, DHT22 conforme especificado
- ✅ **Automação Inteligente**: Decisão baseada em parâmetros da cultura
- ✅ **Interface Web**: Dashboard responsivo e funcional
- ✅ **Simulação Wokwi**: Circuito virtual completo
- ✅ **Documentação**: Manual completo de uso

### 🏆 **Atividades Opcionais - "IR ALÉM" (IMPLEMENTADAS):**
- ✅ **Opcional 1**: Integração Python com API OpenWeatherMap - suspende irrigação por previsão de chuva
- ✅ **Opcional 2**: Análise estatística em R - scripts completos para análise de dados agrícolas
- 🎯 **Status**: **100% COMPLETO** - Qualificado para programas avançados FIAP

---

## 🏆 Resultados Esperados

Após executar o sistema, você deve conseguir:

1. **📱 Monitorar** sensores em tempo real via web
2. **🎛️ Controlar** irrigação manual e automaticamente  
3. **📊 Visualizar** histórico e tendências
4. **🌾 Configurar** diferentes culturas
5. **🔄 Demonstrar** automação inteligente
6. **🌐 Simular** no Wokwi.com
7. **📈 Gerar** relatórios de performance

---

## 📞 Suporte

Para dúvidas ou problemas:

1. 📖 Consulte este README completo
2. 🔍 Verifique o troubleshooting
3. 🧪 Execute `demo_completo.py` para diagnóstico
4. 🌐 Teste simulação no Wokwi primeiro

---

**🌱 FarmTech Solutions - Transformando agricultura com IoT! 🌱**

---

*Desenvolvido para FIAP - Fase 2 - Sistema de Irrigação Inteligente*