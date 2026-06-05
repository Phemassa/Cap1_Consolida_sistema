#!/usr/bin/env python3
"""
Demonstração Completa do Sistema de Irrigação Inteligente
FarmTech Solutions - Fase 2 FIAP

Este script demonstra todos os recursos do sistema integrado:
- Simulador ESP32
- Aplicação Flask
- Interface Web
- Automação de irrigação
"""

import os
import sys
import time
import threading
import webbrowser
import subprocess
from datetime import datetime

def print_header():
    """Imprime cabeçalho da demonstração"""
    print("=" * 60)
    print("🌱 SISTEMA DE IRRIGAÇÃO INTELIGENTE 🌱")
    print("FarmTech Solutions - Fase 2 FIAP")
    print("Demonstração Completa do Sistema")
    print("=" * 60)
    print()

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    required_packages = ['flask', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (não instalado)")
            missing_packages.append(package)
    
    if missing_packages:
        print("\n⚠️  Pacotes faltantes detectados!")
        print("Execute o comando abaixo para instalar:")
        print(f"pip install {' '.join(missing_packages)}")
        
        response = input("\nDeseja continuar mesmo assim? (s/n): ")
        if response.lower() != 's':
            return False
    
    print()
    return True

def run_flask_app():
    """Executa a aplicação Flask em thread separada"""
    try:
        # Adiciona diretório ao path
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'web_app'))
        
        # Importa e executa app
        from app import app
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
        
    except Exception as e:
        print(f"❌ Erro ao executar Flask: {e}")

def run_simulator():
    """Executa simulador ESP32 em thread separada"""
    try:
        from flask_bridge import init_bridge
        
        print("🔧 Iniciando simulador ESP32...")
        bridge = init_bridge()
        
        if bridge.start():
            print("  ✅ Simulador iniciado com sucesso!")
            return bridge
        else:
            print("  ❌ Erro ao iniciar simulador!")
            return None
            
    except Exception as e:
        print(f"❌ Erro no simulador: {e}")
        return None

