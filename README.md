# Expense Tracker

A comprehensive personal finance management tool for tracking accounts, transactions, and visualizing spending patterns.

## Project Goals

The goal of this project is to provide a user-friendly interface for managing personal finances. By allowing users to import bank statements and categorize transactions, the application aims to give a clear picture of spending habits through interactive visualizations.

## Key Features

- **Dashboard**: Real-time visualization of expenses by category and over time.
- **Account Management**: Track multiple bank accounts and their balances.
- **Transaction Tracking**: Manual entry and bulk import of transactions.
- **Bulk Import**: Support for XLSX/XLS bank statement uploads with customizable formats.
- **Categorization**: Organize spending into custom categories.

## Tech Stack

- **Frontend**: React, TypeScript, Vite, D3.js, CSS.
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Alembic.
- **Deployment**: Docker, Docker Compose.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Running the Application with Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd expense-tracker
   ```

2. **Start the services**:
   ```bash
   docker-compose up --build
   ```

3. **Run database migrations**:
   ```bash
   docker-compose run --rm migrate
   ```

4. **Access the application**:
   - Frontend: [http://localhost:5173](http://localhost:5173)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - API Documentation (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)

### Local Development Setup

#### Backend
1. Navigate to the backend directory: `cd backend`
2. Install dependencies using Poetry: `poetry install`
3. Set up your `.env` file with database credentials.
4. Run migrations: `poetry run alembic upgrade head`
5. Start the server: `poetry run uvicorn app.main:app --reload`

#### Frontend
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`

## Documentation

- [PROJECT.md](./PROJECT.md): Detailed feature overview.
- [API.md](./API.md): Comprehensive API endpoint documentation.
