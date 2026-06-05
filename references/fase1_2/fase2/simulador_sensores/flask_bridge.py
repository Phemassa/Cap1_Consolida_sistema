"""
Integração Flask + ESP32 Simulator
Sistema de Irrigação Inteligente FarmTech Solutions

Este módulo conecta o simulador ESP32 com a aplicação Flask,
permitindo controle e monitoramento em tempo real.
"""

import threading
import time
import json
import logging
from datetime import datetime
from esp32_simulator import ESP32Simulator, SerialCommunication

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FlaskESP32Bridge:
    """Ponte entre Flask e ESP32 Simulator"""
    
    def __init__(self, flask_app=None):
        """
        Inicializa a ponte Flask-ESP32
        
        Args:
            flask_app: Instância da aplicação Flask (opcional)
        """
        self.esp32 = ESP32Simulator()
        self.serial = SerialCommunication(self.esp32)
        self.flask_app = flask_app
        
        # Cache de dados para a aplicação web
        self.latest_data = {}
        self.data_history = []
        self.max_history = 100  # Máximo de registros no histórico
        
        # Estados de controle
        self.is_running = False
        self.update_thread = None
        self.update_interval = 3.0  # segundos
        
        # Configurações de irrigação
        self.auto_irrigation = True
        self.manual_override = False
        
    def start(self):
        """Inicia a ponte e o simulador ESP32"""
        try:
            logger.info("Iniciando ponte Flask-ESP32...")
            
            # Inicia simulador ESP32
            self.esp32.start_simulation()
            
            # Inicia thread de atualização
            self.is_running = True
            self.update_thread = threading.Thread(target=self._update_loop)
            self.update_thread.daemon = True
            self.update_thread.start()
            
            logger.info("Ponte iniciada com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao iniciar ponte: {e}")
            return False
    
    def stop(self):
        """Para a ponte e o simulador"""
        try:
            logger.info("Parando ponte Flask-ESP32...")
            
            self.is_running = False
            
            if self.update_thread and self.update_thread.is_alive():
                self.update_thread.join(timeout=5.0)
            
            self.esp32.stop_simulation()
            
            logger.info("Ponte parada com sucesso!")
            
        except Exception as e:
            logger.error(f"Erro ao parar ponte: {e}")
    
    def _update_loop(self):
        """Loop principal de atualização de dados"""
        while self.is_running:
            try:
                # Obtém dados atuais do ESP32
                response = self.serial.send_command("GET_SENSORS")
                data = json.loads(response)
                
                # Atualiza cache
                self.latest_data = data
                
                # Adiciona ao histórico
                self._add_to_history(data)
                
                # Verifica necessidade de irrigação automática
                if self.auto_irrigation and not self.manual_override:
                    self._check_auto_irrigation(data)
                
                # Emite evento para Flask (se disponível)
                if self.flask_app:
                    self._emit_flask_event(data)
                
            except Exception as e:
                logger.error(f"Erro no loop de atualização: {e}")
            
            time.sleep(self.update_interval)
    
    def _add_to_history(self, data):
        """Adiciona dados ao histórico"""
        # Adiciona timestamp se não existir
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        
        self.data_history.append(data)
        
        # Mantém apenas os últimos registros
        if len(self.data_history) > self.max_history:
            self.data_history.pop(0)
    
    def _check_auto_irrigation(self, data):
        """Verifica necessidade de irrigação automática"""
        try:
            # Extrai dados dos sensores
            npk = data.get('npk', {})
            ph_level = data.get('ph', {}).get('ph_level', 7.0)
            temp = data.get('environment', {}).get('temperature', 25.0)
            humidity = data.get('environment', {}).get('humidity', 60.0)
            
            # Parâmetros ideais (tomate por padrão)
            ideal_conditions = {
                'ph_min': 6.0,
                'ph_max': 6.8,
                'humidity_min': 60.0,
                'temp_min': 18.0,
                'temp_max': 26.0,
                'needs_npk': True
            }
            
            needs_irrigation = False
            reasons = []
            
            # Verifica condições
            if ph_level < ideal_conditions['ph_min'] or ph_level > ideal_conditions['ph_max']:
                needs_irrigation = True
                reasons.append(f"pH inadequado ({ph_level:.2f})")
            
            if humidity < ideal_conditions['humidity_min']:
                needs_irrigation = True
                reasons.append(f"Baixa umidade ({humidity:.1f}%)")
            
            if temp < ideal_conditions['temp_min'] or temp > ideal_conditions['temp_max']:
                needs_irrigation = True
                reasons.append(f"Temperatura inadequada ({temp:.1f}°C)")
            
            if ideal_conditions['needs_npk']:
                if not npk.get('nitrogen', False):
                    needs_irrigation = True
                    reasons.append("Falta Nitrogênio")
                if not npk.get('phosphorus', False):
                    needs_irrigation = True
                    reasons.append("Falta Fósforo")
                if not npk.get('potassium', False):
                    needs_irrigation = True
                    reasons.append("Falta Potássio")
            
            # Atua no sistema de irrigação
            current_state = data.get('actuators', {}).get('irrigation_pump', False)
            
            if needs_irrigation and not current_state:
                logger.info(f"Ativando irrigação automática: {', '.join(reasons)}")
                self.set_irrigation(True)
            elif not needs_irrigation and current_state:
                logger.info("Desativando irrigação - condições ideais")
                self.set_irrigation(False)
                
        except Exception as e:
            logger.error(f"Erro na verificação de irrigação: {e}")
    
    def _emit_flask_event(self, data):
        """Emite evento para Flask (implementar se necessário)"""
        # Implementar se usando Flask-SocketIO para updates em tempo real
        pass
    
    def get_current_data(self):
        """Retorna dados atuais dos sensores"""
        if not self.latest_data:
            # Se não há dados, força uma leitura
            try:
                response = self.serial.send_command("GET_SENSORS")
                self.latest_data = json.loads(response)
            except:
                # Retorna dados padrão em caso de erro
                return self._get_default_data()
        
        return self.latest_data.copy()
    
    def get_history(self, limit=None):
        """
        Retorna histórico de dados
        
        Args:
            limit: Número máximo de registros (None = todos)
        """
        if limit:
            return self.data_history[-limit:]
        return self.data_history.copy()
    
    def set_irrigation(self, state):
        """
        Controla irrigação manualmente
        
        Args:
            state: True para ligar, False para desligar
        """
        try:
            command = f"SET_RELAY:{'ON' if state else 'OFF'}"
            response = self.serial.send_command(command)
            
            logger.info(f"Irrigação {'ligada' if state else 'desligada'} manualmente")
            
            # Atualiza override manual
            self.manual_override = True
            
            # Remove override após 60 segundos
            def remove_override():
                time.sleep(60)
                self.manual_override = False
                logger.info("Override manual removido")
            
            threading.Thread(target=remove_override, daemon=True).start()
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao controlar irrigação: {e}")
            return False
    
    def simulate_button_press(self, button):
        """
        Simula pressão de botão NPK
        
        Args:
            button: 'nitrogen', 'phosphorus' ou 'potassium'
        """
        try:
            command = f"PRESS_BUTTON:{button}"
            response = self.serial.send_command(command)
            logger.info(f"Botão {button} simulado")
            return True
        except Exception as e:
            logger.error(f"Erro ao simular botão: {e}")
            return False
    
    def adjust_ph_sensor(self, value):
        """
        Ajusta sensor de pH manualmente
        
        Args:
            value: Valor 0-1023 para o LDR
        """
        try:
            command = f"SET_LDR:{value}"
            response = self.serial.send_command(command)
            ph = (value / 1023.0) * 14.0
            logger.info(f"Sensor pH ajustado: LDR={value}, pH={ph:.2f}")
            return True
        except Exception as e:
            logger.error(f"Erro ao ajustar pH: {e}")
            return False
    
    def set_auto_irrigation(self, enabled):
        """
        Habilita/desabilita irrigação automática
        
        Args:
            enabled: True para habilitar, False para desabilitar
        """
        self.auto_irrigation = enabled
        logger.info(f"Irrigação automática {'habilitada' if enabled else 'desabilitada'}")
    
    def get_system_status(self):
        """Retorna status do sistema"""
        return {
            'esp32_running': self.esp32.running,
            'bridge_running': self.is_running,
            'auto_irrigation': self.auto_irrigation,
            'manual_override': self.manual_override,
            'data_points': len(self.data_history),
            'last_update': self.latest_data.get('timestamp', 'N/A')
        }
    
    def _get_default_data(self):
        """Retorna dados padrão para casos de erro"""
        return {
            'timestamp': datetime.now().isoformat(),
            'npk': {
                'nitrogen': False,
                'phosphorus': False,
                'potassium': False
            },
            'ph': {
                'raw_value': 512,
                'ph_level': 7.0
            },
            'environment': {
                'temperature': 25.0,
                'humidity': 60.0
            },
            'actuators': {
                'irrigation_pump': False
            }
        }

