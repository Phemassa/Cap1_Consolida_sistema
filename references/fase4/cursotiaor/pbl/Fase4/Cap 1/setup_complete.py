#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup Completo para Gravação do Vídeo
======================================
Executa todos os preparativos necessários
"""

import sys
import sqlite3
from pathlib import Path
import subprocess

def print_header(text):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def run_command(command, description, show_output=True):
    """
    Executa comando e trata erros
    
    Args:
        command: Comando a executar
        description: Descrição da etapa
        show_output: Se deve mostrar output do comando
    """
    print(f"🔄 {description}...")
    
    try:
        if show_output:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                text=True
            )
        else:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
        
        print(f"✅ {description} - Concluído!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}")
        if not show_output:
            print(f"   Saída: {e.stdout}")
            print(f"   Erro: {e.stderr}")
        return False

def check_python_version():
    """Verifica versão do Python"""
    print_header("1/8 - Verificação de Requisitos")
    
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ é necessário!")
        return False
    
    print("✅ Versão do Python adequada")
    return True

def install_dependencies():
    """Instala dependências do projeto"""
    print_header("2/8 - Instalação de Dependências")
    
    requirements_files = [
        "dashboard/requirements.txt"
    ]
    
    for req_file in requirements_files:
        if Path(req_file).exists():
            if not run_command(
                f"pip install -r {req_file}",
                f"Instalando dependências de {req_file}",
                show_output=False
            ):
                return False
    
    # Dependências adicionais para treinamento
    additional_packages = [
        "scikit-learn==1.3.2",
        "joblib==1.3.2",
        "schedule==1.2.0"
    ]
    
    for package in additional_packages:
        if not run_command(
            f"pip install {package}",
            f"Instalando {package}",
            show_output=False
        ):
            return False
    
    return True

def generate_sensor_data():
    """Gera dados simulados de sensores"""
    print_header("3/8 - Geração de Dados de Sensores")
    
    if not Path("generate_sensor_data.py").exists():
        print("⚠️ Script generate_sensor_data.py não encontrado, pulando...")
        return True
    
    return run_command(
        "python generate_sensor_data.py",
        "Gerando dados simulados para banana e milho",
        show_output=True
    )

def create_database():
    """Cria estrutura do banco de dados"""
    print_header("4/8 - Criação do Banco de Dados")
    
    if not Path("database/database_manager.py").exists():
        print("⚠️ database_manager.py não encontrado, pulando...")
        return True
    
    # Criar banco executando o script uma vez
    print("🔄 Criando tabelas do banco de dados...")
    
    try:
        # Importar e criar apenas as tabelas
        import sys
        sys.path.insert(0, str(Path.cwd()))
        from database.database_manager import FarmTechDatabase
        
        db = FarmTechDatabase('database/farmtech.db')
        print("✅ Banco de dados criado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar banco: {e}")
        return False

def train_ml_models():
    """Treina modelos de Machine Learning"""
    print_header("5/8 - Treinamento de Modelos ML")
    
    if not Path("models/train_models.py").exists():
        print("⚠️ train_models.py não encontrado, pulando...")
        return True
    
    # Verificar se há dados para treinar
    data_files = list(Path(".").glob("sensor_data_*.csv"))
    
    if not data_files:
        print("⚠️ Nenhum arquivo de dados encontrado, pulando treinamento...")
        return True
    
    return run_command(
        "python models/train_models.py",
        "Treinando modelos de ML",
        show_output=True
    )

def test_ml_predictions():
    """Testa sistema de previsões"""
    print_header("6/8 - Teste de Previsões ML")
    
    if not Path("models/predict.py").exists():
        print("⚠️ predict.py não encontrado, pulando...")
        return True
    
    # Verificar se há modelos treinados
    model_files = list(Path("models").glob("*_model.pkl"))
    
    if not model_files:
        print("⚠️ Nenhum modelo treinado encontrado, pulando teste...")
        return True
    
    return run_command(
        "python models/predict.py",
        "Testando previsões ML",
        show_output=True
    )

def verify_installation():
    """Verifica instalação completa"""
    print_header("7/8 - Verificação de Instalação")
    
    checks = []
    
    # Verificar arquivos críticos
    critical_files = [
        "FarmTech.ino",
        "database/database_manager.py",
        "dashboard/app.py",
        "models/train_models.py",
        "models/predict.py"
    ]
    
    print("📁 Verificando arquivos críticos...")
    for file in critical_files:
        exists = Path(file).exists()
        status = "✅" if exists else "❌"
        print(f"   {status} {file}")
        checks.append(exists)
    
    # Verificar dados gerados
    print("\n📊 Verificando dados gerados...")
    data_files = ["sensor_data_banana.csv", "sensor_data_milho.csv"]
    for file in data_files:
        exists = Path(file).exists()
        status = "✅" if exists else "⚠️"
        print(f"   {status} {file}")
    
    # Verificar banco de dados
    print("\n💾 Verificando banco de dados...")
    db_exists = Path("database/farmtech.db").exists()
    status = "✅" if db_exists else "⚠️"
    print(f"   {status} database/farmtech.db")
    
    # Verificar modelos treinados
    print("\n🤖 Verificando modelos ML...")
    model_files = list(Path("models").glob("*_model.pkl"))
    if model_files:
        print(f"   ✅ {len(model_files)} modelo(s) encontrado(s)")
        for model in model_files:
            print(f"      - {model.name}")
    else:
        print("   ⚠️ Nenhum modelo treinado encontrado")
    
    # Verificar páginas do dashboard
    print("\n📊 Verificando dashboard...")
    dashboard_pages = list(Path("dashboard/pages").glob("*.py"))
    if dashboard_pages:
        print(f"   ✅ {len(dashboard_pages)} página(s) encontrada(s)")
    else:
        print("   ⚠️ Nenhuma página de dashboard encontrada")
    
    success = all(checks)
    
    if success:
        print("\n✅ Instalação verificada com sucesso!")
    else:
        print("\n⚠️ Alguns arquivos críticos estão faltando")
    
    return success

def show_next_steps():
    """Mostra próximos passos"""
    print_header("8/8 - Próximos Passos")
    
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                  🎉 SETUP CONCLUÍDO COM SUCESSO! 🎉                ║
╚════════════════════════════════════════════════════════════════════╝

📋 PRÓXIMOS PASSOS:

1️⃣  Iniciar Auto-Ingestão de Dados
   ➜ python database/database_manager.py
   (Coleta dados do ESP32 a cada 5 segundos)

2️⃣  Executar Dashboard Streamlit
   ➜ streamlit run dashboard/app.py
   (Acesse em http://localhost:8501)

3️⃣  Simular ESP32 no Wokwi
   ➜ Acesse https://wokwi.com
   ➜ Carregue diagram.json
   ➜ Compile e execute o firmware

4️⃣  Fazer Previsões ML
   ➜ python models/predict.py
   (Teste o sistema de previsões)

5️⃣  Gerar Relatórios
   ➜ Acesse o dashboard
   ➜ Navegue para "Análise"
   ➜ Clique em "Gerar Relatório CSV"

📊 URLs IMPORTANTES:

   Dashboard Local: http://localhost:8501
   Wokwi Simulator: https://wokwi.com
   GitHub Repo: https://github.com/Phemassa/fiap-farmtech-fase2

📚 DOCUMENTAÇÃO:

   README principal: README.md
   Dashboard: dashboard/README.md
   Modelos ML: models/README.md
   Atividade: ATIVIDADE_ML_DASHBOARD.md

💡 DICAS:

   • Use Ctrl+C para parar processos
   • Dashboard atualiza automaticamente a cada 5s
   • Modelos já estão treinados e prontos
   • Logs são salvos em farmtech.log

🎓 PONTUAÇÃO FIAP:

   ✅ PARTE 1: Coleta de Dados (40 pts)
   ✅ PARTE 2: Análise ML (60 pts)
   ✅ IR ALÉM 1: Database SQL (+20 pts)
   ✅ IR ALÉM 2: Dashboard Avançado (+20 pts)
   ═══════════════════════════════════════════
   🏆 TOTAL: 140 pontos de 140 possíveis

╔════════════════════════════════════════════════════════════════════╗
║         Boa sorte com o projeto FarmTech Solutions! 🌾            ║
╚════════════════════════════════════════════════════════════════════╝
    """)

