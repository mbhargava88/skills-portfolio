package domain

import "context"

type Product struct {
	ID    int64   `json:"id"`
	Name  string  `json:"name"`
	Price float64 `json:"price"`
}

type ProductRepository interface {
	Create(ctx context.Context, product *Product) error
	GetByID(ctx context.Context, id int64) (*Product, error)
	Update(ctx context.Context, product *Product) error
	Delete(ctx context.Context, id int64) error
	List(ctx context.Context) ([]*Product, error)
}
