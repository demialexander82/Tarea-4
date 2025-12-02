@echo off
echo Reorganizando commits...

REM Limpiar commits anteriores
git update-ref -d HEAD

REM Commit 1: Configuración
git add requirements.txt README.md README_SUBIDA.md
git commit -m "Configuracion inicial y documentacion"

REM Commit 2: Base de datos
git add src/conexion/db_conexion.php src/dump.sql
git commit -m "Sistema de conexion a base de datos SQLite"

REM Commit 3: Autenticación
git add src/login.php src/logout.php src/debug_users.php
git commit -m "Sistema de autenticacion y gestion de usuarios"

REM Commit 4: CRUD
git add src/index.php src/agregar.php src/editar.php src/eliminar.php
git commit -m "Implementacion de CRUD de personajes"

REM Commit 5: Tests
git add tests/test_crud.py
git commit -m "Tests automatizados con Selenium"

REM Commit 6: Drivers y assets
git add download-drivers.cmd INSTRUCCIONES-DRIVER.txt msedgedriver.exe
git commit -m "Configuracion de drivers para Selenium"

REM Commit 7: Resto
git add .
git commit -m "Assets e imagenes del proyecto"

REM Subir al repo
git push --force

echo.
echo Commits reorganizados exitosamente!
pause
