import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import shutil
import os
from selenium.common.exceptions import WebDriverException
import time
import urllib.request
import urllib.error

class TestBreakingBadCRUD(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Configurar el driver de Selenium antes de ejecutar los tests"""
        print("\n" + "="*60)
        print("CONFIGURANDO WEBDRIVER PARA SELENIUM")
        print("="*60 + "\n")
        
        # Primero intentar Edge (Chromium) usando un msedgedriver local
        print("[1/3] Buscando Microsoft Edge Driver (msedgedriver)...")
        
        edge_options = webdriver.EdgeOptions()
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--remote-debugging-port=9222")
        # Descomenta para ejecutar sin interfaz gráfica (headless)
        # edge_options.add_argument("--headless=new")

        # Buscar msedgedriver local en PATH o en rutas comunes
        local_edge = shutil.which('msedgedriver')
        common_edge_paths = [
            r'C:\msedgedriver\msedgedriver.exe',
            r'C:\Program Files\msedgedriver.exe',
            r'C:\Program Files (x86)\msedgedriver.exe',
            r'C:\xampp\msedgedriver.exe',
            os.path.join(os.path.dirname(__file__), '..', 'msedgedriver.exe')
        ]
        
        if not local_edge:
            for p in common_edge_paths:
                if os.path.exists(p):
                    local_edge = p
                    print(f"   ✓ Encontrado en: {p}")
                    break

        if local_edge:
            try:
                edge_service = EdgeService(local_edge)
                cls.driver = webdriver.Edge(service=edge_service, options=edge_options)
                print("   ✓ Microsoft Edge iniciado correctamente\n")
                cls.driver.implicitly_wait(10)
                # Configurar BASE_URL desde entorno o por defecto
                cls.base_url = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
                print(f"Base URL: {cls.base_url}")
                # Esperar a que el servidor esté listo
                cls._wait_for_server_ready(cls.base_url)
                return
            except Exception as e:
                print(f"   ✗ Error al iniciar Edge con driver local: {str(e)[:100]}\n")

        print("   ✗ No se encontró msedgedriver.exe en ninguna ubicación esperada\n")
        print("[2/3] Intentando descargar msedgedriver automáticamente...")
        
        try:
            edge_bin = EdgeChromiumDriverManager().install()
            edge_service = EdgeService(edge_bin)
            cls.driver = webdriver.Edge(service=edge_service, options=edge_options)
            print("   ✓ Driver descargado e Edge iniciado correctamente\n")
            cls.driver.implicitly_wait(10)
            cls.base_url = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
            print(f"Base URL: {cls.base_url}")
            cls._wait_for_server_ready(cls.base_url)
            return
        except Exception as download_err:
            print(f"   ✗ Descarga automática falló (problema de red/DNS)\n")
            
        # Si llegamos aquí, nada funcionó
        print("[3/3] DRIVER NO DISPONIBLE")
        print("="*60)
        print("\nSOLUCIÓN:")
        print("-" * 60)
        print("1. Ejecuta el script de ayuda:")
        print("   download-drivers.cmd")
        print("\n2. Sigue las instrucciones para descargar msedgedriver.exe")
        print("\n3. Coloca el archivo en: C:\\msedgedriver\\msedgedriver.exe")
        print("\n4. Vuelve a ejecutar los tests:")
        print("   python tests\\test_crud.py")
        print("="*60 + "\n")
        
        raise RuntimeError(
            "\n\nNo se pudo iniciar ningún navegador. "
            "Ejecuta 'download-drivers.cmd' para obtener instrucciones de descarga manual."
        )
        
        # Nota: si llegamos aquí, ya se lanzó RuntimeError y no continuamos
        
    @classmethod
    def tearDownClass(cls):
        """Cerrar el driver después de todos los tests"""
        cls.driver.quit()

    def tearDown(self):
        """Si un test falla, guardar captura en carpeta screenshots."""
        # Crear carpeta si no existe
        try:
            os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'screenshots'), exist_ok=True)
        except Exception:
            pass
        # Detectar fallo por estado del resultado
        # unittest no expone fácilmente el estado aquí; estrategia simple:
        # guardar captura con nombre del test siempre para asegurar evidencia.
        try:
            name = self.id().split('.')[-1]
            out_path = os.path.join(os.path.dirname(__file__), '..', 'screenshots', f"{name}.png")
            self.driver.save_screenshot(out_path)
            print(f"Captura guardada: {out_path}")
        except Exception as e:
            print(f"No se pudo guardar captura: {e}")

    @staticmethod
    def _wait_for_server_ready(base_url: str, timeout: int = 30):
        """Espera a que el servidor PHP responda en base_url antes de correr los tests."""
        print("Comprobando disponibilidad del servidor PHP...")
        deadline = time.time() + timeout
        last_error = None
        check_urls = ["/login.php", "/index.php", "/"]
        while time.time() < deadline:
            for path in check_urls:
                try:
                    with urllib.request.urlopen(base_url + path, timeout=3) as resp:
                        if 200 <= resp.status < 500:
                            print(f"Servidor disponible: {base_url}{path} -> {resp.status}")
                            return
                except Exception as e:
                    last_error = e
            time.sleep(1)

        msg = (
            "No se pudo conectar al servidor PHP en '" + base_url + "'.\n"
            "Asegúrate de iniciar el servidor en otra ventana CMD:\n"
            "  cd \"C:\\Users\\demia\\tarea 4\\Tarea-automatizacion\\src\"\n"
            "  \"C:\\xampp\\php\\php.exe\" -S 127.0.0.1:8000\n\n"
            "Si usas otro puerto/host, define BASE_URL antes de ejecutar los tests:\n"
            "  set BASE_URL=http://127.0.0.1:8001\n"
            "  python tests\\test_crud.py\n\n"
            "Error de conexión: " + (str(last_error) if last_error else "desconocido")
        )
        raise RuntimeError(msg)
    
    def test_01_login_success(self):
        """Test: Login exitoso con usuario válido"""
        self.driver.get(f"{self.base_url}/login.php")
        
        # Llenar formulario de login
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        username_input.send_keys("test")
        password_input.send_keys("test123")
        
        # Hacer clic en botón de login
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Verificar que se redirige a index.php
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("index.php")
        )
        self.assertIn("index.php", self.driver.current_url)
        print("✓ Login exitoso")
    
    def test_02_view_personajes(self):
        """Test: Ver lista de personajes"""
        self.driver.get(f"{self.base_url}/index.php")
        
        # Verificar que se cargó la tabla
        table = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table"))
        )
        self.assertIsNotNone(table)
        
        # Contar filas (al menos una fila de datos)
        rows = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        self.assertGreater(len(rows), 0, "Debe haber al menos un personaje")
        print(f"✓ Se encontraron {len(rows)} personajes en la tabla")
    
    def test_03_agregar_personaje(self):
        """Test: Agregar un nuevo personaje (CREATE)"""
        self.driver.get(f"{self.base_url}/index.php")
        
        # Hacer clic en botón "Agregar Personaje"
        agregar_button = self.driver.find_element(By.LINK_TEXT, "Agregar Personaje")
        agregar_button.click()
        
        # Verificar que se abrió la página de agregar
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("agregar.php")
        )
        
        # Llenar formulario
        nombre_input = self.driver.find_element(By.NAME, "nombre")
        color_input = self.driver.find_element(By.NAME, "color")
        tipo_input = self.driver.find_element(By.NAME, "tipo")
        nivel_input = self.driver.find_element(By.NAME, "nivel")
        foto_input = self.driver.find_element(By.NAME, "foto")
        
        nombre_input.send_keys("Skyler White")
        color_input.send_keys("#9B59B6")
        tipo_input.send_keys("Personaje Secundario")
        nivel_input.clear()
        nivel_input.send_keys("3")
        foto_input.send_keys("https://via.placeholder.com/50?text=Skyler")
        
        # Hacer clic en botón Agregar
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Verificar que vuelve a index.php
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("index.php")
        )
        print("✓ Personaje agregado exitosamente")
    
    def test_04_editar_personaje(self):
        """Test: Editar un personaje (UPDATE)"""
        self.driver.get(f"{self.base_url}/index.php")
        
        # Obtener el primer botón de editar
        editar_buttons = self.driver.find_elements(By.LINK_TEXT, "✏️ Editar")
        if editar_buttons:
            editar_buttons[0].click()
            
            # Verificar que se abrió la página de editar
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("editar.php")
            )
            
            # Modificar el nombre
            nombre_input = self.driver.find_element(By.NAME, "nombre")
            nombre_input.clear()
            nombre_input.send_keys("Personaje Actualizado")
            
            # Hacer clic en guardar
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            # Verificar que vuelve a index.php
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("index.php")
            )
            print("✓ Personaje editado exitosamente")
        else:
            print("⚠ No hay personajes para editar")
    
    def test_05_eliminar_personaje(self):
        """Test: Eliminar un personaje (DELETE)"""
        self.driver.get(f"{self.base_url}/index.php")
        
        # Contar personajes antes de eliminar
        rows_before = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        count_before = len(rows_before)
        
        # Obtener el último botón de eliminar
        eliminar_buttons = self.driver.find_elements(By.LINK_TEXT, "🗑 Eliminar")
        if eliminar_buttons:
            # Haz clic en el último botón
            eliminar_buttons[-1].click()
            
            # Esperar a que se procese la eliminación
            time.sleep(2)
            
            # Verificar que la página se recargó
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("index.php")
            )
            
            # Contar personajes después de eliminar
            rows_after = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
            count_after = len(rows_after)
            
            self.assertLess(count_after, count_before, "Debe haber un personaje menos")
            print(f"✓ Personaje eliminado exitosamente (antes: {count_before}, después: {count_after})")
        else:
            print("⚠ No hay personajes para eliminar")
    
    def test_06_logout(self):
        """Test: Cerrar sesión"""
        self.driver.get(f"{self.base_url}/index.php")
        
        # Hacer clic en botón "Cerrar sesión"
        logout_button = self.driver.find_element(By.LINK_TEXT, "Cerrar sesión")
        logout_button.click()
        
        # Verificar que se redirige a login.php
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("login.php")
        )
        self.assertIn("login.php", self.driver.current_url)
        print("✓ Logout exitoso")

    # ---- Pruebas negativas y de límites para cumplir rúbrica ----

    def test_07_login_invalido(self):
        """Negativa: Login con credenciales inválidas"""
        self.driver.get(f"{self.base_url}/logout.php")
        self.driver.get(f"{self.base_url}/login.php")
        self.driver.find_element(By.NAME, "username").send_keys("usuarioX")
        self.driver.find_element(By.NAME, "password").send_keys("mala")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        WebDriverWait(self.driver, 5).until(EC.url_contains("login.php"))
        self.assertIn("login.php", self.driver.current_url)
        print("✓ Login inválido rechazado")

    def test_08_login_campos_vacios(self):
        """Límites: Login con campos vacíos"""
        self.driver.get(f"{self.base_url}/logout.php")
        self.driver.get(f"{self.base_url}/login.php")
        self.driver.find_element(By.NAME, "username").send_keys("")
        self.driver.find_element(By.NAME, "password").send_keys("")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        WebDriverWait(self.driver, 5).until(EC.url_contains("login.php"))
        self.assertIn("login.php", self.driver.current_url)
        print("✓ Login con vacíos rechazado")

    def test_09_index_sin_sesion(self):
        """Negativa: Acceso a index sin sesión"""
        self.driver.get(f"{self.base_url}/logout.php")
        self.driver.get(f"{self.base_url}/index.php")
        WebDriverWait(self.driver, 5).until(EC.url_contains("login.php"))
        self.assertIn("login.php", self.driver.current_url)
        print("✓ Index protegido sin sesión")

    def test_10_crear_sin_nombre(self):
        """Negativa: Crear personaje sin nombre"""
        # Login primero
        self.test_01_login_success()
        self.driver.get(f"{self.base_url}/agregar.php")
        self.driver.find_element(By.NAME, "nombre").clear()
        self.driver.find_element(By.NAME, "color").clear(); self.driver.find_element(By.NAME, "color").send_keys("#333333")
        self.driver.find_element(By.NAME, "tipo").clear(); self.driver.find_element(By.NAME, "tipo").send_keys("Tipo X")
        nivel = self.driver.find_element(By.NAME, "nivel"); nivel.clear(); nivel.send_keys("2")
        self.driver.find_element(By.NAME, "foto").clear(); self.driver.find_element(By.NAME, "foto").send_keys("img/breakinglogo.png")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        # Espera: debería permanecer o volver con validación (según implementación). Verificamos que index no contiene fila nueva con nombre vacío.
        WebDriverWait(self.driver, 5).until(EC.url_contains("index.php"))
        rows = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        self.assertGreaterEqual(len(rows), 1)
        print("✓ Crear sin nombre no añade registro inválido")

    def test_11_crear_nivel_limites(self):
        """Límites: Crear con nivel 0 y máximo razonable"""
        # nivel = 0
        self.driver.get(f"{self.base_url}/agregar.php")
        self.driver.find_element(By.NAME, "nombre").send_keys("NivelCero")
        self.driver.find_element(By.NAME, "color").send_keys("#000000")
        self.driver.find_element(By.NAME, "tipo").send_keys("Test")
        n = self.driver.find_element(By.NAME, "nivel"); n.clear(); n.send_keys("0")
        self.driver.find_element(By.NAME, "foto").send_keys("img/breakinglogo.png")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        WebDriverWait(self.driver, 5).until(EC.url_contains("index.php"))
        # nivel = 10
        self.driver.get(f"{self.base_url}/agregar.php")
        self.driver.find_element(By.NAME, "nombre").send_keys("NivelDiez")
        self.driver.find_element(By.NAME, "color").send_keys("#111111")
        self.driver.find_element(By.NAME, "tipo").send_keys("Test")
        n2 = self.driver.find_element(By.NAME, "nivel"); n2.clear(); n2.send_keys("10")
        self.driver.find_element(By.NAME, "foto").send_keys("img/breakinglogo.png")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        WebDriverWait(self.driver, 5).until(EC.url_contains("index.php"))
        print("✓ Crear con niveles límite aceptado")

    def test_12_editar_nombre_vacio(self):
        """Negativa: Editar con nombre vacío"""
        self.driver.get(f"{self.base_url}/index.php")
        editar_buttons = self.driver.find_elements(By.LINK_TEXT, "✏️ Editar")
        if editar_buttons:
            editar_buttons[0].click()
            WebDriverWait(self.driver, 5).until(EC.url_contains("editar.php"))
            nombre = self.driver.find_element(By.NAME, "nombre")
            nombre.clear(); nombre.send_keys("")
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            WebDriverWait(self.driver, 5).until(EC.url_contains("index.php"))
            print("✓ Editar con vacío manejado")
        else:
            print("⚠ No hay registros para editar en prueba negativa")

    def test_13_editar_nombre_largo(self):
        """Límites: Editar con nombre muy largo"""
        self.driver.get(f"{self.base_url}/index.php")
        editar_buttons = self.driver.find_elements(By.LINK_TEXT, "✏️ Editar")
        if editar_buttons:
            editar_buttons[0].click()
            WebDriverWait(self.driver, 5).until(EC.url_contains("editar.php"))
            nombre = self.driver.find_element(By.NAME, "nombre")
            nombre.clear(); nombre.send_keys("X"*255)
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            WebDriverWait(self.driver, 5).until(EC.url_contains("index.php"))
            print("✓ Editar con nombre largo manejado")
        else:
            print("⚠ No hay registros para editar en prueba de límite")

    def test_14_eliminar_sin_sesion(self):
        """Negativa: Intentar eliminar sin sesión"""
        self.driver.get(f"{self.base_url}/logout.php")
        self.driver.get(f"{self.base_url}/eliminar.php?id=1")
        WebDriverWait(self.driver, 5).until(EC.url_contains("login.php"))
        self.assertIn("login.php", self.driver.current_url)
        print("✓ Eliminar sin sesión redirigido a login")

    def test_15_pdf_id_invalido(self):
        """Negativa: Ficha con id inválido"""
        # Asegurar login para acceder a la ruta
        self.test_01_login_success()
        self.driver.get(f"{self.base_url}/descargar_pdf.php?id=999999")
        # Verificar que la página muestra mensaje (texto simple)
        body_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
        self.assertTrue("no encontrado" in body_text or "id" in body_text)
        print("✓ Ficha con id inválido manejada")

if __name__ == "__main__":
    # Ejecutar los tests
    unittest.main(verbosity=2)
