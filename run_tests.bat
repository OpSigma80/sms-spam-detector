@echo off
REM ============================================
REM EJECUTAR TODAS LAS PRUEBAS
REM ============================================

echo.
echo ==========================================
echo   EJECUTANDO PRUEBAS DEL PROYECTO
echo ==========================================
echo.

REM Verificar que existe el entorno virtual
if not exist "venv\" (
    echo [ERROR] No se encontro el entorno virtual.
    echo [INFO] Ejecuta 'setup.bat' primero.
    pause
    exit /b 1
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Verificar que pytest está instalado
python -c "import pytest" 2>nul
if errorlevel 1 (
    echo [*] Instalando pytest...
    pip install pytest pytest-cov --quiet
)

echo [*] Ejecutando pruebas...
echo.

REM Ejecutar pruebas con pytest
pytest tests/ -v --tb=short

echo.
echo ==========================================
echo   RESULTADO DE LAS PRUEBAS
echo ==========================================
echo.

REM Verificar resultado
if errorlevel 1 (
    echo [X] Algunas pruebas fallaron
    echo [INFO] Revisa los errores arriba
) else (
    echo [OK] Todas las pruebas pasaron!
)

echo.
echo ==========================================
echo   COMANDOS UTILES
echo ==========================================
echo.
echo Ejecutar pruebas especificas:
echo   pytest tests/test_model.py -v
echo.
echo Ejecutar con cobertura:
echo   pytest --cov=. --cov-report=html
echo.
echo Ver reporte HTML:
echo   start htmlcov\index.html
echo.
echo ==========================================

pause