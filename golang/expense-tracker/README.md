# Expense Tracker

This is a full-stack expense tracker application with a React frontend, Go backend, and PostgreSQL database.

## Tech Stack

- **Frontend**: React, TailwindCSS, Recharts
- **Backend**: Go, Domain-Driven Design (DDD)
- **Database**: PostgreSQL
- **Communication**: HTTP (REST) and gRPC
- **Containerization**: Docker, Docker Compose

## Features

- User authentication (signup, login, JWT-based auth).
- CRUD operations for expenses (create, update, delete, list).
- Categories for expenses (e.g. Food, Travel, Rent, Shopping).
- Monthly/weekly summary report endpoints.
- React frontend:
  - Login/Signup page
  - Dashboard with charts (e.g. expenses by category, monthly totals)
  - CRUD UI for managing expenses
- gRPC service:
  - Same business logic as REST (add expense, list expenses, get reports).
  - Example proto files + sample client.

## Project Structure

```
.
├── backend
│   ├── cmd
│   │   ├── grpc
│   │   └── http
│   ├── internal
│   │   ├── application
│   │   ├── domain
│   │   └── infrastructure
│   │       ├── grpc
│   │       ├── http
│   │       └── persistence
│   ├── migrations
│   └── pkg
│       ├── auth
│       ├── config
│       └── logger
├── frontend
│   ├── public
│   └── src
│       ├── auth
│       ├── components
│       ├── pages
│       └── services
├── docker-compose.yml
├── .env
└── README.md
```

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running with Docker Compose

1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd expense-tracker
   ```

2. Create a `.env` file from the example:
   ```sh
   cp .env.example .env
   ```

3. Run the application:
   ```sh
   docker-compose up --build
   ```

- The frontend will be available at `http://localhost:3000`.
- The backend HTTP server will be available at `http://localhost:8080`.
- The backend gRPC server will be available at `localhost:9090`.

### Running Migrations

To run the database migrations, you can use a tool like `migrate`.

1. Install `migrate`:
   ```sh
   go get -u -d github.com/golang-migrate/migrate/v4/cmd/migrate
   ```

2. Run the migrations:
   ```sh
   migrate -path backend/migrations -database "postgres://user:password@localhost:5432/expense_tracker?sslmode=disable" up
   ```

### Example gRPC Calls

You can use a gRPC client like `grpcurl` to interact with the gRPC server.

1. List all expenses for a user:
   ```sh
   grpcurl -plaintext -d '{"user_id": "<user-id>"}' localhost:9090 expenses.ExpenseService/GetExpenses
   ```

2. Create a new expense:
   ```sh
   grpcurl -plaintext -d '{"user_id": "<user-id>", "category_id": "1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed", "amount": 12.34, "description": "Lunch"}' localhost:9090 expenses.ExpenseService/CreateExpense
   ```