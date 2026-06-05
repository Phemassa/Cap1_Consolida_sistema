#!/usr/bin/env python3
"""
🚀 FarmTech Solutions - Teste de Integração Final (Python + R)
═══════════════════════════════════════════════════════════════

OBJETIVO: Demonstrar integração completa entre IR ALÉM 1 (Python) e IR ALÉM 2 (R)

FLUXO TESTADO:
1. Python: Coleta dados climáticos e processa recomendações
2. Python: Gera arquivo CSV com dados processados  
3. R: Lê dados do Python e executa análise estatística
4. R: Treina modelos e gera predições
5. Python: Lê resultados do R e integra com sistema ESP32

Autor: Grupo 59 FIAP
Data: Outubro 2025
"""

import os
import sys
import subprocess
import pandas as pd
import json
from datetime import datetime, timedelta
import numpy as np

# Adiciona o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports dos módulos desenvolvidos
from weather_api import WeatherAPI, SimulatedWeatherAPI
from serial_communication import ESP32SerialCommunication, MockSerialCommunication

class FarmTechIntegrationTest:
    """Classe para teste de integração completa Python + R"""
    
    def __init__(self):
        self.results = {
            'python_weather': None,
            'python_serial': None, 
            'r_analysis': None,
            'integration_success': False
        }
        
        print("🚀 FARMTECH SOLUTIONS - TESTE DE INTEGRAÇÃO FINAL")
        print("=" * 65)
        print("🌱 Testando integração Python (IR ALÉM 1) + R (IR ALÉM 2)")
        print(f"📅 Executado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 65)
        print()
    
    def test_python_weather_system(self):
        """Testa sistema Python de clima"""
        print("🐍 ETAPA 1: Testando sistema Python - Weather API...")
        print("-" * 55)
        
        try:
            # Usa API simulada para testes
            weather_api = SimulatedWeatherAPI()
            
            # Testa múltiplas localizações
            locations = ["São Paulo", "Campinas", "Ribeirão Preto"]
            weather_data = []
            
            for location in locations:
                data = weather_api.get_current_weather(location)
                weather_data.append(data)
                
                print(f"   📍 {location}:")
                print(f"      🌡️ Temperatura: {data['temperature']}°C")
                print(f"      💧 Umidade: {data['humidity']}%")
                print(f"      🌧️ Precipitação: {data['precipitation']}mm")
                print(f"      💨 Vento: {data['wind_speed']} km/h")
            
            self.results['python_weather'] = weather_data
            print("   ✅ Sistema Python Weather funcionando!")
            print()
            return True
            
        except Exception as e:
            print(f"   ❌ Erro no sistema Weather: {str(e)}")
            print()
            return False
    
    def test_python_serial_system(self):
        """Testa sistema Python de comunicação serial"""
        print("📡 ETAPA 2: Testando sistema Python - Serial Communication...")
        print("-" * 55)
        
        try:
            # Usa comunicação mock para testes
            serial_comm = MockSerialCommunication()
            
            # Simula dados do ESP32
            esp32_data = {
                'temperature': 28.5,
                'soil_humidity': 45.2,
                'ph_level': 6.3,
                'npk_nitrogen': 1,
                'npk_phosphorus': 0,
                'npk_potassium': 1,
                'irrigation_status': 0
            }
            
            # Testa envio de dados
            response = serial_comm.send_irrigation_command(esp32_data)
            
            print("   📊 Dados ESP32 simulados:")
            print(f"      🌡️ Temperatura: {esp32_data['temperature']}°C")
            print(f"      💧 Umidade Solo: {esp32_data['soil_humidity']}%")
            print(f"      🧪 pH: {esp32_data['ph_level']}")
            print(f"      🧬 NPK: N={esp32_data['npk_nitrogen']}, P={esp32_data['npk_phosphorus']}, K={esp32_data['npk_potassium']}")
            print(f"      💦 Irrigação: {'Ativada' if esp32_data['irrigation_status'] else 'Desativada'}")
            
            print(f"   📤 Resposta do sistema: {response['status']}")
            print(f"   🎯 Recomendação: {response['recommendation']}")
            
            self.results['python_serial'] = response
            print("   ✅ Sistema Python Serial funcionando!")
            print()
            return True
            
        except Exception as e:
            print(f"   ❌ Erro no sistema Serial: {str(e)}")
            print()
            return False
    
    def create_integrated_dataset(self):
        """Cria dataset integrado para análise R"""
        print("📊 ETAPA 3: Criando dataset integrado Python → R...")
        print("-" * 55)
        
        try:
            # Gera dados sintéticos integrados dos últimos 30 dias
            dates = [datetime.now() - timedelta(days=i) for i in range(30, 0, -1)]
            
            integrated_data = []
            
            for date in dates:
                # Simula variação circadiana
                hour_factor = np.sin(2 * np.pi * date.hour / 24)
                
                record = {
                    'data': date.strftime('%Y-%m-%d'),
                    'hora': date.hour,
                    'timestamp': date.isoformat(),
                    
                    # Dados ambientais (com correlações realistas)
                    'temperatura': round(25 + 5 * hour_factor + np.random.normal(0, 2), 1),
                    'umidade_solo': round(50 - 10 * hour_factor + np.random.normal(0, 5), 1),
                    'ph_solo': round(6.5 + np.random.normal(0, 0.3), 2),
                    'precipitacao': round(max(0, np.random.exponential(2) if np.random.random() > 0.8 else 0), 1),
                    'pressao_atmosferica': round(1013 + np.random.normal(0, 5), 1),
                    'umidade_ar': round(60 + 20 * hour_factor + np.random.normal(0, 8), 1),
                    'vento_kmh': round(max(0, np.random.gamma(2, 1)), 1),
                    
                    # NPK (sensores digitais)
                    'nitrogenio_ok': np.random.random() > 0.3,
                    'fosforo_ok': np.random.random() > 0.35,
                    'potassio_ok': np.random.random() > 0.25,
                    
                    # Decisão de irrigação
                    'irrigacao_realizada': False,  # Será calculado
                    
                    # Metadados
                    'cultura': 'Banana',
                    'fonte': 'Python_Integration_Test'
                }
                
                # Lógica de irrigação
                record['irrigacao_realizada'] = (
                    record['umidade_solo'] < 35 or 
                    (record['temperatura'] > 30 and record['umidade_solo'] < 50) or
                    (record['ph_solo'] < 5.5 or record['ph_solo'] > 7.5)
                )
                
                # Produtividade baseada nos fatores
                prod_score = 70
                prod_score += 10 if abs(record['temperatura'] - 27) < 5 else -10
                prod_score += 15 if 40 <= record['umidade_solo'] <= 70 else -10
                prod_score += 10 if 6.0 <= record['ph_solo'] <= 7.0 else -5
                prod_score += 5 if record['precipitacao'] > 0 else 0
                
                record['produtividade'] = max(20, min(100, prod_score + np.random.normal(0, 8)))
                
                integrated_data.append(record)
            
            # Salva dataset
            df = pd.DataFrame(integrated_data)
            df.to_csv('dados_python_para_r.csv', index=False)
            
            print(f"   📄 Dataset criado: dados_python_para_r.csv")
            print(f"   📊 Registros: {len(df)} observações")
            print(f"   📅 Período: {df['data'].min()} a {df['data'].max()}")
            print(f"   💧 Irrigações: {df['irrigacao_realizada'].sum()}")
            print(f"   📈 Produtividade média: {df['produtividade'].mean():.1f}%")
            print("   ✅ Dataset integrado criado!")
            print()
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao criar dataset: {str(e)}")
            print()
            return False
    
    def run_r_analysis(self):
        """Executa análise R com os dados do Python"""
        print("📊 ETAPA 4: Executando análise R com dados do Python...")
        print("-" * 55)
        
        try:
            # Cria script R temporário para análise
            r_script = """
# Análise R dos dados integrados do Python
library(methods)

# Lê dados do Python
dados <- read.csv('dados_python_para_r.csv', stringsAsFactors = FALSE)

# Converte tipos
dados$data <- as.Date(dados$data)
dados$irrigacao_realizada <- as.logical(dados$irrigacao_realizada)
dados$nitrogenio_ok <- as.logical(dados$nitrogenio_ok)
dados$fosforo_ok <- as.logical(dados$fosforo_ok)  
dados$potassio_ok <- as.logical(dados$potassio_ok)

cat("📊 ANÁLISE R - DADOS INTEGRADOS DO PYTHON\\n")
cat("=" , rep("=", 45), "\\n")

# Estatísticas básicas
cat("\\n📈 Estatísticas Descritivas:\\n")
print(summary(dados[c('temperatura', 'umidade_solo', 'ph_solo', 'produtividade')]))

# Correlações
cor_matriz <- cor(dados[c('temperatura', 'umidade_solo', 'ph_solo', 'produtividade')])
cat("\\n🔗 Correlações Principais:\\n")
cat("Temperatura ↔ Produtividade:", round(cor_matriz['temperatura', 'produtividade'], 3), "\\n")
cat("Umidade ↔ Produtividade:", round(cor_matriz['umidade_solo', 'produtividade'], 3), "\\n")

# Análise NPK
npk_stats <- c(
  mean(dados$nitrogenio_ok) * 100,
  mean(dados$fosforo_ok) * 100, 
  mean(dados$potassio_ok) * 100
)
cat("\\n🧪 Adequação NPK (%):\\n")
cat("N:", round(npk_stats[1], 1), "% | P:", round(npk_stats[2], 1), "% | K:", round(npk_stats[3], 1), "%\\n")

# Modelo simples
modelo <- glm(irrigacao_realizada ~ temperatura + umidade_solo + ph_solo, 
              data = dados, family = binomial)

# Predições
pred <- predict(modelo, type = "response")
acuracia <- mean((pred > 0.5) == dados$irrigacao_realizada)

cat("\\n🤖 Modelo Preditivo:\\n")
cat("Acurácia:", round(acuracia * 100, 1), "%\\n")

# Salva resultados para Python
resultados <- list(
  estatisticas = summary(dados[c('temperatura', 'umidade_solo', 'ph_solo', 'produtividade')]),
  correlacoes = cor_matriz,
  npk_adequacao = npk_stats,
  acuracia_modelo = acuracia,
  irrigacoes_totais = sum(dados$irrigacao_realizada),
  produtividade_media = mean(dados$produtividade)
)

# Salva como JSON para o Python ler
library(jsonlite)
write_json(resultados, "resultados_r_para_python.json")

cat("\\n✅ Análise R concluída! Resultados salvos em resultados_r_para_python.json\\n")
"""
            
            # Salva script R temporário
            with open('temp_analysis.R', 'w', encoding='utf-8') as f:
                f.write(r_script)
            
            # Executa R script
            r_executable = r"C:\Program Files\R\R-4.5.1\bin\x64\Rscript.exe"
            
            if os.path.exists(r_executable):
                result = subprocess.run([r_executable, 'temp_analysis.R'], 
                                      capture_output=True, text=True, encoding='utf-8')
                
                print("   🔍 Saída da análise R:")
                print("   " + result.stdout.replace('\n', '\n   '))
                
                if result.returncode == 0:
                    # Lê resultados do R
                    if os.path.exists('resultados_r_para_python.json'):
                        with open('resultados_r_para_python.json', 'r') as f:
                            r_results = json.load(f)
                        self.results['r_analysis'] = r_results
                        print("   ✅ Análise R executada com sucesso!")
                    else:
                        print("   ⚠️ Análise executou mas arquivo de resultados não encontrado")
                else:
                    print(f"   ❌ Erro na execução R: {result.stderr}")
            else:
                print("   ⚠️ R não encontrado, pulando análise R")
                
            print()
            return True
            
        except Exception as e:
            print(f"   ❌ Erro na análise R: {str(e)}")
            print()
            return False
        finally:
            # Limpa arquivos temporários
            for temp_file in ['temp_analysis.R']:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
    
    def test_python_r_feedback(self):
        """Testa feedback do R para o Python"""
        print("🔄 ETAPA 5: Testando feedback R → Python...")
        print("-" * 55)
        
        try:
            if self.results['r_analysis']:
                r_results = self.results['r_analysis']
                
                # Integra resultados do R no sistema Python
                print("   📊 Resultados recebidos do R:")
                print(f"      🎯 Acurácia do modelo R: {r_results.get('acuracia_modelo', 0) * 100:.1f}%")
                print(f"      💧 Total de irrigações: {r_results.get('irrigacoes_totais', 0)}")
                print(f"      📈 Produtividade média: {r_results.get('produtividade_media', 0):.1f}%")
                
                # Usa resultados do R para otimizar recomendações Python
                if r_results.get('acuracia_modelo', 0) > 0.8:
                    optimization_factor = 1.2  # Modelo confiável, mais agressivo
                else:
                    optimization_factor = 0.8  # Modelo menos confiável, mais conservador
                
                print(f"   🧠 Fator de otimização calculado: {optimization_factor}")
                
                # Testa nova recomendação otimizada
                test_sensor_data = {
                    'temperature': 29.5,
                    'soil_humidity': 42.0,
                    'ph_level': 6.2
                }
                
                # Recomendação Python original
                python_recommendation = "Irrigação recomendada" if test_sensor_data['soil_humidity'] < 45 else "Monitorar"
                
                # Recomendação otimizada com feedback do R
                optimized_recommendation = python_recommendation
                if optimization_factor > 1.0 and "Monitorar" in python_recommendation:
                    optimized_recommendation = "Irrigação preventiva recomendada"
                elif optimization_factor < 1.0 and "Irrigação" in python_recommendation:
                    optimized_recommendation = "Monitorar com atenção"
                
                print(f"   🐍 Recomendação Python original: {python_recommendation}")
                print(f"   🔄 Recomendação otimizada (R+Python): {optimized_recommendation}")
                
                print("   ✅ Feedback R → Python funcionando!")
            else:
                print("   ⚠️ Sem resultados do R para processar")
            
            print()
            return True
            
        except Exception as e:
            print(f"   ❌ Erro no feedback: {str(e)}")
            print()
            return False
    
    def generate_final_report(self):
        """Gera relatório final da integração"""
        print("📋 RELATÓRIO FINAL DE INTEGRAÇÃO")
        print("=" * 65)
        
        # Verifica sucessos
        successes = []
        if self.results['python_weather']: successes.append("Python Weather API")
        if self.results['python_serial']: successes.append("Python Serial Comm")
        if self.results['r_analysis']: successes.append("R Statistical Analysis")
        
        success_rate = len(successes) / 3 * 100
        
        print(f"🎯 Taxa de Sucesso da Integração: {success_rate:.1f}%")
        print()
        
        print("✅ COMPONENTES FUNCIONANDO:")
        for success in successes:
            print(f"   ✅ {success}")
        
        if len(successes) < 3:
            print("\n⚠️ COMPONENTES COM PROBLEMAS:")
            if not self.results['python_weather']: print("   ❌ Python Weather API")
            if not self.results['python_serial']: print("   ❌ Python Serial Communication")
            if not self.results['r_analysis']: print("   ❌ R Statistical Analysis")
        
        print()
        
        if success_rate >= 80:
            print("🏆 INTEGRAÇÃO PYTHON + R FUNCIONANDO CORRETAMENTE!")
            print("🚀 Sistema pronto para produção!")
            self.results['integration_success'] = True
        else:
            print("⚠️ Integração parcial. Alguns componentes precisam de ajustes.")
        
        print("=" * 65)
        
        return self.results['integration_success']
    
    def run_full_integration_test(self):
        """Executa teste completo de integração"""
        success_count = 0
        
        # Executa todos os testes
        if self.test_python_weather_system():
            success_count += 1
        
        if self.test_python_serial_system():
            success_count += 1
            
        if self.create_integrated_dataset():
            success_count += 1
            
        if self.run_r_analysis():
            success_count += 1
            
        if self.test_python_r_feedback():
            success_count += 1
        
        # Relatório final
        final_success = self.generate_final_report()
        
        return final_success, self.results

def main():
    """Função principal"""
    print("Iniciando teste de integração FarmTech Solutions...")
    print()
    
    # Executa teste completo
    tester = FarmTechIntegrationTest()
    success, results = tester.run_full_integration_test()
    
    # Limpa arquivos temporários
    temp_files = ['dados_python_para_r.csv', 'resultados_r_para_python.json']
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    print(f"\n🎉 Teste de integração {'CONCLUÍDO COM SUCESSO' if success else 'FINALIZADO COM PROBLEMAS'}!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)