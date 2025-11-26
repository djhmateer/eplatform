 -- CREATE DATABASE eplatform
--   CHARACTER SET utf8mb4
--   COLLATE utf8mb4_unicode_ci;


create table user
(
    id       int auto_increment primary key,
    username varchar(100) not null unique,
    email    varchar(200) not null,
    password varchar(255) not null
); 
  
CREATE TABLE session (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL UNIQUE,
    user_id INT NOT NULL,
    expires_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    INDEX idx_session_id (session_id),
    INDEX idx_expires_at (expires_at)
);