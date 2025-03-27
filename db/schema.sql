
CREATE DATABASE IF NOT EXISTS dicedux_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE dicedux_db;

-- جدول ثبت تریدها
CREATE TABLE IF NOT EXISTS trades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(20),
    action ENUM('BUY', 'SELL'),
    entry_price DECIMAL(18,8),
    exit_price DECIMAL(18,8),
    confidence FLOAT,
    profit_usdt DECIMAL(18,8),
    status ENUM('OPEN', 'CLOSED') DEFAULT 'OPEN',
    entry_time DATETIME,
    exit_time DATETIME,
    features TEXT
);

-- جدول بالانس دارایی‌ها
CREATE TABLE IF NOT EXISTS balances (
    symbol VARCHAR(20) PRIMARY KEY,
    balance DECIMAL(18,8),
    open_position BOOLEAN DEFAULT FALSE,
    open_price DECIMAL(18,8),
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
