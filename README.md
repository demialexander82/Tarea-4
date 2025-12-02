# Tarea 4: Pruebas Automatizadas con Selenium

Aplicación PHP CRUD de personajes de Breaking Bad con suite de pruebas automatizadas usando Selenium y Python.

## 📋 Requisitos

- PHP 7.4 o superior (incluido en XAMPP)
- Python 3.7 o superior
- Microsoft Edge (navegador)
- msedgedriver (WebDriver para Edge)

## 🚀 Instalación Rápida

### 1. Instalar dependencias de Python

```cmd
cd "C:\Users\demia\tarea 4\Tarea-automatizacion"
python -m pip install -r requirements.txt
```

### 2. Configurar WebDriver para Selenium

**IMPORTANTE:** Los tests de Selenium requieren el driver del navegador.

#### Opción A: Script automático (Recomendado)

Ejecuta el script de ayuda que detectará tu versión de Edge y te guiará:

```cmd
download-drivers.cmd
```

#### Opción B: Descarga manual

1. Abre Microsoft Edge y ve a: `edge://settings/help`
2. Anota tu versión (ejemplo: `119.0.2144.57`)
3. Ve a: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
4. Descarga la versión compatible con tu Edge
5. Extrae `msedgedriver.exe` del ZIP
6. Coloca el archivo en: `C:\msedgedriver\msedgedriver.exe`

### 3. Verificar instalación del driver

```cmd
C:\msedgedriver\msedgedriver.exe --version
```

Deberías ver algo como: `Microsoft Edge WebDriver 119.0.2144.57`

## 🎯 Ejecución

### Paso 1: Iniciar el servidor PHP

Abre una ventana de `cmd` y ejecuta:

```cmd
cd "C:\Users\demia\tarea 4\Tarea-automatizacion\src"
"C:\xampp\php\php.exe" -S 127.0.0.1:8000
```

Verás: `PHP 8.x.x Development Server (http://127.0.0.1:8000) started`

**Deja esta ventana abierta** mientras ejecutas los tests.

### Paso 2: Ejecutar los tests (en otra ventana cmd)

Abre una **segunda** ventana de `cmd` y ejecuta:

```cmd
cd "C:\Users\demia\tarea 4\Tarea-automatizacion"
python tests\test_crud.py
```

## 📊 Tests Incluidos

La suite de pruebas automatizadas cubre:

1. ✅ **test_01_login_success** - Login con credenciales válidas
2. ✅ **test_02_view_personajes** - Visualización de la lista de personajes
3. ✅ **test_03_agregar_personaje** - Crear un nuevo personaje (CREATE)
4. ✅ **test_04_editar_personaje** - Modificar un personaje existente (UPDATE)
5. ✅ **test_05_eliminar_personaje** - Eliminar un personaje (DELETE)
6. ✅ **test_06_logout** - Cerrar sesión

## 🔑 Credenciales de Prueba

- **Usuario:** `test`
- **Contraseña:** `test123`

## 🗄️ Base de Datos

El proyecto usa SQLite (sin necesidad de MySQL).

- Archivo de BD: `src/data/breaking_bad.db`
- Se crea automáticamente al acceder a la aplicación por primera vez
- Incluye datos de ejemplo (personajes de Breaking Bad)

Para reiniciar la BD:

```cmd
del "src\data\breaking_bad.db"
```

La próxima vez que accedas a la aplicación se recreará con datos iniciales.

## 🛠️ Solución de Problemas

### Error: "Failed to resolve 'msedgedriver.azureedge.net'"

**Causa:** No hay conexión a internet o problemas de DNS para descargar el driver automáticamente.

**Solución:** Descarga manual del driver (ver sección "Configurar WebDriver").

### Error: "WinError 193 %1 is not a valid Win32 application"

**Causa:** Driver incompatible (arquitectura incorrecta o versión no coincide).

**Solución:** 
1. Elimina drivers antiguos: `del C:\msedgedriver\msedgedriver.exe`
2. Verifica tu versión de Edge: `edge://settings/help`
3. Descarga el driver exacto para esa versión

### Error: "php is not recognized"

**Causa:** PHP no está en el PATH del sistema.

**Solución:** Usa la ruta completa de XAMPP:

```cmd
"C:\xampp\php\php.exe" -S 127.0.0.1:8000
```

### El servidor no inicia (puerto ocupado)

**Verificar qué usa el puerto 8000:**

```cmd
netstat -ano | findstr :8000
```

**Cerrar proceso:**

```cmd
taskkill /PID <numero_de_proceso> /F
```

### Los tests fallan pero el servidor está corriendo

1. Verifica que puedes acceder manualmente: http://127.0.0.1:8000/login.php
2. Verifica que el driver esté en: `C:\msedgedriver\msedgedriver.exe`
3. Cierra Edge completamente antes de ejecutar tests
4. Revisa que no haya firewall bloqueando localhost

## 📁 Estructura del Proyecto

```
Tarea-automatizacion/
├── src/                    # Código fuente PHP
│   ├── conexion/          # Conexión a base de datos
│   │   └── db_conexion.php
│   ├── data/              # Base de datos SQLite (auto-generada)
│   ├── index.php          # Lista de personajes
│   ├── login.php          # Inicio de sesión
│   ├── agregar.php        # Agregar personaje
│   ├── editar.php         # Editar personaje
│   ├── eliminar.php       # Eliminar personaje
│   └── logout.php         # Cerrar sesión
├── tests/                 # Suite de pruebas Selenium
│   └── test_crud.py       # Tests CRUD completos
├── requirements.txt       # Dependencias Python
├── download-drivers.cmd   # Script de ayuda para drivers
└── README.md             # Este archivo
```

## 🎓 Uso Académico

Este proyecto fue creado para la **Tarea 4: Pruebas Automatizadas con Selenium**.

Objetivos cumplidos:
- ✅ Aplicación web funcional con operaciones CRUD
- ✅ Suite de pruebas automatizadas con Selenium
- ✅ Tests escritos en Python (lenguaje permitido)
- ✅ Cobertura completa: Create, Read, Update, Delete
- ✅ Gestión de sesiones y autenticación
- ✅ Documentación completa

## 📝 Notas Adicionales

- El proyecto usa SQLite en lugar de MySQL para simplificar la configuración
- Los tests usan Microsoft Edge (Chromium) por defecto
- El servidor PHP integrado es solo para desarrollo/testing
- Para producción, considera usar Apache/Nginx con MySQL

## 🤝 Contribuciones

Este es un proyecto académico. Para consultas o mejoras, contacta al autor.

---

**Última actualización:** Diciembre 2025
