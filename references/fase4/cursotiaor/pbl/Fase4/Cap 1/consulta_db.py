#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Consulta Rápida do Banco de Dados FarmTech
==========================================
Script para visualizar dados do SQLite de forma formatada
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime

# Configurar encoding UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Caminho do banco
DB_PATH = Path(__file__).parent / 'database' / 'farmtech.db'

def conectar():
    """Conecta ao banco de dados"""
    if not DB_PATH.exists():
        print(f"❌ Banco não encontrado: {DB_PATH}")
        sys.exit(1)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def exibir_estatisticas(conn):
    """Exibe estatísticas gerais"""
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("📊 ESTATÍSTICAS DO BANCO DE DADOS FARMTECH")
    print("="*80)
    
    # Total de leituras
    cursor.execute("SELECT COUNT(*) as total FROM sensor_readings")
    total_leituras = cursor.fetchone()['total']
    
    # Total de previsões
    cursor.execute("SELECT COUNT(*) as total FROM predictions")
    total_previsoes = cursor.fetchone()['total']
    
    # Total de ações de irrigação
    cursor.execute("SELECT COUNT(*) as total FROM irrigation_actions")
    total_acoes = cursor.fetchone()['total']
    
    # Total de culturas
    cursor.execute("SELECT COUNT(*) as total FROM culturas")
    total_culturas = cursor.fetchone()['total']
    
    print(f"\n📈 Total de Leituras de Sensores: {total_leituras}")
    print(f"🔮 Total de Previsões ML: {total_previsoes}")
    print(f"💧 Total de Ações de Irrigação: {total_acoes}")
    print(f"🌾 Total de Culturas Cadastradas: {total_culturas}")

def exibir_ultimas_leituras(conn, limit=10):
    """Exibe últimas leituras de sensores"""
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print(f"📊 ÚLTIMAS {limit} LEITURAS DE SENSORES")
    print("="*80)
    
    cursor.execute(f"""
        SELECT 
            id,
            timestamp,
            temperatura,
            umidade_solo,
            ph_solo,
            nitrogenio,
            fosforo,
            potassio,
            irrigacao_ativa,
            cultura
        FROM sensor_readings
        ORDER BY timestamp DESC
        LIMIT {limit}
    """)
    
    leituras = cursor.fetchall()
    
    if not leituras:
        print("\n⚠️  Nenhuma leitura encontrada")
        return
    
    for leitura in leituras:
        print(f"\n🆔 ID: {leitura['id']}")
        print(f"   📅 Timestamp: {leitura['timestamp']}")
        print(f"   🌡️  Temperatura: {leitura['temperatura']:.1f}°C")
        print(f"   💧 Umidade Solo: {leitura['umidade_solo']:.1f}%")
        print(f"   🧪 pH Solo: {leitura['ph_solo']:.2f}")
        print(f"   🔵 Nitrogênio: {'✅ OK' if leitura['nitrogenio'] else '❌ Baixo'}")
        print(f"   🟡 Fósforo: {'✅ OK' if leitura['fosforo'] else '❌ Baixo'}")
        print(f"   🟢 Potássio: {'✅ OK' if leitura['potassio'] else '❌ Baixo'}")
        print(f"   🚰 Irrigação: {'🟢 ATIVA' if leitura['irrigacao_ativa'] else '⚪ INATIVA'}")
        print(f"   🌾 Cultura: {leitura['cultura'].upper()}")

def exibir_acoes_irrigacao(conn, limit=10):
    """Exibe ações de irrigação"""
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print(f"💧 ÚLTIMAS {limit} AÇÕES DE IRRIGAÇÃO")
    print("="*80)
    
    cursor.execute(f"""
        SELECT 
            i.id,
            i.timestamp,
            i.acao,
            i.motivo,
            i.volume_aplicado,
            i.duracao_minutos,
            s.temperatura,
            s.umidade_solo,
            s.cultura
        FROM irrigation_actions i
        JOIN sensor_readings s ON i.reading_id = s.id
        ORDER BY i.timestamp DESC
        LIMIT {limit}
    """)
    
    acoes = cursor.fetchall()
    
    if not acoes:
        print("\n⚠️  Nenhuma ação encontrada")
        return
    
    for acao in acoes:
        icone = "🟢" if acao['acao'] == 'LIGAR' else "🔴"
        print(f"\n{icone} ID: {acao['id']} | {acao['acao']}")
        print(f"   📅 Timestamp: {acao['timestamp']}")
        print(f"   💡 Motivo: {acao['motivo']}")
        print(f"   💧 Volume: {acao['volume_aplicado']:.1f} L/m²")
        print(f"   ⏱️  Duração: {acao['duracao_minutos']} minutos")
        print(f"   🌡️  Temp: {acao['temperatura']:.1f}°C | 💧 Umid: {acao['umidade_solo']:.1f}% | 🌾 {acao['cultura'].upper()}")

