# FarmTech Solutions - AI Coding Instructions

## Project Overview
This is a **FIAP academic project** for an IoT-based smart irrigation system targeting agricultural optimization. The project simulates precision agriculture using ESP32 microcontrollers with NPK nutrient monitoring, pH sensing, and automated irrigation control.

## Architecture & Key Components

### Hardware Simulation (Wokwi.com)
- **ESP32 DevKit v1**: Main microcontroller
- **NPK Sensors**: 3 green buttons (GPIO 2, 4, 5) simulating Nitrogen, Phosphorus, Potassium levels
- **pH Sensor**: LDR on analog pin A0 (GPIO 34) with **realistic NPK-pH interaction** (see below)
- **Soil Moisture**: DHT22 on GPIO 21 (simulates soil humidity via air humidity * 0.8)
- **Irrigation Control**: Relay module on GPIO 18 controlling water pump

### NPK-pH Chemical Interaction (v2.0 - Updated 12/10/2025)
**Key Innovation**: Pressing NPK buttons now **automatically adjusts pH** (realistic chemistry):
```cpp
// pH Base from LDR
float pHBase = 9.0 - (ldrValue/4095.0) * 6.0;  // 3.0-9.0

// NPK Adjustments (EMBRAPA data)
float ajustePH = 0.0;
if (nitrogenioOK) ajustePH -= 0.4;  // N acidifies
if (fosforoOK)    ajustePH -= 0.3;  // P acidifies
if (potassioOK)   ajustePH += 0.1;  // K alkalizes

// Final pH
phSolo = constrain(pHBase + ajustePH, 3.0, 9.0);
```
**Documentation**: See `docs/RELACAO_NPK_PH.md` for scientific foundation

### Project Structure
```
Fase2/cursotiaor/pbl/Fase2/Cap 1/
├── FarmTech.ino          # Main ESP32 firmware (527 lines)
├── diagram.json          # Wokwi circuit diagram
├── platformio.ini        # PlatformIO configuration
└── wokwi.toml           # Wokwi simulator settings
```

## Critical Business Logic

### Crop-Specific NPK Requirements
The system supports two crops with distinct nutrient priorities:
- **BANANA** (`CULTURA_BANANA = 0`): Potassium-critical (20 g/m²) - `potassioOK` must be true first
- **MILHO** (`CULTURA_MILHO = 1`): Nitrogen-critical (12 g/m²) - `nitrogenioOK` must be true first

### Irrigation Decision Engine
Located in `decidirIrrigacao()` function with 6 priority conditions:
1. **Soil too dry**: `umidadeSolo < UMIDADE_MINIMA (40%)`
2. **Soil waterlogged**: `umidadeSolo > UMIDADE_MAXIMA (80%)` → NEVER irrigate
3. **NPK insufficient + suboptimal moisture**: Complex crop-specific logic
4. **pH out of range** (5.5-7.5) + low moisture
5. **High temperature** (>30°C) + low moisture
6. **Optimal conditions**: Turn off irrigation

### Key Constants & Thresholds
```cpp
#define UMIDADE_MINIMA 40.0    // Critical irrigation threshold
#define UMIDADE_IDEAL 60.0     // Target moisture level
#define UMIDADE_MAXIMA 80.0    // Prevent overwatering
#define PH_MINIMO 5.5 / PH_MAXIMO 7.5  // Agricultural pH range
```

## Development Workflows

### Wokwi Simulation
- Primary development environment: https://wokwi.com
- Upload `diagram.json` to recreate circuit
- Use Serial Monitor (115200 baud) for real-time debugging
- **Critical**: Manually adjust LDR when changing NPK buttons (no real pH sensor)

### PlatformIO Build Process
```bash
# Install dependencies
pio lib install "adafruit/DHT sensor library@^1.4.4"
# Build firmware
pio run
# Monitor serial output
pio device monitor --baud 115200
```

### Testing Scenarios
- **NPK Testing**: Press/release green buttons, observe `verificarNPKAdequado()` logic
- **pH Simulation**: Cover/uncover LDR to simulate pH 3.0-9.0 range
- **Irrigation Logic**: Monitor relay state changes in Serial output
- **Culture Switching**: Change `culturaAtual` variable to test different crop priorities

## Code Patterns & Conventions

### Sensor Reading Pattern
All sensor functions follow this pattern:
1. Raw hardware read (`digitalRead`, `analogRead`, `dht.readTemperature()`)
2. Mathematical conversion/validation
3. Global variable update
4. Error handling with fallback values

### Serial Output Structure
- **Banner**: System identification and crop selection
- **Status Display**: Structured sensor readings every 5 seconds
- **Irrigation Events**: Visual indicators with motives (`💧💧💧` for ON, `⏸️⏸️⏸️` for OFF)
- **Recommendations**: Context-aware suggestions based on current conditions

### Brazilian Portuguese Labels
- Component labels and output messages use Portuguese
- Technical terms maintain English (NPK, pH, GPIO)
- Comments and function names in English for code readability

## Integration Points

### Serial Communication
- **Baud Rate**: 115200 (consistent across all files)
- **Protocol**: Human-readable status updates every 5 seconds
- **Future Extension**: `Serial.available()` prepared for Python API integration

### External APIs (Optional Enhancement)
- OpenWeather API integration planned for rainfall prediction
- Suspend irrigation during expected rain events
- Located in future Python integration layer

## Academic Context & Constraints

### FIAP Submission Requirements
- **GitHub Structure**: Must follow `meugit/cursotiaor/pbl/fase3/` pattern
- **Documentation**: README.md in Portuguese explaining complete functionality
- **Media**: Wokwi circuit screenshots + 5-minute YouTube video
- **Timeline**: October 15, 2025 deadline with 70% penalty after 3 days

### Data Sources
Use official Brazilian agricultural data:
- EMBRAPA (crop requirements)
- CONAB (agricultural statistics)  
- IBGE (regional data)
- CEPEA (market prices)
- MAPA (policies)

### Anti-Plagiarism
- **Critical**: Never copy-paste from AI tools without modification
- All generated code must be reviewed, understood, and adapted
- Original analysis and commentary required in documentation

## Common Development Tasks

### Adding New Sensors
1. Define GPIO pin in configuration section
2. Add reading logic in `lerSensores()`
3. Update decision logic in `decidirIrrigacao()`
4. Modify status display in `exibirStatus()`
5. Update Wokwi `diagram.json` with new component

### Crop Addition
1. Add constants for NPK requirements (research EMBRAPA data)
2. Update `verificarNPKAdequado()` with crop-specific logic
3. Add display function like `exibirRequisitosBanana()`
4. Test thoroughly with different sensor combinations

### Debugging Tips
- Monitor `contadorLeituras` for timing issues
- Check `releLigado` state vs actual GPIO output
- Validate sensor readings before decision logic
- Use `millis()` timestamps for performance analysis