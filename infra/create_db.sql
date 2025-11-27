
-- todo move to utf8mb4_0900_ai_ci once I know this is all working

CREATE DATABASE eplatform
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE eplatform;

create table user
(
    id       int auto_increment primary key,
    email    varchar(200) not null unique,
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