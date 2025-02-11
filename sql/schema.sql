CREATE TABLE cards (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE card_prices (
    card_id UUID REFERENCES cards(id),
    price_date DATE NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (id, price_date)
);