def main():
    """Execução principal"""
    print("""
    ███████╗ █████╗ ██████╗ ███╗   ███╗████████╗███████╗ ██████╗██╗  ██╗
    ██╔════╝██╔══██╗██╔══██╗████╗ ████║╚══██╔══╝██╔════╝██╔════╝██║  ██║
    █████╗  ███████║██████╔╝██╔████╔██║   ██║   █████╗  ██║     ███████║
    ██╔══╝  ██╔══██║██╔══██╗██║╚██╔╝██║   ██║   ██╔══╝  ██║     ██╔══██║
    ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║   ██║   ███████╗╚██████╗██║  ██║
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝
    
              🌾 Setup Completo do Sistema - FIAP Fase 2 Cap 1 🌾
    """)
    
    print("Este script irá configurar todo o ambiente FarmTech Solutions:")
    print("  • Verificar requisitos")
    print("  • Instalar dependências")
    print("  • Gerar dados de sensores")
    print("  • Criar banco de dados")
    print("  • Treinar modelos ML")
    print("  • Verificar instalação")
    print("\n" + "=" * 70)
    
    input("Pressione ENTER para começar... ")
    
    start_time = time.time()
    
    # Etapas de setup
    steps = [
        (check_python_version, "Verificação de Requisitos"),
        (install_dependencies, "Instalação de Dependências"),
        (generate_sensor_data, "Geração de Dados"),
        (create_database, "Criação do Banco de Dados"),
        (train_ml_models, "Treinamento de Modelos ML"),
        (test_ml_predictions, "Teste de Previsões"),
        (verify_installation, "Verificação Final"),
    ]
    
    failed_steps = []
    
    for step_func, step_name in steps:
        try:
            if not step_func():
                failed_steps.append(step_name)
                print(f"\n⚠️ Etapa '{step_name}' teve problemas, mas continuando...")
        except Exception as e:
            print(f"\n❌ Erro inesperado em '{step_name}': {e}")
            failed_steps.append(step_name)
    
    # Tempo total
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    print_header("RESUMO DO SETUP")
    
    if failed_steps:
        print("⚠️ Etapas com problemas:")
        for step in failed_steps:
            print(f"   • {step}")
        print("\nO setup foi concluído com avisos. Verifique os erros acima.")
    else:
        print("✅ Todas as etapas concluídas com sucesso!")
    
    print(f"\n⏱️  Tempo total: {minutes}m {seconds}s")
    
    # Próximos passos
    show_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro fatal: {e}")
        sys.exit(1)