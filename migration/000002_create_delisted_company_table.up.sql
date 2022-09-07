CREATE TABLE
  IF NOT EXISTS delisted_company (
    symbol VARCHAR(30),
    company_name VARCHAR(1000),
    exchange VARCHAR(1000),
    ipo_date DATE,
    delisted_date DATE,
    PRIMARY KEY (symbol, exchange, ipo_date)
  );