package domain

import "time"

// Expense represents an expense record.

type Expense struct {
	ID          string    `json:"id"`
	UserID      string    `json:"user_id"`
	CategoryID  string    `json:"category_id"`
	Amount      float64   `json:"amount"`
	Description string    `json:"description"`
	Date        time.Time `json:"date"`
	CreatedAt   time.Time `json:"created_at"`
}

// Category represents an expense category.

type Category struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

// ExpenseRepository defines the interface for expense persistence.

type ExpenseRepository interface {
	Create(expense *Expense) error
	Update(expense *Expense) error
	Delete(id string) error
	GetByID(id string) (*Expense, error)
	GetByUserID(userID string) ([]*Expense, error)
	GetSummaryByUserID(userID string, period string) (map[string]float64, error)
}
