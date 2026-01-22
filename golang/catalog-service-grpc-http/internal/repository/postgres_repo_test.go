package repository_test

import (
	"context"
	"database/sql"
	"testing"

	"github.com/DATA-DOG/go-sqlmock"
	"github.com/example/catalog-mgmt-app/internal/domain"
	"github.com/example/catalog-mgmt-app/internal/repository"
	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
)

func TestRepository(t *testing.T) {
	RegisterFailHandler(Fail)
	RunSpecs(t, "Repository Suite")
}

var _ = Describe("PostgresRepository", func() {
	var (
		repo *repository.PostgresRepository
		mock sqlmock.Sqlmock
		db   *sql.DB
		ctx  context.Context
	)

	BeforeEach(func() {
		var err error
		db, mock, err = sqlmock.New()
		Expect(err).ToNot(HaveOccurred())
		repo = repository.NewPostgresRepository(db)
		ctx = context.Background()
	})

	AfterEach(func() {
		db.Close()
	})

	Describe("Create", func() {
		It("should save the product and return ID", func() {
			p := &domain.Product{Name: "Test", Price: 10.0}
			mock.ExpectQuery("INSERT INTO products").
				WithArgs(p.Name, p.Price).
				WillReturnRows(sqlmock.NewRows([]string{"id"}).AddRow(1))

			err := repo.Create(ctx, p)
			Expect(err).ToNot(HaveOccurred())
			Expect(p.ID).To(Equal(int64(1)))
		})
	})

	Describe("GetByID", func() {
		It("should return product", func() {
			rows := sqlmock.NewRows([]string{"id", "name", "price"}).
				AddRow(1, "Test", 10.0)
			mock.ExpectQuery("SELECT id, name, price FROM products WHERE id = \\$1").
				WithArgs(1).
				WillReturnRows(rows)

			p, err := repo.GetByID(ctx, 1)
			Expect(err).ToNot(HaveOccurred())
			Expect(p.ID).To(Equal(int64(1)))
			Expect(p.Name).To(Equal("Test"))
		})
	})
})
