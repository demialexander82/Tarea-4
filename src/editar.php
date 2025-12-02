<?php
require_once 'conexion/db_conexion.php';
session_start();
if (!isset($_SESSION['user_id'])) { header('Location: login.php'); exit(); }
$conn = conectarDB();
$id = $_GET['id'] ?? null;
if (!$id) { header('Location: index.php'); exit(); }
$stmt = $conn->prepare("SELECT * FROM personajes WHERE id = ?");
$stmt->execute([$id]);
$row = $stmt->fetch(PDO::FETCH_ASSOC);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nombre = $_POST['nombre'];
    $color = $_POST['color'];
    $tipo = $_POST['tipo'];
    $nivel = intval($_POST['nivel']);
    $foto = $_POST['foto'];
    $stmt = $conn->prepare("UPDATE personajes SET nombre=?, color=?, tipo=?, nivel=?, foto=? WHERE id=?");
    $stmt->execute([$nombre, $color, $tipo, $nivel, $foto, $id]);
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
    <h3>Editar Personaje</h3>
    <form method="POST">
        <div class="mb-3">
            <label class="form-label">Nombre</label>
            <input name="nombre" class="form-control" value="<?= htmlspecialchars($row['nombre']) ?>" required>
        </div>
        <div class="mb-3">
            <label class="form-label">Color</label>
            <input name="color" class="form-control" value="<?= htmlspecialchars($row['color']) ?>">
        </div>
        <div class="mb-3">
            <label class="form-label">Tipo</label>
            <input name="tipo" class="form-control" value="<?= htmlspecialchars($row['tipo']) ?>">
        </div>
        <div class="mb-3">
            <label class="form-label">Nivel</label>
            <input name="nivel" class="form-control" type="number" value="<?= htmlspecialchars($row['nivel']) ?>">
        </div>
        <div class="mb-3">
            <label class="form-label">URL Foto</label>
            <input name="foto" class="form-control" value="<?= htmlspecialchars($row['foto']) ?>">
        </div>
        <button class="btn btn-warning">Guardar</button>
        <a href="index.php" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
</body>
</html>
