-- Step 1: Create the database (optional)
CREATE DATABASE IF NOT EXISTS sampledb;
USE sampledb;

-- Step 2: Create the users table
CREATE TABLE IF NOT EXISTS userinfo (
    id INT AUTO_INCREMENT PRIMARY KEY,      -- Unique ID for each user
    username VARCHAR(50) NOT NULL UNIQUE,   -- Username field (must be unique)
    email VARCHAR(100) NOT NULL UNIQUE,     -- Email field (must be unique)
    password_hash VARCHAR(255) NOT NULL,    -- Password hash (store hashed passwords)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Automatically sets the timestamp on account creation
);

CREATE TABLE IF NOT EXISTS chat_messages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
