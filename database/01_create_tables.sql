--Creates tables.
---Products table.
CREATE TABLE IF NOT EXISTS products (
id 
INT 
PRIMARY KEY,
name
VARCHAR(50),
price
float
);

---Couriers table.
CREATE TABLE IF NOT EXISTS couriers (
id 
INT 
PRIMARY KEY,
name
VARCHAR(50),
phone
INT
);