@echo off
echo ========================================
echo   DESCARGA DE DRIVERS PARA SELENIUM
echo ========================================
echo.

REM Detectar version de Edge
echo [1/4] Detectando version de Microsoft Edge...
echo.

REM Intentar obtener version de Edge desde el registro
for /f "tokens=3" %%i in ('reg query "HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon" /v version 2^>nul') do set EDGE_VERSION=%%i

if defined EDGE_VERSION (
    echo    Version de Edge detectada: %EDGE_VERSION%
    echo.
) else (
    echo    No se pudo detectar automaticamente.
    echo    Abre Microsoft Edge y ve a: edge://settings/help
    echo    Anota la version completa (ejemplo: 119.0.2144.57^)
    echo.
    set /p EDGE_VERSION="    Ingresa tu version de Edge: "
)

REM Extraer version principal (ejemplo: 119 de 119.0.2144.57)
for /f "tokens=1 delims=." %%a in ("%EDGE_VERSION%") do set EDGE_MAJOR=%%a

echo.
echo [2/4] Version principal de Edge: %EDGE_MAJOR%
echo.

REM Crear directorio para drivers si no existe
if not exist "C:\msedgedriver" (
    echo [3/4] Creando directorio C:\msedgedriver...
    mkdir "C:\msedgedriver"
    echo    Directorio creado.
) else (
    echo [3/4] Directorio C:\msedgedriver ya existe.
)
echo.

echo [4/4] DESCARGA MANUAL REQUERIDA
echo ========================================
echo.
echo Debido a restricciones de red, debes descargar manualmente el driver.
echo.
echo PASOS:
echo.
echo 1. Abre tu navegador y ve a:
echo    https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
echo.
echo 2. Busca la version %EDGE_MAJOR% o la mas cercana compatible con %EDGE_VERSION%
echo.
echo 3. Descarga el archivo ZIP para Windows x64 (o x86 si tu sistema es 32-bit^)
echo.
echo 4. Extrae el archivo msedgedriver.exe del ZIP
echo.
echo 5. Copia msedgedriver.exe a: C:\msedgedriver\
echo.
echo 6. Verifica que el archivo este en: C:\msedgedriver\msedgedriver.exe
echo.
echo ========================================
echo.

REM Verificar si ya existe el driver
if exist "C:\msedgedriver\msedgedriver.exe" (
    echo [OK] Driver encontrado en C:\msedgedriver\msedgedriver.exe
    echo.
    echo Version del driver:
    "C:\msedgedriver\msedgedriver.exe" --version
    echo.
    echo Puedes ejecutar los tests ahora con:
    echo    python tests\test_crud.py
) else (
    echo [PENDIENTE] No se encontro msedgedriver.exe en C:\msedgedriver\
    echo.
    echo Despues de descargar y colocar el archivo, ejecuta este script
    echo nuevamente para verificar la instalacion.
)

echo.
pause
