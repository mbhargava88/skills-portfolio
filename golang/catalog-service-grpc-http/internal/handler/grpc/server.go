package grpc

import (
	"context"

	"github.com/example/catalog-mgmt-app/internal/service"
	pb "github.com/example/catalog-mgmt-app/proto"
)

type ProductGrpcServer struct {
	pb.UnimplementedProductServiceServer
	svc *service.ProductService
}

func NewProductGrpcServer(svc *service.ProductService) *ProductGrpcServer {
	return &ProductGrpcServer{svc: svc}
}

func (s *ProductGrpcServer) CreateProduct(ctx context.Context, req *pb.CreateProductRequest) (*pb.ProductResponse, error) {
	p, err := s.svc.CreateProduct(ctx, req.Name, req.Price)
	if err != nil {
		return nil, err
	}

	return &pb.ProductResponse{
		Id:    p.ID,
		Name:  p.Name,
		Price: p.Price,
	}, nil
}

func (s *ProductGrpcServer) GetProduct(ctx context.Context, req *pb.GetProductRequest) (*pb.ProductResponse, error) {
	p, err := s.svc.GetProduct(ctx, req.Id)
	if err != nil {
		return nil, err
	}
	if p == nil {
		// You might want to return a specific gRPC error code for not found
		return &pb.ProductResponse{}, nil
	}

	return &pb.ProductResponse{
		Id:    p.ID,
		Name:  p.Name,
		Price: p.Price,
	}, nil
}
