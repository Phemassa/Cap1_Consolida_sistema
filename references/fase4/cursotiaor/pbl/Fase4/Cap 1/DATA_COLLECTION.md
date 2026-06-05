# 📊 Coleta de Dados dos Sensores - FarmTech

## Visão Geral

Este diretório contém scripts para coletar dados dos sensores ESP32/Wokwi de duas formas:
1. **Dados Simulados** - Gera datasets sintéticos realistas
2. **Dados Reais** - Coleta via porta serial do ESP32/Wokwi

---

## 🎯 Opção 1: Dados Simulados (Recomendado para ML)

### Uso Rápido

```bash
python generate_sensor_data.py
```

### Características dos Dados Gerados

| Variável | Tipo | Faixa | Descrição |
|----------|------|-------|-----------|
| `timestamp` | datetime | - | Data/hora da leitura |
| `temperatura` | float | 18-38°C | Temperatura do ar |
| `umidade_solo` | float | 25-90% | Umidade do solo |
| `ph_solo` | float | 5.0-8.0 | pH do solo |
| `nitrogenio` | boolean | 0/1 | Nível adequado de N |
| `fosforo` | boolean | 0/1 | Nível adequado de P |
| `potassio` | boolean | 0/1 | Nível adequado de K |
| `irrigacao_ativa` | boolean | 0/1 | Sistema de irrigação |
| `cultura` | string | banana/milho | Tipo de cultura |

### Variáveis Target (para ML)

| Variável Target | Tipo | Descrição |
|-----------------|------|-----------|
| `volume_irrigacao_recomendado` | float | Litros/m² recomendados |
| `dosagem_n_recomendada` | float | Gramas/m² de Nitrogênio |
| `dosagem_p_recomendada` | float | Gramas/m² de Fósforo |
| `dosagem_k_recomendada` | float | Gramas/m² de Potássio |
| `rendimento_estimado` | float | Kg/hectare esperado |

### Exemplo de Dados Gerados

```csv
timestamp,temperatura,umidade_solo,ph_solo,nitrogenio,fosforo,potassio,irrigacao_ativa,cultura,volume_irrigacao_recomendado,rendimento_estimado
2025-10-09 20:00:00,25.3,45.2,6.8,1,1,0,0,banana,5.2,22500
2025-10-09 20:00:05,25.5,44.8,6.7,1,1,0,0,banana,5.5,22800
2025-10-09 20:00:10,25.4,44.5,6.9,1,0,0,1,banana,6.0,20100
```

### Padrões Simulados

#### 🌡️ Variação de Temperatura
- Segue ciclo diurno (senoidal)
- Pico às 14h, mínimo às 2h
- Variação natural ±0.5°C

#### 💧 Umidade do Solo
- Diminui sem irrigação (-0.5%/leitura)
- Aumenta com irrigação (+2%/leitura)
- Limite: 25-90%

#### 🧪 pH do Solo
- Influenciado por NPK:
  - N acidifica (-0.05)
  - P acidifica (-0.03)
  - K alcaliniza (+0.02)
- Tende ao equilíbrio (6.0-7.0)

#### 🌾 Comportamento por Cultura

**Banana:**
- Crítico: Potássio (K)
- K deficiente 50% do tempo
- Rendimento base: 25000 kg/ha

**Milho:**
- Crítico: Nitrogênio (N)
- N deficiente 50% do tempo
- Rendimento base: 8000 kg/ha

### Personalização

```python
# Gerar mais amostras
df = gerar_dados_simulados(
    num_samples=5000,      # Mais dados
    cultura="milho",       # Trocar cultura
    output_format="json"   # Formato JSON
)

# Ajustar parâmetros
simulator = SensorSimulator(cultura="banana")
simulator.temperatura_base = 28.0  # Região mais quente
simulator.umidade_base = 70.0      # Região mais úmida
```

---

## 🔌 Opção 2: Dados Reais (Serial do Wokwi/ESP32)

### Pré-requisitos

```bash
pip install pyserial
```

### Uso Básico

```bash
python collect_serial_data.py
```

### Configuração

#### 1. Identificar Porta Serial

**Windows:**
```
COM3, COM4, COM5, etc.
```

**Linux/Mac:**
```
/dev/ttyUSB0
/dev/ttyACM0
/dev/cu.usbserial-XXXX
```

#### 2. Ajustar no Código

```python
collector = SerialDataCollector(
    port='COM3',        # Sua porta
    baudrate=115200     # Baud rate do ESP32
)

collector.collect_data(
    duration_minutes=30,                # Duração
    output_file='sensor_data_real.csv'  # Arquivo de saída
)
```

