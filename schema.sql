CREATE DATABASE IF NOT EXISTS localizacion_itsp
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE localizacion_itsp;

CREATE TABLE IF NOT EXISTS locations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL UNIQUE,
  building VARCHAR(120) NOT NULL,
  floor VARCHAR(40) NULL,
  location_type ENUM('aula','oficina','laboratorio','área común','otro') NOT NULL DEFAULT 'otro'
);

CREATE TABLE IF NOT EXISTS personnel (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(160) NOT NULL,
  role ENUM('docente','administrativo') NOT NULL,
  department VARCHAR(120) NOT NULL,
  subject VARCHAR(160) NULL,
  schedule VARCHAR(160) NULL,
  office VARCHAR(120) NULL,
  room VARCHAR(120) NULL,
  current_location_id INT NULL,
  location_status ENUM('located','unknown','off_campus') NOT NULL DEFAULT 'unknown',
  location_updated_at DATETIME NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_personnel_location FOREIGN KEY (current_location_id) REFERENCES locations(id) ON DELETE SET NULL,
  INDEX idx_personnel_name (full_name),
  INDEX idx_personnel_role (role)
);

-- Espacios de ejemplo: reemplazar por ubicaciones confirmadas del ITSP.
INSERT IGNORE INTO locations (name, building, floor, location_type) VALUES
  ('Aula de demostración', 'Edificio de demostración', 'Planta baja', 'aula'),
  ('Cubículo de demostración', 'Edificio de demostración', 'Planta alta', 'oficina'),
  ('Área común de demostración', 'Edificio de demostración', 'Planta baja', 'área común');

-- Registros ficticios para comprobar la interfaz. Bórralos al cargar información real.
INSERT INTO personnel (full_name, role, department, subject, schedule, office, room, current_location_id, location_status, location_updated_at)
SELECT 'Docente de demostración', 'docente', 'Sistemas Computacionales', 'Programación', 'Lun–Vie · 09:00–14:00', 'Cubículo de demostración', 'Aula de demostración', l.id, 'located', NOW()
FROM locations l WHERE l.name='Aula de demostración'
AND NOT EXISTS (SELECT 1 FROM personnel WHERE full_name='Docente de demostración');

INSERT INTO personnel (full_name, role, department, schedule, office, current_location_id, location_status, location_updated_at)
SELECT 'Personal administrativo de demostración', 'administrativo', 'Servicios Escolares', 'Lun–Vie · 08:00–15:00', 'Oficina de demostración', l.id, 'unknown', NULL
FROM locations l WHERE l.name='Área común de demostración'
AND NOT EXISTS (SELECT 1 FROM personnel WHERE full_name='Personal administrativo de demostración');
