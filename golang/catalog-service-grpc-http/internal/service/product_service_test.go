package service_test

import (
	"context"
	"testing"

	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"

	"github.com/example/catalog-mgmt-app/internal/domain"
	"github.com/example/catalog-mgmt-app/internal/service"
)

func TestService(t *testing.T) {
	RegisterFailHandler(Fail)
	RunSpecs(t, "Service Suite")
}

// Manual mock for ProductRepository
type MockRepo struct {
	products map[int64]*domain.Product
	nextID   int64
	err      error
}

func NewMockRepo() *MockRepo {
	return &MockRepo{
		products: make(map[int64]*domain.Product),
		nextID:   1,
	}
}

func (m *MockRepo) Create(ctx context.Context, p *domain.Product) error {
	if m.err != nil {
		return m.err
	}
	p.ID = m.nextID
	m.products[p.ID] = p
	m.nextID++
	return nil
}

func (m *MockRepo) GetByID(ctx context.Context, id int64) (*domain.Product, error) {
	if m.err != nil {
		return nil, m.err
	}
	if p, ok := m.products[id]; ok {
		return p, nil
	}
	return nil, nil // Not found
}

func (m *MockRepo) Update(ctx context.Context, p *domain.Product) error {
	if m.err != nil {
		return m.err
	}
	m.products[p.ID] = p
	return nil
}

func (m *MockRepo) Delete(ctx context.Context, id int64) error {
	if m.err != nil {
		return m.err
	}
	delete(m.products, id)
	return nil
}

func (m *MockRepo) List(ctx context.Context) ([]*domain.Product, error) {
	if m.err != nil {
		return nil, m.err
	}
	var list []*domain.Product
	for _, p := range m.products {
		list = append(list, p)
	}
	return list, nil
}

var _ = Describe("ProductService", func() {
	var (
		svc  *service.ProductService
		repo *MockRepo
		ctx  context.Context
	)

	BeforeEach(func() {
		repo = NewMockRepo()
		svc = service.NewProductService(repo)
		ctx = context.Background()
	})

	Describe("CreateProduct", func() {
		It("should create a product successfully", func() {
			p, err := svc.CreateProduct(ctx, "TestProduct", 10.0)
			Expect(err).ToNot(HaveOccurred())
			Expect(p.ID).ToNot(BeZero())
			Expect(p.Name).To(Equal("TestProduct"))
		})

		It("should fail if name is empty", func() {
			_, err := svc.CreateProduct(ctx, "", 10.0)
			Expect(err).To(HaveOccurred())
			Expect(err.Error()).To(Equal("name cannot be empty"))
		})

		It("should fail if price is zero", func() {
			_, err := svc.CreateProduct(ctx, "Test", 0)
			Expect(err).To(HaveOccurred())
			Expect(err.Error()).To(Equal("price must be greater than zero"))
		})
	})

	Describe("GetProduct", func() {
		It("should return a product if it exists", func() {
			p, _ := svc.CreateProduct(ctx, "Test", 10.0)
			found, err := svc.GetProduct(ctx, p.ID)
			Expect(err).ToNot(HaveOccurred())
			Expect(found).To(Equal(p))
		})
	})
})
