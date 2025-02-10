CREATE TABLE cards (
    oracle_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE card_prices (
    oracle_id UUID REFERENCES cards(oracle_id),
    price_date DATE NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (oracle_id, price_date)
);