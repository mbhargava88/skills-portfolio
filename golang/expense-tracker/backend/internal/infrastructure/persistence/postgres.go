package persistence

import (
	"expense-tracker/backend/internal/domain"

	"github.com/jmoiron/sqlx"
)

// PostgresUserRepository is a PostgreSQL implementation of the UserRepository.

type PostgresUserRepository struct {
	DB *sqlx.DB
}

// NewPostgresUserRepository creates a new PostgresUserRepository.
func NewPostgresUserRepository(db *sqlx.DB) *PostgresUserRepository {
	return &PostgresUserRepository{DB: db}
}

// Create creates a new user.
func (r *PostgresUserRepository) Create(user *domain.User) error {
	_, err := r.DB.Exec("INSERT INTO users (id, username, password) VALUES ($1, $2, $3)", user.ID, user.Username, user.Password)
	return err
}

// GetByUsername gets a user by username.
func (r *PostgresUserRepository) GetByUsername(username string) (*domain.User, error) {
	var user domain.User
	err := r.DB.Get(&user, "SELECT * FROM users WHERE username = $1", username)
	return &user, err
}

// GetByID gets a user by ID.
func (r *PostgresUserRepository) GetByID(id string) (*domain.User, error) {
	var user domain.User
	err := r.DB.Get(&user, "SELECT * FROM users WHERE id = $1", id)
	return &user, err
}

// PostgresExpenseRepository is a PostgreSQL implementation of the ExpenseRepository.

type PostgresExpenseRepository struct {
	DB *sqlx.DB
}

// NewPostgresExpenseRepository creates a new PostgresExpenseRepository.
func NewPostgresExpenseRepository(db *sqlx.DB) *PostgresExpenseRepository {
	return &PostgresExpenseRepository{DB: db}
}

// Create creates a new expense.
func (r *PostgresExpenseRepository) Create(expense *domain.Expense) error {
	_, err := r.DB.Exec("INSERT INTO expenses (id, user_id, category_id, amount, description, date) VALUES ($1, $2, $3, $4, $5, $6)", expense.ID, expense.UserID, expense.CategoryID, expense.Amount, expense.Description, expense.Date)
	return err
}

// Update updates an existing expense.
func (r *PostgresExpenseRepository) Update(expense *domain.Expense) error {
	_, err := r.DB.Exec("UPDATE expenses SET category_id = $1, amount = $2, description = $3, date = $4 WHERE id = $5", expense.CategoryID, expense.Amount, expense.Description, expense.Date, expense.ID)
	return err
}

// Delete deletes an expense.
func (r *PostgresExpenseRepository) Delete(id string) error {
	_, err := r.DB.Exec("DELETE FROM expenses WHERE id = $1", id)
	return err
}

// GetByID gets an expense by ID.
func (r *PostgresExpenseRepository) GetByID(id string) (*domain.Expense, error) {
	var expense domain.Expense
	err := r.DB.Get(&expense, "SELECT * FROM expenses WHERE id = $1", id)
	return &expense, err
}

// GetByUserID gets all expenses for a user.
func (r *PostgresExpenseRepository) GetByUserID(userID string) ([]*domain.Expense, error) {
	var expenses []*domain.Expense
	err := r.DB.Select(&expenses, "SELECT * FROM expenses WHERE user_id = $1", userID)
	return expenses, err
}

// GetSummaryByUserID gets an expense summary for a user.
func (r *PostgresExpenseRepository) GetSummaryByUserID(userID string, period string) (map[string]float64, error) {
	// This is a simplified summary. A real implementation would be more complex.
	rows, err := r.DB.Queryx("SELECT c.name, SUM(e.amount) FROM expenses e JOIN categories c ON e.category_id = c.id WHERE e.user_id = $1 GROUP BY c.name", userID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	summary := make(map[string]float64)
	for rows.Next() {
		var categoryName string
		var total float64
		if err := rows.Scan(&categoryName, &total); err != nil {
			return nil, err
		}
		summary[categoryName] = total
	}

	return summary, nil
}
