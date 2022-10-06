
CREATE TABLE stock (
    moneyId INTEGER PRIMARY KEY,
    quantity DECIMAL,
    totalExpense DECIMAL,
    moneyEvolution INTEGER,
    lastPrice DECIMAL
);

CREATE TABLE gains (
    day TIMESTAMP,
    gain DECIMAL
);