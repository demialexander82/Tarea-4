-- Base de datos para la aplicación Breaking Bad CRUD
CREATE DATABASE IF NOT EXISTS breakingdb DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE breakingdb;

CREATE TABLE IF NOT EXISTS usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS personajes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  color VARCHAR(50) DEFAULT '#FFFFFF',
  tipo VARCHAR(100) DEFAULT '',
  nivel INT DEFAULT 1,
  foto VARCHAR(500) DEFAULT ''
);

-- Usuario de ejemplo (usuario: test, contraseña: test123)
-- Hash generado con: password_hash('test123', PASSWORD_DEFAULT)
INSERT INTO usuarios (username, password_hash) VALUES ('test', '$2y$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcg7b3XeKeUxWdeS86E36XQuvKO');

-- Datos de ejemplo
INSERT INTO personajes (nombre, color, tipo, nivel, foto) VALUES
('Walter White', '#2980B9', 'Protagonista', 5, 'https://via.placeholder.com/50?text=Walter'),
('Jesse Pinkman', '#E74C3C', 'Coprotagornista', 4, 'https://via.placeholder.com/50?text=Jesse'),
('Hank Schrader', '#F39C12', 'Antagonista', 4, 'https://via.placeholder.com/50?text=Hank');
