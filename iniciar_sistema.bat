@echo off
REM ========================================
REM Script de Inicio - Sistema de Detección de Fraude
REM ========================================

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   Sistema de Detección de Fraude Financiero - MLOps       ║
echo ║                    Inicio del Sistema                      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Verificar que el entorno virtual existe
if not exist "mlops_pipeline-venv\Scripts\activate.bat" (
    echo [ERROR] El entorno virtual no existe!
    echo Por favor, ejecuta setup.bat primero.
    pause
    exit /b 1
)

echo [1/3] Activando entorno virtual...
call mlops_pipeline-venv\Scripts\activate.bat

echo [2/3] Iniciando API FastAPI en el puerto 8000...
start "API FastAPI - Puerto 8000" cmd /k "mlops_pipeline-venv\Scripts\activate.bat && python -m mlops_pipeline.src.model_deploy"

REM Esperar 5 segundos para que la API inicie
timeout /t 5 /nobreak >nul

echo [3/3] Iniciando Frontend Streamlit en el puerto 8501...
start "Frontend Streamlit - Puerto 8501" cmd /k "mlops_pipeline-venv\Scripts\activate.bat && mlops_pipeline-venv\Scripts\streamlit.exe run mlops_pipeline\src\app_frontend.py"

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                    SISTEMA INICIADO                        ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo [✓] API FastAPI:      http://localhost:8000
echo [✓] Documentación:    http://localhost:8000/docs
echo [✓] Frontend:         http://localhost:8501
echo.
echo Se han abierto 2 ventanas de terminal:
echo   - Terminal 1: API FastAPI (puerto 8000)
echo   - Terminal 2: Frontend Streamlit (puerto 8501)
echo.
echo IMPORTANTE: NO CIERRES estas ventanas mientras uses el sistema.
echo Para detener el sistema, cierra ambas ventanas o presiona Ctrl+C en cada una.
echo.
echo El navegador se abrirá automáticamente en unos segundos...
echo.

REM Esperar 8 segundos más para que Streamlit inicie completamente
timeout /t 8 /nobreak >nul

REM Abrir el navegador en la URL de Streamlit
start http://localhost:8501

echo ╔════════════════════════════════════════════════════════════╗
echo ║         ¡Sistema listo! Usa el navegador abierto.          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
echo (Las otras 2 ventanas seguirán activas)
pause >nul
