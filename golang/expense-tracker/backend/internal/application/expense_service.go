package application

import (
	"errors"
	"expense-tracker/backend/internal/domain"
	"time"

	"github.com/google/uuid"
)

// ExpenseService provides expense management services.

type ExpenseService struct {
	expenseRepo domain.ExpenseRepository
}

// NewExpenseService creates a new ExpenseService.
func NewExpenseService(expenseRepo domain.ExpenseRepository) *ExpenseService {
	return &ExpenseService{expenseRepo: expenseRepo}
}

// CreateExpense creates a new expense.
func (s *ExpenseService) CreateExpense(userID, categoryID string, amount float64, description string, date time.Time) (*domain.Expense, error) {
	expense := &domain.Expense{
		ID:          uuid.New().String(),
		UserID:      userID,
		CategoryID:  categoryID,
		Amount:      amount,
		Description: description,
		Date:        date,
	}

	if err := s.expenseRepo.Create(expense); err != nil {
		return nil, err
	}

	return expense, nil
}

// UpdateExpense updates an existing expense.
func (s *ExpenseService) UpdateExpense(id, userID, categoryID string, amount float64, description string, date time.Time) (*domain.Expense, error) {
	expense, err := s.expenseRepo.GetByID(id)
	if err != nil {
		return nil, err
	}

	if expense.UserID != userID {
		return nil, errors.New("permission denied")
	}

	expense.CategoryID = categoryID
	expense.Amount = amount
	expense.Description = description
	expense.Date = date

	if err := s.expenseRepo.Update(expense); err != nil {
		return nil, err
	}

	return expense, nil
}

// DeleteExpense deletes an expense.
func (s *ExpenseService) DeleteExpense(id, userID string) error {
	expense, err := s.expenseRepo.GetByID(id)
	if err != nil {
		return err
	}

	if expense.UserID != userID {
		return errors.New("permission denied")
	}

	return s.expenseRepo.Delete(id)
}

// GetExpense returns an expense by ID.
func (s *ExpenseService) GetExpense(id, userID string) (*domain.Expense, error) {
	expense, err := s.expenseRepo.GetByID(id)
	if err != nil {
		return nil, err
	}

	if expense.UserID != userID {
		return nil, errors.New("permission denied")
	}

	return expense, nil
}

// GetExpenses returns all expenses for a user.
func (s *ExpenseService) GetExpenses(userID string) ([]*domain.Expense, error) {
	return s.expenseRepo.GetByUserID(userID)
}

// GetExpenseSummary returns an expense summary for a user.
func (s *ExpenseService) GetExpenseSummary(userID, period string) (map[string]float64, error) {
	return s.expenseRepo.GetSummaryByUserID(userID, period)
}
