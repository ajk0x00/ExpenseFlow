# Expense Tracker - API Documentation

This document provides detailed information about the API endpoints available in the Expense Tracker application. All endpoints are prefixed with `/api/v1`.

## Authentication API
Manage user authentication and registration.

### `POST /auth/jwt/login`
Login to obtain an access token.
- **Body (form-data)**: `OAuth2PasswordRequestForm`
  - `username`: Email address.
  - `password`: User password.
- **Response**: Access token.
  ```json
  {
    "access_token": "eyJhbG...",
    "token_type": "bearer"
  }
  ```

### `POST /auth/jwt/logout`
Logout the current user.
- **Response**: Empty 204 response.

### `POST /auth/register`
Register a new user.
- **Body**: `UserCreate` object.
  ```json
  {
    "email": "user@example.com",
    "password": "strongpassword",
    "is_active": true,
    "is_superuser": false,
    "is_verified": false
  }
  ```
- **Response**: The created `User` object.

### `GET /users/me`
Get current authenticated user details.
- **Response**: `UserRead` object.
  ```json
  {
    "id": "uuid...",
    "email": "user@example.com",
    "is_active": true,
    "is_superuser": false,
    "is_verified": false
  }
  ```

---

## Accounts API
Manage bank accounts.

### `GET /accounts/`
Retrieve a list of bank accounts.
- **Parameters**:
  - `skip` (int, optional): Number of records to skip. Default: 0.
  - `limit` (int, optional): Maximum number of records to return. Default: 100.
- **Response**: List of `BankAccount` objects.
  ```json
  [
    {
      "id": 1,
      "account_name": "Main Savings",
      "bank_name": "Global Bank",
      "description": "Primary savings account",
      "account_type": "savings",
      "metadata_": null
    }
  ]
  ```

### `POST /accounts/`
Create a new bank account.
- **Body**: `BankAccountCreate` object.
  ```json
  {
    "account_name": "Main Savings",
    "bank_name": "Global Bank",
    "description": "Primary savings account",
    "account_type": "savings",
    "metadata_": {}
  }
  ```
- **Response**: The created `BankAccount` object.
  ```json
  {
    "id": 1,
    "account_name": "Main Savings",
    "bank_name": "Global Bank",
    "description": "Primary savings account",
    "account_type": "savings",
    "metadata_": {}
  }
  ```

### `GET /accounts/{id}`
Get a specific bank account by ID.
- **Parameters**:
  - `id` (int): Account ID.
- **Response**: `BankAccount` object.

### `PUT /accounts/{id}`
Update an existing bank account.
- **Parameters**:
  - `id` (int): Account ID.
- **Body**: `BankAccountUpdate` object.
  ```json
  {
    "account_name": "Updated Savings Name",
    "account_type": "savings"
  }
  ```
- **Response**: The updated `BankAccount` object.

### `DELETE /accounts/{id}`
Delete a bank account.
- **Parameters**:
  - `id` (int): Account ID.
- **Response**: The deleted `BankAccount` object.

---

## Transactions API
Manage financial transactions.

### `GET /transactions/`
Retrieve a list of transactions.
- **Parameters**:
  - `skip` (int, optional): Number of records to skip.
  - `limit` (int, optional): Maximum number of records to return.
- **Response**: List of `Transaction` objects.
  ```json
  [
    {
      "id": 1,
      "account_id": 1,
      "date": "2023-10-27T10:00:00",
      "narration": "Grocery Store",
      "withdrawal_amount": "50.25",
      "deposit_amount": "0.00",
      "metadata_": null,
      "categories": [
        {
          "id": 1,
          "name": "Food",
          "description": "Groceries and dining"
        }
      ]
    }
  ]
  ```

### `POST /transactions/`
Create a new transaction manually.
- **Body**: `TransactionCreate` object.
  ```json
  {
    "account_id": 1,
    "date": "2023-10-27T10:00:00",
    "narration": "Grocery Store",
    "withdrawal_amount": 50.25,
    "deposit_amount": 0.00,
    "category_ids": [1]
  }
  ```
- **Response**: The created `Transaction` object.

### `POST /transactions/upload`
Upload and import transactions from a bank statement (XLSX/XLS).
- **Body (Form-Data)**:
  - `file`: The statement file.
  - `statement_format_id` (int): ID of the format to use for parsing.
  - `account_id` (int): ID of the account to associate transactions with.
- **Response**: Summary of the import.
  ```json
  {
    "success": true,
    "count": 45,
    "total_withdrawals": 1250.50,
    "total_deposits": 3000.00,
    "net": 1749.50
  }
  ```

### `GET /transactions/{id}`
Get a specific transaction by ID.
- **Response**: `Transaction` object.

---

## Categories API
Manage transaction categories.

### `GET /categories/`
Retrieve all categories.
- **Response**: List of `Category` objects.
  ```json
  [
    {
      "id": 1,
      "name": "Food",
      "description": "Groceries and dining"
    }
  ]
  ```

### `POST /categories/`
Create a new category.
- **Body**: `CategoryCreate` object.
  ```json
  {
    "name": "Entertainment",
    "description": "Movies, concerts, and hobbies"
  }
  ```
- **Response**: The created `Category` object.

---

## Analytics API
Data visualization and reporting endpoints.

### `GET /analytics/expenses-by-category`
Get total expenses grouped by category.
- **Parameters**:
  - `start_date` (string, optional): ISO date string.
  - `end_date` (string, optional): ISO date string.
- **Response**: `ExpensesByCategoryResponse`.
  ```json
  {
    "items": [
      {
        "category_name": "Food",
        "amount": 450.75,
        "percentage": 35.5
      },
      {
        "category_name": "Rent",
        "amount": 800.00,
        "percentage": 63.1
      }
    ],
    "total_amount": 1267.50
  }
  ```

### `GET /analytics/expenses-over-time`
Get total expenses grouped by date for time-series charts.
- **Parameters**:
  - `start_date` (string, optional): ISO date string.
  - `end_date` (string, optional): ISO date string.
- **Response**: List of `ExpenseOverTime` objects.
  ```json
  [
    {
      "date": "2023-10-01",
      "amount": 50.00
    },
    {
      "date": "2023-10-02",
      "amount": 25.50
    }
  ]
  ```

---

## Statement Formats API
Manage parsing rules for different bank statements.

### `GET /statement-formats/`
Retrieve all statement formats.
- **Response**: List of `StatementFormat` objects.
  ```json
  [
    {
      "id": 1,
      "format_name": "Standard Bank CSV",
      "bank_name": "Standard Bank",
      "data_start_row": 2,
      "date_column": "A",
      "narration_column": "B",
      "withdrawal_column": "C",
      "deposit_column": "D",
      "created_at": "2023-10-27T10:00:00",
      "updated_at": "2023-10-27T10:00:00"
    }
  ]
  ```

### `POST /statement-formats/`
Create a new statement format.
- **Body**: `StatementFormatCreate` object.
  ```json
  {
    "format_name": "New Bank Format",
    "bank_name": "New Bank",
    "data_start_row": 1,
    "date_column": "Date",
    "narration_column": "Description",
    "withdrawal_column": "Debit",
    "deposit_column": "Credit"
  }
  ```
- **Response**: The created `StatementFormat` object.
