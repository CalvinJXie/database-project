-- ===============================================
-- Example SQL Script for the MoneyMaker Project
-- ===============================================

-- Step 1: Drop the database if it exists to start fresh.
DROP DATABASE IF EXISTS MoneyMaker;

-- Step 2: Create a new database named MoneyMaker.
CREATE DATABASE MoneyMaker;

-- Step 3: Use the newly created database.
USE MoneyMaker;

-- ===============================================
-- Create the Users Table
-- ===============================================
CREATE TABLE Users (
    user_id   INT NOT NULL AUTO_INCREMENT,
    username  VARCHAR(50) NOT NULL,
    password  VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_id)
) ENGINE=InnoDB;

-- ===============================================
-- Create the Portfolio Table
-- ===============================================
CREATE TABLE Portfolio (
    portfolio_id INT NOT NULL AUTO_INCREMENT,
    user_id      INT NOT NULL,
    balance      DECIMAL(15,2) DEFAULT 0.00 NOT NULL,
    PRIMARY KEY (portfolio_id),
    CONSTRAINT fk_portfolio_user
        FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- ===============================================
-- Create the Stock Table
-- ===============================================
CREATE TABLE Stock (
    stock_id     INT NOT NULL AUTO_INCREMENT,
    company_name VARCHAR(100) NOT NULL,
    ticker       VARCHAR(10) NOT NULL,
    sector       VARCHAR(50),
    exchange     VARCHAR(50),
    PRIMARY KEY (stock_id)
) ENGINE=InnoDB;

-- ===============================================
-- Create the Transaction Table
-- ===============================================
CREATE TABLE Transaction (
    transaction_id   INT NOT NULL AUTO_INCREMENT,
    user_id          INT NOT NULL,
    stock_id         INT NOT NULL,
    price            DECIMAL(15,4) NOT NULL,
    quantity         INT NOT NULL,
    transaction_type VARCHAR(4) NOT NULL,  -- For instance: 'BUY' or 'SELL'
    transaction_time DATETIME NOT NULL,
    PRIMARY KEY (transaction_id),
    CONSTRAINT fk_transaction_user
        FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_transaction_stock
        FOREIGN KEY (stock_id)
        REFERENCES Stock(stock_id)
        ON DELETE NO ACTION
) ENGINE=InnoDB;

-- ===============================================
-- Create the Stock_Data Table
-- ===============================================
CREATE TABLE Stock_Data (
    stock_id      INT NOT NULL,
    current_price DECIMAL(15,4) NOT NULL,
    open_price    DECIMAL(15,4) NOT NULL,
    close_price   DECIMAL(15,4) NOT NULL,
    low_price     DECIMAL(15,4) NOT NULL,
    high_price    DECIMAL(15,4) NOT NULL,
    volume        INT NOT NULL,
    data_time     DATETIME NOT NULL,
    PRIMARY KEY (stock_id, data_time),
    CONSTRAINT fk_stockdata_stock
        FOREIGN KEY (stock_id)
        REFERENCES Stock(stock_id)
        ON DELETE NO ACTION
) ENGINE=InnoDB;

-- ===============================================
-- Insert Sample Data into Users Table
-- ===============================================
INSERT INTO Users (username, password)
VALUES
  ('alice', 'alicepass'),
  ('bob', 'bobpass'),
  ('carol', 'carolpass');

-- ===============================================
-- Insert Sample Data into Portfolio Table
-- ===============================================
INSERT INTO Portfolio (user_id, balance)
VALUES
  (1, 1000.00),
  (2, 1500.00),
  (3, 2000.00);

-- ===============================================
-- Insert Sample Data into Stock Table
-- ===============================================
INSERT INTO Stock (company_name, ticker, sector, exchange)
VALUES
  ('Apple Inc', 'AAPL', 'Technology', 'NASDAQ'),
  ('Microsoft Corp', 'MSFT', 'Technology', 'NASDAQ'),
  ('Tesla Inc', 'TSLA', 'Automotive', 'NASDAQ');

-- ===============================================
-- Insert Sample Data into Transaction Table
-- ===============================================
INSERT INTO Transaction (user_id, stock_id, price, quantity, transaction_type, transaction_time)
VALUES
  (1, 1, 150.0000, 10, 'BUY', '2023-01-10 10:00:00'),
  (2, 2, 250.0000, 5,  'BUY', '2023-01-11 11:00:00'),
  (3, 3, 800.0000, 3,  'SELL', '2023-01-12 12:00:00');

-- ===============================================
-- Insert Sample Data into Stock_Data Table
-- ===============================================
INSERT INTO Stock_Data (stock_id, current_price, open_price, close_price, low_price, high_price, volume, data_time)
VALUES
  (1, 155.0000, 150.0000, 153.0000, 149.5000, 157.0000, 50000, '2023-01-10 10:00:00'),
  (1, 152.0000, 153.0000, 150.0000, 148.0000, 155.0000, 60000, '2023-01-11 10:00:00'),
  (2, 248.0000, 250.0000, 249.0000, 245.0000, 251.0000, 35000, '2023-01-11 11:00:00');
