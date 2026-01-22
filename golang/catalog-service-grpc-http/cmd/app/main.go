package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/example/catalog-mgmt-app/internal/handler/grpc"
	httpHandler "github.com/example/catalog-mgmt-app/internal/handler/http"
	"github.com/example/catalog-mgmt-app/internal/repository"
	"github.com/example/catalog-mgmt-app/internal/service"
	pb "github.com/example/catalog-mgmt-app/proto"
	_ "github.com/lib/pq"
	googleGrpc "google.golang.org/grpc"
)

func main() {
	// 1. Configuration (env vars)
	dbHost := os.Getenv("DB_HOST")
	dbPort := os.Getenv("DB_PORT")
	dbUser := os.Getenv("DB_USER")
	dbPass := os.Getenv("DB_PASSWORD")
	dbName := os.Getenv("DB_NAME")

	if dbHost == "" {
		dbHost = "localhost"
	}
	if dbPort == "" {
		dbPort = "5470"
	}
	if dbUser == "" {
		dbUser = "postgres"
	}
	if dbName == "" {
		dbName = "catalogs"
	}

	connStr := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		dbHost, dbPort, dbUser, dbPass, dbName)

	// 2. Database Connection
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		log.Fatalf("Failed to open db connection: %v", err)
	}
	defer db.Close()

	if err := db.Ping(); err != nil {
		log.Printf("Warning: Failed to ping db: %v", err)
		// We might continue or fail here depending on strategy.
		// For k8s, it might restart.
	}

	// 3. Dependencies
	repo := repository.NewPostgresRepository(db)
	svc := service.NewProductService(repo)
	h := httpHandler.NewProductHandler(svc)
	grpcSvc := grpc.NewProductGrpcServer(svc)

	// 4. Servers
	// HTTP Server
	httpMux := http.NewServeMux()
	httpMux.HandleFunc("/products", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodGet {
			h.GetProduct(w, r)
		} else if r.Method == http.MethodPost {
			h.CreateProduct(w, r)
		} else {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	httpServer := &http.Server{
		Addr:    ":8080",
		Handler: httpMux,
	}

	// gRPC Server
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("Failed to listen for gRPC: %v", err)
	}
	grpcServer := googleGrpc.NewServer()
	pb.RegisterProductServiceServer(grpcServer, grpcSvc)

	// 5. Start Servers (Goroutines)
	go func() {
		log.Println("Starting HTTP server on :8080")
		if err := httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("HTTP server error: %v", err)
		}
	}()

	go func() {
		log.Println("Starting gRPC server on :50051")
		if err := grpcServer.Serve(lis); err != nil {
			log.Fatalf("gRPC server error: %v", err)
		}
	}()

	// 6. Graceful Shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Println("Shutting down servers...")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := httpServer.Shutdown(ctx); err != nil {
		log.Printf("HTTP server shutdown error: %v", err)
	}

	grpcServer.GracefulStop()
	log.Println("Servers stopped.")
}
