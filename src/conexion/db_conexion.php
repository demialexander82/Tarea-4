<?php
function conectarDB() {
    $db_path = __DIR__ . '/../data/breaking_bad.db';
    
    // Crear carpeta data si no existe
    $data_dir = __DIR__ . '/../data';
    if (!is_dir($data_dir)) {
        mkdir($data_dir, 0755, true);
    }
    
    // Conectar a SQLite
    try {
        $conn = new PDO('sqlite:' . $db_path);
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        
        // Inicializar BD si es nueva
        if (!file_exists($db_path) || filesize($db_path) === 0) {
            inicializarDB($conn);
        }
    } catch (PDOException $e) {
        die('Error de conexión: ' . $e->getMessage());
    }
    
    return $conn;
}

function inicializarDB($conn) {
    $sql = "
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS personajes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        color TEXT DEFAULT '#FFFFFF',
        tipo TEXT DEFAULT '',
        nivel INTEGER DEFAULT 1,
        foto TEXT DEFAULT ''
    );
    ";
    
    $conn->exec($sql);
    
    // Insertar usuario (test/test123) con hash generado en tiempo de inicialización
    $hash = password_hash('test123', PASSWORD_DEFAULT);
    $stmt = $conn->prepare("INSERT INTO usuarios (username, password_hash) VALUES (?, ?)");
    $stmt->execute(['test', $hash]);
    
    // Insertar datos de ejemplo
    $conn->exec("
        INSERT INTO personajes (nombre, color, tipo, nivel, foto) VALUES
        ('Walter White', '#2980B9', 'Protagonista', 5, 'https://via.placeholder.com/50?text=Walter'),
        ('Jesse Pinkman', '#E74C3C', 'Coprotagornista', 4, 'https://via.placeholder.com/50?text=Jesse'),
        ('Hank Schrader', '#F39C12', 'Antagonista', 4, 'https://via.placeholder.com/50?text=Hank')
    ");
}
?>
