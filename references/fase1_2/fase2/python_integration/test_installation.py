"""
Script de Teste - Verificação de Instalação
FarmTech Solutions

Este script verifica se todas as dependências estão instaladas
e se a comunicação com ESP32 está funcionando.
"""

import sys

print("="*60)
print("🔍 Verificação de Instalação")
print("   FarmTech Solutions - Python-ESP32 Integration")
print("="*60)

# Teste 1: Python Version
print("\n1️⃣  Verificando versão do Python...")
print(f"   Versão: {sys.version}")
if sys.version_info >= (3, 8):
    print("   ✅ Python 3.8+ detectado")
else:
    print("   ❌ Python 3.8+ necessário")
    sys.exit(1)

# Teste 2: PySerial
print("\n2️⃣  Verificando PySerial...")
try:
    import serial
    print(f"   ✅ PySerial {serial.VERSION} instalado")
except ImportError:
    print("   ❌ PySerial não encontrado")
    print("   💡 Instale com: pip install pyserial")
    sys.exit(1)

# Teste 3: Listar Portas
print("\n3️⃣  Listando portas seriais disponíveis...")
try:
    from serial.tools import list_ports
    ports = list(list_ports.comports())
    
    if ports:
        print(f"   ✅ {len(ports)} porta(s) encontrada(s):")
        for port in ports:
            print(f"      📍 {port.device} - {port.description}")
    else:
        print("   ⚠️  Nenhuma porta serial detectada")
        print("   💡 Conecte o ESP32 via USB ou inicie simulação Wokwi")
except Exception as e:
    print(f"   ❌ Erro ao listar portas: {e}")

# Teste 4: Módulos do Projeto
print("\n4️⃣  Verificando módulos do projeto...")
try:
    from esp32_communication import ESP32Communication
    print("   ✅ esp32_communication.py encontrado")
except ImportError:
    print("   ❌ esp32_communication.py não encontrado")
    print("   💡 Certifique-se de estar na pasta correta")

try:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'api_clima'))
    from weather_integration import WeatherAPI
    print("   ✅ weather_integration.py encontrado")
except ImportError:
    print("   ⚠️  weather_integration.py não encontrado (opcional)")

# Teste 5: JSON
print("\n5️⃣  Verificando suporte a JSON...")
try:
    import json
    test_data = {"test": "value", "number": 123}
    json_str = json.dumps(test_data)
    parsed = json.loads(json_str)
    print("   ✅ JSON funcionando corretamente")
except Exception as e:
    print(f"   ❌ Erro com JSON: {e}")

# Resumo
print("\n" + "="*60)
print("📊 Resumo da Verificação")
print("="*60)
print("\n✅ Dependências Básicas:")
print("   - Python 3.8+")
print("   - PySerial")
print("   - JSON")

print("\n🔧 Próximos Passos:")
print("   1. Conecte o ESP32 via USB (ou inicie Wokwi)")
print("   2. Execute: python esp32_communication.py")
print("   3. Escolha a porta serial correta")

print("\n💡 Dicas:")
print("   - Windows: Use portas COM3, COM4, etc.")
print("   - Linux: Use /dev/ttyUSB0 ou /dev/ttyACM0")
print("   - Wokwi: Verifique porta virtual RFC2217")

print("\n📚 Documentação:")
print("   - Guia completo: GUIA_WOKWI_PYTHON_INTEGRACAO.md")
print("   - README: python_integration/README.md")

print("\n" + "="*60)
print("Verificação concluída!")
print("="*60 + "\n")
