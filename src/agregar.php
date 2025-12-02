<?php
require_once 'conexion/db_conexion.php';
session_start();
if (!isset($_SESSION['user_id'])) { header('Location: login.php'); exit(); }
$conn = conectarDB();
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nombre = $_POST['nombre'];
    $color = $_POST['color'];
    $tipo = $_POST['tipo'];
    $nivel = intval($_POST['nivel']);
    $foto = $_POST['foto'];
    $stmt = $conn->prepare("INSERT INTO personajes (nombre, color, tipo, nivel, foto) VALUES (?, ?, ?, ?, ?)");
    $stmt->execute([$nombre, $color, $tipo, $nivel, $foto]);
    header('Location: index.php');
    exit();
}
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container mt-5">
    <h3>Agregar Personaje</h3>
    <form method="POST">
        <div class="mb-3">
            <label class="form-label">Nombre</label>
            <input name="nombre" class="form-control" required>
        </div>
        <div class="mb-3">
            <label class="form-label">Color</label>
            <input name="color" class="form-control" value="#53A548">
        </div>
        <div class="mb-3">
            <label class="form-label">Tipo</label>
            <input name="tipo" class="form-control">
        </div>
        <div class="mb-3">
            <label class="form-label">Nivel</label>
            <input name="nivel" class="form-control" type="number" value="1">
        </div>
        <div class="mb-3">
            <label class="form-label">URL Foto</label>
            <input name="foto" class="form-control" value="img/breakinglogo.png">
        </div>
        <button class="btn btn-success">Agregar</button>
        <a href="index.php" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
</body>
</html>
