"""
FarmTech Solutions - Gerador de Dados Simulados
================================================
Gera dados realistas dos sensores ESP32/Wokwi para treinamento de ML
Simula comportamento agrícola real com padrões e variações
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import random

class SensorSimulator:
    """Simula leituras dos sensores do FarmTech"""
    
    def __init__(self, cultura="banana"):
        self.cultura = cultura
        self.timestamp_start = datetime.now()
        
    def simulate_readings(self, num_samples=1000, interval_seconds=5):
        """
        Gera leituras simuladas dos sensores
        
        Args:
            num_samples: Número de amostras a gerar
            interval_seconds: Intervalo entre leituras (segundos)
        
        Returns:
            DataFrame com dados simulados
        """
        data = []
        current_time = self.timestamp_start
        
        # Estado inicial
        temperatura_base = 25.0
        umidade_base = 60.0
        ph_base = 6.5
        irrigacao_ativa = False
        
        for i in range(num_samples):
            # Simula variação diária (temperatura aumenta durante o dia)
            hora_do_dia = (current_time.hour + current_time.minute/60.0)
            variacao_temperatura = 5 * np.sin((hora_do_dia - 6) * np.pi / 12)
            
            # Temperatura: 20-35°C com variação diurna
            temperatura = temperatura_base + variacao_temperatura + np.random.normal(0, 0.5)
            temperatura = np.clip(temperatura, 18, 38)
            
            # Umidade do solo: diminui com temperatura, aumenta com irrigação
            if irrigacao_ativa:
                umidade_base = min(umidade_base + 2, 85)
            else:
                umidade_base = max(umidade_base - 0.5, 30)
            
            umidade_solo = umidade_base + np.random.normal(0, 2)
            umidade_solo = np.clip(umidade_solo, 25, 90)
            
            # pH: varia lentamente, influenciado por NPK
            ph_variacao = np.random.normal(0, 0.1)
            ph_solo = np.clip(ph_base + ph_variacao, 5.0, 8.0)
            
            # NPK: simulação baseada na cultura
            if self.cultura == "banana":
                # Banana precisa mais K (potássio)
                nitrogenio = random.choice([True, True, False])
                fosforo = random.choice([True, True, False])
                potassio = random.choice([True, False, False])  # Mais crítico
            else:  # milho
                # Milho precisa mais N (nitrogênio)
                nitrogenio = random.choice([True, False, False])  # Mais crítico
                fosforo = random.choice([True, True, False])
                potassio = random.choice([True, True, False])
            
            # Ajusta pH baseado em NPK (química real)
            if nitrogenio:
                ph_base -= 0.05  # N acidifica
            if fosforo:
                ph_base -= 0.03  # P acidifica
            if potassio:
                ph_base += 0.02  # K alcaliniza
            
            ph_base = np.clip(ph_base, 5.5, 7.5)
            
            # Decisão de irrigação (lógica simplificada)
            if umidade_solo < 40:
                irrigacao_ativa = True
            elif umidade_solo > 75:
                irrigacao_ativa = False
            
            # Registra leitura
            reading = {
                'timestamp': current_time,
                'temperatura': round(temperatura, 1),
                'umidade_solo': round(umidade_solo, 1),
                'ph_solo': round(ph_solo, 2),
                'nitrogenio': int(nitrogenio),
                'fosforo': int(fosforo),
                'potassio': int(potassio),
                'irrigacao_ativa': int(irrigacao_ativa),
                'cultura': self.cultura
            }
            
            data.append(reading)
            current_time += timedelta(seconds=interval_seconds)
        
        return pd.DataFrame(data)
    
    def add_target_variables(self, df):
        """
        Adiciona variáveis target para ML (o que queremos prever)
        """
        # Volume de irrigação recomendado (litros/m²)
        df['volume_irrigacao_recomendado'] = df.apply(
            lambda row: self._calcular_volume_irrigacao(row), axis=1
        )
        
        # Dosagem NPK recomendada (g/m²)
        df['dosagem_n_recomendada'] = df.apply(
            lambda row: 0 if row['nitrogenio'] else (12 if row['cultura'] == 'milho' else 15),
            axis=1
        )
        df['dosagem_p_recomendada'] = df.apply(
            lambda row: 0 if row['fosforo'] else (8 if row['cultura'] == 'milho' else 10),
            axis=1
        )
        df['dosagem_k_recomendada'] = df.apply(
            lambda row: 0 if row['potassio'] else (10 if row['cultura'] == 'milho' else 20),
            axis=1
        )
        
        # Rendimento estimado (kg/hectare) - baseado nas condições
        df['rendimento_estimado'] = df.apply(
            lambda row: self._estimar_rendimento(row), axis=1
        )
        
        return df
    
    def _calcular_volume_irrigacao(self, row):
        """Calcula volume de irrigação necessário"""
        if row['umidade_solo'] > 70:
            return 0.0
        elif row['umidade_solo'] < 40:
            volume = 15 - (row['umidade_solo'] * 0.2)
        else:
            volume = 8 - (row['umidade_solo'] * 0.1)
        
        # Ajusta por temperatura
        if row['temperatura'] > 30:
            volume += 2
        
        return round(max(0, volume), 1)
    
    def _estimar_rendimento(self, row):
        """Estima rendimento baseado nas condições"""
        # Rendimento base por cultura
        base_rendimento = 25000 if row['cultura'] == 'banana' else 8000  # kg/ha
        
        # Fatores multiplicadores
        fator_umidade = 1.0 if 50 <= row['umidade_solo'] <= 70 else 0.8
        fator_ph = 1.0 if 6.0 <= row['ph_solo'] <= 7.0 else 0.85
        fator_temperatura = 1.0 if 20 <= row['temperatura'] <= 30 else 0.9
        
        fator_npk = (
            (0.9 if row['nitrogenio'] else 0.7) *
            (0.9 if row['fosforo'] else 0.8) *
            (0.9 if row['potassio'] else 0.7)
        )
        
        rendimento = base_rendimento * fator_umidade * fator_ph * fator_temperatura * fator_npk
        return round(rendimento + np.random.normal(0, 500), 0)


def gerar_dados_simulados(num_samples=1000, cultura="banana", output_format="csv"):
    """
    Função principal para gerar dados simulados
    
    Args:
        num_samples: Número de amostras
        cultura: 'banana' ou 'milho'
        output_format: 'csv' ou 'json'
    
    Returns:
        DataFrame com dados simulados
    """
    print(f"🌾 Gerando {num_samples} amostras para cultura: {cultura.upper()}")
    
    simulator = SensorSimulator(cultura=cultura)
    df = simulator.simulate_readings(num_samples)
    df = simulator.add_target_variables(df)
    
    # Estatísticas
    print("\n📊 Estatísticas dos Dados Gerados:")
    print(f"   Temperatura: {df['temperatura'].min():.1f}°C - {df['temperatura'].max():.1f}°C")
    print(f"   Umidade Solo: {df['umidade_solo'].min():.1f}% - {df['umidade_solo'].max():.1f}%")
    print(f"   pH Solo: {df['ph_solo'].min():.2f} - {df['ph_solo'].max():.2f}")
    print(f"   Irrigações Ativas: {df['irrigacao_ativa'].sum()} ({df['irrigacao_ativa'].mean()*100:.1f}%)")
    
    # Salvar arquivo
    if output_format == "csv":
        filename = f"sensor_data_{cultura}.csv"
        df.to_csv(filename, index=False)
        print(f"\n✅ Arquivo salvo: {filename}")
    elif output_format == "json":
        filename = f"sensor_data_{cultura}.json"
        df.to_json(filename, orient='records', date_format='iso', indent=2)
        print(f"\n✅ Arquivo salvo: {filename}")
    
    return df


if __name__ == "__main__":
    # Gerar dados para Banana
    df_banana = gerar_dados_simulados(
        num_samples=1000,
        cultura="banana",
        output_format="csv"
    )
    
    # Gerar dados para Milho
    df_milho = gerar_dados_simulados(
        num_samples=1000,
        cultura="milho",
        output_format="csv"
    )
    
    print("\n✅ Dados simulados gerados com sucesso!")
    print("📁 Arquivos criados:")
    print("   - sensor_data_banana.csv")
    print("   - sensor_data_milho.csv")
    print("\n💡 Use esses dados para treinar os modelos de ML!")