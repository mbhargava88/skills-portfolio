package repository

import (
	"context"
	"database/sql"
	"errors"

	"github.com/example/catalog-mgmt-app/internal/domain"
	_ "github.com/lib/pq"
)

type PostgresRepository struct {
	db *sql.DB
}

func NewPostgresRepository(db *sql.DB) *PostgresRepository {
	return &PostgresRepository{db: db}
}

func (r *PostgresRepository) Create(ctx context.Context, product *domain.Product) error {
	query := `INSERT INTO products (name, price) VALUES ($1, $2) RETURNING id`
	return r.db.QueryRowContext(ctx, query, product.Name, product.Price).Scan(&product.ID)
}

func (r *PostgresRepository) GetByID(ctx context.Context, id int64) (*domain.Product, error) {
	query := `SELECT id, name, price FROM products WHERE id = $1`
	row := r.db.QueryRowContext(ctx, query, id)

	var product domain.Product
	err := row.Scan(&product.ID, &product.Name, &product.Price)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, nil // Not found
		}
		return nil, err
	}
	return &product, nil
}

func (r *PostgresRepository) Update(ctx context.Context, product *domain.Product) error {
	query := `UPDATE products SET name = $1, price = $2 WHERE id = $3`
	result, err := r.db.ExecContext(ctx, query, product.Name, product.Price, product.ID)
	if err != nil {
		return err
	}
	rows, err := result.RowsAffected()
	if err != nil {
		return err
	}
	if rows == 0 {
		return errors.New("product not found")
	}
	return nil
}

func (r *PostgresRepository) Delete(ctx context.Context, id int64) error {
	query := `DELETE FROM products WHERE id = $1`
	result, err := r.db.ExecContext(ctx, query, id)
	if err != nil {
		return err
	}
	rows, err := result.RowsAffected()
	if err != nil {
		return err
	}
	if rows == 0 {
		return errors.New("product not found")
	}
	return nil
}

func (r *PostgresRepository) List(ctx context.Context) ([]*domain.Product, error) {
	query := `SELECT id, name, price FROM products`
	rows, err := r.db.QueryContext(ctx, query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var products []*domain.Product
	for rows.Next() {
		var p domain.Product
		if err := rows.Scan(&p.ID, &p.Name, &p.Price); err != nil {
			return nil, err
		}
		products = append(products, &p)
	}
	return products, rows.Err()
}
