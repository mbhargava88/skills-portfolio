package http

import (
	"expense-tracker/backend/internal/application"
	int_auth "expense-tracker/backend/pkg/auth"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

// NewRouter creates a new Gin router.
func NewRouter(authService *application.AuthService, expenseService *application.ExpenseService, jwtSecret string) *gin.Engine {
	router := gin.Default()

	// Configure and use CORS middleware
	config := cors.Config{
		AllowOrigins:     []string{"http://localhost:3000"},
		AllowMethods:     []string{"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}
	router.Use(cors.New(config))

	authHandler := NewAuthHandler(authService, jwtSecret)
	expenseHandler := NewExpenseHandler(expenseService)

	api := router.Group("/api")
	{
		auth := api.Group("/auth")
		{
			auth.POST("/register", authHandler.Register)
			auth.POST("/login", authHandler.Login)
		}

		expenses := api.Group("/expenses").Use(int_auth.AuthMiddleware(jwtSecret))
		{
			expenses.POST("", expenseHandler.CreateExpense)
			// ... other routes
		}
	}

	return router
}
