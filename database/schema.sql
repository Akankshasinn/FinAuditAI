CREATE DATABASE IF NOT EXISTS finauditai;
USE finauditai;

CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_date DATE NOT NULL,
    vendor_name VARCHAR(120) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    payment_reference VARCHAR(120) NOT NULL,
    category VARCHAR(80),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_vendor_amount (vendor_name, amount),
    INDEX idx_payment_reference (payment_reference)
);

CREATE TABLE IF NOT EXISTS audit_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    risk_score DECIMAL(5,2) NOT NULL,
    anomaly_type VARCHAR(120) NOT NULL,
    audit_status VARCHAR(40) NOT NULL DEFAULT 'Needs review',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_audit_transaction FOREIGN KEY (transaction_id)
        REFERENCES transactions(id) ON DELETE CASCADE
);
