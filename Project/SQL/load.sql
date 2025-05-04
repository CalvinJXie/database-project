SET GLOBAL local_infile=1;

-- ===============================================
-- Load data into the Users table
-- ===============================================
LOAD DATA LOCAL INFILE '~/git/database-project/data/users.csv'
INTO TABLE Users
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(user_id, username, password);


-- ===============================================
-- Load data into the Portfolio table
-- ===============================================
LOAD DATA LOCAL INFILE '~/git/database-project/data/portfolio.csv'
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
LOAD DATA LOCAL INFILE '~/git/database-project/data/stock.csv'
INTO TABLE Stock
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(stock_id, company_name, ticker, sector, exchange);


-- ===============================================
-- Load data into the Transaction table
-- ===============================================
LOAD DATA LOCAL INFILE '~/git/database-project/data/transaction.csv'
INTO TABLE Transaction
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(transaction_id, user_id, stock_id, price, quantity, transaction_type, transaction_time);

LOAD DATA LOCAL INFILE '~/git/database-project/data/user3.csv'
INTO TABLE Transaction
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
(transaction_id, user_id, stock_id, price, quantity, transaction_type, transaction_time)
SET 
    price = CAST(price AS DECIMAL(10,4)),
    quantity = CAST(quantity AS UNSIGNED),
    transaction_time = STR_TO_DATE(transaction_time, '%Y-%m-%d %H:%i:%s');


-- ===============================================
-- Load data into the Stock_Data table
-- ===============================================
LOAD DATA LOCAL INFILE '~/git/database-project/data/stock_data.csv'
INTO TABLE Stock_Data
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(stock_id, current_price, open_price, close_price, low_price, high_price, volume, data_time);




-- C:/Users/itayk/Desktop/CS_4347/Phase_3_Task_C/data/users.csv