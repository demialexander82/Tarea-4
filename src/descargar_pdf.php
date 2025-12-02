<?php
session_start();
require_once 'conexion/db_conexion.php';

if (!isset($_SESSION['user_id'])) {
    header('Location: login.php');
    exit();
}

if (!isset($_GET['id'])) {
    die('ID no especificado');
}

$id = intval($_GET['id']);
$conn = conectarDB();
$stmt = $conn->prepare("SELECT * FROM personajes WHERE id = ?");
$stmt->execute([$id]);
$personaje = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$personaje) {
    die('Personaje no encontrado');
}

// Enviar contenido HTML normal y permitir imprimir/guardar como PDF desde el navegador
header('Content-Type: text/html; charset=UTF-8');
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Personaje - <?= htmlspecialchars($personaje['nombre']) ?></title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            border-bottom: 3px solid #333;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .info-row {
            margin: 15px 0;
            padding: 10px;
            border-left: 4px solid <?= htmlspecialchars($personaje['color']) ?>;
            background: #f5f5f5;
        }
        .label {
            font-weight: bold;
            color: #555;
        }
        img {
            max-width: 200px;
            border-radius: 10px;
            margin: 20px auto;
            display: block;
        }
        @media print {
            .no-print { display: none; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Breaking Bad - Ficha de Personaje</h1>
    </div>
    
    <img src="<?= htmlspecialchars($personaje['foto']) ?>" alt="<?= htmlspecialchars($personaje['nombre']) ?>">
    
    <div class="info-row">
        <span class="label">Nombre:</span>
        <?= htmlspecialchars($personaje['nombre']) ?>
    </div>
    
    <div class="info-row">
        <span class="label">Color:</span>
        <span style="color: <?= htmlspecialchars($personaje['color']) ?>;">
            <?= htmlspecialchars($personaje['color']) ?>
        </span>
    </div>
    
    <div class="info-row">
        <span class="label">Tipo:</span>
        <?= htmlspecialchars($personaje['tipo']) ?>
    </div>
    
    <div class="info-row">
        <span class="label">Nivel:</span>
        <?= htmlspecialchars($personaje['nivel']) ?>
    </div>
    
    <div style="text-align: center; margin-top: 50px;" class="no-print">
        <button onclick="window.print()">Imprimir / Guardar como PDF</button>
        <a href="index.php" style="margin-left: 20px;">Volver</a>
    </div>
    
    <script>
        // Auto-abrir diálogo de impresión
        // window.print();
    </script>
</body>
</html>
