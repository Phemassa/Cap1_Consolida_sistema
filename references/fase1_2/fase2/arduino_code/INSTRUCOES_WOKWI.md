# Como usar o Sistema no Wokwi.com

## Configuração no Wokwi

### Passo 1: Criar novo projeto
1. Acesse [wokwi.com](https://wokwi.com)
2. Clique em "New Project"
3. Selecione "Arduino ESP32"

### Passo 2: Configurar o hardware
1. Copie o conteúdo do arquivo `wokwi_diagram.json`
2. No Wokwi, clique no ícone de configuração (⚙️)
3. Cole o JSON na área de diagrama
4. O circuito será montado automaticamente

### Passo 3: Adicionar o código
1. Copie todo o conteúdo do arquivo `farm_irrigation_system.ino`
2. Cole no editor de código do Wokwi
3. Clique em "Start Simulation"

## Componentes do Sistema

### 🟢 Botões NPK (Verdes)
- **Nitrogênio**: Pino D2 - Simula presença de nitrogênio no solo
- **Fósforo**: Pino D4 - Simula presença de fósforo no solo  
- **Potássio**: Pino D5 - Simula presença de potássio no solo

### 📊 Sensor LDR (pH)
- **Pino**: A0 (Analógico)
- **Função**: Simula medição de pH do solo
- **Conversão**: 0-1023 → 0-14 pH
- Clique e arraste para alterar a luminosidade

### 🌡️ Sensor DHT22
- **Pino**: D21
- **Função**: Temperatura e umidade do ar
- Clique no sensor para alterar os valores

### 💧 Relé da Bomba
- **Pino**: D18
- **Função**: Controla a bomba d'água
- LED azul indica quando está ativa

### 💡 LED Status
- **Pino**: D23
- **Função**: Indica que o sistema está funcionando
- Pisca durante as leituras dos sensores

## Como Testar o Sistema

### 1. Monitor Serial
- Abra o Monitor Serial (ícone de terminal)
- Velocidade: 115200 baud
- Observe as mensagens do sistema

### 2. Comandos Disponíveis
Digite no Monitor Serial:

```
GET_SENSORS       - Retorna dados em JSON
SET_RELAY:ON      - Liga a bomba manualmente
SET_RELAY:OFF     - Desliga a bomba
PRINT_DATA        - Mostra dados formatados
SET_CULTURE:0     - Muda para Tomate
SET_CULTURE:1     - Muda para Milho
SET_CULTURE:2     - Muda para Soja
SET_CULTURE:3     - Muda para Banana  
SET_CULTURE:4     - Muda para Café
CHECK_IRRIGATION  - Força verificação de irrigação
HELP              - Lista todos os comandos
```

### 3. Teste Automático
1. Inicie a simulação
2. Observe a leitura inicial no Serial Monitor
3. Pressione os botões NPK para simular deficiência
4. Altere o LDR para mudar o pH
5. Modifique temperatura/umidade no DHT22
6. O sistema irá automaticamente ligar/desligar a bomba

### 4. Cenários de Teste

#### Cenário 1: Solo com deficiência de NPK
1. Configure cultura: `SET_CULTURE:0` (Tomate)
2. Não pressione nenhum botão NPK
3. Sistema deve ativar irrigação automaticamente

#### Cenário 2: pH inadequado
1. Altere o LDR para simular pH ácido (< 6.0) ou básico (> 6.8)
2. Sistema deve detectar e ativar irrigação

#### Cenário 3: Baixa umidade
1. Configure DHT22 para umidade < 60%
2. Sistema deve ativar irrigação

#### Cenário 4: Condições ideais
1. Pressione todos os botões NPK
2. Configure pH entre 6.0-6.8
3. Umidade > 60%
4. Temperatura entre 18-26°C
5. Sistema deve manter bomba desligada

## Integração com Flask

O simulador Python `esp32_simulator.py` pode ser usado junto com a aplicação Flask:

### 1. Execute o simulador:
```bash
cd "c:\Fiap Projeto\FarmTechSolutions\fase2\simulador_sensores"
python esp32_simulator.py
```

### 2. Execute a aplicação Flask:
```bash
cd "c:\Fiap Projeto\FarmTechSolutions\fase2\web_app"
python app.py
```

### 3. Acesse o dashboard:
- Abra o navegador em `http://localhost:5000`
- Monitore os dados em tempo real
- Configure diferentes culturas
- Visualize histórico e relatórios

## Parâmetros das Culturas

| Cultura | pH Min | pH Max | Umidade Min | Temp Min | Temp Max | NPK Necessário |
|---------|--------|--------|-------------|----------|----------|----------------|
| Tomate  | 6.0    | 6.8    | 60%         | 18°C     | 26°C     | N, P, K       |
| Milho   | 6.0    | 7.0    | 55%         | 20°C     | 30°C     | N, P, K       |
| Soja    | 6.0    | 7.0    | 50%         | 22°C     | 28°C     | P, K          |
| Banana  | 5.5    | 6.5    | 65%         | 24°C     | 30°C     | N, P, K       |
| Café    | 6.0    | 6.5    | 70%         | 18°C     | 24°C     | N, P          |

## Troubleshooting

### Problema: Sensor DHT22 retorna NaN
- **Solução**: Valores padrão são usados (25°C, 60%)
- É normal na simulação

### Problema: Botões não respondem
- **Solução**: Verifique se está pressionando corretamente
- Use debounce de 50ms

### Problema: JSON não válido
- **Solução**: Verifique se o ArduinoJson está instalado
- No Wokwi já está incluído automaticamente

### Problema: Irrigação não ativa automaticamente
- **Solução**: Aguarde 30 segundos (intervalo de verificação)
- Use comando `CHECK_IRRIGATION` para forçar

## Links Úteis

- [Wokwi.com](https://wokwi.com) - Simulador online
- [Documentação DHT22](https://wokwi.com/parts/wokwi-dht22)
- [Documentação ESP32](https://wokwi.com/parts/wokwi-esp32-devkit-v1)
- [ArduinoJson Library](https://arduinojson.org/)

## Demonstração Completa

Para uma demonstração completa do sistema:

1. Configure o Wokwi com o código fornecido
2. Execute o simulador Python em paralelo  
3. Rode a aplicação Flask
4. Compare os dados entre Wokwi e o dashboard web
5. Teste diferentes cenários de irrigação
6. Demonstre a automação inteligente do sistema

O sistema está pronto para apresentação acadêmica e demonstra todos os conceitos de IoT, automação e agricultura inteligente conforme solicitado no projeto FIAP.