def demonstrate_system(bridge):
    """Demonstra funcionalidades do sistema"""
    print("\n🎯 INICIANDO DEMONSTRAÇÃO...")
    print("-" * 40)
    
    scenarios = [
        {
            'name': 'Condições Ideais',
            'description': 'Todos os parâmetros dentro do ideal',
            'actions': [
                ('nitrogen', True),
                ('phosphorus', True),
                ('potassium', True),
                ('ph', 6.5),
                ('wait', 5)
            ]
        },
        {
            'name': 'Deficiência de NPK',
            'description': 'Solo com carência de nutrientes',
            'actions': [
                ('nitrogen', False),
                ('phosphorus', False),
                ('potassium', False),
                ('wait', 8)
            ]
        },
        {
            'name': 'pH Inadequado',
            'description': 'Solo muito ácido',
            'actions': [
                ('ph', 4.5),
                ('wait', 5)
            ]
        },
        {
            'name': 'Recuperação',
            'description': 'Voltando às condições normais',
            'actions': [
                ('nitrogen', True),
                ('phosphorus', True), 
                ('potassium', True),
                ('ph', 6.2),
                ('wait', 5)
            ]
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📋 Cenário {i}: {scenario['name']}")
        print(f"   {scenario['description']}")
        
        for action, value in scenario['actions']:
            if action == 'wait':
                print(f"   ⏳ Aguardando {value} segundos...")
                for j in range(value):
                    time.sleep(1)
                    print(".", end="", flush=True)
                print()
            
            elif action in ['nitrogen', 'phosphorus', 'potassium']:
                if bridge:
                    if value:
                        bridge.simulate_button_press(action)
                        print(f"   ✅ {action.capitalize()} ativado")
                    else:
                        print(f"   ❌ {action.capitalize()} desativado")
            
            elif action == 'ph':
                if bridge:
                    ldr_value = int((value / 14.0) * 1023)
                    bridge.adjust_ph_sensor(ldr_value)
                    print(f"   📊 pH ajustado para {value}")
        
        # Mostra dados atuais
        if bridge:
            data = bridge.get_current_data()
            show_sensor_data(data)
    
    print("\n✅ Demonstração concluída!")

def show_sensor_data(data):
    """Mostra dados dos sensores formatados"""
    print("\n   📈 Dados atuais dos sensores:")
    
    # NPK
    npk = data.get('npk', {})
    n_status = "✅" if npk.get('nitrogen') else "❌"
    p_status = "✅" if npk.get('phosphorus') else "❌"
    k_status = "✅" if npk.get('potassium') else "❌"
    print(f"      NPK: N{n_status} P{p_status} K{k_status}")
    
    # pH
    ph_level = data.get('ph', {}).get('ph_level', 0)
    ph_status = "✅" if 6.0 <= ph_level <= 6.8 else "⚠️"
    print(f"      pH: {ph_level:.2f} {ph_status}")
    
    # Ambiente
    env = data.get('environment', {})
    temp = env.get('temperature', 0)
    humidity = env.get('humidity', 0)
    print(f"      Temperatura: {temp:.1f}°C")
    print(f"      Umidade: {humidity:.1f}%")
    
    # Bomba
    pump = data.get('actuators', {}).get('irrigation_pump', False)
    pump_status = "💧 LIGADA" if pump else "🚫 DESLIGADA"
    print(f"      Bomba: {pump_status}")

def open_dashboard():
    """Abre o dashboard no navegador"""
    print("🌐 Abrindo dashboard no navegador...")
    time.sleep(3)  # Aguarda Flask iniciar
    try:
        webbrowser.open('http://localhost:5000')
        print("  ✅ Dashboard aberto!")
    except Exception as e:
        print(f"  ⚠️  Erro ao abrir navegador: {e}")
        print("  🔗 Acesse manualmente: http://localhost:5000")

def show_instructions():
    """Mostra instruções para o usuário"""
    print("\n📖 INSTRUÇÕES PARA USO:")
    print("-" * 30)
    print("1. 🌐 Dashboard Web: http://localhost:5000")
    print("2. 📊 Monitore os dados em tempo real")
    print("3. ⚙️  Configure diferentes culturas")
    print("4. 📈 Visualize relatórios e histórico")
    print("5. 🎛️  Use os controles manuais se necessário")
    print()
    print("💡 DICAS:")
    print("- O sistema monitora automaticamente")
    print("- Irrigação ativa quando necessário") 
    print("- Dados são atualizados a cada 3 segundos")
    print("- Histórico mantém últimos 100 registros")
    print()

def main():
    """Função principal da demonstração"""
    print_header()
    
    # Verifica dependências
    if not check_dependencies():
        return
    
    # Configuração inicial
    flask_thread = None
    bridge = None
    
    try:
        print("🚀 Iniciando Sistema Completo...")
        print("-" * 40)
        
        # 1. Inicia simulador ESP32
        bridge = run_simulator()
        if not bridge:
            print("❌ Falha ao iniciar simulador. Saindo...")
            return
        
        # 2. Inicia aplicação Flask
        print("🌐 Iniciando aplicação Flask...")
        flask_thread = threading.Thread(target=run_flask_app, daemon=True)
        flask_thread.start()
        print("  ✅ Flask iniciado em background!")
        
        # 3. Abre dashboard
        dashboard_thread = threading.Thread(target=open_dashboard, daemon=True)
        dashboard_thread.start()
        
        # 4. Mostra instruções
        show_instructions()
        
        # 5. Pergunta se quer demonstração automática
        print("🎯 Opções de demonstração:")
        print("1. Automática - Executa cenários predefinidos")
        print("2. Manual - Você controla o sistema")
        print("3. Apenas monitorar - Sistema livre")
        
        choice = input("\nEscolha uma opção (1-3): ").strip()
        
        if choice == '1':
            demonstrate_system(bridge)
        elif choice == '2':
            manual_control(bridge)
        else:
            monitor_mode(bridge)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrompido pelo usuário")
    
    except Exception as e:
        print(f"\n❌ Erro na demonstração: {e}")
    
    finally:
        # Cleanup
        print("\n🧹 Finalizando sistema...")
        if bridge:
            bridge.stop()
        print("✅ Sistema finalizado!")

def manual_control(bridge):
    """Modo de controle manual"""
    print("\n🎮 MODO CONTROLE MANUAL")
    print("-" * 25)
    print("Comandos disponíveis:")
    print("  n - Toggle Nitrogênio")
    print("  p - Toggle Fósforo") 
    print("  k - Toggle Potássio")
    print("  b - Toggle Bomba")
    print("  d - Mostrar dados")
    print("  q - Sair")
    print()
    
    while True:
        try:
            cmd = input("Digite comando: ").strip().lower()
            
            if cmd == 'q':
                break
            elif cmd == 'n':
                bridge.simulate_button_press('nitrogen')
                print("✅ Nitrogênio alternado")
            elif cmd == 'p':
                bridge.simulate_button_press('phosphorus')
                print("✅ Fósforo alternado")
            elif cmd == 'k':
                bridge.simulate_button_press('potassium')
                print("✅ Potássio alternado")
            elif cmd == 'b':
                data = bridge.get_current_data()
                current_state = data.get('actuators', {}).get('irrigation_pump', False)
                bridge.set_irrigation(not current_state)
                print(f"✅ Bomba {'desligada' if current_state else 'ligada'}")
            elif cmd == 'd':
                data = bridge.get_current_data()
                show_sensor_data(data)
            else:
                print("❌ Comando inválido")
                
        except KeyboardInterrupt:
            break

def monitor_mode(bridge):
    """Modo apenas monitoramento"""
    print("\n📡 MODO MONITORAMENTO")
    print("-" * 20)
    print("Sistema em operação automática...")
    print("Pressione Ctrl+C para sair")
    print()
    
    try:
        while True:
            data = bridge.get_current_data()
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            print(f"\r[{timestamp}] ", end="")
            
            # Status resumido
            npk = data.get('npk', {})
            ph = data.get('ph', {}).get('ph_level', 0)
            pump = data.get('actuators', {}).get('irrigation_pump', False)
            
            npk_count = sum([npk.get('nitrogen', False), 
                           npk.get('phosphorus', False), 
                           npk.get('potassium', False)])
            
            print(f"NPK:{npk_count}/3 pH:{ph:.1f} Bomba:{'ON' if pump else 'OFF'}", 
                  end="", flush=True)
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n")

if __name__ == "__main__":
    main()