@echo off
echo ============================================
echo FarmTech Solutions - Dashboard de Irrigacao
echo ============================================
echo.

echo Verificando instalacao das dependencias...
python -c "import streamlit, cx_Oracle, pandas, plotly" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Dependencias nao encontradas.
    echo Execute: pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✅ Dependencias encontradas.
echo.

echo Testando conexao com Oracle...
python test_connection.py
if %errorlevel% neq 0 (
    echo ❌ Falha na conexao com Oracle.
    echo Verifique as configuracoes e tente novamente.
    pause
    exit /b 1
)

echo.
echo ✅ Conexao OK. Iniciando dashboard...
echo.

streamlit run dashboard.py

pause