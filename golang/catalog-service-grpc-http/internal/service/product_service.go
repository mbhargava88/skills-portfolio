package service

import (
	"context"
	"errors"

	"github.com/example/catalog-mgmt-app/internal/domain"
)

type ProductService struct {
	repo domain.ProductRepository
}

func NewProductService(repo domain.ProductRepository) *ProductService {
	return &ProductService{repo: repo}
}

func (s *ProductService) CreateProduct(ctx context.Context, name string, price float64) (*domain.Product, error) {
	if name == "" {
		return nil, errors.New("name cannot be empty")
	}
	if price <= 0 {
		return nil, errors.New("price must be greater than zero")
	}

	product := &domain.Product{
		Name:  name,
		Price: price,
	}

	err := s.repo.Create(ctx, product)
	if err != nil {
		return nil, err
	}

	return product, nil
}

func (s *ProductService) GetProduct(ctx context.Context, id int64) (*domain.Product, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *ProductService) UpdateProduct(ctx context.Context, id int64, name string, price float64) error {
	product, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return err
	}
	if product == nil {
		return errors.New("product not found")
	}

	if name != "" {
		product.Name = name
	}
	if price > 0 {
		product.Price = price
	}

	return s.repo.Update(ctx, product)
}

func (s *ProductService) DeleteProduct(ctx context.Context, id int64) error {
	return s.repo.Delete(ctx, id)
}

func (s *ProductService) ListProducts(ctx context.Context) ([]*domain.Product, error) {
	return s.repo.List(ctx)
}
