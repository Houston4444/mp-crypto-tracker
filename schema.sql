
CREATE TABLE stock (
    moneyId INTEGER PRIMARY KEY,
    quantity DECIMAL,
    totalExpense DECIMAL
);

CREATE TABLE gains (
    day TIMESTAMP,
    gain DECIMAL
);