SET GLOBAL local_infile=1;

-- ===============================================
-- Load data into the Users table
-- ===============================================
LOAD DATA LOCAL INFILE 'C:/Users/itayk/Desktop/CS_4347/Phase_3_Task_C/data/users.csv'
INTO TABLE Users
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(user_id, username, pass_word);


-- ===============================================
-- Load data into the Portfolio table
-- ===============================================
LOAD DATA LOCAL INFILE 'C:/Users/itayk/Desktop/CS_4347/Phase_3_Task_C/data/portfolio.csv'
INTO TABLE Portfolio
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(portfolio_id, user_id, balance);


-- ===============================================
-- Load data into the Stock table
-- ===============================================
-- Note: If the stock_id is auto-incremented in your table,
-- you can omit it from the LOAD statement if your CSV
-- does not include it. Here we assume the CSV includes stock_id.
LOAD DATA LOCAL INFILE 'C:/Users/itayk/Desktop/CS_4347/Phase_3_Task_C/data/stock.csv'
INTO TABLE Stock
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(stock_id, company_name, ticker, sector, exchange);


-- ===============================================
-- Load data into the Transaction table
-- ===============================================
LOAD DATA LOCAL INFILE 'C:/Users/itayk/Desktop/CS_4347/Phase_3_Task_C/data/transaction.csv'
INTO TABLE Transaction
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(transaction_id, user_id, stock_id, price, quantity, transaction_type, transaction_time);


-- ===============================================
-- Load data into the Stock_Data table
-- ===============================================
LOAD DATA LOCAL INFILE 'C:/Users/itayk/Desktop/CS_4347/Phase_3_Task_C/data/stock_data.csv'
INTO TABLE Stock_Data
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(stock_id, current_price, open_price, close_price, low_price, high_price, volume, data_time);