# Instância global para uso na aplicação Flask
bridge = None

def init_bridge(flask_app=None):
    """Inicializa a ponte Flask-ESP32"""
    global bridge
    bridge = FlaskESP32Bridge(flask_app)
    return bridge

def get_bridge():
    """Obtém instância da ponte"""
    global bridge
    return bridge

if __name__ == "__main__":
    # Teste standalone da ponte
    print("Testando ponte Flask-ESP32...")
    
    bridge = FlaskESP32Bridge()
    
    try:
        # Inicia ponte
        bridge.start()
        
        # Testa por 30 segundos
        for i in range(10):
            time.sleep(3)
            data = bridge.get_current_data()
            print(f"\nDados {i+1}:")
            print(f"  pH: {data.get('ph', {}).get('ph_level', 0):.2f}")
            print(f"  Temp: {data.get('environment', {}).get('temperature', 0):.1f}°C")
            print(f"  Umidade: {data.get('environment', {}).get('humidity', 0):.1f}%")
            print(f"  Bomba: {'ON' if data.get('actuators', {}).get('irrigation_pump') else 'OFF'}")
        
        # Testa controles
        print("\nTestando controles...")
        bridge.simulate_button_press('nitrogen')
        time.sleep(2)
        bridge.set_irrigation(True)
        time.sleep(3)
        bridge.set_irrigation(False)
        
    except KeyboardInterrupt:
        print("\nEncerrando teste...")
    
    finally:
        bridge.stop()
    
    print("Teste concluído!")