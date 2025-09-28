package http

import (
	"expense-tracker/backend/internal/application"
	_ "expense-tracker/backend/internal/domain"
	"expense-tracker/backend/pkg/auth"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

// AuthHandler handles authentication requests.

type AuthHandler struct {
	authService *application.AuthService
	jwtSecret   string
}

// NewAuthHandler creates a new AuthHandler.
func NewAuthHandler(authService *application.AuthService, jwtSecret string) *AuthHandler {
	return &AuthHandler{authService: authService, jwtSecret: jwtSecret}
}

// Register registers a new user.
func (h *AuthHandler) Register(c *gin.Context) {
	var req struct {
		Username string `json:"username"`
		Password string `json:"password"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	user, err := h.authService.Register(req.Username, req.Password)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, user)
}

// Login logs in a user.
func (h *AuthHandler) Login(c *gin.Context) {
	var req struct {
		Username string `json:"username"`
		Password string `json:"password"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	user, err := h.authService.Login(req.Username, req.Password)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid credentials"})
		return
	}

	token, err := auth.GenerateToken(user.ID, h.jwtSecret)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not generate token"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"token": token})
}

// ExpenseHandler handles expense requests.

type ExpenseHandler struct {
	expenseService *application.ExpenseService
}

// NewExpenseHandler creates a new ExpenseHandler.
func NewExpenseHandler(expenseService *application.ExpenseService) *ExpenseHandler {
	return &ExpenseHandler{expenseService: expenseService}
}

// CreateExpense creates a new expense.
func (h *ExpenseHandler) CreateExpense(c *gin.Context) {
	var req struct {
		CategoryID  string    `json:"category_id"`
		Amount      float64   `json:"amount"`
		Description string    `json:"description"`
		Date        time.Time `json:"date"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	userID := c.GetString("userID")

	expense, err := h.expenseService.CreateExpense(userID, req.CategoryID, req.Amount, req.Description, req.Date)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, expense)
}

// ... other handlers (Update, Delete, Get, GetAll, GetSummary)
