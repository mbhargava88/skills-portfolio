package main

import (
	"expense-tracker/backend/internal/application"
	"expense-tracker/backend/internal/infrastructure/http"
	"expense-tracker/backend/internal/infrastructure/persistence"
	"expense-tracker/backend/pkg/config"
	"expense-tracker/backend/pkg/logger"
	"log"

	"github.com/golang-migrate/migrate/v4"
	_ "github.com/golang-migrate/migrate/v4/database/postgres"
	_ "github.com/golang-migrate/migrate/v4/source/file"
	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
	"go.uber.org/zap"
)

func main() {
	cfg, err := config.LoadConfig(".")
	if err != nil {
		log.Fatal("cannot load config:", err)
	}

	logger, err := logger.NewLogger()
	if err != nil {
		log.Fatal("cannot create logger:", err)
	}

	db, err := sqlx.Connect(cfg.DBDriver, cfg.DBSource)
	if err != nil {
		logger.Fatal("cannot connect to db", zap.Error(err))
	}

	// Run database migrations
	m, err := migrate.New(
		"file://migrations",
		cfg.DBSource,
	)
	if err != nil {
		logger.Fatal("cannot create new migrate instance", zap.Error(err))
	}
	if err = m.Up(); err != nil && err != migrate.ErrNoChange {
		logger.Fatal("cannot run migrate up", zap.Error(err))
	}
	logger.Info("db migrated successfully")

	userRepo := persistence.NewPostgresUserRepository(db)
	expenseRepo := persistence.NewPostgresExpenseRepository(db)

	authService := application.NewAuthService(userRepo)
	expenseService := application.NewExpenseService(expenseRepo)

	router := http.NewRouter(authService, expenseService, cfg.JWTSecret)

	if err := router.Run(cfg.HTTPServerAddress); err != nil {
		logger.Fatal("cannot start http server", zap.Error(err))
	}
}
