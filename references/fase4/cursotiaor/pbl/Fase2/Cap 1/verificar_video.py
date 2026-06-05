#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificação Pré-Gravação do Vídeo
==================================
Verifica se tudo está pronto para gravar
"""

import sys
import sqlite3
from pathlib import Path

# Configurar UTF-8
sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = Path(__file__).parent / 'database' / 'farmtech.db'

def verificar_banco():
    """Verifica se há dados suficientes no banco"""
    print("\n" + "="*80)
    print("📊 VERIFICAÇÃO DO BANCO DE DADOS")
    print("="*80)
    
    if not DB_PATH.exists():
        print("❌ Banco de dados não encontrado!")
        print(f"   Execute: python database/database_manager.py")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verificar leituras
    cursor.execute("SELECT COUNT(*) FROM sensor_readings")
    total_leituras = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_previsoes = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM irrigation_actions")
    total_acoes = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\n✅ Total de leituras: {total_leituras}")
    print(f"✅ Total de previsões: {total_previsoes}")
    print(f"✅ Total de irrigações: {total_acoes}")
    
    if total_leituras < 50:
        print(f"\n⚠️  ATENÇÃO: Apenas {total_leituras} leituras disponíveis")
        print("   Recomendado: Mínimo 50 leituras para vídeo")
        print("   Execute: python database/database_manager.py")
        print("   Deixe rodar por 5 minutos para gerar ~60 leituras")
        return False
    
    return True

def verificar_modelos():
    """Verifica se modelos ML foram treinados"""
    print("\n" + "="*80)
    print("🤖 VERIFICAÇÃO DOS MODELOS ML")
    print("="*80)
    
    models_dir = Path(__file__).parent / 'models'
    
    arquivos = [
        'rendimento_estimado_model.pkl',
        'rendimento_estimado_metrics.json',
        'rendimento_estimado_feature_importance.json'
    ]
    
    todos_ok = True
    for arquivo in arquivos:
        caminho = models_dir / arquivo
        if caminho.exists():
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - NÃO ENCONTRADO")
            todos_ok = False
    
    if not todos_ok:
        print("\n⚠️  Execute: python models/train_models.py")
        return False
    
    return True

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    print("\n" + "="*80)
    print("📦 VERIFICAÇÃO DE DEPENDÊNCIAS")
    print("="*80)
    
    modulos = [
        'streamlit',
        'pandas',
        'plotly',
        'sklearn',
        'numpy',
        'schedule',
        'statsmodels'
    ]
    
    todos_ok = True
    for modulo in modulos:
        try:
            __import__(modulo)
            print(f"✅ {modulo}")
        except ImportError:
            print(f"❌ {modulo} - NÃO INSTALADO")
            todos_ok = False
    
    if not todos_ok:
        print("\n⚠️  Execute: pip install streamlit pandas plotly scikit-learn statsmodels schedule")
        return False
    
    return True

def exibir_metricas_importantes():
    """Exibe métricas para mencionar no vídeo"""
    print("\n" + "="*80)
    print("📈 MÉTRICAS PARA MENCIONAR NO VÍDEO")
    print("="*80)
    
    if not DB_PATH.exists():
        print("❌ Banco não disponível")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Estatísticas gerais
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            ROUND(AVG(temperatura), 1) as temp_media,
            ROUND(AVG(umidade_solo), 1) as umid_media,
            ROUND(AVG(ph_solo), 2) as ph_medio
        FROM sensor_readings
    """)
    stats = cursor.fetchone()
    
    print(f"\n📊 LEITURAS DE SENSORES:")
    print(f"   Total: {stats[0]}")
    print(f"   Temperatura média: {stats[1]}°C")
    print(f"   Umidade média: {stats[2]}%")
    print(f"   pH médio: {stats[3]}")
    
    # NPK adequado
    cursor.execute("""
        SELECT COUNT(*) 
        FROM sensor_readings 
        WHERE nitrogenio = 1 AND fosforo = 1 AND potassio = 1
    """)
    npk_ok = cursor.fetchone()[0]
    perc_npk = (npk_ok / stats[0] * 100) if stats[0] > 0 else 0
    
    print(f"\n🧪 NPK ADEQUADO:")
    print(f"   Total: {npk_ok} ({perc_npk:.1f}%)")
    
    # Irrigações
    cursor.execute("SELECT COUNT(*) FROM irrigation_actions")
    total_irrigacoes = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(volume_aplicado) FROM irrigation_actions")
    volume_total = cursor.fetchone()[0] or 0
    
    print(f"\n💧 IRRIGAÇÕES:")
    print(f"   Total de ações: {total_irrigacoes}")
    print(f"   Volume total: {volume_total:.1f} L/m²")
    
    # Culturas
    cursor.execute("SELECT cultura, COUNT(*) FROM sensor_readings GROUP BY cultura")
    culturas = cursor.fetchall()
    
    print(f"\n🌾 DISTRIBUIÇÃO POR CULTURA:")
    for cultura, count in culturas:
        print(f"   {cultura.capitalize()}: {count} leituras")
    
    conn.close()

def exibir_checklist_final():
    """Exibe checklist para gravação"""
    print("\n" + "="*80)
    print("✅ CHECKLIST PRÉ-GRAVAÇÃO")
    print("="*80)
    
    checklist = [
        "[ ] Dashboard rodando em http://localhost:8502",
        "[ ] Auto-ingestão gerando dados (terminal separado)",
        "[ ] Navegador em tela cheia (F11)",
        "[ ] Abas desnecessárias fechadas",
        "[ ] Microfone testado e funcionando",
        "[ ] OBS Studio ou ferramenta de gravação aberta",
        "[ ] Resolução 1280x720 ou superior",
        "[ ] Roteiro lido e ensaiado (ROTEIRO_VIDEO_5MIN.md)",
        "[ ] Notas com métricas do banco anotadas",
        "[ ] Cronômetro ou timer visível (5 minutos máximo)",
    ]
    
    print("\nAntes de gravar, confirme:\n")
    for item in checklist:
        print(f"  {item}")
    
    print("\n" + "="*80)

def main():
    print("\n🎥 VERIFICAÇÃO PRÉ-GRAVAÇÃO - FARMTECH SOLUTIONS")
    print("="*80)
    
    # Verificações
    check1 = verificar_dependencias()
    check2 = verificar_modelos()
    check3 = verificar_banco()
    
    if check1 and check2 and check3:
        print("\n" + "="*80)
        print("✅ SISTEMA PRONTO PARA GRAVAÇÃO!")
        print("="*80)
        
        exibir_metricas_importantes()
        exibir_checklist_final()
        
        print("\n📚 PRÓXIMOS PASSOS:")
        print("   1. Leia o ROTEIRO_VIDEO_5MIN.md")
        print("   2. Execute: python database/database_manager.py (terminal 1)")
        print("   3. Execute: streamlit run dashboard/app.py (terminal 2)")
        print("   4. Abra http://localhost:8502 no navegador")
        print("   5. Pressione F11 (tela cheia)")
        print("   6. Inicie a gravação!")
        print("\n🎬 BOA SORTE! 🚀\n")
    else:
        print("\n" + "="*80)
        print("⚠️  SISTEMA NÃO ESTÁ PRONTO")
        print("="*80)
        print("\nCorreja os problemas acima antes de gravar.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificação interrompida")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
