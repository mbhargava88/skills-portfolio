package grpc

import (
	"context"
	"expense-tracker/backend/internal/application"
	pb "expense-tracker/backend/internal/infrastructure/grpc/proto"

	"google.golang.org/protobuf/types/known/timestamppb"
)

// Server is the gRPC server.

type Server struct {
	pb.UnimplementedExpenseServiceServer
	expenseService *application.ExpenseService
}

// NewServer creates a new gRPC server.
func NewServer(expenseService *application.ExpenseService) *Server {
	return &Server{expenseService: expenseService}
}

// CreateExpense creates a new expense.
func (s *Server) CreateExpense(ctx context.Context, req *pb.CreateExpenseRequest) (*pb.CreateExpenseResponse, error) {
	date := req.Date.AsTime()
	expense, err := s.expenseService.CreateExpense(req.UserId, req.CategoryId, req.Amount, req.Description, date)
	if err != nil {
		return nil, err
	}

	return &pb.CreateExpenseResponse{
		Expense: &pb.Expense{
			Id:          expense.ID,
			UserId:      expense.UserID,
			CategoryId:  expense.CategoryID,
			Amount:      expense.Amount,
			Description: expense.Description,
			Date:        timestamppb.New(expense.Date),
			CreatedAt:   timestamppb.New(expense.CreatedAt),
		},
	}, nil
}

// GetExpenses gets all expenses for a user.
func (s *Server) GetExpenses(ctx context.Context, req *pb.GetExpensesRequest) (*pb.GetExpensesResponse, error) {
	expenses, err := s.expenseService.GetExpenses(req.UserId)
	if err != nil {
		return nil, err
	}

	var pbExpenses []*pb.Expense
	for _, expense := range expenses {
		pbExpenses = append(pbExpenses, &pb.Expense{
			Id:          expense.ID,
			UserId:      expense.UserID,
			CategoryId:  expense.CategoryID,
			Amount:      expense.Amount,
			Description: expense.Description,
			Date:        timestamppb.New(expense.Date),
			CreatedAt:   timestamppb.New(expense.CreatedAt),
		})
	}

	return &pb.GetExpensesResponse{Expenses: pbExpenses}, nil
}
