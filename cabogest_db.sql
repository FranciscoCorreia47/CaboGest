CREATE USER 'cabogest'@'%' IDENTIFIED BY 'c4b0_g3st#' WITH caching_sha2_password;
CREATE SCHEMA cabogest_db;

USE cabogest_db;

CREATE TABLE rooms (
  id INT AUTO_INCREMENT,
  bed_qty INT NOT NULL DEFAULT 1,
  category ENUM("regular", "view") NOT NULL DEFAULT "regular",
  type ENUM("single", "suite") NOT NULL DEFAULT "single",
  occupied TINYINT NOT NULL DEFAULT 0,
  description TINYTEXT,
  price_per_night FLOAT NOT NULL,
  PRIMARY KEY (id),
  INDEX idx_occupied (occupied)
);

CREATE TABLE clients (
  id INT AUTO_INCREMENT,
  f_name VARCHAR(16) NOT NULL,
  l_name VARCHAR(16) NOT NULL,
  email VARCHAR(64) NOT NULL UNIQUE,
  birth_date DATE,
  nationality VARCHAR(64) NOT NULL,
  PRIMARY KEY (id),
  INDEX idx_name (f_name, l_name),
  INDEX idx_l_name (l_name)
);

CREATE TABLE reservations (
  id INT AUTO_INCREMENT,
  client_id INT NOT NULL,
  room_id INT NOT NULL,
  start_date DATETIME NOT NULL DEFAULT NOW(),
  end_date DATETIME NOT NULL,
  status ENUM("checked_in", "checked_out", "transfered", "canceled") NOT NULL,
  total_price FLOAT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (client_id)
      REFERENCES clients(id),
  FOREIGN KEY (room_id)
      REFERENCES rooms(id),
  INDEX idx_s_date (start_date),
  INDEX idx_e_date (end_date)
);

CREATE TABLE Users (
  id INT AUTO_INCREMENT,
  f_name VARCHAR(16) NOT NULL,
  l_name VARCHAR(16) NOT NULL,
  email VARCHAR(64) NOT NULL UNIQUE,
  role VARCHAR(32) NOT NULL,
  password VARCHAR(32) NOT NULL,
  PRIMARY KEY (id)
);

GRANT ALL PRIVILEGES ON cabogest_db.* TO 'cabogest'@'%';
FLUSH PRIVILEGES;