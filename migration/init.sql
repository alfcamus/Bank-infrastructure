-- Init DB
CREATE DATABASE IF NOT EXISTS bank_infrastructure;
USE bank_infrastructure;

-- Clients table
CREATE TABLE clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    pesel CHAR(11) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Accounts table
CREATE TABLE accounts (
    account_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),  -- UUID stored as 36-char string
    client_id INT NOT NULL,
    balance DECIMAL(15,2) DEFAULT 0.00,
    account_type ENUM('CHECKING', 'SAVINGS', 'CREDIT') DEFAULT 'CHECKING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);

CREATE INDEX idx_accounts_client_id ON accounts(client_id);

ALTER TABLE clients
ADD login varchar(7) NOT NULL;
ALTER TABLE clients
ADD UNIQUE (login);