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