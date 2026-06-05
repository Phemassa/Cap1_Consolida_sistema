#!/usr/bin/env python3
"""
Demo Rápida - FarmTech Solutions
Demonstração rápida da comunicação Python-ESP32

Execute este script para ver uma demonstração rápida do sistema.
"""

import time
import sys
import os

# Banner
print("\n" + "="*70)
print(" "*20 + "🌾 FarmTech Solutions 🌾")
print(" "*15 + "Sistema de Irrigação Inteligente")
print(" "*18 + "Demo Rápida - Fase 2")
print("="*70 + "\n")

# Verificar instalação
print("📋 Verificando instalação...")

try:
    import serial
    print("✅ PySerial instalado")
except ImportError:
    print("❌ PySerial não encontrado!")
    print("\n💡 Execute: pip install pyserial")
    input("\nPressione Enter para sair...")
    sys.exit(1)

try:
    from esp32_communication import ESP32Communication
    print("✅ Módulo de comunicação encontrado")
except ImportError:
    print("❌ Módulo esp32_communication não encontrado!")
    print("\n💡 Certifique-se de estar na pasta: fase2/python_integration")
    input("\nPressione Enter para sair...")
    sys.exit(1)

print("\n" + "="*70)
print("🚀 Iniciando Demo...")
print("="*70 + "\n")

# Menu de demo
print("Escolha o modo de demonstração:\n")
print("1. 🔍 Leitura Única de Dados")
print("   └─► Conecta, lê dados e desconecta")
print()
print("2. 💧 Teste de Bomba")
print("   └─► Liga bomba por 5 segundos e desliga")
print()
print("3. 🔄 Monitoramento Contínuo")
print("   └─► Monitora dados a cada 10 segundos")
print()
print("4. 🧪 Teste Completo")
print("   └─► Executa todos os comandos disponíveis")
print()
print("5. 🎯 Menu Interativo Completo")
print("   └─► Abre menu com todas as opções")
print()
print("6. ❌ Sair")

choice = input("\nEscolha uma opção (1-6): ").strip()

if choice not in ['1', '2', '3', '4', '5']:
    print("\n👋 Até logo!")
    sys.exit(0)

# Solicitar porta
print("\n" + "-"*70)
port = input("Porta serial do ESP32 [COM3]: ").strip() or "COM3"

# Criar conexão
print(f"\n🔌 Conectando em {port}...")
esp = ESP32Communication(port=port)

if not esp.connect():
    print("\n❌ Falha na conexão!")
    print("\n💡 Dicas:")
    print("   1. Verifique se o ESP32 está conectado")
    print("   2. Confirme a porta no Gerenciador de Dispositivos")
    print("   3. Inicie a simulação Wokwi se estiver usando VS Code")
    input("\nPressione Enter para sair...")
    sys.exit(1)

# Aguarda estabilização
print("⏳ Aguardando estabilização...")
time.sleep(2)

try:
    if choice == '1':
        # Demo 1: Leitura única
        print("\n" + "="*70)
        print("📊 DEMO 1: Leitura Única de Dados")
        print("="*70)
        
        print("\n🔄 Solicitando dados do ESP32...")
        data = esp.get_sensor_data()
        
        if data:
            esp.display_sensor_data(data)
            print("✅ Demo concluída com sucesso!")
        else:
            print("❌ Erro ao obter dados")
    
    elif choice == '2':
        # Demo 2: Teste de bomba
        print("\n" + "="*70)
        print("💧 DEMO 2: Teste de Bomba")
        print("="*70)
        
        print("\n🟢 Ligando bomba...")
        esp.set_relay(True)
        time.sleep(1)
        response = esp.read_line(timeout=1.0)
        if response:
            print(f"   ESP32: {response}")
        
        print("\n⏳ Aguardando 5 segundos...")
        for i in range(5, 0, -1):
            print(f"   {i}...", end="\r")
            time.sleep(1)
        
        print("\n🔴 Desligando bomba...")
        esp.set_relay(False)
        time.sleep(1)
        response = esp.read_line(timeout=1.0)
        if response:
            print(f"   ESP32: {response}")
        
        print("\n✅ Teste de bomba concluído!")
    
    elif choice == '3':
        # Demo 3: Monitoramento contínuo
        print("\n" + "="*70)
        print("🔄 DEMO 3: Monitoramento Contínuo")
        print("="*70)
        print("\n⚠️  Pressione Ctrl+C para parar\n")
        
        esp.monitor_continuous(interval=10, duration=60)
        
        print("\n✅ Monitoramento concluído!")
    
    elif choice == '4':
        # Demo 4: Teste completo
        print("\n" + "="*70)
        print("🧪 DEMO 4: Teste Completo de Comandos")
        print("="*70)
        
        tests = [
            ("GET_STATUS", "Status do sistema"),
            ("GET_SENSORS", "Dados dos sensores"),
            ("SET_CULTURE:3", "Mudar para cultura Banana"),
            ("CHECK_IRRIGATION", "Verificar necessidade de irrigação"),
            ("SET_RELAY:ON", "Ligar bomba"),
            ("SET_RELAY:OFF", "Desligar bomba"),
        ]
        
        for i, (command, description) in enumerate(tests, 1):
            print(f"\n[{i}/{len(tests)}] {description}")
            print(f"    Comando: {command}")
            
            esp.send_command(command)
            time.sleep(1)
            
            # Lê múltiplas respostas
            for _ in range(5):
                line = esp.read_line(timeout=0.5)
                if line:
                    if command == "GET_SENSORS" and line.startswith('{'):
                        # Parse JSON
                        import json
                        try:
                            data = json.loads(line)
                            print(f"    ✅ JSON recebido: {len(line)} bytes")
                        except:
                            print(f"    📄 {line}")
                    else:
                        print(f"    📄 {line}")
            
            time.sleep(1)
        
        print("\n✅ Todos os testes executados!")
    
    elif choice == '5':
        # Demo 5: Menu interativo
        print("\n" + "="*70)
        print("🎯 DEMO 5: Menu Interativo Completo")
        print("="*70)
        print("\nAbrindo menu interativo...\n")
        
        from esp32_communication import interactive_menu
        interactive_menu(esp)

except KeyboardInterrupt:
    print("\n\n⚠️  Interrompido pelo usuário")

finally:
    print("\n" + "="*70)
    print("🔌 Desconectando...")
    esp.disconnect()
    print("="*70)
    print("\n✅ Demo finalizada!")
    print("\n📚 Para mais informações:")
    print("   - Guia completo: GUIA_WOKWI_PYTHON_INTEGRACAO.md")
    print("   - README: python_integration/README.md")
    print("\n" + "="*70 + "\n")

input("Pressione Enter para sair...")
