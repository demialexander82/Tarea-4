<?php
require_once __DIR__ . '/conexion/db_conexion.php';
$conn = conectarDB();
header('Content-Type: text/plain; charset=utf-8');
if (isset($_GET['reset']) && $_GET['reset'] === '1') {
    $hash = password_hash('test123', PASSWORD_DEFAULT);
    $stmt = $conn->prepare('UPDATE usuarios SET password_hash = ? WHERE username = ?');
    $stmt->execute([$hash, 'test']);
    echo "Password del usuario 'test' reiniciada a test123\n\n";
}
$rows = $conn->query('SELECT id, username FROM usuarios')->fetchAll(PDO::FETCH_ASSOC);
if (!$rows) {
    echo "No hay usuarios en la tabla.\n";
    exit;
}
foreach ($rows as $r) {
    echo $r['id'] . ':' . $r['username'] . "\n";
}
