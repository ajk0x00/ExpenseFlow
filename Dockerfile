# Stage 1: Build Frontend
FROM node:20-slim AS frontend-builder

WORKDIR /frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY frontend/ ./

# Build the frontend
RUN npm run build

# Stage 2: Build Backend
FROM python:3.12-slim

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy dependency files
COPY backend/pyproject.toml backend/poetry.lock* /app/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the backend code
COPY backend/ /app/

# Copy the built frontend assets from Stage 1
COPY --from=frontend-builder /frontend/dist /app/static

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
