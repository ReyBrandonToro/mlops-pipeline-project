@echo off
echo ========================================
echo Configuracion del Proyecto MLOps Pipeline
echo ========================================
echo.
echo Creando entorno virtual 'mlops_pipeline-venv'...
python -m venv mlops_pipeline-venv

echo.
echo Activando entorno virtual...
call mlops_pipeline-venv\Scripts\activate

echo.
echo Instalando dependencias desde requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Configuracion completada exitosamente!
echo ========================================
echo.
echo Para activar el entorno virtual, ejecuta:
echo   mlops_pipeline-venv\Scripts\activate
echo.
pause
