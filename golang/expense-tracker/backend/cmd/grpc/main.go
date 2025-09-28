package main

import (
	"expense-tracker/backend/internal/application"
	grpchandler "expense-tracker/backend/internal/infrastructure/grpc"
	pb "expense-tracker/backend/internal/infrastructure/grpc/proto"
	"expense-tracker/backend/internal/infrastructure/persistence"
	"expense-tracker/backend/pkg/config"
	"expense-tracker/backend/pkg/logger"
	"log"
	"net"

	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
	"go.uber.org/zap"
	"google.golang.org/grpc"
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

	expenseRepo := persistence.NewPostgresExpenseRepository(db)
	expenseService := application.NewExpenseService(expenseRepo)

	lis, err := net.Listen("tcp", cfg.GRPCServerAddress)
	if err != nil {
		logger.Fatal("cannot create listener", zap.Error(err))
	}

	grpcServer := grpc.NewServer()
	expenseServer := grpchandler.NewServer(expenseService)
	pb.RegisterExpenseServiceServer(grpcServer, expenseServer)

	logger.Info("starting gRPC server", zap.String("address", cfg.GRPCServerAddress))
	if err := grpcServer.Serve(lis); err != nil {
		logger.Fatal("cannot start gRPC server", zap.Error(err))
	}
}
