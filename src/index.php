<?php
session_start();
require_once 'conexion/db_conexion.php';
if (!isset($_SESSION['user_id'])) {
    header('Location: login.php');
    exit();
}
$conn = conectarDB();
$stmt = $conn->query("SELECT * FROM personajes");
$result = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Breaking Bad - CRUD</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="text-center mb-0">Personajes de Breaking Bad</h2>
            <div>
                <span class="me-3">Bienvenido, <?= htmlspecialchars($_SESSION['username']) ?></span>
                <a href="logout.php" class="btn btn-secondary">Cerrar sesión</a>
            </div>
        </div>
        <a href="agregar.php" class="btn btn-success mb-3">Agregar Personaje</a>
        <table class="table table-dark table-striped">
            <thead>
                <tr>
                    <th>Foto</th>
                    <th>Nombre</th>
                    <th>Color</th>
                    <th>Tipo</th>
                    <th>Nivel</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($result as $row): ?>
                <tr>
                    <td><img src="<?= htmlspecialchars($row['foto']) ?>" width="50" height="50" style="border-radius:50%;"></td>
                    <td><?= htmlspecialchars($row['nombre']) ?></td>
                    <td style="color: <?= htmlspecialchars($row['color']) ?>;"><?= htmlspecialchars($row['color']) ?></td>
                    <td><?= htmlspecialchars($row['tipo']) ?></td>
                    <td><?= htmlspecialchars($row['nivel']) ?></td>
                    <td>
                        <a href="editar.php?id=<?= $row['id'] ?>" class="btn btn-warning btn-sm">✏️ Editar</a>
                        <a href="eliminar.php?id=<?= $row['id'] ?>" class="btn btn-danger btn-sm">🗑 Eliminar</a>
                        <a href="descargar_pdf.php?id=<?= $row['id'] ?>" class="btn btn-primary btn-sm">📄 PDF</a>
                    </td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
</body>
</html>
