-- Create a new database
CREATE DATABASE bank_churn;

-- Use the database
USE bank_churn;

-- Create customers table
CREATE TABLE customers (
    RowNumber INT,
    CustomerId INT PRIMARY KEY,
    Surname VARCHAR(50),
    CreditScore INT,
    Geography VARCHAR(50),
    Gender VARCHAR(10),
    Age INT,
    Tenure INT,
    Balance FLOAT,
    NumOfProducts INT,
    HasCrCard BOOLEAN,
    IsActiveMember BOOLEAN,
    EstimatedSalary FLOAT,
    Exited BOOLEAN
);
