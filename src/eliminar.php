<?php
require_once 'conexion/db_conexion.php';
session_start();
if (!isset($_SESSION['user_id'])) { header('Location: login.php'); exit(); }
$id = $_GET['id'] ?? null;
if ($id) {
    $conn = conectarDB();
    $stmt = $conn->prepare("DELETE FROM personajes WHERE id = ?");
    $stmt->execute([$id]);
}
header('Location: index.php');
exit();
?>