### Como Funciona

1. **Conecta à porta serial** (115200 baud)
2. **Lê linhas do Serial Monitor** do ESP32
3. **Extrai dados** usando regex:
   ```
   🧪 NPK - Níveis de Nutrientes:
      🔵 Nitrogênio (N): ✅ OK  → nitrogenio=1
      🟡 Fósforo (P):    ❌ BAIXO → fosforo=0
   
   🌡️ Condições Ambientais:
      🌡️  Temperatura: 25.3 °C → temperatura=25.3
      💧 Umidade Solo: 45.2 % → umidade_solo=45.2
   ```
4. **Salva em CSV** quando todos os sensores foram lidos

### Exemplo de Saída

```csv
timestamp,temperatura,umidade_solo,ph_solo,nitrogenio,fosforo,potassio,irrigacao_ativa
2025-10-09T20:30:15,25.3,45.2,6.8,1,1,0,0
2025-10-09T20:30:20,25.5,44.8,6.7,1,1,0,0
```

### Troubleshooting

#### ❌ Porta não encontrada
```bash
# Listar portas disponíveis
python -m serial.tools.list_ports
```

#### ❌ Permissão negada (Linux)
```bash
sudo usermod -a -G dialout $USER
# Reinicie o sistema
```

#### ❌ Wokwi não tem porta serial real
Use a opção **Dados Simulados** em vez disso.

---

## 📦 Estrutura de Arquivos Gerados

```
Cap 1/
├── sensor_data_banana.csv       # Dados simulados banana
├── sensor_data_milho.csv        # Dados simulados milho
├── sensor_data_real.csv         # Dados reais via serial
└── data/                        # Diretório para datasets
    ├── raw/                     # Dados brutos
    ├── processed/               # Dados processados
    └── train_test_split/        # Train/test sets
```

---

## 🔄 Pipeline de Dados para ML

### 1. Gerar/Coletar Dados
```bash
python generate_sensor_data.py
```

### 2. Pré-processamento (próximo passo)
```python
import pandas as pd

# Carregar dados
df = pd.read_csv('sensor_data_banana.csv')

# Limpeza
df = df.dropna()
df = df[df['temperatura'] > 0]

# Feature Engineering
df['hora_do_dia'] = pd.to_datetime(df['timestamp']).dt.hour
df['npk_adequado'] = df['nitrogenio'] & df['fosforo'] & df['potassio']

# Salvar processado
df.to_csv('data/processed/sensor_data_clean.csv', index=False)
```

### 3. Treinar Modelo (próximo passo)
```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Features e Target
X = df[['temperatura', 'umidade_solo', 'ph_solo', 'nitrogenio', 'fosforo', 'potassio']]
y = df['volume_irrigacao_recomendado']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Treinar
model = LinearRegression()
model.fit(X_train, y_train)
```

---

## 🎓 Dicas para o Projeto FIAP

### Para PARTE 1 (Dashboard Streamlit):
✅ Use `generate_sensor_data.py` para criar 1000+ amostras  
✅ Treine modelos simples de regressão  
✅ Mostre métricas no dashboard  

### Para PARTE 2 (Algoritmos Preditivos):
✅ Gere datasets para múltiplas culturas  
✅ Compare modelos (Linear, Ridge, Random Forest)  
✅ Documente MAE, MSE, RMSE, R²  

### Quantidade Recomendada:
- **Treino**: 800 amostras (80%)
- **Teste**: 200 amostras (20%)
- **Total**: 1000-2000 amostras por cultura

---

## 📚 Próximos Passos

1. ✅ **Gerar dados** (você está aqui!)
2. ⏭️ **Pré-processar** dados (normalização, encoding)
3. ⏭️ **Feature engineering** (criar features derivadas)
4. ⏭️ **Treinar modelos** ML (regressão)
5. ⏭️ **Avaliar modelos** (métricas)
6. ⏭️ **Dashboard Streamlit** (visualização)

---

## 🆘 Suporte

- **Documentação**: [ATIVIDADE_ML_DASHBOARD.md](./ATIVIDADE_ML_DASHBOARD.md)
- **Issues**: Abra issue no GitHub se precisar de ajuda
- **Dúvidas**: Consulte o código comentado

---

**Status**: ✅ Scripts prontos para uso  
**Última atualização**: Outubro 2025  
**Grupo**: FarmTech Solutions - FIAP