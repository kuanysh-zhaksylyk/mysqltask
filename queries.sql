-- 2.1) Show total revenue in year 2020 in Chennai

EXPLAIN SELECT SUM(sales_amount) AS total_revenue
FROM sales.transactions
WHERE YEAR(order_date) = 2020
AND market_code = 'Chennai';

-- sql tuning
CREATE INDEX idx_order_date ON sales.transactions(order_date);
CREATE INDEX idx_product_code ON sales.transactions(product_code);
CREATE INDEX idx_customer_code ON sales.transactions(customer_code);
CREATE INDEX idx_market_code ON sales.transactions(market_code);


-- 2.2) Show total revenue in year 2020, January Month

SELECT SUM(sales_amount) AS total_revenue
FROM sales.transactions
WHERE YEAR(order_date) = 2020
AND MONTH(order_date) = 1;

-- 2.3) Show the most profitable markets_name and total sales_amount for them

SELECT m.markets_name, SUM(t.sales_amount) AS total_sales_amount
FROM sales.transactions t
JOIN sales.markets m ON t.market_code = m.markets_code
GROUP BY t.market_code
ORDER BY total_sales_amount DESC
LIMIT 1;

-- 2.4) Show the customer who bought the most product Prod048

SELECT customer_code, SUM(sales_qty) AS total_quantity
FROM sales.transactions
WHERE product_code = 'Prod048'
GROUP BY customer_code
ORDER BY total_quantity DESC
LIMIT 1;

-- 2.5) Show the average number of products sold per month

SELECT YEAR(order_date) AS order_year, MONTH(order_date) AS order_month, AVG(sales_qty) AS average_products_sold
FROM sales.transactions
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY order_year, order_month;

SELECT AVG(sales_qty) AS average_products_sold_per_month
FROM sales.transactions
GROUP BY YEAR(order_date), MONTH(order_date);

-- 2.6) Show top 10 customers who have made the most purchases in 2017

SELECT customer_code, SUM(sales_qty) AS total_quantity
FROM transactions
WHERE YEAR(order_date) = 2017
GROUP BY customer_code
ORDER BY total_quantity DESC
LIMIT 10;

-- Some tips

-- 1. USE EXPLAIN FOR YOUR SELECT QUERIES
-- 2. LIMIT 1 WHEN YOU NEED A SINGLE ROW
-- 3. INDEX THE FIELDS YOU ARE SEARCHING BY
-- 4. INDEX THE FIELDS FOR JOINING AND USE CONSISTENT COLUMN TYPES FOR THEM
-- 5. AVOID USING ORDER BY RAND() FOR LARGE TABLES
-- 6. AVOID SELECT *
