CREATE TABLE
  IF NOT EXISTS historical_dividend (
    symbol VARCHAR(30),
    date DATE,
    label VARCHAR(250),
    adj_dividend DECIMAL(28, 9),
    dividend DECIMAL(28, 9),
    record_date DATE,
    payment_date DATE,
    declaration_date DATE,
    PRIMARY KEY (symbol, date)
  );