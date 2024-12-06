-- establish the db
CREATE DATABASE IF NOT EXISTS sampledb;
USE sampledb;

-- create users table
CREATE TABLE IF NOT EXISTS userinfo (
    id INT AUTO_INCREMENT PRIMARY KEY,      -- unique integer for each user
    username VARCHAR(50) NOT NULL UNIQUE,   -- username field (must be unique)
    email VARCHAR(100) NOT NULL UNIQUE,     -- email field (must be unique)
    password_hash VARCHAR(255) NOT NULL,    -- password hash (store hashed passwords)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- sets the timestamp on account creation
);

CREATE TABLE IF NOT EXISTS chat_messages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
