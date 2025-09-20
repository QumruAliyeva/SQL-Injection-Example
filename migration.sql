CREATE DATABASE IF NOT EXISTS secinfo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE secinfo;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  role VARCHAR(50) NOT NULL
);

INSERT IGNORE INTO users (username, password, role)
VALUES ('admin', 'admin', 'admin');