def exibir_previsoes(conn, limit=5):
    """Exibe previsões ML"""
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print(f"🔮 ÚLTIMAS {limit} PREVISÕES DE MACHINE LEARNING")
    print("="*80)
    
    cursor.execute(f"""
        SELECT 
            p.id,
            p.timestamp,
            p.volume_irrigacao,
            p.dosagem_n,
            p.dosagem_p,
            p.dosagem_k,
            p.rendimento_estimado,
            p.confianca,
            p.modelo_versao,
            s.cultura
        FROM predictions p
        JOIN sensor_readings s ON p.reading_id = s.id
        ORDER BY p.timestamp DESC
        LIMIT {limit}
    """)
    
    previsoes = cursor.fetchall()
    
    if not previsoes:
        print("\n⚠️  Nenhuma previsão encontrada")
        return
    
    for prev in previsoes:
        print(f"\n🔮 ID: {prev['id']}")
        print(f"   📅 Timestamp: {prev['timestamp']}")
        print(f"   🌾 Cultura: {prev['cultura'].upper()}")
        print(f"   💧 Volume Irrigação Recomendado: {prev['volume_irrigacao']:.1f} L/m²")
        print(f"   🔵 Nitrogênio: {prev['dosagem_n']} g/m²")
        print(f"   🟡 Fósforo: {prev['dosagem_p']} g/m²")
        print(f"   🟢 Potássio: {prev['dosagem_k']} g/m²")
        print(f"   📈 Rendimento Estimado: {prev['rendimento_estimado']:.0f} kg/ha")
        print(f"   🎯 Confiança: {prev['confianca']*100:.0f}%")
        print(f"   🤖 Modelo: {prev['modelo_versao']}")

def exibir_culturas(conn):
    """Exibe culturas cadastradas"""
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("🌾 CULTURAS CADASTRADAS")
    print("="*80)
    
    cursor.execute("""
        SELECT 
            nome,
            n_requerido,
            p_requerido,
            k_requerido,
            ph_minimo,
            ph_maximo,
            umidade_minima,
            umidade_maxima
        FROM culturas
        ORDER BY nome
    """)
    
    culturas = cursor.fetchall()
    
    if not culturas:
        print("\n⚠️  Nenhuma cultura cadastrada")
        return
    
    for cultura in culturas:
        print(f"\n🌱 {cultura['nome'].upper()}")
        print(f"   🔵 Nitrogênio: {cultura['n_requerido']} g/m²")
        print(f"   🟡 Fósforo: {cultura['p_requerido']} g/m²")
        print(f"   🟢 Potássio: {cultura['k_requerido']} g/m²")
        print(f"   🧪 pH: {cultura['ph_minimo']} - {cultura['ph_maximo']}")
        print(f"   💧 Umidade: {cultura['umidade_minima']}% - {cultura['umidade_maxima']}%")

def menu_principal():
    """Menu interativo"""
    conn = conectar()
    
    while True:
        print("\n" + "="*80)
        print("🌾 FARMTECH DATABASE CONSULTA")
        print("="*80)
        print("\nEscolha uma opção:")
        print("  1 - 📊 Estatísticas Gerais")
        print("  2 - 📈 Últimas Leituras de Sensores")
        print("  3 - 💧 Ações de Irrigação")
        print("  4 - 🔮 Previsões de ML")
        print("  5 - 🌾 Culturas Cadastradas")
        print("  6 - 🔍 Consulta SQL Customizada")
        print("  0 - ❌ Sair")
        print("\n" + "="*80)
        
        opcao = input("\n👉 Digite a opção: ").strip()
        
        if opcao == '1':
            exibir_estatisticas(conn)
        
        elif opcao == '2':
            try:
                limit = int(input("Quantas leituras? [10]: ").strip() or "10")
                exibir_ultimas_leituras(conn, limit)
            except ValueError:
                print("❌ Número inválido")
        
        elif opcao == '3':
            try:
                limit = int(input("Quantas ações? [10]: ").strip() or "10")
                exibir_acoes_irrigacao(conn, limit)
            except ValueError:
                print("❌ Número inválido")
        
        elif opcao == '4':
            try:
                limit = int(input("Quantas previsões? [5]: ").strip() or "5")
                exibir_previsoes(conn, limit)
            except ValueError:
                print("❌ Número inválido")
        
        elif opcao == '5':
            exibir_culturas(conn)
        
        elif opcao == '6':
            print("\n🔍 Consulta SQL Customizada")
            print("Digite sua query SQL (ex: SELECT * FROM sensor_readings LIMIT 5):")
            query = input("SQL> ").strip()
            
            try:
                cursor = conn.cursor()
                cursor.execute(query)
                resultados = cursor.fetchall()
                
                if resultados:
                    print(f"\n✅ {len(resultados)} resultado(s):\n")
                    for i, row in enumerate(resultados, 1):
                        print(f"--- Registro {i} ---")
                        for key in row.keys():
                            print(f"  {key}: {row[key]}")
                        print()
                else:
                    print("\n⚠️  Consulta executada, mas sem resultados")
            
            except Exception as e:
                print(f"\n❌ Erro na consulta: {e}")
        
        elif opcao == '0':
            print("\n✅ Encerrando...")
            conn.close()
            break
        
        else:
            print("\n❌ Opção inválida")
        
        input("\n⏸️  Pressione ENTER para continuar...")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrompido pelo usuário")
        sys.exit(0)
