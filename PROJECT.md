# Expense Tracker - Project Overview

The Expense Tracker is a modern web application designed to help users manage their personal finances by tracking bank accounts, transactions, and categories. It features a powerful dashboard for data visualization and supports bulk importing of bank statements.

## Key Features

### 📊 Dashboard & Analytics
- **Visual Insights**: Interactive charts (Pie and Line) powered by D3.js to visualize spending habits.
- **Expense Breakdown**: View total expenses grouped by category with percentage distributions.
- **Spending Trends**: Track expenses over time to identify patterns and manage budgets effectively.

### 🏦 Account Management
- **Multiple Accounts**: Manage multiple bank accounts in one place.
- **Account Details**: Track account names, types, and current balances.
- **CRUD Operations**: Easily add, update, or remove bank accounts.

### 💸 Transaction Management
- **Detailed Tracking**: Record every transaction with date, description, withdrawal, and deposit amounts.
- **Categorization**: Assign transactions to specific categories for better organization.
- **Account Association**: Link transactions to their respective bank accounts.

### 🏷️ Category Management
- **Custom Categories**: Create and manage custom categories tailored to your spending needs.
- **Organization**: Group transactions into categories like "Food", "Rent", "Utilities", etc.

### 📤 Statement Formats & Bulk Import
- **Flexible Parsing**: Define custom statement formats to match different bank statement layouts (XLSX/XLS).
- **Bulk Upload**: Import hundreds of transactions at once by uploading bank statement files.
- **Automated Extraction**: The system automatically extracts transaction data based on the defined formats.

## Tech Stack

- **Backend**: FastAPI (Python 3.12), SQLAlchemy (Asynchronous), PostgreSQL.
- **Frontend**: React (TypeScript), Vite, D3.js for visualizations.
- **DevOps**: Docker & Docker Compose for easy deployment and development.
