# Banking Application Using SQLite3

## Overview
This is a simple banking application that connects to an SQLite3 database and provides the following features:
- Register a new account
- Generate a PIN
- Deposit money
- Withdraw money
- Transfer money between accounts

The application uses Python's `sqlite3` module to handle database operations. Below is the step-by-step guide and the code implementation.

## Prerequisites
- Python 3.x
- SQLite3

## Database Setup
First, we need to create an SQLite3 database named `banking.db` and a table `accounts` to store user account information.

```python
import sqlite3

# Connect to SQLite3 database
conn = sqlite3.connect('banking.db')

# Create a cursor object
cursor = conn.cursor()

# Create accounts table
cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    account_number INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    pin INTEGER NOT NULL,
    balance REAL DEFAULT 0.0
);
''')

# Commit changes and close the connection
conn.commit()
conn.close()
```

## Features

### 1. Register a New Account
```python
import sqlite3

def register(name, pin):
    conn = sqlite3.connect('banking.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts (name, pin) VALUES (?, ?)", (name, pin))
    conn.commit()
    print("Account registered successfully!")
    conn.close()
```

### 2. Generate a PIN
```python
import random

def generate_pin():
    return random.randint(1000, 9999)

# Example usage
new_pin = generate_pin()
print(f"Your new PIN is: {new_pin}")
```

### 3. Deposit Money
```python
import sqlite3

def deposit(account_number, amount):
    conn = sqlite3.connect('banking.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_number = ?", (amount, account_number))
    conn.commit()
    print("Deposit successful!")
    conn.close()
```

### 4. Withdraw Money
```python
import sqlite3

def withdraw(account_number, amount):
    conn = sqlite3.connect('banking.db')
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_number,))
    balance = cursor.fetchone()[0]

    if balance >= amount:
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_number = ?", (amount, account_number))
        conn.commit()
        print("Withdrawal successful!")
    else:
        print("Insufficient balance!")

    conn.close()
```

### 5. Transfer Money Between Accounts
```python
import sqlite3

def transfer(from_account, to_account, amount):
    conn = sqlite3.connect('banking.db')
    cursor = conn.cursor()

    # Check balance of sender
    cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (from_account,))
    from_balance = cursor.fetchone()[0]

    if from_balance >= amount:
        # Deduct from sender
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_number = ?", (amount, from_account))
        # Add to recipient
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_number = ?", (amount, to_account))
        conn.commit()
        print("Transfer successful!")
    else:
        print("Insufficient balance!")

    conn.close()
```

## Running the Application
1. Copy the code snippets into your Python file (e.g., `banking_app.py`).
2. Run the file using the command:
   ```
   python banking_app.py
   ```
3. Call the functions as needed to perform banking operations.

## Example Usage
```python
# Register a new account
register("Anji", 1234)

# Deposit money
deposit(1, 500.0)

# Withdraw money
withdraw(1, 200.0)

# Transfer money
transfer(1, 2, 100.0)
```


